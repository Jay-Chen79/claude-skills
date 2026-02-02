# Figure Generation Templates

Publication-quality figure templates using matplotlib and seaborn.

## Setup

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Publication-quality settings
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# Consistent color palette
COLORS = {
    'treatment': '#1f77b4',  # Blue
    'control': '#ff7f0e',    # Orange
    'male': '#2ca02c',       # Green
    'female': '#d62728',     # Red
    'highlight': '#9467bd',  # Purple
}
```

## Box Plot (Group Comparison)

```python
def create_boxplot(data, x_col, y_col, title, ylabel, output_path):
    """Create publication-quality box plot."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Box plot with individual points
    sns.boxplot(data=data, x=x_col, y=y_col, ax=ax,
                palette=[COLORS['treatment'], COLORS['control']],
                width=0.5)
    
    # Add individual data points
    sns.stripplot(data=data, x=x_col, y=y_col, ax=ax,
                  color='black', alpha=0.4, size=4, jitter=0.1)
    
    ax.set_xlabel('')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Add statistical annotation
    # (Calculate p-value separately and add)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Bar Plot with Error Bars

```python
def create_barplot(means, sems, labels, ylabel, title, output_path):
    """Create bar plot with error bars (SEM or 95% CI)."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    x = np.arange(len(labels))
    colors = [COLORS['treatment'], COLORS['control']]
    
    bars = ax.bar(x, means, yerr=sems, capsize=5, 
                  color=colors[:len(labels)], 
                  edgecolor='black', linewidth=1)
    
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    
    # Add value labels on bars
    for bar, mean, sem in zip(bars, means, sems):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + sem + 0.5,
                f'{mean:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Line Plot (Longitudinal Data)

```python
def create_lineplot(data, time_col, value_col, group_col, 
                    xlabel, ylabel, title, output_path):
    """Create line plot for longitudinal data."""
    fig, ax = plt.subplots(figsize=(7, 5))
    
    for i, (group, group_data) in enumerate(data.groupby(group_col)):
        color = list(COLORS.values())[i]
        
        # Calculate mean and SEM at each time point
        summary = group_data.groupby(time_col)[value_col].agg(['mean', 'sem'])
        
        ax.errorbar(summary.index, summary['mean'], yerr=summary['sem'],
                   label=group, color=color, marker='o', 
                   capsize=3, linewidth=2, markersize=6)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='best', frameon=True)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Kaplan-Meier Survival Curve

```python
def create_km_plot(time, event, group, group_names, 
                   xlabel, title, output_path):
    """Create Kaplan-Meier survival plot."""
    from lifelines import KaplanMeierFitter
    
    fig, ax = plt.subplots(figsize=(7, 5))
    
    kmf = KaplanMeierFitter()
    
    for i, (g, name) in enumerate(zip(np.unique(group), group_names)):
        mask = group == g
        color = list(COLORS.values())[i]
        
        kmf.fit(time[mask], event[mask], label=name)
        kmf.plot_survival_function(ax=ax, color=color, linewidth=2)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Survival Probability')
    ax.set_title(title)
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower left', frameon=True)
    
    # Add number at risk table (optional)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Scatter Plot with Correlation

```python
def create_scatter(data, x_col, y_col, xlabel, ylabel, title, output_path):
    """Create scatter plot with regression line and correlation."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Scatter points
    ax.scatter(data[x_col], data[y_col], alpha=0.6, 
               color=COLORS['treatment'], edgecolor='white', s=50)
    
    # Regression line
    z = np.polyfit(data[x_col].dropna(), data[y_col].dropna(), 1)
    p = np.poly1d(z)
    x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2, label='Linear fit')
    
    # Calculate correlation
    r, pval = stats.pearsonr(data[x_col].dropna(), data[y_col].dropna())
    
    # Add correlation annotation
    ax.text(0.05, 0.95, f'r = {r:.3f}\np = {pval:.3f}',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Forest Plot

```python
def create_forest_plot(labels, effects, lower_ci, upper_ci, 
                       xlabel, title, output_path):
    """Create forest plot for meta-analysis or subgroup analysis."""
    fig, ax = plt.subplots(figsize=(8, len(labels)*0.5 + 2))
    
    y_pos = np.arange(len(labels))
    
    # Plot effect sizes with CIs
    ax.errorbar(effects, y_pos, xerr=[effects-lower_ci, upper_ci-effects],
                fmt='s', color=COLORS['treatment'], 
                markersize=8, capsize=3, linewidth=2)
    
    # Reference line at 0 (or 1 for OR/RR)
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.invert_yaxis()  # Top to bottom
    
    # Add effect values on right
    for i, (eff, lo, hi) in enumerate(zip(effects, lower_ci, upper_ci)):
        ax.text(ax.get_xlim()[1] + 0.1, i, 
                f'{eff:.2f} [{lo:.2f}, {hi:.2f}]',
                va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## CONSORT Flow Diagram

```python
def create_consort_flowchart(numbers, output_path):
    """Create CONSORT flow diagram.
    
    numbers dict should contain:
    - assessed, excluded, not_meeting, declined, other
    - randomized
    - alloc_intervention, received_intervention, not_received_intervention
    - alloc_control, received_control, not_received_control
    - lost_intervention, lost_control
    - analyzed_intervention, analyzed_control
    """
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Box style
    box_props = dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='black', linewidth=1.5)
    
    # Enrollment
    ax.text(5, 11, f"Assessed for eligibility\n(n={numbers['assessed']})",
            ha='center', va='center', fontsize=10, bbox=box_props)
    
    ax.text(7.5, 10, f"Excluded (n={numbers['excluded']})\n"
                     f"• Not meeting criteria (n={numbers['not_meeting']})\n"
                     f"• Declined (n={numbers['declined']})\n"
                     f"• Other (n={numbers['other']})",
            ha='left', va='center', fontsize=9, bbox=box_props)
    
    # Randomized
    ax.text(5, 9, f"Randomized\n(n={numbers['randomized']})",
            ha='center', va='center', fontsize=10, bbox=box_props)
    
    # Allocation
    ax.text(2.5, 7, f"Allocated to intervention\n(n={numbers['alloc_intervention']})\n"
                    f"• Received intervention (n={numbers['received_intervention']})\n"
                    f"• Did not receive (n={numbers['not_received_intervention']})",
            ha='center', va='center', fontsize=9, bbox=box_props)
    
    ax.text(7.5, 7, f"Allocated to control\n(n={numbers['alloc_control']})\n"
                    f"• Received control (n={numbers['received_control']})\n"
                    f"• Did not receive (n={numbers['not_received_control']})",
            ha='center', va='center', fontsize=9, bbox=box_props)
    
    # Follow-up
    ax.text(2.5, 4.5, f"Lost to follow-up\n(n={numbers['lost_intervention']})",
            ha='center', va='center', fontsize=9, bbox=box_props)
    
    ax.text(7.5, 4.5, f"Lost to follow-up\n(n={numbers['lost_control']})",
            ha='center', va='center', fontsize=9, bbox=box_props)
    
    # Analysis
    ax.text(2.5, 2, f"Analyzed\n(n={numbers['analyzed_intervention']})",
            ha='center', va='center', fontsize=10, bbox=box_props)
    
    ax.text(7.5, 2, f"Analyzed\n(n={numbers['analyzed_control']})",
            ha='center', va='center', fontsize=10, bbox=box_props)
    
    # Arrows
    arrow_props = dict(arrowstyle='->', color='black', linewidth=1.5)
    
    # Vertical arrows
    ax.annotate('', xy=(5, 10.2), xytext=(5, 9.6), arrowprops=arrow_props)
    ax.annotate('', xy=(5, 8.3), xytext=(5, 7.8), arrowprops=arrow_props)
    
    # Branch arrows
    ax.annotate('', xy=(2.5, 7.8), xytext=(5, 8.3), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 7.8), xytext=(5, 8.3), arrowprops=arrow_props)
    
    # Continue down
    ax.annotate('', xy=(2.5, 6), xytext=(2.5, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 6), xytext=(7.5, 5.2), arrowprops=arrow_props)
    ax.annotate('', xy=(2.5, 3.8), xytext=(2.5, 2.8), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 3.8), xytext=(7.5, 2.8), arrowprops=arrow_props)
    
    # Exclusion arrow
    ax.annotate('', xy=(6, 10), xytext=(5.5, 10.5), arrowprops=arrow_props)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Violin Plot

```python
def create_violin(data, x_col, y_col, title, ylabel, output_path):
    """Create violin plot showing distribution."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    sns.violinplot(data=data, x=x_col, y=y_col, ax=ax,
                   palette=[COLORS['treatment'], COLORS['control']],
                   inner='box')
    
    ax.set_xlabel('')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Heatmap (Correlation Matrix)

```python
def create_correlation_heatmap(data, columns, title, output_path):
    """Create correlation heatmap."""
    fig, ax = plt.subplots(figsize=(8, 7))
    
    corr_matrix = data[columns].corr()
    
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', 
                center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5, ax=ax,
                fmt='.2f', annot_kws={'size': 9})
    
    ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)
    plt.close()
```

## Figure Sizing Guide

| Figure Type | Single Column | Full Width |
|-------------|---------------|------------|
| Simple plot | 3.5 × 3 in | 7 × 5 in |
| Flow diagram | N/A | 7 × 9 in |
| Multi-panel | 3.5 × 6 in | 7 × 8 in |
| Correlation | 4 × 4 in | 7 × 7 in |

## Color-Blind Friendly Palette

```python
CB_PALETTE = {
    'blue': '#0072B2',
    'orange': '#E69F00',
    'green': '#009E73',
    'pink': '#CC79A7',
    'light_blue': '#56B4E9',
    'red': '#D55E00',
    'yellow': '#F0E442',
}
```
