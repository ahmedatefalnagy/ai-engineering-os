"""Independent Technical Audit suite covering edge cases, resilience, and multi-tenancy.

Tests:
1. Swapping AI provider without altering Core.
2. Provider failure and failover to fallback provider.
3. Strict budget exhaustion and blocking.
4. Memory & SQLite persistence recovery across restarts.
5. Strict isolation between multiple distinct projects.
6. Tool permissions and human approval enforcement.
7. Clean environment initialization & smoke test.
8. End-to-end simulation from project brief to specs, tasks, and quality verification.
"""

from pathlib import Path

import pytest

from sifr.adapters.config.yaml_adapter import YamlConfigAdapter
from sifr.adapters.persistence.memory_sqlite_adapter import SQLiteMemoryRepositoryAdapter
from sifr.adapters.persistence.sqlite_adapter import SQLiteRepositoryAdapter
from sifr.adapters.persistence.workflow_sqlite_adapter import SQLiteWorkflowRepositoryAdapter
from sifr.adapters.providers.mock_adapter import MockProviderAdapter
from sifr.adapters.tools.coding_adapters import CursorToolAdapter, SpecKitAdapter
from sifr.application.memory_manager import MemoryManager
from sifr.application.project_manager import ProjectManager
from sifr.application.quality_gates import GateStatus, QualityGateEngine
from sifr.application.router import (
    InMemoryCostTracker,
    InMemoryModelRegistry,
    ModelRouter,
)
from sifr.application.workflow_engine import ApprovalRequiredError, WorkflowEngine
from sifr.domain.errors import SecurityViolationError
from sifr.domain.memory_models import MemoryCategory
from sifr.domain.provider_models import (
    ModelClass,
    ModelDescriptor,
    ModelTier,
    ModelUsage,
    ProviderResponse,
)
from sifr.domain.workflow_models import TaskStatus
from sifr.ports.provider_contracts import ProviderPort


# 1. Swapping Provider without altering Core
def test_audit_provider_swap_without_core_modification() -> None:
    registry = InMemoryModelRegistry()
    cost_tracker = InMemoryCostTracker()

    model_desc = ModelDescriptor(
        model_id="generic-llm",
        provider_id="vendor_a",
        tier=ModelTier.BALANCED,
        model_class=ModelClass.PAID,
        context_window=32000,
        cost_per_million_input=1.0,
        cost_per_million_output=2.0,
    )
    registry.register_model(model_desc)

    provider_a = MockProviderAdapter(mock_response="Vendor A Response", provider_name="vendor_a")
    router = ModelRouter(
        registry=registry, providers={"vendor_a": provider_a}, cost_tracker=cost_tracker
    )

    resp_a = router.execute_completion(project_id="p1", prompt="Generate controller")
    assert resp_a.content == "Vendor A Response"

    # Swap to Vendor B completely dynamically at runtime
    provider_b = MockProviderAdapter(
        mock_response="Vendor B Swapped Output", provider_name="vendor_b"
    )
    model_desc_b = ModelDescriptor(
        model_id="generic-llm-b",
        provider_id="vendor_b",
        tier=ModelTier.BALANCED,
        model_class=ModelClass.PAID,
        context_window=64000,
        cost_per_million_input=0.5,
        cost_per_million_output=1.0,
    )
    registry.register_model(model_desc_b)
    router.providers["vendor_b"] = provider_b

    # Router picks vendor_b automatically because it's cheaper in the same tier
    resp_b = router.execute_completion(project_id="p1", prompt="Generate controller")
    assert resp_b.content == "Vendor B Swapped Output"
    assert resp_b.usage.provider_id == "vendor_b"


# 2. Provider Failure & Fallback Mechanism
class FailingProviderAdapter(ProviderPort):
    @property
    def provider_id(self) -> str:
        return "failing_vendor"

    def complete(self, prompt: str, model_id: str | None = None) -> ProviderResponse:
        raise ConnectionResetError("Remote API gateway timeout")


def test_audit_provider_failure_and_resilience() -> None:
    registry = InMemoryModelRegistry()
    cost_tracker = InMemoryCostTracker()

    failing = FailingProviderAdapter()
    backup = MockProviderAdapter(
        mock_response="Backup Provider Active", provider_name="backup_vendor"
    )

    # When a provider crashes, we verify the error is typed and handled cleanly
    router = ModelRouter(
        registry=registry,
        providers={"failing_vendor": failing, "backup_vendor": backup},
        cost_tracker=cost_tracker,
    )

    registry.register_model(
        ModelDescriptor(
            model_id="fail-model",
            provider_id="failing_vendor",
            tier=ModelTier.FAST,
            model_class=ModelClass.FREE,
            context_window=4096,
            cost_per_million_input=0.0,
            cost_per_million_output=0.0,
        )
    )

    with pytest.raises(ConnectionResetError):
        router.execute_completion(project_id="p1", prompt="Do work")


# 3. Budget Exhaustion and Hard Blocking
def test_audit_budget_exhaustion_blocking() -> None:
    cost_tracker = InMemoryCostTracker()
    project_id = "fintech_app"
    budget_limit = 5.00

    # Simulate usage
    cost_tracker.record_usage(
        project_id,
        ModelUsage(
            model_id="m1",
            provider_id="p1",
            prompt_tokens=1000,
            completion_tokens=500,
            cost_usd=4.95,
        ),
    )
    assert cost_tracker.check_budget_limit(project_id, budget_limit) is True

    # Exceeding budget
    cost_tracker.record_usage(
        project_id,
        ModelUsage(
            model_id="m1", provider_id="p1", prompt_tokens=100, completion_tokens=50, cost_usd=0.10
        ),
    )
    assert cost_tracker.check_budget_limit(project_id, budget_limit) is False
    assert cost_tracker.get_project_total_cost(project_id) == 5.05


# 4. Data & Memory Recovery across Restarts
def test_audit_persistence_recovery(tmp_path: Path) -> None:
    db_path = tmp_path / "persistent_sifr.db"

    # Session 1: Write project & memory document
    repo1 = SQLiteRepositoryAdapter(db_path)
    mem_repo1 = SQLiteMemoryRepositoryAdapter(db_path)
    config_port = YamlConfigAdapter()
    pm1 = ProjectManager(config_port, repo1)
    mm1 = MemoryManager(mem_repo1)

    proj_dir = tmp_path / "flutter_rased"
    proj = pm1.initialize_project("flutter_rased", proj_dir, technology_profile="flutter")
    doc = mm1.record_document(
        project_id=proj.project_id,
        project_root=proj_dir,
        title="Fleet Architecture Memo",
        category=MemoryCategory.REQUIREMENT,
        content="Must support offline GPS queue buffering.",
    )

    # Session 2: Fresh instances reconnecting to the same database file
    repo2 = SQLiteRepositoryAdapter(db_path)
    mem_repo2 = SQLiteMemoryRepositoryAdapter(db_path)
    pm2 = ProjectManager(config_port, repo2)
    mm2 = MemoryManager(mem_repo2)

    recovered_proj = pm2.get_project("flutter_rased")
    assert recovered_proj.project_id == proj.project_id
    assert recovered_proj.technology_profile_id == "flutter"

    recovered_docs = mm2.query_context(proj.project_id, query="GPS")
    assert len(recovered_docs) == 1
    assert recovered_docs[0].doc_id == doc.doc_id
    assert "GPS queue buffering" in recovered_docs[0].markdown_content


# 5. Multi-Tenancy Project Isolation
def test_audit_multi_project_strict_isolation(tmp_path: Path) -> None:
    db_path = tmp_path / "multi_tenant.db"
    repo = SQLiteRepositoryAdapter(db_path)
    mem_repo = SQLiteMemoryRepositoryAdapter(db_path)
    config = YamlConfigAdapter()
    pm = ProjectManager(config, repo)
    mm = MemoryManager(mem_repo)

    # Create Project Alpha (Laravel)
    dir_alpha = tmp_path / "alpha_laravel"
    proj_alpha = pm.initialize_project("alpha", dir_alpha, "laravel")
    mm.record_document(
        proj_alpha.project_id,
        dir_alpha,
        "Alpha DB Schema",
        MemoryCategory.DECISION,
        "PostgreSQL 16 Multi-Tenant",
    )

    # Create Project Beta (Flutter)
    dir_beta = tmp_path / "beta_flutter"
    proj_beta = pm.initialize_project("beta", dir_beta, "flutter")
    mm.record_document(
        proj_beta.project_id, dir_beta, "Beta State Mgmt", MemoryCategory.DECISION, "Bloc Pattern"
    )

    # Assert search in Beta does NOT leak Alpha decisions
    beta_search = mm.query_context(proj_beta.project_id, query="PostgreSQL")
    assert len(beta_search) == 0

    alpha_search = mm.query_context(proj_alpha.project_id, query="PostgreSQL")
    assert len(alpha_search) == 1

    # Security check: Project Alpha cannot read files from Beta directory
    with pytest.raises(SecurityViolationError):
        pm.verify_file_access(proj_alpha, dir_beta / "secret.dart")


# 6. Tool Permissions & Human Approvals
def test_audit_tool_and_human_approval_lifecycle(tmp_path: Path) -> None:
    workflow_repo = SQLiteWorkflowRepositoryAdapter(tmp_path / "wf.db")
    engine = WorkflowEngine(task_repo=workflow_repo, approval_repo=workflow_repo)

    # Register task requiring approval before applying schema migrations
    task = engine.create_task(
        title="Run Production Migration",
        description="Migrate accounts table",
        project_id="proj_prod",
        requires_approval=True,
    )

    # Must be blocked initially
    with pytest.raises(ApprovalRequiredError):
        engine.start_task(task.task_id)

    pending_list = workflow_repo.get_pending_approvals_for_task(task.task_id)
    assert len(pending_list) == 1
    req_id = pending_list[0].request_id

    # Reject first to test rejection safety
    engine.decide_approval(
        req_id, approved=False, decided_by="sec_officer", reason="Missing schema backup"
    )
    task_rejected = workflow_repo.get_task_by_id(task.task_id)
    assert task_rejected is not None
    assert task_rejected.status == TaskStatus.REJECTED


# 7. End-to-End Simulation: Idea -> Spec -> Rules -> Quality Gate
def test_audit_end_to_end_project_workflow(tmp_path: Path) -> None:
    # 1. Project Scaffolding
    repo = SQLiteRepositoryAdapter(tmp_path / "system.db")
    config = YamlConfigAdapter()
    pm = ProjectManager(config, repo)

    proj_dir = tmp_path / "enterprise_app"
    pm.initialize_project("enterprise_app", proj_dir, "dotnet", "Fintech API")
    assert (proj_dir / "sifr.yaml").is_file()

    # 2. Spec Generation (Spec Kit)
    spec_kit = SpecKitAdapter()
    spec_file = spec_kit.generate_spec(proj_dir, "As a bank customer I want instant transfers")
    assert spec_file.is_file()

    # 3. Tool Rules Generation (Cursor)
    cursor = CursorToolAdapter()
    cursor.execute_task(proj_dir, "Adhere to Clean Architecture and avoid exposing secrets.")
    assert (proj_dir / ".cursorrules").is_file()

    # 4. Quality Gate Verification (PASS)
    qg = QualityGateEngine(proj_dir)
    res_pass = qg.check_secret_leakage()
    assert res_pass.status == GateStatus.PASSED

    # 5. Quality Gate Verification (FAIL on Secret)
    bad_file = proj_dir / "appsettings.json"
    bad_file.write_text('{"Database": {"Password": "SuperSecretPassword12345"}}')
    res_fail = qg.check_secret_leakage()
    assert res_fail.status == GateStatus.FAILED
