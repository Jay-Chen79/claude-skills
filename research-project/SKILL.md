---
name: research-project
description: |
  Use when user wants to generate teaching/educational research projects with realistic but fictional data,
  including research papers, datasets, charts, and ethics documents.
  Trigger on: "research project", "teaching materials", "fictional study", "sample data", "mock research",
  "generate study", "create academic materials"
---

# Research Project Generator

## Overview

Generate complete educational research project materials for teaching purposes. Creates realistic but fictional studies across all research fields with IMRaD-format papers, high-fidelity data, visualizations, and IRB/ethics documents.

**IMPORTANT:** All projects are **educational tools only** - clearly marked as fictional to prevent misuse.

## When to Use

**Trigger phrases:**
- "Generate a research project"
- "Create teaching materials for research methods"
- "Need fictional data for my class"
- "Mock IRB application"
- "Sample research paper"
- "Generate a study about..."

**Do NOT use for:**
- Real research proposals
- Actual data collection
- Genuine ethics submissions
- Any form of academic misconduct

---

## Five-Phase Workflow

**CRITICAL: Each phase REQUIRES user confirmation before proceeding.**

```
Phase 1: Clarification
    ↓ User confirms
Phase 2: Outline
    ↓ User confirms
Phase 3: Paper
    ↓ User confirms
Phase 4: Data
    ↓ User confirms
Phase 5: Charts & Ethics
    → Complete
```

---

## Phase 1: Clarification Questions

Ask these questions **ONE AT A TIME**. Wait for answer before asking next.

### Mandatory Questions

| # | Question | Purpose | Options to Present |
|---|----------|---------|-------------------|
| 1 | What is the **research field/domain**? | Determines data patterns and methodology | Biomedical, Social Science, Engineering, Humanities, Business, Physical Science, Other |
| 2 | What is the **research methodology**? | Determines study design and statistical approaches | Experimental, Quasi-experimental, Observational, Survey, Qualitative, Mixed Methods, Meta-analysis, Case Study |
| 3 | What is the **target sample size**? | Determines data generation parameters | Small (n<50), Medium (n=50-200), Large (n>200), Specify exact number |
| 4 | What **statistical methods** should be used? | Determines analysis approach and results | Descriptive only, t-tests/ANOVA, Regression, Correlation, Chi-square, Non-parametric, Advanced (specify) |
| 5 | What is the **intended educational level**? | Determines paper complexity and terminology | High school, Undergraduate, Graduate, Professional |
| 6 | Are there **specific variables** to include? | Ensures relevant data dimensions | Dependent variable(s), Independent variable(s), Covariates, Demographics |
| 7 | What **statistical software** is being taught? | Determines output format | SPSS, R, Python, Stata, SAS, Excel, None needed |
| 8 | Any **classic papers** to reference? | Ensures citation relevance | Specify authors/years/topics, or use automatic selection |

### Exit Condition for Phase 1

Proceed when sufficient detail exists to generate a coherent project outline. If user appears stuck, offer preset "research templates":

- **"Simple Two-Group Experiment"** - t-test focus, control vs treatment
- **"Survey Correlational Study"** - Regression focus, multiple variables
- **"Pre-Post Intervention"** - Paired t-test focus, before/after design
- **"Multi-Group Comparison"** - ANOVA focus, 3+ groups

---

## Phase 2: Generate Outline

### Create outline with these sections:

1. **Study Background**
   - Research gap/opportunity
   - Theoretical framework
   - Significance

2. **Research Questions/Hypotheses**
   - Primary question(s)
   - Secondary questions (if applicable)
   - Specific hypotheses (directional if appropriate)

3. **Methods Overview**
   - Study design
   - Participants/recruitment
   - Measures/instruments
   - Procedure
   - Analysis plan

4. **Expected Results**
   - Descriptive statistics plan
   - Inferential statistics plan
   - Potential findings

5. **Discussion Framework**
   - Interpretation approach
   - Limitations to acknowledge
   - Implications

6. **Data Structure**
   - Variables list with types
   - Missing data strategy
   - Outlier handling approach

### Confirmation Template

```
Based on your inputs, here's the project outline:

[Insert outline]

Does this outline capture what you need? Any adjustments?
```

---

## Phase 3: Generate Research Paper (IMRaD Format)

### File: `{project-folder}/paper/{project-name}-paper.md`

### Required Sections:

#### Title Page
- Title
- Fictional authors (realistic names for the field)
- Affiliation (fictional but realistic)
- Date

#### Abstract (150-250 words)
- Background (1-2 sentences)
- Methods (2-3 sentences)
- Results (2-3 sentences with key findings)
- Conclusion (1-2 sentences)
- Keywords (5-7 terms)

#### Introduction (~500-800 words)
- Hook and context
- Problem statement
- Literature review citing 3-5 **real classic papers**
- Theoretical framework
- Research questions/hypotheses
- Significance/rationale

#### Methods (~400-600 words)
- **Study Design:** Type, groups, timing
- **Participants:** N=___, demographics, recruitment method
- **Materials/Instruments:** Validity/reliability info where relevant
- **Procedure:** Step-by-step process
- **Data Analysis Plan:** Statistical tests, alpha level (typically .05), software used
- **Ethical Considerations:** IRB approval, informed consent, confidentiality

#### Results (~400-600 words)
- **Descriptive Statistics:** Table 1 with demographics, means/SDs
- **Main Inferential Results:** Tables/Figures with:
  - Exact test statistics (t, F, χ², r, etc.)
  - Exact p-values
  - Effect sizes (Cohen's d, η², R², etc.)
  - Confidence intervals where appropriate
- **Supplementary Analyses:** (if applicable)

#### Discussion (~600-800 words)
- **Interpretation of Findings:** What do results mean?
- **Comparison to Prior Research:** How do they align with literature?
- **Theoretical Implications:** Contributions to theory
- **Practical Implications:** Real-world applications
- **Limitations:** 3-5 specific limitations
- **Future Research Directions:** Suggested next studies
- **Conclusion:** Brief summary and take-home message

#### References
- **8-12 citations total**
- **Mix of real classic papers and clearly marked fictional papers**
- Fictional papers must include: `*Fictional citation for educational purposes only*`
- Use appropriate format (APA, MLA, Chicago, etc.) for field

### Writing Standards
- Academic tone appropriate for educational level
- Clear transitions between sections
- Precise statistical reporting (APA style or field equivalent)
- Avoid overclaiming - stay modest about findings

### Confirmation Template

```
Paper generated at: {path}

Key sections:
- Title: {title}
- Hypotheses: {n} hypotheses
- Sample: N={sample_size}
- Main finding: {brief_summary}

Review the paper. Any sections to revise?
```

---

## Phase 4: Generate Raw Data

### Files to Create:
- `{project-folder}/data/raw/{project-name}-data.xlsx` - Main dataset
- `{project-folder}/data/codebook.md` - Variable definitions
- `{project-folder}/data/data-dictionary.md` - Complete documentation

### Data Requirements:

#### 1. Variable Types
- ID variables (participant IDs)
- Independent variable(s) with appropriate coding
- Dependent variable(s) with realistic distributions
- Covariates (age, gender, etc.) as appropriate
- Missing values (MCAR pattern, ~5-10%)

#### 2. Realism Constraints
- Follow known distribution patterns for the field
- Include plausible outliers (1-3% of data)
- Ensure effect sizes match planned statistical power
- Include realistic within-group variability
- Correlations between related variables should be sensible

#### 3. Statistical Properties
- Means/SDs appropriate for population
- Group differences matching hypotheses
- P-values reflecting planned significance (or not)
- Correct degrees of freedom for design

#### Excel Structure (Multiple Sheets):
- **Sheet 1: Raw Data** - Formatted with headers, appropriate data types
- **Sheet 2: Data Dictionary** - Variable names, labels, values, missing codes
- **Sheet 3: Summary Statistics** - Descriptives by group
- **Sheet 4: Embedded Charts** - Excel-generated visualizations

### Python Data Generation Template

```python
import pandas as pd
import numpy as np
from scipy import stats

# Set seed for reproducibility
np.random.seed(42)

# Define parameters
N = 100  # Sample size
alpha = 0.05

# Generate variables with realistic patterns
# Example: Two-group experimental design
group = np.random.choice(['Control', 'Treatment'], size=N, p=[0.5, 0.5])

# Generate DV with effect size
control_mean, treatment_mean = 100, 108  # Cohen's d ≈ 0.5
control_scores = np.random.normal(control_mean, 15, sum(group=='Control'))
treatment_scores = np.random.normal(treatment_mean, 15, sum(group=='Treatment'))

# Add small missing data
missing_mask = np.random.random(N) < 0.05  # 5% MCAR

# Create DataFrame and save to Excel
df = pd.DataFrame({'group': group, 'score': scores})
df.to_excel('data.xlsx', index=False, sheet_name='Raw Data')
```

### Confirmation Template

```
Data generated at: {path}

- Variables: {n} variables
- Sample size: N={n}
- Missing data: {percent}%
- Effect size: {effect_size}

Review the data. Any variables to adjust?
```

---

## Phase 5: Generate Charts and Ethics Documents

### Charts

#### Files to Create:
- `{project-folder}/charts/{project-name}-figure1.py` - Python code
- `{project-folder}/charts/{project-name}-figure1.png` - Rendered figure
- `{project-folder}/charts/conceptual-diagram.png` - Study design diagram

#### Required Figures:

1. **Conceptual Diagram**
   - Study design flowchart (participants → groups → measures → analysis)
   - Variables and relationships
   - Group comparisons (if applicable)

2. **Results Visualizations** (2-3 figures appropriate for methodology)

| Methodology | Recommended Charts |
|-------------|-------------------|
| Experimental | Bar charts with error bars, interaction plots |
| Correlational | Scatter plots with regression lines |
| Survey | Likert scale distributions, stacked bar charts |
| Pre-post | Paired comparison plots, before-after figures |
| Longitudinal | Line charts with confidence intervals |

#### Technical Requirements:
- Python/Matplotlib code provided
- Publication-quality figures (300 DPI, appropriate sizing)
- Colorblind-friendly palettes (use viridis, ColorBrewer)
- Clear axis labels, legends, titles
- APA-style formatting where appropriate

### Python Chart Template:

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.figsize'] = (6, 4)

# Colorblind-friendly palette
colors = sns.color_palette("colorblind")

# Create plot
fig, ax = plt.subplots()
# [plotting code]

# Labels and styling
ax.set_xlabel('X Label', fontsize=12)
ax.set_ylabel('Y Label', fontsize=12)
ax.set_title('Figure Title', fontsize=14, fontweight='bold')
ax.legend(['Group 1', 'Group 2'])

plt.tight_layout()
plt.savefig('figure1.png', dpi=300, bbox_inches='tight')
plt.close()
```

### Ethics Documents

#### Files to Create:
- `{project-folder}/ethics/irb-application.md`
- `{project-folder}/ethics/consent-form-template.md`
- `{project-folder}/ethics/risk-assessment.md`

#### IRB Application Sections:
1. Study Summary (purpose, design, duration)
2. Recruitment Methods
3. Risks and Benefits
4. Confidentiality Procedures
5. Informed Consent Process
6. Data Security Measures
7. Compensation (if applicable)
8. Investigator Qualifications

#### Informed Consent Template Sections:
1. Study Purpose
2. Procedures
3. Risks/Discomforts
4. Benefits
5. Confidentiality
6. Voluntary Participation/Withdrawal
7. Contact Information
8. Signature Lines

#### Risk Assessment Matrix:
| Risk Type | Likelihood | Severity | Mitigation Strategy |
|-----------|------------|----------|---------------------|
| Physical | Minimal | None | N/A |
| Psychological | Low | Mild | Debriefing, counseling resources |
| Social | Minimal | None | Anonymous data collection |

### Completion Template

```
✅ Research project generation complete!

Project: {project_name}
Location: {project_path}

Generated files:
├── paper/
│   └── {project-name}-paper.md
├── data/
│   ├── raw/{project-name}-data.xlsx
│   ├── codebook.md
│   └── data-dictionary.md
├── charts/
│   ├── {project-name}-figure1.py
│   ├── {project-name}-figure1.png
│   └── conceptual-diagram.png
├── ethics/
│   ├── irb-application.md
│   ├── consent-form-template.md
│   └── risk-assessment.md
└── references/
    └── citations.md

Total files: {n}

Remember: This is a fictional educational project. Do not use for actual research.
```

---

## File Organization

```
{project-name}/
├── README.md                # Project overview and file guide
├── paper/
│   └── {project-name}-paper.md
├── data/
│   ├── raw/
│   │   └── {project-name}-data.xlsx
│   ├── codebook.md
│   └── data-dictionary.md
├── charts/
│   ├── {project-name}-figure1.py
│   ├── {project-name}-figure1.png
│   └── conceptual-diagram.png
├── ethics/
│   ├── irb-application.md
│   ├── consent-form-template.md
│   └── risk-assessment.md
└── references/
    └── citations.md
```

### Naming Conventions
- Project folder: Slugify title (e.g., `effects-of-caffeine-on-cognitive-performance`)
- Paper: `{project-slug}-paper.md`
- Data: `{project-slug}-data.xlsx`
- Charts: `{project-slug}-figure{n}.{ext}`

---

## Quality Checks

### Data Realism Verification

| Check | Standard |
|-------|----------|
| Distribution | Matches field patterns (normal, skewed, bimodal as appropriate) |
| Effect Size | Cohen's conventions: small=0.2, medium=0.5, large=0.8 |
| Sample Size | Adequate power (>0.70) for planned tests |
| Missing Data | MCAR pattern, 5-10% maximum |
| Outliers | 1-3% of data, plausible values |
| Correlations | Sensible relationships between variables |

### Statistical Validity

| Check | Standard |
|-------|----------|
| P-values | Align with effect sizes and sample sizes |
| Degrees of Freedom | Correct for design |
| Effect Sizes | Reported with confidence intervals where appropriate |
| Test Assumptions | Addressed (normality, homoscedasticity, independence) |

### Reference Accuracy

| Type | Requirement |
|------|-------------|
| Classic Papers | **REAL citations only** - verify via known sources |
| Fictional Papers | Clearly marked with `*Educational purposes only*` |
| Formatting | Strict APA/MLA/Chicago as appropriate |

### Example: Real Classic Citations by Field

| Field | Example Classics |
|-------|------------------|
| Psychology | Bandura (1977), Festinger (1957), Milgram (1963) |
| Medicine | Cohen (1988), Sackett (1996) |
| Education | Bloom (1956), Vygotsky (1978) |
| Sociology | Bourdieu (1984), Goffman (1959) |

---

## Dependencies

### Python Packages

```
pandas>=2.0.0           # Data manipulation and Excel export
numpy>=1.24.0           # Statistical distributions and random generation
matplotlib>=3.7.0       # Visualization
openpyxl>=3.1.0         # Excel file writing with formatting
scipy>=1.10.0           # Statistical functions
seaborn>=0.12.0         # Enhanced plotting with colorblind palettes
```

### Installation

```bash
pip install pandas numpy matplotlib openpyxl scipy seaborn
```

---

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Generate all phases at once | **Wait for confirmation at each phase** |
| Use unrealistic effect sizes | **Cohen's conventions for field** |
| Skip missing data | **Include 5-10% MCAR pattern** |
| Fictional classic citations | **Use real seminal works only** |
| No ethical disclaimers | **Clearly mark as educational only** |
| Data doesn't match paper | **Ensure statistics align between data and paper** |

---

## Red Flags - STOP and Ask User

| Situation | Action |
|-----------|--------|
| User wants to use for real research | Clarify educational purpose, add disclaimers |
| Request for non-consensual data | Refuse - educational projects must model ethical research |
| Request for deceptive materials | Refuse - teaching materials must demonstrate ethical practices |
| Request to bypass ethics review | Explain that all research (even fictional) should demonstrate ethics awareness |

---

## Quick Reference Summary

1. **Ask questions ONE AT A TIME** in Phase 1
2. **Get CONFIRMATION** before each subsequent phase
3. **Use REAL classic citations** only
4. **Mark clearly as educational** throughout
5. **Ensure data-paper alignment** - statistics must match
6. **Generate ALL file types**: paper, data, charts, ethics
