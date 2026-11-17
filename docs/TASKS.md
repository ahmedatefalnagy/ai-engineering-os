# TASKS.md — AI Engineering OS (Draft v3)

> لا مهمة قابلة للبدء قبل اعتماد Phase 0 وحل D-02 (مدير الحزم). التقدير: S صغير · M متوسط · L كبير.

## المرحلة 1 (تفصيلية)
| Task | الوصف | المتطلبات | تعتمد على | المخرجات | الاختبارات | الحجم |
|---|---|---|---|---|---|---|
| T1.00 | تهيئة المستودع: إنشاء المجلد، `git init`، `.gitignore` (يشمل `.env`، `*.db`) — **يتطلب موافقتك** | REPO-001, PROC-005 | Phase 0 approval | مستودع فارغ منظم | — | S |
| T1.01 | `pyproject.toml` (PEP 621، `requires-python >= 3.12`)، src layout، أدوات (pytest، ruff، mypy: D-06) | REPO-001, TC-001 | T1.00, D-02 | هيكل حزم | import test | S |
| T1.02 | نماذج النطاق (dataclasses أو pydantic: D-04)، تسمية أنواع التكامل الأربعة | DOM-001, ARCH-006 | T1.01 | `domain/` | Unit | M |
| T1.03 | الإعدادات: محمل YAML آمن، مخطط تحقق، طبقات عام/مشروع، مراجع أسرار بأسماء متغيرات البيئة فقط | CFG-001, CFG-002 | T1.02 | `adapters/config/` | Unit + malicious-YAML | M |
| T1.04 | Persistence: `RepositoryPort`، SQLite (stdlib `sqlite3`)، in-memory، جدول `schema_version` + ترحيلات | DB-001 | T1.02 | `adapters/persistence/` | Repository contract suite | M |
| T1.05 | Project Manager: إنشاء، تسجيل، عرض، حالة؛ حماية جذر المشروع؛ technology id معتم | PRJ-001 | T1.03, T1.04 | `application/projects` | Unit + path-escape test | M |
| T1.06 | CLI skeleton (D-07): أوامر P1 فعلية؛ الأوامر الأصلية الأخرى تُسجَّل وتُظهر "متاح في المرحلة X" | CLI-000, CLI-001..N, PRV-002 | T1.05, **قائمة SPEC** | `cli/` | CLI tests (بلا شبكة/مفاتيح) | M |
| T1.07 | إعداد الاختبارات والتغطية؛ مصفوفة 3.12 / 3.15 محليًا | TEST-002, TEST-001 | T1.01 | `tests/`، تقرير تغطية | — | S |
| T1.08 | وثائق التطوير: README، دليل إعداد بيئة التطوير، نقل وثائق Phase 0 إلى `docs/` | DOC-001 | T1.00 | `docs/` | Doc checklist | S |
| T1.09 | اختبار الحدود المعمارية + فحص الاعتماديات المحظورة + اختبار عدم الوصول لمسار Rased Fleet | CORE-001, ARCH-*, TC-004..007, ARCH-009 | T1.02 | `tests/architecture/` | Boundary tests | S |
| T1.10 | تحديث TRACEABILITY و PROJECT_STATE، وتقرير نهاية المرحلة | PROC-002/003/007 | الكل | تقرير | Review | S |

**المسار الحرج:** T1.00 → T1.01 → T1.02 → (T1.03 ∥ T1.04) → T1.05 → T1.06 → T1.10

## المرحلة 2
T2.01 Agent Manager · T2.02 خصائص الوكيل (⚠️ SPEC) · T2.03 الصلاحيات + PermissionPort (deny-by-default) · T2.04 حقل الميزانية · T2.05 Workflow Engine + StepExecutorPort · T2.06 مراحل سير العمل الأصلية (⚠️ SPEC) · T2.07 GateHookPort · T2.08 Task Management · T2.09 Approval System · T2.10 تتبع وتقرير.

## المرحلة 3
T3.01 Native/Gateway Provider ports + registry + PRV-005 · T3.02 Mock Provider + contract suite · T3.03 Model Registry + discovery port + السجل اليدوي + المستويات · T3.04 Router (المعايير، السياسات، fallback) · T3.05 ربط Router بـ StepExecutor · T3.06 (محجوز لقرار D-01) · T3.07 Cost Tracking (أحداث، `unknown`) · T3.08 فرض الميزانيات · T3.09 تتبع وتقرير.

## المرحلة 4
T4.01 Memory Manager (Markdown + فهرس SQLite) · T4.02 مخطط Technology Profile · T4.03 الملفات الأصلية (⚠️ SPEC) · T4.04 محرك القوالب · T4.05 القوالب الأصلية (⚠️ SPEC) · T4.06 التحقق من technology ids القديمة من P1 · T4.07 تتبع وتقرير.

## المرحلة 5
T5.00 **تحقق موثق** لكل إطار وأداة (يتطلب إذن تصفح الويب: D-08) · T5.01 CodingToolPort + SpecFrameworkPort · T5.02–T5.04 Spec Kit / OpenSpec / Superpowers · T5.05–T5.09 Codex / Claude Code / Cursor / Copilot / Gemini CLI · T5.10 Antigravity (بوابة AGY-G1) · T5.11 absence tests · T5.12 تتبع وتقرير.

## المرحلة 6
T6.01 Quality Gates (تنفيذ GateHook من Profiles) · T6.02 Security Controls (PermissionPort كامل، أسرار، تدقيق) · T6.03 اختبارات التكامل الشاملة · T6.04 التثبيت على Ubuntu (D-02) · T6.05 فحص الأسرار · T6.06 تتبع وتقرير.

## المرحلة 7
T7.01 تدقيق التتبع · T7.02 إعادة تحقق التكاملات · T7.03 مراجعة أمنية واعتماديات · T7.04 التقرير النهائي.
