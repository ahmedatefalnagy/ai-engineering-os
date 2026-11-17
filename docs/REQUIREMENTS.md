# REQUIREMENTS.md — AI Engineering OS (Draft v3)

> **حالة المصدر:** ملف المواصفات الأصلي (590 سطرًا) **غير متاح** حتى الآن. بحثت (قراءة فقط) في `/home/ahmed` عن الملف وعن أي ملف نصي/PDF أُضيف اليوم، ولم أجد إلا ملف PDF لفاتورة في التنزيلات، وهو غير ذي صلة.
> لذلك كل متطلب مصدره المواصفات يحمل المرجع `SPEC§?` وحالة تتبع `Pending`. لا يُعتبر أي بند هنا مطابقًا للنص الأصلي حتى أقرأه.

## مفاتيح المراجع
| الرمز | المصدر |
|---|---|
| `SPEC§?` | المواصفات الأصلية — غير مقروءة؛ رقم القسم مجهول |
| `U1§n` | رسالة المرحلة صفر الأولى (الخطوة n / القاعدة n) |
| `U2§n` | رسالة التصحيح (القسم n) |
| `U3§n` | رسالة النسخة الثالثة (القسم n) |

## قواعد المعرفات
- الصيغة `AEOS-<AREA>-<NNN>`. لا يُعاد ترقيم معرف ولا يُعاد استخدامه.
- كل معرفات v1 و v2 محفوظة. المعرفات التي كانت نطاقات في v2 (مثل `PRV-010..017`) فُصّلت إلى معرفات فردية **بنفس الأرقام**.

## مفردات الحالة
- **Trace:** `Mapped` (له مرجع مقروء ومكون ومرحلة ومعيار قبول) · `Pending` (المصدر غير مقروء أو بانتظار قرار) · `Proposed` (إضافة مقترحة غير موجودة في المصدر).
- **Implementation:** `Not Implemented` → `Implemented` → `Verified` (اختبار ناجح مربوط) → `Accepted` (موافقتك).
- **كل البنود الآن `Not Implemented`.** لا يُستخدم `Verified` لمجرد التوثيق.

---

## A. المراحل والهيكل الأساسي (Phase 1)
| ID | الوصف | النوع | المصدر | الاعتماديات |
|---|---|---|---|---|
| AEOS-REPO-001 | هيكل المستودع (src layout، فصل domain/application/ports/adapters/cli) | Functional | U3§2 (P1), SPEC§? | — |
| AEOS-DOM-001 | نماذج النطاق الأساسية. ⚠️ قائمة الكيانات حسب SPEC | Functional | U3§2, SPEC§? | REPO-001 |
| AEOS-CFG-001 | نظام الإعدادات: تحميل، تحقق، طبقات (عام/مشروع) | Functional | U3§2, SPEC§? | DOM-001 |
| AEOS-CFG-002 | YAML لإعدادات المشاريع والوكلاء (تحميل آمن) | Constraint | U3§6, SPEC§? | CFG-001 |
| AEOS-PRJ-001 | Project Manager | Functional | U1§4, U2§1, U3§2 | DOM-001, CFG-001, DB-001 |
| AEOS-CLI-000 | هيكل الـ CLI | Functional | U3§2 | PRJ-001 |
| AEOS-CLI-001..N | **جميع أوامر الـ CLI الأصلية**. ⚠️ أسماء الأوامر ووسائطها غير معروفة | Functional | U2§1, U3§3, SPEC§? | CLI-000 |
| AEOS-DB-001 | SQLite مع Repository abstraction ونظام ترحيل للمخطط (migrations) | Functional | U3§2, U3§6 | DOM-001 |
| AEOS-TEST-002 | اختبارات الوحدة للمرحلة الأولى | Quality | U3§2 | كل بنود P1 |

## B. الوكلاء وسير العمل (Phase 2)
| ID | الوصف | النوع | المصدر | الاعتماديات |
|---|---|---|---|---|
| AEOS-AGT-001 | Agent Manager | Functional | U1§4, U2§1, U3§2 | DOM-001, CFG-002 |
| AEOS-AGT-002 | خصائص الوكيل. ⚠️ الحقول حسب SPEC | Functional | U3§3, SPEC§? | AGT-001 |
| AEOS-AGT-003 | صلاحيات الوكيل: تُعلن في P2، وتُفرض كاملة مع SEC-001 في P6 | Functional | U3§3, SPEC§? | AGT-001 |
| AEOS-AGT-004 | ميزانية الوكيل: تُعرّف في P2، وتُفرض مع COST-002 في P3 | Functional | U3§3, SPEC§? | AGT-001 |
| AEOS-WF-001 | Workflow Engine | Functional | U1§4, U3§2 | AGT-001, TASK-001 |
| AEOS-WF-002 | **جميع مراحل سير العمل الأصلية**. ⚠️ غير معروفة | Functional | U2§1, SPEC§? | WF-001 |
| AEOS-WF-003 | منفذ تنفيذ الخطوات (StepExecutor port)، لفك اعتماد WF على Router | Architecture | U3§5 (حل C-02) | WF-001 |
| AEOS-WF-004 | نقطة ربط بوابات الجودة (Gate hook): البوابة غير المهيأة تظهر `not evaluated` ولا تظهر `passed` أبدًا | Architecture | U3§5 (حل C-05) | WF-001 |
| AEOS-TASK-001 | Task Management | Functional | U3§2, SPEC§? | DOM-001, DB-001 |
| AEOS-APR-001 | Approval System | Functional | U3§2, SPEC§? | WF-001 |

## C. التوجيه والمزودون والتكلفة (Phase 3)
| ID | الوصف | النوع | المصدر | الاعتماديات |
|---|---|---|---|---|
| AEOS-RTR-001 | Model Router | Functional | U1§4, U3§2 | PRV-001, MDL-001 |
| AEOS-RTR-002 | المحلي والمجاني يُفضَّلان **فقط** إذا حققا متطلبات المهمة | Functional | U2§2 | RTR-001 |
| AEOS-RTR-003 | معايير التوجيه. ⚠️ القائمة حسب SPEC | Functional | U3§3, SPEC§? | RTR-001 |
| AEOS-RTR-004 | مستويات النماذج (Model tiers). ⚠️ الأسماء والتعريفات حسب SPEC، ولن أخترعها | Functional | U3§3, SPEC§? | MDL-001 |
| AEOS-RTR-005 | توجيه يقدّم الجودة ويراعي التكلفة، وقابل للتهيئة | Functional | U2§2 | RTR-001, COST-001 |
| AEOS-PRV-001 | Provider Interfaces + Provider Registry | Functional | U1§4, U3§2 | DOM-001 |
| AEOS-PRV-002 | لا مزود إلزامي | Constraint | U2§2 | PRV-001 |
| AEOS-PRV-003 | Mock Provider | Functional | U3§2, U3§3 | PRV-001 |
| AEOS-PRV-004 | اختبارات العقد (contract tests) لكل محول مزود؛ الـ Mock يجب أن يجتازها | Quality | U3§3 | PRV-003 |
| AEOS-PRV-005 | أسرار المزودين تُشار إليها عبر متغيرات البيئة ولا تُسجَّل أبدًا (حد أدنى قبل SEC-001) | Security | U3§5 (حل C-07) | PRV-001 |
| AEOS-MDL-001 | Model Registry | Functional | U2§1 | PRV-001 |
| AEOS-MDL-002 | اكتشاف ديناميكي للنماذج **فقط** عند وجود واجهة رسمية موثقة | Functional | U2§1, U3§4 | MDL-001 |
| AEOS-MDL-003 | تصنيف النماذج: مجاني / مدفوع / محلي | Functional | U2§1 | MDL-001 |
| AEOS-MDL-004 | تسجيل يدوي لبيانات النموذج، مع مصدر السعر وتاريخ التحقق | Functional | U3§4 | MDL-001 |
| AEOS-COST-001 | Cost Tracking | Functional | U1§4, U3§2 | PRV-001 |
| AEOS-COST-002 | إدارة الميزانيات (وكيل / مهمة / مشروع. ⚠️ المستويات حسب SPEC) | Functional | U2§1, U3§3 | COST-001, AGT-004 |
| AEOS-COST-003 | حالة "تكلفة غير معروفة" للأدوات أو المزودين الذين لا يعيدون بيانات الاستهلاك | Functional | Proposed (حل C-15) | COST-001 |

## D. تصنيف التكاملات (الإضافات المعتمدة)
| ID | الوصف | النوع الفرعي | المصدر | المرحلة |
|---|---|---|---|---|
| AEOS-ARCH-006 | فصل أربعة أنواع: Native AI Provider / Model Gateway / AI Coding Tool / Spec Framework | Architecture | U3§3, U3§4 | P1 (عقد) |
| AEOS-PRV-010 | OpenAI | Native Provider | U2§1, U3§4, SPEC§? | ⚠️ D-01 |
| AEOS-PRV-011 | Anthropic | Native Provider | U2§1, U3§4, SPEC§? | ⚠️ D-01 |
| AEOS-PRV-012 | DeepSeek | Native Provider | U1§4, U3§4 (إضافة معتمدة) | ⚠️ D-01 |
| AEOS-PRV-013 | Google Gemini | Native Provider | U1§4, U3§4, SPEC§? | ⚠️ D-01 |
| AEOS-PRV-014 | OpenRouter (**أعيد تصنيفه** من Provider إلى Gateway) | Model Gateway | U1§4, U3§4 | ⚠️ D-01 |
| AEOS-PRV-015 | Groq (إضافة قابلة للتوسع) | Native Provider | U2§1, U3§4 | ⚠️ D-01 |
| AEOS-PRV-016 | Mistral (إضافة قابلة للتوسع) | Native Provider | U2§1, U3§4 | ⚠️ D-01 |
| AEOS-PRV-017 | Ollama (محلي) | Native Provider (Local) | U1§4, U3§4 | ⚠️ D-01 |
| AEOS-PRV-018 | مزودون مستقبليون كإضافات دون تعديل النواة | Extensibility | U2§1, U3§4 | P3 (عقد) |
| AEOS-PRV-019 | LiteLLM كـ Model Gateway اختياري | Model Gateway | U3§3, SPEC§? | ⚠️ D-01 |
| AEOS-PRV-020 | الاتصال المباشر بالمزودين، دون الحاجة لأي Gateway | Architecture | U3§3, SPEC§? | P3 (عقد) |
| AEOS-FREE-001 | دعم النماذج المجانية والمحلية | Functional | U1§4 (إضافة معتمدة) | P3 / D-01 |

## E. الذاكرة والملفات التقنية والقوالب (Phase 4)
| ID | الوصف | المصدر | الاعتماديات |
|---|---|---|---|
| AEOS-MEM-001 | Memory Manager: Markdown + SQLite، بلا Vector DB | U1§4, U2§2, U3§2, U3§6 | DB-001, PRJ-001 |
| AEOS-TECH-001 | Technology Profiles كبيانات (YAML) | U1§4, U3§2 | CFG-002 |
| AEOS-TECH-002 | **جميع ملفات التعريف التقنية المطلوبة**. ⚠️ القائمة حسب SPEC | U3§3, SPEC§? | TECH-001 |
| AEOS-TPL-001 | Project Templates | U2§1, U3§2 | PRJ-001, TECH-001 |
| AEOS-TPL-002 | القوالب المحددة. ⚠️ القائمة حسب SPEC | U3§3, SPEC§? | TPL-001 |

## F. أطر المواصفات وأدوات البرمجة (Phase 5)
| ID | الوصف | النوع | المصدر |
|---|---|---|---|
| AEOS-SPEC-001 | Spec Kit | Spec Framework | U2§1, U3§2 |
| AEOS-SPEC-002 | OpenSpec | Spec Framework | U2§1, U3§2 |
| AEOS-SPEC-003 | Superpowers | Spec Framework | U2§1, U3§2 |
| AEOS-TOOL-000 | واجهة AI Tool Adapter | Coding Tool | U3§2 |
| AEOS-TOOL-001 | Codex | Coding Tool | U2§1 |
| AEOS-TOOL-002 | Claude Code | Coding Tool | U2§1 |
| AEOS-TOOL-003 | Cursor | Coding Tool | U2§1 |
| AEOS-TOOL-004 | GitHub Copilot | Coding Tool | U2§1 |
| AEOS-TOOL-005 | Gemini CLI | Coding Tool | U2§1 |
| AEOS-AGY-001 | Google Antigravity: **اختياري**، ولا يُنفذ إلا بعد إثبات واجهة رسمية موثقة وصالحة للاستخدام (بوابة AGY-G1) | Coding Tool | U1§4 (إضافة معتمدة), U3§4 |

## G. الجودة والأمان والتثبيت (Phase 6)
| ID | الوصف | المصدر |
|---|---|---|
| AEOS-QG-001 | Quality Gates | U1§4, U3§2 |
| AEOS-SEC-001 | Security Controls & Permissions | U1§4, U3§2 |
| AEOS-TEST-003 | اختبارات التكامل | U3§2 |
| AEOS-INST-001 | التثبيت على Ubuntu | U3§2, SPEC§? |

## H. متطلبات شاملة (Cross-cutting)
| ID | الوصف | المصدر |
|---|---|---|
| AEOS-CORE-001 | نواة مستقلة عن المزود واللغة والتقنية | U1 rule 6, U2§2 |
| AEOS-TEST-001 | Testing Strategy. ⚠️ العتبات حسب SPEC | U2§1, U3§3 |
| AEOS-DOC-001 | Documentation Requirements. ⚠️ التفاصيل حسب SPEC | U2§1, U3§3 |
| AEOS-PROC-009 | **جميع قواعد التنفيذ الإلزامية في SPEC**. ⚠️ غير معروفة | U3§3, SPEC§? |
| AEOS-PROC-010 | توثيق سبب كل تغيير في التصميم | U3 (الخاتمة) |
| AEOS-AUD-001 | Final Audit بعد المرحلة السادسة | U2§3, U3§2 |

## I. القيود التقنية
| ID | القيد | المصدر |
|---|---|---|
| AEOS-TC-001 | Python 3.12 حدًا أدنى مبدئيًا | U3§6 |
| AEOS-TC-002 | CLI-first | U2§2, U3§6 |
| AEOS-TC-003 | لا Dashboard في المرحلة الأولى؛ الـ API والـ Dashboard امتدادات مستقبلية | U2§2, U3§6 |
| AEOS-TC-004 | لا Kubernetes ولا Kafka | U3§6 |
| AEOS-TC-005 | Docker للتكاملات المستقبلية فقط، وليس شرطًا لتشغيل النواة | U3§6 |
| AEOS-TC-006 | لا Vector DB في التنفيذ الأولي | U2§2 |
| AEOS-TC-007 | لا بنية تحتية غير ضرورية | U2§2 |

## J. القواعد المعمارية والإجرائية (من v1/v2، محفوظة)
| ID | الوصف | المصدر | علاقة |
|---|---|---|---|
| AEOS-ARCH-001 | فصل AI Providers عن AI Coding Tools | U1 rule 4 | توسّع إلى ARCH-006 |
| AEOS-ARCH-002 | لا افتراض لتوحيد البروتوكولات | U1 rule 3 | — |
| AEOS-ARCH-003 | لا افتراض لتكامل Antigravity غير موثق | U1 rule 5 | ≈ AGY-001 (مكرر موثق) |
| AEOS-ARCH-004 | عدم ربط النواة بمزود أو لغة | U1 rule 6 | ≈ CORE-001 (مكرر موثق) |
| AEOS-ARCH-005 | لا اختراع لخصائص أو APIs؛ التحقق من الوثائق الرسمية | U1 rules 1-2, U2§2 | — |
| AEOS-ARCH-007 | Hexagonal / Ports & Adapters | U2§2 | — |
| AEOS-ARCH-008 | الاستقلال عن التقنيات | U2§2 | ≈ CORE-001 جزئيًا |
| AEOS-ARCH-009 | عزل تام عن Rased Fleet | U2§4 | — |
| AEOS-PROC-001 | معرف فريد ثابت لكل متطلب | U1 step 2 | — |
| AEOS-PROC-002 | مصفوفة تتبع Req→Comp→Task→Impl→Test→Acceptance | U1 step 3 | — |
| AEOS-PROC-003 | لا اكتمال لمتطلب بلا دليل تنفيذ واختبار | U1 step 3 | — |
| AEOS-PROC-004 | تسجيل كل قرار معماري وأسبابه | U1 rule 8 | — |
| AEOS-PROC-005 | المحافظة على الملفات الموجودة | U1 step 1 | — |
| AEOS-PROC-006 | لا تنفيذ قبل موافقة صريحة | U1 rule 9, U3§8 | — |
| AEOS-PROC-007 | تقرير في نهاية كل مهمة | U1 rule 10 | — |
| AEOS-PROC-008 | ثماني وثائق للمرحلة صفر | U1 step 6, U2§6, U3§7 | — |
| AEOS-SEC-002 | توثيق تعرض الأسرار في ملف Rased Fleet دون نسخ قيمه | U2§4 | → R-02 |

**الإجمالي:** 97 معرفًا فرديًا، إضافة إلى البند المفتوح `CLI-001..N`.
- من هذه المعرفات، **14 بندًا** يحتوي على ⚠️ بمعنى أن محتواه التفصيلي في SPEC فقط: DOM-001، CLI-001..N، AGT-002/003/004، WF-002، TASK-001، APR-001، RTR-003، RTR-004، COST-002، TECH-002، TPL-002، PROC-009 (إضافة إلى TEST-001 و DOC-001 جزئيًا).
