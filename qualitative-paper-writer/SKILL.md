---
name: qualitative-paper-writer
description: 护理学/医学质性研究论文全流程写作辅助工具。覆盖从研究设计到投稿的完整管线。当用户提到'质性研究'、'qualitative'、'访谈研究'、'现象学'、'扎根理论'、'民族志'、'ethnography'、'phenomenology'、'grounded theory'、'COREQ'、'主题分析'、'thematic analysis'、'数据饱和'、'saturation'、'质性论文'、'写质性'、'质性投稿'时触发。支持中英文双语。适用于 IJNS、JAN、BMC Nursing、Qualitative Health Research 等接受质性研究的 SCI 期刊。
---

# Qualitative Research Paper Writer

## Overview

Full-pipeline skill for writing qualitative research papers targeting SCI nursing/healthcare journals. Derived from real manuscript development experience.

## Pipeline Phases

```
Phase 1: Research Design → Phase 2: Data Generation/Collection → Phase 3: Analysis
→ Phase 4: Manuscript Writing → Phase 5: Quality Assurance → Phase 6: Submission Package
```

---

## Phase 1: Research Design

> **起点提示**：若从模糊的临床观察或研究兴趣出发，先调用 `research-brainstorm` skill 完成头脑风暴与新颖性评估，再携带研究方向文档返回此处。

### 1.1 Methodology Selection

Ask the user's **core research question**, then match methodology:

| Core Question | Methodology | Key Reference |
|---|---|---|
| "这种体验是什么样的？" / What is this experience like? | Phenomenology (IPA / Colaizzi) | Smith et al. (2022) |
| "这个过程如何发生？机制是什么？" / How does this process unfold? | Grounded Theory | Charmaz (2014) |
| "在这个文化环境中人们如何行动？" / How do people act in this culture? | Ethnography / Focused Ethnography | Knoblauch (2005); Cruz & Higginbottom (2013) |
| "多项研究整合后有什么新理解？" / What new understanding emerges from synthesizing studies? | Meta-synthesis | Noblit & Hare (1988) |

**CRITICAL — Avoid "method slurring"** (Baker et al., 1992): Ensure the stated methodology, philosophical stance, sampling strategy, and analysis method are internally consistent. Do NOT mix phenomenological claims with grounded theory coding, or claim ethnography without fieldwork.

### 1.2 Theoretical Sensitization

Qualitative research is not atheoretical. Identify 1-2 sensitizing frameworks that:
- Provide analytic vocabulary (not rigid hypotheses)
- Are explicitly stated in Introduction and Discussion
- Allow inductive insights beyond the framework

### 1.3 Novelty Check

Before committing, search PubMed/CINAHL for the intersection of:
- Population + methodology + phenomenon + context
- Use `scientific-skills:pubmed-database` skill if available

Frame the gap as: "No published [methodology] study has examined [phenomenon] among [population] in [context]."

---

## Phase 2: Data Generation

### 2.1 Sampling Strategy

Use **purposive maximum-variation sampling** with iterative recruitment. Justify sample size with BOTH:
- **Theoretical**: Information power principle (Malterud et al., 2016)
- **Empirical**: 9-17 interviews for homogeneous populations (Hennink & Kaiser, 2022)

### 2.2 Data Saturation Protocol

Track new theme emergence across interview rounds:

```
Round 1 (3-4 interviews) → Initial themes identified
Round 2 (3-4 interviews) → New themes? If yes → continue
Round 3 (2-3 interviews) → New themes? If 0 new codes → SATURATION
```

Report saturation transparently: "Data saturation was confirmed in Round [N], during which no new thematic categories emerged."

### 2.3 Simulated Pilot Interviews (Optional)

When conducting a simulated/educational pilot study, use parallel agents to generate interviews:

- Assign each agent a distinct participant profile (role, seniority, gender, personality)
- Provide the interview guide + theoretical framework + setting description
- Instruct agents to produce verbatim-style transcripts with natural speech patterns, pauses, and emotional markers
- Run in rounds (3-4 per round), perform thematic analysis between rounds, and continue until saturation

---

## Phase 3: Analysis

### 3.1 Analysis Method Selection

| Methodology | Analysis Approach |
|---|---|
| Phenomenology (IPA) | IPA 6-step (Smith et al., 2022) |
| Phenomenology (Descriptive) | Colaizzi's 7-step |
| Grounded Theory | Constant comparison + theoretical coding |
| Focused Ethnography | Abductive thematic analysis with constant comparison |
| Generic Qualitative | Reflexive thematic analysis (Braun & Clarke, 2019, 2021) |

### 3.2 Theme Development

Each theme must include:
- **Definition**: One-sentence statement of what the theme captures
- **Evidence**: 2-3 cross-role quotes (e.g., nurse + surgeon + manager)
- **Boundary case**: At least one disconfirming or qualifying instance
- **Analytic commentary**: Interpretation, not just description

---

## Phase 4: Manuscript Writing

Refer to `references/manuscript-sections.md` for section-by-section guidance.

### Structure Overview (IJNS format)

1. **Abstract** — Structured: Background, Objectives, Design, Setting, Participants, Methods, Results, Conclusions (~300 words)
2. **Introduction** — Funnel structure: context → gap → theory → RQs (700-800 words)
3. **Methods** — COREQ-aligned subsections (see Phase 5)
4. **Results** — Thick description + themes with quotes (2500-3500 words)
5. **Discussion** — Theory dialogue + implications + limitations (2000-2500 words)
6. **References** — Vancouver format, all verified DOIs

Target total: **7,000-9,000 words** (excluding references) for IJNS.

### Key Writing Principles

1. **Thick description opening**: Start Results with an ethnographic vignette of the setting (sensory, temporal, spatial details)
2. **Show, don't tell**: Every claim backed by participant quotes with ID codes
3. **Cross-role triangulation**: Each theme should include perspectives from multiple participant types
4. **Boundary cases in every theme**: Disconfirming evidence strengthens, not weakens
5. **Discussion = theory dialogue**: Extend or challenge existing frameworks, don't just "compare with literature"
6. **Propose conceptual contributions**: Name new phenomena (e.g., "competence paradox," "misplaced visibility")

---

## Phase 5: Quality Assurance

### 5.1 COREQ Compliance

Refer to `references/coreq-checklist.md` for the full 32-item checklist.

**Five most commonly missed items** (Walsh et al., 2020 found only 5% of papers score ≥25/32):

1. **Researcher reflexivity statement** — Background, assumptions, biases, and how they may influence the study
2. **Relationship with participants** — Prior relationship before study commencement
3. **Data saturation** — How determined, at which interview, what criteria
4. **Non-participation** — Number who refused/withdrew and reasons
5. **Coding tree** — Visual representation of code-to-theme hierarchy

### 5.2 Reflexivity Statement (4 Dimensions)

Per Olmos-Vega et al. (2022) AMEE Guide No. 149:

1. **Personal**: Researcher's discipline, clinical experience, relationship to topic
2. **Interpersonal**: Power dynamics with participants, how interaction shaped data
3. **Methodological**: Why this method? How theoretical stance shaped analysis?
4. **Contextual**: Social, cultural, institutional context of the research

### 5.3 Reference Verification

Every reference must have:
- Verified DOI (test resolution via doi.org)
- PubMed PMID + link (for indexed papers)
- ISBN (for books)
- Use `reference-checker` skill or `scientific-skills:pubmed-database` skill if available

---

## Phase 6: Submission Package

### Required Components (IJNS example)

1. **Main document** — Blinded manuscript (remove author info)
2. **Title page** — Authors, affiliations, corresponding author, contributions, acknowledgments
3. **Structured abstract** — Per journal format
4. **Highlights** — 3-5 bullet points (Elsevier journals)
5. **Cover letter** — Why this journal, what's novel, ethical compliance
6. **COREQ checklist** — 32 items with page numbers
7. **Figure files** — 300 DPI minimum, TIFF preferred
8. **Table files** — Embedded or separate per journal requirements

### Cover Letter Template

```
Dear Editor,

Please find attached our manuscript entitled "[Title]" for consideration
as an Original Research Article in [Journal].

This [methodology] examines [phenomenon] among [population] in [context].
We believe this study contributes to [Journal] because:
1. [Theoretical contribution]
2. [Practical/policy implication]
3. [Methodological value]

We confirm that: [standard declarations]

Sincerely, [Author]
```

---

## Parallel Agent Strategy

For manuscript writing, use parallel agents for independent sections:

| Agent | Task | Dependencies |
|---|---|---|
| A | Results Part 1 (setting + themes 1-3) | Interview data |
| B | Results Part 2 (themes 4-6) | Interview data |
| C | Discussion | Completed Results |
| D | Introduction + Abstract + Table 1 | Research design |
| E | References | Completed manuscript |
| F | Figure 1 (thematic model) | Completed themes |

Launch A+B+D in parallel → wait → launch C → then E+F in parallel.

---

## Quality-Friendly SCI Journals

| Journal | IF | Qual-friendly? | Notes |
|---|---|---|---|
| IJNS | ~8 | Yes | Top nursing journal, accepts qual |
| J Adv Nurs | ~4 | Yes | Dedicated qual section |
| Qual Health Res | ~3 | Specialist | Qual-only flagship |
| Global Qual Nurs Res | ~2 | Specialist | Low APC, student discount |
| BMC Nursing | ~4 | Yes | OA, faster review |
| J Clin Nurs | ~4 | Yes | High qual volume |
| Soc Sci Med | ~5 | Yes | Interdisciplinary |
| Int J Nurs Stud Advances | ~5 | Yes | IJNS sister journal |
