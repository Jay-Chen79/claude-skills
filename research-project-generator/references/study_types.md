# Study Type Guidelines

Detailed specifications for each research design.

## Randomized Controlled Trial (RCT)

### Data Generation Specifics

**Required variables**:
- Randomization ID
- Allocation group (Treatment/Control)
- Randomization date
- Stratification factors (if any)

**Baseline balance**: Generate data so groups are similar at baseline (p>0.05 for demographics).

**Sample distribution example** (N=100):
```python
treatment_n = 50  # or use block randomization
control_n = 50
```

**Dropout simulation**:
- Typical rates: 5-20% depending on study duration
- Reasons: lost to follow-up, withdrawal, adverse events
- ITT: include all randomized; Per-protocol: exclude dropouts

### Paper Sections Emphasis

**Methods must include**:
- Eligibility criteria (inclusion/exclusion)
- Randomization method (block, stratified, simple)
- Allocation concealment
- Blinding (who was blinded, how maintained)
- Sample size calculation rationale

**Results must include**:
- CONSORT flow diagram
- Baseline table comparing groups
- Primary analysis with 95% CI
- Per-protocol sensitivity analysis
- Adverse events table

### CONSORT Flow Diagram Template

```
Assessed for eligibility (n=XXX)
    |
    ├── Excluded (n=XX)
    │   ├── Not meeting criteria (n=XX)
    │   ├── Declined to participate (n=XX)
    │   └── Other reasons (n=XX)
    |
Randomized (n=XXX)
    |
    ├── Allocated to intervention (n=XX)
    │   ├── Received intervention (n=XX)
    │   └── Did not receive (n=XX, reasons)
    |
    ├── Allocated to control (n=XX)
    │   ├── Received control (n=XX)
    │   └── Did not receive (n=XX, reasons)
    |
    ├── Lost to follow-up (intervention: n=XX, control: n=XX)
    |
    └── Analyzed (intervention: n=XX, control: n=XX)
```

---

## Cohort Study

### Data Generation Specifics

**Required variables**:
- Enrollment date
- Exposure status (binary or categorical)
- Follow-up visits with dates
- Event occurrence (yes/no)
- Event date (if occurred)
- Censoring date (if no event)

**Time-to-event data**:
```python
# Person-years calculation
follow_up_months = random.gauss(24, 6)  # mean 2 years
event_occurred = random.random() < event_rate
if event_occurred:
    event_time = random.exponential(scale=mean_survival)
```

**Loss to follow-up**: 
- Simulate 5-15% over study duration
- Can be random or differential

### Paper Sections Emphasis

**Methods must include**:
- Cohort definition and source
- Exposure ascertainment
- Outcome ascertainment
- Follow-up procedures
- Handling of loss to follow-up

**Results must include**:
- Follow-up duration (median, IQR)
- Person-years at risk
- Incidence rates by exposure
- Hazard ratios or relative risks with 95% CI
- Kaplan-Meier curves (if applicable)

---

## Case-Control Study

### Data Generation Specifics

**Case-control ratio**: Usually 1:1 to 1:4

**Matching variables** (if matched):
- Age (±5 years)
- Sex
- Other relevant factors

**Exposure data**:
```python
# Odds ratio = (a*d)/(b*c)
# To achieve target OR, adjust exposure rates
case_exposure_rate = 0.40  # higher if OR > 1
control_exposure_rate = 0.25
```

**Recall bias simulation**: 
- Cases may recall exposures differently
- Can introduce slight differential misclassification

### Paper Sections Emphasis

**Methods must include**:
- Case definition and source
- Control selection method
- Matching criteria (if any)
- Exposure assessment method
- How recall bias was minimized

**Results must include**:
- Cases and controls characteristics
- Exposure frequencies by group
- Crude and adjusted odds ratios
- Stratified analyses (if matching)

---

## Cross-Sectional Study

### Data Generation Specifics

**Single time point**: All variables measured simultaneously

**Prevalence calculation**:
```python
# Number with condition / Total sample
prevalence = diseased_n / total_n
# 95% CI using Wilson score interval
```

**Sampling weights** (if complex sampling):
- Stratification weights
- Cluster adjustments

### Paper Sections Emphasis

**Methods must include**:
- Sampling frame and method
- Response rate
- Data collection procedures
- Variable definitions

**Results must include**:
- Response rate
- Prevalence with 95% CI
- Association measures (prevalence ratios or ORs)
- Subgroup analyses

**Limitations must address**:
- Cannot establish temporality
- Prevalent cases only (survival bias)
- Potential selection bias

---

## Case Series

### Data Generation Specifics

**No control group**: Descriptive only

**Variables**:
- Demographics
- Clinical presentation
- Treatment details
- Outcomes

**Sample sizes**: Typically 5-50 cases

### Paper Sections Emphasis

**Focus on**:
- Detailed case descriptions
- Common patterns across cases
- Unique or notable features
- Comparison to literature

**Must acknowledge**:
- Cannot establish causation
- No comparison group
- Potential selection bias

---

## Statistical Test Selection Guide

| Comparison | Outcome Type | Distribution | Test |
|------------|--------------|--------------|------|
| 2 groups | Continuous | Normal | Independent t-test |
| 2 groups | Continuous | Non-normal | Mann-Whitney U |
| >2 groups | Continuous | Normal | One-way ANOVA |
| >2 groups | Continuous | Non-normal | Kruskal-Wallis |
| 2 groups | Categorical | - | Chi-square / Fisher's exact |
| Paired | Continuous | Normal | Paired t-test |
| Paired | Continuous | Non-normal | Wilcoxon signed-rank |
| Correlation | Continuous | Normal | Pearson's r |
| Correlation | Continuous | Non-normal | Spearman's rho |
| Time-to-event | - | - | Log-rank test |

---

## Effect Size Benchmarks

### Cohen's d (continuous outcomes)
- Small: 0.2
- Medium: 0.5
- Large: 0.8

### Odds Ratio
- Small: 1.5
- Medium: 2.0
- Large: 3.0

### Relative Risk
- Small: 1.2
- Medium: 1.5
- Large: 2.0

### Correlation (r)
- Small: 0.1
- Medium: 0.3
- Large: 0.5
