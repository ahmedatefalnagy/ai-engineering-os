# SIFR Engineering Standard: Native Bilingual Architecture (I18N & L10N)

## 1. Core Principle
Any enterprise software system designed, scaffolded, or governed by **SIFR (AI Engineering OS)** MUST treat **Arabic (العربية)** and **English** as first-class, co-equal citizens. Systems cannot be "retrofitted" for Arabic as an afterthought.

---

## 2. Mandatory Architectural Invariants

### Invariant 1: Dual-Language Data Entry (Database Schema)
Every master data entity or descriptive record entered by users must feature dual-language fields in the persistence layer:
- Master Name: `name_ar` (Arabic) and `name_en` (English)
- Descriptions: `description_ar` (Arabic) and `description_en` (English)
- Lookup Codes & Badges: Dual localized display tags

### Invariant 2: Bidirectional UI (RTL / LTR)
- User interfaces must natively support bidirectional layout:
  - When Arabic is active: `dir="rtl"`, mirrored menus, proper Arabic typography (`Cairo`, `Plus Jakarta Sans`, `IBM Plex Arabic`), and correct icon orientations.
  - When English is active: `dir="ltr"`, standard left-to-right alignment.
- Layout switching must be instantaneous without requiring full page reload.

### Invariant 3: Form Input Fields
Whenever user input is requested for entities (e.g. Products, Accounts, Drivers, Vehicle Models, Categories):
- The UI MUST provide an **Arabic input field** alongside an **English input field**.
- Both are persisted to the database and indexed for bilingual search and reporting.

### Invariant 4: Quality Gate Enforcement
The SIFR `QualityGateEngine` enforces `bilingual_compliance` as a mandatory validation check in CI/CD before any delivery is accepted.
