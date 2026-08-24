# Research Infrastructure Module — Versioned Index

**Purpose:** Engine B research pipeline — source validation, citation formats, prompts, verified samples, contact tracking.

---

## Versioned Files

| Version | File | Description |
|---------|------|-------------|
| **v1** | `citation_templates.md` | Per-outlet Engine B citation formats (12 publishers, 4 tiers) |
| **v1** | `engine_b_prompt.md` | Main research prompt with source allowlist (Tier 1-4) |
| **v1** | `monthly_template.md` | Monthly research batch template |
| **v1** | `batch_july17-30.md` | July 17-30 research batch example |
| **v1** | `validation_gate.md` | Source validation gate script requirements |
| **v1** | `verified_samples.md` | Verified sample data notes |
| **v2** | `media_landscape_with_sprints.md` | Full VI Catholic media landscape with sprints, partnership tracker, contact CSV ref |
| **v3** | `media_contacts.csv` | Partnership outreach tracker (when created) |

---

## Pipeline Components

| Component | File | Status |
|-----------|------|--------|
| Source allowlist (Tier 1-4) | v1/engine_b_prompt.md | 🟢 Complete |
| Citation format validator | v1/citation_templates.md | 🟢 Complete |
| Validation gate script | v1/validation_gate.md | 🟢 Spec complete |
| Research prompt template | v1/engine_b_prompt.md | 🟢 Complete |
| Monthly batch workflow | v1/monthly_template.md | 🟢 Complete |
| Verified sample corpus | v1/verified_samples.md, v1/batch_july17-30.md | 🟢 Complete |
| Media partnership CRM | v2/media_landscape_with_sprints.md, v3/media_contacts.csv | 🟡 CSV pending |

---

## Source Tiers (from v1/engine_b_prompt.md)

| Tier | Publishers | Validation Rule |
|------|------------|-----------------|
| **1** | Vatican News VI, Radio Vatican VI, VCC OC | No additional validation |
| **2** | VietCatholicNews/TV, Parish livestreams (3) | `accessed` date within 90 days |
| **3** | KVNR 1480, VNCR 106.3 | Explicit `notes` with program + broadcast date |
| **4** | TGPSG, HDGM Vietnam, Redemptorists Vietnam | **Require** "Produced in Vietnam; state context applies" in notes |

---

## Entry Points for Workers

| Task | Worker Type | Input Files |
|------|-------------|-------------|
| Build citation validator (Python) | `deepseek-worker` | v1/citation_templates.md, v1/validation_gate.md |
| Generate Engine B prompt with allowlist | `deepseek-worker` | v1/engine_b_prompt.md, v2/media_landscape_with_sprints.md |
| Build media partnership CRM | `yolo-worker` | v2/media_landscape_with_sprints.md (partnership tracker), v3/media_contacts.csv |
| Validate research batch output | `deepseek-worker` | v1/validation_gate.md, v1/batch_july17-30.md |