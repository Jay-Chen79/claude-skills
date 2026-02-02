---
name: research-project-generator
description: "Generate complete educational research projects for teaching purposes. Creates: (1) Full academic paper with title, abstract, introduction, methods, results, discussion, and real references with in-text citations, (2) Realistic virtual raw data in Excel matching real-world patterns, (3) Statistical figures and charts from the data, (4) Ethics application documents. Use when asked to create a teaching/educational research project, mock study, sample research for students, or complete research package for educational purposes."
---

# Educational Research Project Generator

Generate complete research project packages for teaching purposes.

## Workflow Overview

1. **Gather project requirements** via interactive Q&A
2. **Generate raw data** matching real-world patterns
3. **Create statistical analyses and figures**
4. **Write academic paper** with proper citations
5. **Generate ethics documents**
6. **Package all outputs**

## Step 1: Requirements Gathering

When given a research topic, gather essential information before proceeding. Ask about:

### Required Information
- **Study type**: RCT, cohort, case-control, cross-sectional, case series
- **Sample size**: Total N, group distribution
- **Primary outcome**: Main variable being measured
- **Groups/arms**: Control vs intervention, or exposure categories

### Context-Dependent Questions
Based on study type, ask relevant follow-ups:

**Clinical trials**:
- Intervention details, dosing, duration
- Randomization method
- Blinding status

**Observational studies**:
- Follow-up period
- Matching criteria (if case-control)
- Exposure definition

**All studies**:
- Key demographics to include
- Secondary outcomes
- Expected effect size direction (positive/negative/null)

### Question Strategy
- Ask 3-5 essential questions first
- Follow up based on answers
- Proceed when core parameters are clear
- Offer sensible defaults for unspecified details

## Step 2: Data Generation

Create realistic virtual data in Excel format.

### Data Realism Principles

**Demographics must reflect real populations**:
- Age: appropriate distribution for condition (e.g., pediatric vs geriatric)
- Sex: use real-world ratios unless study-specific
- Include relevant comorbidities at realistic rates

**Outcome variables**:
- Match real-world ranges (e.g., IOP 10-21 mmHg for normal eyes)
- Include appropriate variance (not too perfect)
- Add realistic outliers (2-5%)
- Missing data at realistic rates (1-10%)

**Effect sizes**:
- Base on published literature when possible
- Use clinically meaningful differences
- Statistical significance should be realistic (not all p<0.001)

### Data Structure Template

```
Sheet 1: Raw Data
- ID, Demographics, Baseline measures, Follow-up measures, Outcomes

Sheet 2: Data Dictionary
- Variable name, Description, Type, Units, Valid range

Sheet 3: Summary Statistics
- Formulas calculating means, SDs, frequencies
```

### Excel Generation
Use openpyxl for data creation. See /mnt/skills/public/xlsx/SKILL.md for detailed Excel formatting rules.

Key requirements:
- Use Excel formulas for summary statistics
- Apply proper number formatting
- Include data validation where appropriate
- Run recalc.py after creation

## Step 3: Statistical Analyses and Figures

### Required Analyses (study-type dependent)

**Descriptive statistics**:
- Table 1: Demographics by group
- Continuous: mean ± SD or median (IQR)
- Categorical: n (%)

**Comparative statistics**:
- Choose test based on data type and distribution
- Report exact p-values (not p<0.05)
- Include effect sizes and 95% CIs

**Regression (if applicable)**:
- Univariate then multivariate
- Report coefficients, CIs, p-values

### Figure Generation

Create publication-quality figures using Python matplotlib/seaborn:

**Standard figures**:
1. Flow diagram (enrollment/exclusions)
2. Primary outcome comparison (bar/box plot)
3. Correlation or trend plots
4. Kaplan-Meier if survival data

**Figure requirements**:
- Resolution: 300 DPI minimum
- Format: PNG or TIFF
- Consistent styling across all figures
- Clear axis labels with units
- Error bars where appropriate

## Step 4: Academic Paper

### Document Structure

```
1. Title Page
   - Title (concise, informative)
   - Authors (use placeholder names)
   - Affiliations
   - Corresponding author

2. Abstract (structured)
   - Purpose/Background
   - Methods
   - Results
   - Conclusions
   - Keywords

3. Introduction
   - Background and significance
   - Literature gap
   - Study objectives

4. Methods
   - Study design
   - Participants
   - Interventions/Exposures
   - Outcomes
   - Statistical analysis
   - Ethics statement

5. Results
   - Participant flow
   - Baseline characteristics (Table 1)
   - Primary outcome
   - Secondary outcomes
   - Adverse events (if applicable)

6. Discussion
   - Key findings summary
   - Comparison with literature
   - Strengths and limitations
   - Clinical implications
   - Future directions

7. References
   - Real, verifiable citations
   - Proper formatting (Vancouver or APA)
```

### Citation Requirements

**CRITICAL: Use only real, verifiable references**

Web search for:
- Seminal papers in the field
- Recent systematic reviews/meta-analyses
- Guidelines or consensus statements
- Similar methodology papers

For each citation:
- Verify the paper exists
- Confirm authors and year
- Use correct journal name
- Include DOI when available

In-text citation format:
- Vancouver style: superscript numbers [1,2,3]
- Number in order of appearance

### Document Generation
Use docx-js for Word document creation. See /mnt/skills/public/docx/SKILL.md for formatting rules.

## Step 5: Ethics Documents

Generate IRB/ethics committee application materials:

### Ethics Package Contents

1. **Protocol synopsis** (1-2 pages)
   - Study title
   - Principal investigator
   - Study objectives
   - Design summary
   - Population and sample size
   - Key procedures
   - Risk/benefit assessment

2. **Informed consent template**
   - Study purpose (lay language)
   - Procedures
   - Risks and benefits
   - Confidentiality
   - Voluntary participation
   - Contact information

3. **Data management plan**
   - Data collection methods
   - Storage and security
   - Access controls
   - Retention period

## Output Organization

Create organized folder structure:

```
[Project_Name]/
├── Paper/
│   └── manuscript.docx
├── Data/
│   ├── raw_data.xlsx
│   └── data_dictionary.xlsx
├── Figures/
│   ├── figure1_flowchart.png
│   ├── figure2_primary_outcome.png
│   └── figure3_secondary.png
├── Tables/
│   └── tables.xlsx (Tables 1-N with formatting)
├── Ethics/
│   ├── protocol_synopsis.docx
│   ├── informed_consent.docx
│   └── data_management_plan.docx
└── README.txt
```

## Study Type Reference

### RCT Checklist
- [ ] CONSORT flow diagram
- [ ] Randomization description
- [ ] Blinding details
- [ ] ITT vs per-protocol analysis
- [ ] Trial registration mention

### Cohort Study Checklist
- [ ] Exposure definition
- [ ] Follow-up duration
- [ ] Loss to follow-up rate
- [ ] Time-to-event analysis if applicable

### Case-Control Checklist
- [ ] Case definition
- [ ] Control selection criteria
- [ ] Matching variables
- [ ] Odds ratios with CIs

### Cross-Sectional Checklist
- [ ] Sampling method
- [ ] Response rate
- [ ] Prevalence calculations
- [ ] Limitations of temporality

## Quality Checks

Before delivering outputs:

- [ ] Data ranges are realistic for the condition
- [ ] Statistics match the raw data
- [ ] Figures accurately represent data
- [ ] All references are real and accessible
- [ ] In-text citations match reference list
- [ ] Methods and results are internally consistent
- [ ] Effect sizes are clinically plausible
- [ ] Ethics documents align with study design
