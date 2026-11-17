# TRACEABILITY.md — AI Engineering OS (Draft v3)

> **تحذير المطابقة:** عمود "المرجع الأصلي" يجب أن يحمل رقم قسم أو فقرة في SPEC. بما أن SPEC غير مقروء، فالقيمة `SPEC§?` وحالة التتبع `Pending` لكل بند مصدره المواصفات. الأعمدة **Impl** و **Test evidence** فارغة، و **Impl = Not Implemented** لكل البنود.

السلسلة المطبقة: Requirement → Component → Task → Implementation → Test → Acceptance

| Req ID | المرجع الأصلي | مرجع ثانوي | المكون | المرحلة | Task | معيار القبول | طريقة الاختبار | Trace | Impl |
|---|---|---|---|---|---|---|---|---|---|
| REPO-001 | SPEC§? | U3§2 | repo | 1 | T1.01 | الهيكل يطابق ARCHITECTURE §3، و `pytest` يكتشف الحزم | فحص هيكلي + import test | Pending | Not Implemented |
| DOM-001 | SPEC§? | U3§2 | domain | 1 | T1.02 | كل كيان في SPEC ممثل كنموذج مُتحقق منه، والنطاق لا يستورد adapters | Unit + boundary test | Pending | Not Implemented |
| CFG-001 | SPEC§? | U3§2 | config | 1 | T1.03 | الدمج بين الطبقات حتمي؛ الخطأ يعطي رسالة واضحة ورمز خروج ≠ 0 | Unit (table-driven) | Pending | Not Implemented |
| CFG-002 | SPEC§? | U3§6 | config | 1 | T1.03 | YAML يُحمَّل بـ safe-load فقط، ويُتحقق منه بمخطط | Unit + malicious-YAML test | Pending | Not Implemented |
| PRJ-001 | SPEC§? | U3§2 | project-manager | 1 | T1.05 | إنشاء/تسجيل/عرض مشروع في مجلد مؤقت؛ رفض الكتابة خارج جذر المشروع | Unit + CLI integration | Pending | Not Implemented |
| CLI-000 | SPEC§? | U3§2 | cli | 1 | T1.06 | `<cli> --help` يعمل بلا شبكة وبلا مفاتيح | CLI smoke test | Pending | Not Implemented |
| CLI-001..N | SPEC§? | U2§1 | cli | حسب الأمر | T1.06+ | كل أمر أصلي موجود أو مُعلَّم صراحة "مؤجل لمرحلة X" | CLI tests لكل أمر | **Pending (قائمة مجهولة)** | Not Implemented |
| DB-001 | SPEC§? | U3§2, U3§6 | persistence | 1 | T1.04 | تطبيقا SQLite و in-memory يجتازان نفس مجموعة الاختبارات؛ الترحيل قابل للتكرار | Repository contract tests | Pending | Not Implemented |
| TEST-002 | SPEC§? | U3§2 | testing | 1 | T1.07 | تغطية ≥ العتبة (⚠️ SPEC، والمقترح 80%) على 3.12 و 3.15 | pytest + coverage | Pending | Not Implemented |
| AGT-001 | SPEC§? | U3§2 | agent-manager | 2 | T2.01 | CRUD لتعريفات الوكلاء من YAML مع التحقق | Unit | Pending | Not Implemented |
| AGT-002 | SPEC§? | U3§3 | agent-manager | 2 | T2.02 | كل خاصية في SPEC ممثلة ومُتحقق منها | Unit | Pending | Not Implemented |
| AGT-003 | SPEC§? | U3§3 | agent-manager → security | 2 (إعلان) / 6 (فرض) | T2.03, T6.02 | P2: الصلاحيات تُقرأ وتُفحص عبر PermissionPort بسياسة deny-by-default. P6: فرض كامل | Unit / Security tests | Pending | Not Implemented |
| AGT-004 | SPEC§? | U3§3 | agent-manager → cost | 2 (تعريف) / 3 (فرض) | T2.04, T3.08 | P2: الحقل مُتحقق منه. P3: تجاوزه يمنع أو ينبه حسب السياسة | Unit | Pending | Not Implemented |
| WF-001 | SPEC§? | U3§2 | workflow | 2 | T2.05 | تنفيذ DAG، checkpoints، استئناف بعد مقاطعة | Unit + integration | Pending | Not Implemented |
| WF-002 | SPEC§? | U2§1 | workflow | 2 | T2.06 | كل مرحلة أصلية معرفة وقابلة للتنفيذ | Integration | **Pending (قائمة مجهولة)** | Not Implemented |
| WF-003 | — | U3§5 | workflow | 2 | T2.05 | Workflow لا يستورد router أو providers | Boundary test | Proposed | Not Implemented |
| WF-004 | — | U3§5 | workflow | 2 | T2.07 | بوابة غير مهيأة → `not evaluated`، ولا تعطي `passed` أبدًا | Unit | Proposed | Not Implemented |
| TASK-001 | SPEC§? | U3§2 | task-management | 2 | T2.08 | دورة حياة المهمة محفوظة في SQLite | Unit + repo tests | Pending | Not Implemented |
| APR-001 | SPEC§? | U3§2 | approval | 2 | T2.09 | الخطوة المعلّمة تتوقف حتى الموافقة أو الرفض، ويُسجَّل القرار | Integration | Pending | Not Implemented |
| RTR-001 | SPEC§? | U3§2 | router | 3 | T3.04 | اختيار حتمي لسيناريوهات محددة | Table-driven unit | Pending | Not Implemented |
| RTR-002 | — | U2§2 | router | 3 | T3.04 | لا يُختار نموذج محلي أو مجاني يفتقد قدرة مطلوبة | Unit | Mapped (U2) | Not Implemented |
| RTR-003 | SPEC§? | U3§3 | router | 3 | T3.04 | كل معيار أصلي له اختبار | Unit | Pending | Not Implemented |
| RTR-004 | SPEC§? | U3§3 | router/registry | 3 | T3.03 | كل مستوى أصلي معرّف وله أمثلة اختبار | Unit | Pending | Not Implemented |
| RTR-005 | — | U2§2 | router | 3 | T3.04 | تبديل السياسة يغير النتيجة كما هو متوقع | Unit | Mapped (U2) | Not Implemented |
| PRV-001 | SPEC§? | U3§2 | provider-port | 3 | T3.01 | واجهات Native و Gateway منفصلة، مع إعلان صريح للقدرات | Contract tests | Pending | Not Implemented |
| PRV-002 | — | U2§2 | registry | 1 (اختبار) / 3 | T1.06, T3.01 | الـ CLI يعمل بالكامل بلا أي مزود مهيأ | CLI test بلا متغيرات بيئة | Mapped (U2) | Not Implemented |
| PRV-003 | SPEC§? | U3§2 | mock-provider | 3 | T3.02 | الـ Mock يجتاز مجموعة اختبارات العقد كاملة | Contract tests | Pending | Not Implemented |
| PRV-004 | SPEC§? | U3§3 | testing | 3 | T3.02 | مجموعة عقد قابلة لإعادة الاستخدام لكل محول | Contract suite | Pending | Not Implemented |
| PRV-005 | — | U3§5 | provider-port | 3 | T3.01 | لا يظهر أي سر في السجلات أو الأخطاء | Log-redaction test | Proposed | Not Implemented |
| PRV-010..017, 019 | SPEC§? / إضافة | U2§1, U3§4 | provider adapters | **D-01** | — | تحقق موثق (رابط + تاريخ) + اجتياز اختبارات العقد | Contract (mock HTTP) + live اختياري | Pending (D-01 + تحقق) | Not Implemented |
| PRV-018 | — | U2§1 | provider-port | 3 | T3.01 | مزود تجريبي يُضاف كإضافة (plugin) دون تعديل النواة | Integration | Mapped (U2) | Not Implemented |
| PRV-020 | SPEC§? | U3§3 | provider-port | 3 | T3.01 | المسار المباشر لا يعتمد على أي Gateway | Boundary test | Pending | Not Implemented |
| MDL-001 | — | U2§1 | registry | 3 | T3.03 | بيانات النموذج محفوظة مع المصدر والتاريخ | Unit | Mapped (U2) | Not Implemented |
| MDL-002 | — | U2§1, U3§4 | registry | 3 (آلية) / D-01 (محولات) | T3.03 | الاكتشاف يُفعّل فقط لمحول يعلن endpoint موثقًا | Contract | Mapped (U3) | Not Implemented |
| MDL-003 | — | U2§1 | registry | 3 | T3.03 | الحقل إلزامي ومُتحقق منه | Unit | Mapped (U2) | Not Implemented |
| MDL-004 | — | U3§4 | registry | 3 | T3.03 | سجل يدوي بلا مصدر سعر أو تاريخ تحقق يُرفض | Unit | Mapped (U3) | Not Implemented |
| COST-001 | SPEC§? | U3§2 | cost | 3 | T3.07 | كل استدعاء يُسجَّل بالاستهلاك والتكلفة | Unit + Mock | Pending | Not Implemented |
| COST-002 | SPEC§? | U3§3 | cost | 3 | T3.08 | تجاوز الميزانية يطبق السياسة المهيأة | Unit | Pending | Not Implemented |
| COST-003 | — | Proposed | cost | 3 | T3.07 | الاستهلاك الغائب يُسجَّل `unknown`، وليس صفرًا | Unit | Proposed | Not Implemented |
| FREE-001 | إضافة | U1§4 | registry/router | 3 / D-01 | T3.03 | تمييز المجاني والمحلي + RTR-002 | Unit | Mapped (U1) | Not Implemented |
| ARCH-006 | SPEC§? | U3§4 | ports | 1 (تسمية) / 3 / 5 | T1.02 | أربع واجهات منفصلة؛ لا محول ينفذ نوعين | Boundary test | Pending | Not Implemented |
| MEM-001 | SPEC§? | U3§2 | memory | 4 | T4.01 | حفظ واسترجاع القرارات والسياق؛ ملفات Markdown قابلة للقراءة البشرية | Unit + integration | Pending | Not Implemented |
| TECH-001 | SPEC§? | U3§2 | profiles | 4 | T4.02 | إضافة ملف تعريف تقنية لا تتطلب تغيير الكود | Schema + integration | Pending | Not Implemented |
| TECH-002 | SPEC§? | U3§3 | profiles | 4 | T4.03 | كل ملف تعريف أصلي موجود ومُتحقق منه | Schema tests | **Pending (قائمة مجهولة)** | Not Implemented |
| TPL-001 | SPEC§? | U3§2 | templates | 4 | T4.04 | إنشاء مشروع من قالب في مجلد مؤقت | Integration | Pending | Not Implemented |
| TPL-002 | SPEC§? | U3§3 | templates | 4 | T4.05 | كل قالب أصلي موجود | Integration | **Pending (قائمة مجهولة)** | Not Implemented |
| SPEC-001..003 | SPEC§? | U3§2 | spec-framework adapters | 5 | T5.02-04 | تحقق موثق + اختبار تكامل على مشروع تجريبي معزول | Contract/integration | Pending | Not Implemented |
| TOOL-000 | SPEC§? | U3§2 | tool-port | 5 | T5.01 | واجهة تعلن مستوى القدرة (تشغيل / ملفات تعليمات فقط) | Contract | Pending | Not Implemented |
| TOOL-001..005 | SPEC§? | U2§1 | tool adapters | 5 | T5.05-09 | تحقق موثق لكل أداة؛ يعمل النظام بغياب أي أداة | Contract + absence test | Pending | Not Implemented |
| AGY-001 | إضافة | U1§4, U3§4 | tool adapter (اختياري) | 5 | T5.10 | **بوابة AGY-G1:** واجهة رسمية موثقة مثبتة؛ وإلا يُسجَّل `Deferred` | Absence test + contract | Pending (AGY-G1) | Not Implemented |
| QG-001 | SPEC§? | U3§2 | quality-gates | 6 | T6.01 | فشل أي بوابة يمنع القبول | Integration | Pending | Not Implemented |
| SEC-001 | SPEC§? | U3§2 | security | 6 | T6.02 | أوامر وملفات خارج السياسة تُمنع أو تتطلب موافقة | Security tests | Pending | Not Implemented |
| TEST-003 | SPEC§? | U3§2 | testing | 6 | T6.03 | سيناريو شامل ناجح باستخدام Mock Provider | Integration/E2E | Pending | Not Implemented |
| INST-001 | SPEC§? | U3§2 | packaging | 6 | T6.04 | تثبيت نظيف على Ubuntu 24.04 وفق الوثيقة | Clean-env install test | Pending | Not Implemented |
| CORE-001 | — | U1, U2§2 | core | 1→ | T1.09 | النواة لا تستورد أي adapter أو SDK خارجي | Boundary test (CI) | Mapped (U1) | Not Implemented |
| TEST-001 | SPEC§? | U2§1 | testing | كل المراحل | T*.test | العتبات الأصلية مطبقة | CI محلي | Pending | Not Implemented |
| DOC-001 | SPEC§? | U2§1 | docs | كل المراحل | T*.doc | كل وثيقة مطلوبة في SPEC موجودة | Doc checklist | Pending | Not Implemented |
| PROC-009 | SPEC§? | U3§3 | process | كل المراحل | — | كل قاعدة أصلية لها فحص | Review | **Pending (قائمة مجهولة)** | Not Implemented |
| PROC-010 | — | U3 | process | كل المراحل | — | كل تغيير في DECISIONS أو CHANGELOG مع سببه | Review | Mapped (U3) | Not Implemented |
| AUD-001 | — | U2§3, U3§2 | audit | 7 | T7.* | كل متطلب `Verified` أو `Deferred` بقرار موثق | Audit checklist | Mapped (U3) | Not Implemented |
| TC-001..007 | — | U2§2, U3§6 | cross-cutting | 1→ | T1.01, T1.07 | 3.12 في CI؛ لا Docker/K8s/Kafka/VectorDB في الاعتماديات | Dependency check | Mapped (U2/U3) | Not Implemented |
| ARCH-001..005, 007..009 | — | U1, U2 | cross-cutting | 1→ | T1.09 | Boundary tests؛ لا وصول لمسار Rased Fleet | Boundary + path test | Mapped (U1/U2) | Not Implemented |
| PROC-001..008 | — | U1 | process | 0→ | — | وثائق المرحلة صفر | Review | Mapped (U1) | Not Implemented |
| SEC-002 | — | U2§4 | risk | 0 | — | الخطر R-02 موثق دون قيم | Review | Mapped (U2) | Not Implemented |

## تقرير التغطية
| الفئة | العدد | التفاصيل |
|---|---|---|
| **مطابق للمواصفات الأصلية (SPEC Mapped)** | **0 من ? (0%)** | لم يُقرأ أي سطر من الـ 590 |
| Mapped إلى رسائلك (U1–U3) | 36 / 97 | بنود مصدرها قرارات أو قواعد صريحة منك |
| Pending | 57 / 97 | منها 9 تحتاج أيضًا قرار المرحلة D-01، و 14 محتواها التفصيلي في SPEC فقط |
| Pending: قائمة محتوى مجهولة | 7 مجموعات | CLI، مراحل سير العمل، خصائص الوكلاء، معايير التوجيه ومستوياته، ملفات التقنية، القوالب، القواعد الإلزامية |
| Proposed (إضافات مني تحتاج موافقة) | 4 / 97 (+ اقتراح تقسيم) | WF-003، WF-004، PRV-005، COST-003، إضافة إلى تقسيم AGT-003/004 بين مرحلتين |
| مكرر (موثق دون حذف) | 4 | ARCH-003≈AGY-001، ARCH-004≈CORE-001، ARCH-008⊂CORE-001، ARCH-001⊂ARCH-006 |
| يحتاج قرار مرحلة | 9 | PRV-010..017, 019 ← D-01 (و FREE-001 جزئيًا) |
| **Missing (معروف غيابه)** | غير قابل للعد | أي متطلب في SPEC لم يرد في رسائلك |
