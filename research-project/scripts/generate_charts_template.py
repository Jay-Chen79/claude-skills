"""
Research Project Chart Generator - Template
This is a template for generating publication-quality charts for research papers.
Uses colorblind-friendly palettes and APA-style formatting.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ============================================
# CONFIGURATION
# ============================================

# Set publication-quality settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13

# Colorblind-friendly palette (Wong 2011)
COLORBLIND_PALETTE = [
    '#0072B2',  # Blue
    '#D55E00',  # Orange
    '#009E73',  # Green
    '#CC79A7',  # Red/Pink
    '#F0E442',  # Yellow
    '#56B4E9',  # Light Blue
    '#999999',  # Grey
]

# Set style
sns.set_style("whitegrid")
sns.set_palette(COLORBLIND_PALETTE)

# ============================================
# CHART TYPES
# ============================================

def bar_chart_with_error_bars(df, group_col, value_col, title, ylabel,
                               xlabel='Group', filename='bar_chart.png'):
    """
    Create a bar chart with error bars (standard error).

    Use for: Comparing means across 2+ groups
    """
    # Calculate means and standard errors
    summary = df.groupby(group_col)[value_col].agg(['mean', 'sem']).reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))

    bars = ax.bar(summary[group_col], summary['mean'],
                  yerr=summary['sem'],
                  capsize=5,
                  alpha=0.8,
                  color=COLORBLIND_PALETTE[:len(summary)])

    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)

    # Add value labels on bars
    for bar, mean in zip(bars, summary['mean']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{mean:.2f}',
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ Bar chart saved: {filename}")
    return fig

def box_plot(df, group_col, value_col, title, ylabel,
             xlabel='Group', filename='box_plot.png'):
    """
    Create a box plot showing distributions.

    Use for: Showing distribution, outliers, quartiles
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    sns.boxplot(data=df, x=group_col, y=value_col, ax=ax,
                palette=COLORBLIND_PALETTE[:df[group_col].nunique()])

    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ Box plot saved: {filename}")
    return fig

def scatter_with_regression(df, x_col, y_col, title,
                            xlabel=None, ylabel=None,
                            filename='scatter_plot.png'):
    """
    Create a scatter plot with regression line.

    Use for: Showing correlation between two continuous variables
    """
    if xlabel is None:
        xlabel = x_col.replace('_', ' ').title()
    if ylabel is None:
        ylabel = y_col.replace('_', ' ').title()

    fig, ax = plt.subplots(figsize=(6, 5))

    # Calculate correlation
    corr = df[[x_col, y_col]].corr().iloc[0, 1]

    # Create scatter and regression line
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax,
                scatter_kws={'alpha': 0.6, 's': 30},
                line_kws={'color': COLORBLIND_PALETTE[0]})

    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)

    # Add correlation text
    ax.text(0.05, 0.95, f'r = {corr:.3f}',
            transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
            fontsize=10, verticalalignment='top')

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ Scatter plot saved: {filename}")
    return fig

def histogram_by_group(df, value_col, group_col, title, xlabel,
                       filename='histogram.png'):
    """
    Create overlapping histograms by group.

    Use for: Showing distribution comparison between groups
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    groups = df[group_col].unique()

    for i, group in enumerate(sorted(groups)):
        data = df[df[group_col] == group][value_col].dropna()
        ax.hist(data, alpha=0.5, label=group,
                color=COLORBLIND_PALETTE[i], bins=20, edgecolor='white')

    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ Histogram saved: {filename}")
    return fig

def interaction_plot(df, iv1_col, iv2_col, dv_col, title,
                     xlabel=None, ylabel=None,
                     filename='interaction_plot.png'):
    """
    Create an interaction plot (2-way ANOVA visualization).

    Use for: Showing interaction between two categorical variables
    """
    if xlabel is None:
        xlabel = iv1_col.replace('_', ' ').title()
    if ylabel is None:
        ylabel = dv_col.replace('_', ' ').title()

    fig, ax = plt.subplots(figsize=(6, 4))

    # Calculate means for each combination
    means = df.groupby([iv1_col, iv2_col])[dv_col].mean().reset_index()

    iv2_levels = sorted(df[iv2_col].unique())
    iv1_levels = sorted(df[iv1_col].unique())

    x_pos = np.arange(len(iv1_levels))

    for i, level in enumerate(iv2_levels):
        data = means[means[iv2_col] == level]
        y_vals = [data[data[iv1_col] == lvl][dv_col].values[0] if lvl in data[iv1_col].values else np.nan
                  for lvl in iv1_levels]
        ax.plot(x_pos, y_vals, marker='o', label=level,
                color=COLORBLIND_PALETTE[i], linewidth=2, markersize=8)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(iv1_levels)
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend(title=iv2_col.replace('_', ' ').title())

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ Interaction plot saved: {filename}")
    return fig

def conceptual_flow_diagram(groups, procedures, outcome, filename='conceptual_diagram.png'):
    """
    Create a simple conceptual flow diagram for study design.

    Use for: Illustrating research design in paper
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')

    # Define positions
    positions = [(1, 1.5), (4, 1.5), (7, 1.5)]
    labels = [groups, procedures, outcome]

    # Draw boxes and arrows
    for i, (x, y) in enumerate(positions):
        # Box
        rect = plt.Rectangle((x-0.8, y-0.4), 1.6, 0.8,
                            facecolor=COLORBLIND_PALETTE[i],
                            edgecolor='black', linewidth=2, alpha=0.7)
        ax.add_patch(rect)

        # Label
        ax.text(x, y, labels[i], ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Arrow (except last)
        if i < len(positions) - 1:
            ax.annotate('', xy=(x+1, y), xytext=(x+1.2, y),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))

    ax.set_title('Study Design Flowchart', fontweight='bold', fontsize=13, pad=20)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white', dpi=300)
    plt.close()

    print(f"✅ Conceptual diagram saved: {filename}")
    return fig

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """Generate example charts"""

    # Create example data
    np.random.seed(42)
    n = 100

    example_df = pd.DataFrame({
        'group': np.random.choice(['Control', 'Treatment'], n),
        'age': np.random.normal(35, 12, n),
        'score': np.concatenate([
            np.random.normal(100, 15, 50),
            np.random.normal(108, 15, 50)
        ])
    })
    example_df['score'][:50] = np.where(np.random.random(50) < 0.05, np.nan, example_df['score'][:50])

    # Generate example charts
    print("Generating example charts...\n")

    bar_chart_with_error_bars(
        example_df, 'group', 'score',
        title='Mean Scores by Group',
        ylabel='Test Score',
        filename='example_bar_chart.png'
    )

    box_plot(
        example_df, 'group', 'score',
        title='Score Distribution by Group',
        ylabel='Test Score',
        filename='example_box_plot.png'
    )

    scatter_with_regression(
        example_df, 'age', 'score',
        title='Relationship Between Age and Test Score',
        xlabel='Age (years)',
        ylabel='Test Score',
        filename='example_scatter.png'
    )

    conceptual_flow_diagram(
        'N=100\nRandomized',
        'Intervention\n(4 weeks)',
        'Post-test\nScores',
        filename='example_conceptual.png'
    )

    print("\n✅ All example charts generated successfully!")

if __name__ == "__main__":
    main()
