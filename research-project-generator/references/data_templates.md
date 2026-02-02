# Data Generation Templates

Python code templates for generating realistic research data.

## Basic Data Generation Setup

```python
import numpy as np
import pandas as pd
from scipy import stats
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)
```

## Demographics Generation

### Age (Gaussian with constraints)

```python
def generate_age(n, mean_age, sd_age, min_age, max_age):
    """Generate ages within realistic bounds."""
    ages = []
    while len(ages) < n:
        age = np.random.normal(mean_age, sd_age)
        if min_age <= age <= max_age:
            ages.append(int(round(age)))
    return ages

# Examples:
# Pediatric: generate_age(n, 8, 3, 3, 16)
# Adult: generate_age(n, 45, 15, 18, 75)
# Elderly: generate_age(n, 72, 8, 60, 95)
```

### Sex Distribution

```python
def generate_sex(n, female_ratio=0.5):
    """Generate sex with specified female ratio."""
    return np.random.choice(['Male', 'Female'], n, p=[1-female_ratio, female_ratio])

# Disease-specific ratios:
# Breast cancer: female_ratio=0.99
# Prostate cancer: female_ratio=0.0
# Lupus: female_ratio=0.9
# General population: female_ratio=0.5
```

### BMI Generation

```python
def generate_bmi(n, mean=25, sd=5, min_bmi=16, max_bmi=50):
    """Generate BMI with realistic distribution."""
    bmis = []
    while len(bmis) < n:
        bmi = np.random.normal(mean, sd)
        if min_bmi <= bmi <= max_bmi:
            bmis.append(round(bmi, 1))
    return bmis
```

## Clinical Variables

### Continuous Variables (Normal)

```python
def generate_normal_var(n, mean, sd, decimal_places=1):
    """Generate normally distributed continuous variable."""
    values = np.random.normal(mean, sd, n)
    return [round(v, decimal_places) for v in values]

# Examples:
# IOP (mmHg): generate_normal_var(n, 15, 3)
# Visual acuity (logMAR): generate_normal_var(n, 0.2, 0.15)
# Blood pressure systolic: generate_normal_var(n, 125, 15)
```

### Continuous Variables (Skewed)

```python
def generate_skewed_var(n, mean, sd, skew='right'):
    """Generate skewed distribution using log-normal."""
    if skew == 'right':
        # Log-normal for right skew
        sigma = np.sqrt(np.log(1 + (sd/mean)**2))
        mu = np.log(mean) - sigma**2/2
        return np.random.lognormal(mu, sigma, n)
    else:
        # Reflect for left skew
        max_val = mean + 3*sd
        values = generate_skewed_var(n, mean, sd, 'right')
        return max_val - values

# Examples:
# Hospital length of stay: generate_skewed_var(n, 5, 3, 'right')
# Biomarker levels: generate_skewed_var(n, 50, 30, 'right')
```

### Categorical Variables

```python
def generate_categorical(n, categories, probabilities):
    """Generate categorical variable with specified distribution."""
    return np.random.choice(categories, n, p=probabilities)

# Examples:
# Disease stage: generate_categorical(n, ['I','II','III','IV'], [0.3,0.35,0.25,0.1])
# Smoking status: generate_categorical(n, ['Never','Former','Current'], [0.5,0.3,0.2])
```

## Treatment Effects

### Adding Treatment Effect

```python
def add_treatment_effect(baseline, effect_size, effect_sd=None):
    """Add treatment effect to baseline values."""
    n = len(baseline)
    if effect_sd is None:
        effect_sd = abs(effect_size) * 0.3  # 30% variability
    
    individual_effects = np.random.normal(effect_size, effect_sd, n)
    return baseline + individual_effects
```

### Creating Group Differences

```python
def create_two_groups(n_total, control_mean, control_sd, 
                      effect_size, allocation_ratio=1):
    """Generate two-group comparison data."""
    n_control = n_total // (1 + allocation_ratio)
    n_treatment = n_total - n_control
    
    control = np.random.normal(control_mean, control_sd, n_control)
    
    # Effect in same units as outcome
    treatment_mean = control_mean + effect_size
    treatment = np.random.normal(treatment_mean, control_sd, n_treatment)
    
    return control, treatment
```

## Time-to-Event Data

### Survival Data Generation

```python
def generate_survival_data(n, median_survival, hazard_ratio=1.0, 
                           max_follow_up=60, censoring_rate=0.2):
    """Generate survival times with censoring."""
    # Baseline hazard (exponential)
    lambda_base = np.log(2) / median_survival
    
    # Generate times
    survival_times = np.random.exponential(1/lambda_base, n)
    
    # Apply hazard ratio for treatment group (first half)
    n_treatment = n // 2
    survival_times[:n_treatment] = np.random.exponential(
        1/(lambda_base * hazard_ratio), n_treatment
    )
    
    # Apply censoring
    censoring_times = np.random.uniform(0, max_follow_up, n)
    
    observed_times = np.minimum(survival_times, censoring_times)
    events = survival_times <= censoring_times
    
    # Additional random censoring
    random_censor = np.random.random(n) < censoring_rate
    events[random_censor] = False
    
    return observed_times, events
```

## Missing Data

### Introduce Missing Values

```python
def add_missing_values(data, missing_rate=0.05, mechanism='MCAR'):
    """Add missing values to data."""
    data = data.copy()
    n = len(data)
    
    if mechanism == 'MCAR':
        # Missing completely at random
        missing_idx = np.random.random(n) < missing_rate
        data[missing_idx] = np.nan
    
    elif mechanism == 'MAR':
        # Missing at random (based on another variable)
        # Higher values more likely to be missing
        missing_prob = (data - data.min()) / (data.max() - data.min())
        missing_prob = missing_prob * missing_rate * 2
        missing_idx = np.random.random(n) < missing_prob
        data[missing_idx] = np.nan
    
    return data
```

## Outliers

### Add Realistic Outliers

```python
def add_outliers(data, outlier_rate=0.02, outlier_factor=3):
    """Add outliers to continuous data."""
    data = data.copy()
    n = len(data)
    n_outliers = int(n * outlier_rate)
    
    outlier_idx = np.random.choice(n, n_outliers, replace=False)
    data_sd = np.std(data)
    data_mean = np.mean(data)
    
    for idx in outlier_idx:
        # Random direction
        direction = np.random.choice([-1, 1])
        data[idx] = data_mean + direction * outlier_factor * data_sd
    
    return data
```

## Complete Dataset Example

```python
def generate_rct_dataset(n_total=100, seed=42):
    """Generate complete RCT dataset."""
    np.random.seed(seed)
    
    n_treatment = n_total // 2
    n_control = n_total - n_treatment
    
    data = {
        'ID': [f'P{i:03d}' for i in range(1, n_total+1)],
        'Group': ['Treatment']*n_treatment + ['Control']*n_control,
        'Age': generate_age(n_total, 55, 12, 30, 75),
        'Sex': generate_sex(n_total, 0.45),
        'BMI': generate_bmi(n_total, 27, 5),
    }
    
    # Baseline outcome (same for both groups)
    baseline = generate_normal_var(n_total, 20, 4)
    data['Baseline_Outcome'] = baseline
    
    # Follow-up outcome (treatment effect for treatment group)
    followup = baseline.copy()
    followup[:n_treatment] = add_treatment_effect(
        baseline[:n_treatment], effect_size=-3, effect_sd=1
    )
    followup[n_treatment:] = add_treatment_effect(
        baseline[n_treatment:], effect_size=0, effect_sd=1
    )
    data['Followup_Outcome'] = followup
    
    # Add some missing
    data['Followup_Outcome'] = add_missing_values(
        np.array(data['Followup_Outcome']), 0.05
    )
    
    return pd.DataFrame(data)
```

## Validation Checks

```python
def validate_dataset(df, expected_ranges):
    """Validate generated data against expected ranges."""
    issues = []
    
    for col, (min_val, max_val) in expected_ranges.items():
        if col in df.columns:
            actual_min = df[col].min()
            actual_max = df[col].max()
            
            if actual_min < min_val or actual_max > max_val:
                issues.append(f"{col}: range [{actual_min}, {actual_max}] "
                            f"outside expected [{min_val}, {max_val}]")
    
    return issues

# Example usage:
expected = {
    'Age': (18, 90),
    'BMI': (15, 50),
    'IOP': (5, 40),
}
issues = validate_dataset(df, expected)
```
