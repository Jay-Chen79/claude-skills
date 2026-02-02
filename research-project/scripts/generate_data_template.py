"""
Research Project Data Generator - Template
This is a template for generating realistic research data for educational purposes.
Modify this template according to your specific research design.
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURATION - Modify for your study
# ============================================

# Random seed for reproducibility
np.random.seed(42)

# Sample size
N = 100  # Total participants

# Study groups (for experimental designs)
GROUPS = ['Control', 'Treatment']
GROUP_PROPORTIONS = [0.5, 0.5]

# Missing data proportion (MCAR - Missing Completely At Random)
MISSING_RATE = 0.05  # 5% missing data

# ============================================
# DATA GENERATION
# ============================================

def generate_demographics(n):
    """Generate realistic demographic variables"""
    data = {}

    # Participant ID
    data['participant_id'] = range(1, n + 1)

    # Age (example: adults 18-65, roughly normal distribution)
    data['age'] = np.random.normal(35, 12, n).astype(int)
    data['age'] = np.clip(data['age'], 18, 65)

    # Gender (categorical)
    data['gender'] = np.random.choice(['Male', 'Female', 'Non-binary', 'Prefer not to say'],
                                      n, p=[0.45, 0.48, 0.05, 0.02])

    # Education level (ordinal)
    data['education'] = np.random.choice(['High School', 'Bachelor', 'Master', 'Doctorate'],
                                         n, p=[0.25, 0.40, 0.25, 0.10])

    return pd.DataFrame(data)

def generate_two_group_experiment(n, effect_size=0.5):
    """
    Generate data for a two-group experimental design.

    Parameters:
    - n: Total sample size
    - effect_size: Cohen's d (0.2=small, 0.5=medium, 0.8=large)
    """
    # Assign groups
    group_assignment = np.random.choice(GROUPS, n, p=GROUP_PROPORTIONS)

    # Group sizes
    n_control = sum(group_assignment == 'Control')
    n_treatment = sum(group_assignment == 'Treatment')

    # Generate outcome variable with specified effect size
    # Assuming pooled SD = 15 (common in social sciences)
    pooled_sd = 15

    control_mean = 100
    treatment_mean = control_mean + (effect_size * pooled_sd)

    control_scores = np.random.normal(control_mean, pooled_sd, n_control)
    treatment_scores = np.random.normal(treatment_mean, pooled_sd, n_treatment)

    # Combine scores
    scores = np.concatenate([control_scores, treatment_scores])
    np.random.shuffle(scores)  # Match with shuffled group assignment

    df = pd.DataFrame({
        'group': group_assignment,
        'outcome_score': scores
    })

    return df

def add_missing_data(df, missing_rate=0.05):
    """Add MCAR (Missing Completely At Random) missing data"""
    df_missing = df.copy()

    for col in df_missing.select_dtypes(include=[np.number]).columns:
        if col != 'participant_id':  # Don't add missing to ID
            missing_mask = np.random.random(len(df_missing)) < missing_rate
            df_missing.loc[missing_mask, col] = np.nan

    return df_missing

def add_outliers(df, outlier_rate=0.02, n_sd=3):
    """Add a small proportion of realistic outliers"""
    df_outliers = df.copy()

    numeric_cols = df_outliers.select_dtypes(include=[np.number]).columns
    n_outliers = int(len(df_outliers) * outlier_rate)

    for col in numeric_cols:
        if col != 'participant_id':
            # Randomly select indices for outliers
            outlier_indices = np.random.choice(len(df_outliers), n_outliers, replace=False)
            mean = df_outliers[col].mean()
            sd = df_outliers[col].std()

            # Add extreme values
            df_outliers.loc[outlier_indices, col] = mean + (n_sd * sd * np.random.choice([-1, 1], n_outliers))

    return df_outliers

def calculate_summary_stats(df, group_col=None, outcome_col=None):
    """Calculate descriptive statistics"""
    if group_col and outcome_col:
        # Group-wise statistics
        summary = df.groupby(group_col)[outcome_col].agg([
            ('N', 'count'),
            ('Mean', 'mean'),
            ('SD', 'std'),
            ('Min', 'min'),
            ('Max', 'max'),
            ('Missing', lambda x: x.isna().sum())
        ]).round(2)

        # Add t-test results
        groups = df[group_col].unique()
        if len(groups) == 2:
            group1 = df[df[group_col] == groups[0]][outcome_col].dropna()
            group2 = df[df[group_col] == groups[1]][outcome_col].dropna()

            t_stat, p_value = stats.ttest_ind(group1, group2)

            # Cohen's d
            pooled_sd = np.sqrt(((len(group1)-1)*group1.std()**2 + (len(group2)-1)*group2.std()**2) /
                               (len(group1) + len(group2) - 2))
            cohens_d = (group1.mean() - group2.mean()) / pooled_sd

            summary.loc['Test statistic'] = ['', t_stat, '', '', '', '']
            summary.loc['p-value'] = ['', p_value, '', '', '', '']
            summary.loc["Cohen's d"] = ['', cohens_d, '', '', '', '']

    else:
        # Overall statistics
        summary = df.describe().round(2)

    return summary

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Generate complete research dataset"""

    # 1. Generate demographics
    print("Generating demographics...")
    demographics = generate_demographics(N)

    # 2. Generate experimental data
    print("Generating experimental data...")
    experiment = generate_two_group_experiment(N, effect_size=0.5)

    # 3. Combine datasets
    print("Combining datasets...")
    df = pd.concat([demographics, experiment], axis=1)

    # 4. Add missing data
    print(f"Adding {MISSING_RATE*100}% missing data...")
    df = add_missing_data(df, missing_rate=MISSING_RATE)

    # 5. Add outliers
    print("Adding realistic outliers...")
    df = add_outliers(df, outlier_rate=0.02)

    # 6. Calculate summary statistics
    print("Calculating summary statistics...")
    summary = calculate_summary_stats(df, 'group', 'outcome_score')

    # 7. Save to Excel with multiple sheets
    output_file = 'research_data.xlsx'
    print(f"Saving to {output_file}...")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        summary.to_excel(writer, sheet_name='Summary Statistics')

        # Data dictionary sheet
        data_dict = pd.DataFrame({
            'Variable': df.columns,
            'Type': df.dtypes.astype(str),
            'Description': [
                'Unique participant identifier',
                'Age in years (18-65)',
                'Self-reported gender',
                'Highest education level',
                'Experimental group assignment',
                'Primary outcome measure (continuous)'
            ],
            'Missing Code': ['None', 'NaN', 'NaN', 'None', 'None', 'NaN']
        })
        data_dict.to_excel(writer, sheet_name='Data Dictionary', index=False)

    print(f"\n✅ Data generation complete!")
    print(f"   - Total participants: {N}")
    print(f"   - Variables: {len(df.columns)}")
    print(f"   - Missing data: {df.isna().sum().sum()} cells")
    print(f"   - Output file: {output_file}")

    # Print summary statistics
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    print(summary)

    return df

if __name__ == "__main__":
    df = main()
