# PDCA图表生成模板

PDCA项目常用图表的Python代码。

## 基础设置

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 图表通用设置
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.size': 10,
})

# 配色方案
COLORS = {
    'before': '#ff7f0e',      # 橙色-改进前
    'after': '#1f77b4',       # 蓝色-改进后
    'target': '#d62728',      # 红色-目标线
    'baseline': '#7f7f7f',    # 灰色-基线
    'success': '#2ca02c',     # 绿色-达成
}
```

## 改进前后对比柱状图

```python
def create_before_after_bar(before_data, after_data, labels, 
                            target, title, ylabel, output_path):
    """
    创建改进前后对比柱状图
    
    参数:
        before_data: 改进前各周期数据列表
        after_data: 改进后各周期数据列表
        labels: x轴标签（周次）
        target: 目标值
        title: 图表标题
        ylabel: y轴标签
        output_path: 输出路径
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    n_before = len(before_data)
    n_after = len(after_data)
    x = np.arange(n_before + n_after)
    
    # 合并数据
    all_data = list(before_data) + list(after_data)
    colors = [COLORS['before']] * n_before + [COLORS['after']] * n_after
    
    # 绑制柱状图
    bars = ax.bar(x, all_data, color=colors, edgecolor='black', linewidth=0.5)
    
    # 改进前后分隔线
    ax.axvline(x=n_before - 0.5, color='gray', linestyle=':', linewidth=2)
    
    # 均值线
    before_mean = np.mean(before_data)
    after_mean = np.mean(after_data)
    ax.hlines(before_mean, -0.5, n_before - 0.5, colors=COLORS['before'], 
              linestyles='--', linewidth=2, label=f'改进前均值: {before_mean:.1f}')
    ax.hlines(after_mean, n_before - 0.5, n_before + n_after - 0.5, 
              colors=COLORS['after'], linestyles='--', linewidth=2, 
              label=f'改进后均值: {after_mean:.1f}')
    
    # 目标线
    ax.axhline(y=target, color=COLORS['target'], linestyle='-', 
               linewidth=2, label=f'目标值: {target}')
    
    # 标签
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='upper right')
    
    # 添加阶段标注
    ax.text(n_before/2 - 0.5, ax.get_ylim()[1] * 0.95, '改进前', 
            ha='center', fontsize=12, fontweight='bold', color=COLORS['before'])
    ax.text(n_before + n_after/2 - 0.5, ax.get_ylim()[1] * 0.95, '改进后', 
            ha='center', fontsize=12, fontweight='bold', color=COLORS['after'])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    return before_mean, after_mean
```

## 趋势折线图

```python
def create_trend_line(data, labels, target, baseline, 
                      title, ylabel, output_path, 
                      implementation_start=None):
    """
    创建趋势折线图
    
    参数:
        data: 所有时间点的数据
        labels: 时间标签
        target: 目标值
        baseline: 基线值（改进前均值）
        title: 图表标题
        ylabel: y轴标签
        output_path: 输出路径
        implementation_start: 开始实施的时间点索引
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(data))
    
    # 折线图
    ax.plot(x, data, 'bo-', linewidth=2, markersize=8, label='实际值')
    
    # 填充改进前后区域
    if implementation_start:
        ax.axvspan(-0.5, implementation_start - 0.5, alpha=0.1, 
                   color=COLORS['before'], label='改进前')
        ax.axvspan(implementation_start - 0.5, len(data) - 0.5, alpha=0.1, 
                   color=COLORS['after'], label='改进后')
        ax.axvline(x=implementation_start - 0.5, color='gray', 
                   linestyle=':', linewidth=2)
    
    # 目标线和基线
    ax.axhline(y=target, color=COLORS['target'], linestyle='-', 
               linewidth=2, label=f'目标值: {target}')
    ax.axhline(y=baseline, color=COLORS['baseline'], linestyle='--', 
               linewidth=1.5, label=f'基线: {baseline}')
    
    # 标注数值
    for i, (xi, yi) in enumerate(zip(x, data)):
        offset = 5 if i % 2 == 0 else -15
        ax.annotate(f'{yi:.1f}', (xi, yi), textcoords="offset points",
                   xytext=(0, offset), ha='center', fontsize=8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

## 目标达成仪表盘

```python
def create_gauge_chart(achievement_rate, title, output_path):
    """
    创建目标达成率仪表盘
    
    参数:
        achievement_rate: 达成率（0-150之间的百分比数值）
        title: 图表标题
        output_path: 输出路径
    """
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
    
    # 仪表盘范围 0-150%
    max_val = 150
    
    # 背景弧（分区）
    theta_bg = np.linspace(0, np.pi, 100)
    
    # 分区颜色：红-黄-绿
    ax.fill_between(np.linspace(0, np.pi*0.4, 50), 0.6, 1, 
                    color='#ffcccc', alpha=0.5)  # <60% 红
    ax.fill_between(np.linspace(np.pi*0.4, np.pi*0.67, 50), 0.6, 1, 
                    color='#ffffcc', alpha=0.5)  # 60-100% 黄
    ax.fill_between(np.linspace(np.pi*0.67, np.pi, 50), 0.6, 1, 
                    color='#ccffcc', alpha=0.5)  # >100% 绿
    
    # 指针
    achievement_rate = min(achievement_rate, max_val)  # 限制最大值
    pointer_angle = np.pi * (1 - achievement_rate / max_val)
    ax.annotate('', xy=(pointer_angle, 0.9), xytext=(pointer_angle, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=3))
    
    # 中心显示数值
    ax.text(np.pi/2, 0.3, f'{achievement_rate:.1f}%', 
            ha='center', va='center', fontsize=24, fontweight='bold')
    ax.text(np.pi/2, 0.1, '目标达成率', 
            ha='center', va='center', fontsize=12)
    
    # 刻度标签
    for pct, angle in [(0, np.pi), (50, np.pi*0.67), (100, np.pi*0.33), (150, 0)]:
        ax.text(angle, 1.15, f'{pct}%', ha='center', va='center', fontsize=10)
    
    ax.set_ylim(0, 1.2)
    ax.set_theta_zero_location('W')
    ax.set_theta_direction(-1)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    ax.axis('off')
    ax.set_title(title, y=1.1, fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

## PDCA甘特图

```python
def create_pdca_gantt(tasks, title, output_path):
    """
    创建PDCA项目甘特图
    
    参数:
        tasks: 任务列表，每个任务是字典 {
            'phase': 'P/D/C/A',
            'task': '任务名称',
            'start': 开始周,
            'duration': 持续周数,
            'owner': '负责人'
        }
        title: 图表标题
        output_path: 输出路径
    """
    fig, ax = plt.subplots(figsize=(14, len(tasks) * 0.5 + 2))
    
    # 阶段颜色
    phase_colors = {
        'P': '#3498db',  # 蓝色
        'D': '#2ecc71',  # 绿色
        'C': '#f39c12',  # 橙色
        'A': '#9b59b6',  # 紫色
    }
    
    for i, task in enumerate(tasks):
        color = phase_colors.get(task['phase'], '#95a5a6')
        ax.barh(i, task['duration'], left=task['start'] - 1, 
               height=0.6, color=color, edgecolor='black', alpha=0.8)
        
        # 任务名称在条形内
        mid = task['start'] - 1 + task['duration'] / 2
        ax.text(mid, i, f"{task['task']}", ha='center', va='center', 
               fontsize=9, color='white', fontweight='bold')
        
        # 负责人在右侧
        ax.text(task['start'] + task['duration'] + 0.2, i, 
               task['owner'], va='center', fontsize=9)
    
    # Y轴标签（阶段）
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"[{t['phase']}] {t['task']}" for t in tasks])
    
    ax.set_xlabel('周次')
    ax.set_title(title)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    # 图例
    legend_elements = [plt.Rectangle((0,0),1,1, color=c, label=f'{p}阶段') 
                      for p, c in phase_colors.items()]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

## 简化鱼骨图（文本版）

```python
def create_fishbone_text(problem, causes_4m):
    """
    生成文本格式的鱼骨图
    
    参数:
        problem: 问题描述
        causes_4m: 字典 {'人':[], '机':[], '料':[], '法':[]}
    
    返回:
        文本格式的鱼骨图
    """
    lines = []
    lines.append("=" * 60)
    lines.append(f"问题：{problem}".center(60))
    lines.append("=" * 60)
    lines.append("")
    
    # 上半部分（人、机）
    for category in ['人 (Man)', '机 (Machine)']:
        key = category[0]
        if key in causes_4m:
            lines.append(f"  【{category}】")
            for cause in causes_4m[key]:
                lines.append(f"    ├─ {cause}")
            lines.append("")
    
    # 中间箭头
    lines.append("─" * 25 + "→ " + problem[:15])
    lines.append("")
    
    # 下半部分（料、法）
    for category in ['料 (Material)', '法 (Method)']:
        key = category[0]
        if key in causes_4m:
            lines.append(f"  【{category}】")
            for cause in causes_4m[key]:
                lines.append(f"    ├─ {cause}")
            lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)
```

## 数据对比表格生成

```python
def create_comparison_table(before_stats, after_stats, 
                           indicator_name, output_path):
    """
    生成改进前后对比表格（Excel）
    
    参数:
        before_stats: 改进前统计 {'mean':, 'std':, 'n':, 'min':, 'max':}
        after_stats: 改进后统计
        indicator_name: 指标名称
        output_path: 输出Excel路径
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    
    wb = Workbook()
    ws = wb.active
    ws.title = "改进前后对比"
    
    # 表头
    headers = ['统计项', '改进前', '改进后', '变化']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
        cell.fill = PatternFill(start_color='DAEEF3', fill_type='solid')
    
    # 数据行
    rows = [
        ('样本量', before_stats['n'], after_stats['n'], '-'),
        ('均值', f"{before_stats['mean']:.2f}", f"{after_stats['mean']:.2f}", 
         f"{((after_stats['mean']-before_stats['mean'])/before_stats['mean']*100):+.1f}%"),
        ('标准差', f"{before_stats['std']:.2f}", f"{after_stats['std']:.2f}", '-'),
        ('最小值', f"{before_stats['min']:.2f}", f"{after_stats['min']:.2f}", '-'),
        ('最大值', f"{before_stats['max']:.2f}", f"{after_stats['max']:.2f}", '-'),
    ]
    
    for row_idx, row_data in enumerate(rows, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = Alignment(horizontal='center')
    
    # 调整列宽
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 12
    
    wb.save(output_path)
```

## 使用示例

```python
# 示例：生成完整的PDCA图表

# 1. 改进前后对比
before = [12.5, 13.2, 11.8, 12.9, 13.5]  # 改进前5周数据
after = [8.2, 7.5, 7.8, 7.2, 7.0]        # 改进后5周数据
labels = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10']

create_before_after_bar(
    before, after, labels,
    target=8.0,
    title='急诊预检分诊时间改进前后对比',
    ylabel='分诊时间（分钟）',
    output_path='comparison.png'
)

# 2. 目标达成率
achievement = 85.5
create_gauge_chart(achievement, '目标达成率', 'gauge.png')

# 3. 甘特图
tasks = [
    {'phase': 'P', 'task': '现状调查', 'start': 1, 'duration': 2, 'owner': '张三'},
    {'phase': 'P', 'task': '原因分析', 'start': 2, 'duration': 1, 'owner': '李四'},
    {'phase': 'P', 'task': '制定计划', 'start': 3, 'duration': 1, 'owner': '张三'},
    {'phase': 'D', 'task': '措施实施', 'start': 4, 'duration': 4, 'owner': '全体'},
    {'phase': 'C', 'task': '效果评价', 'start': 8, 'duration': 2, 'owner': '李四'},
    {'phase': 'A', 'task': '标准化', 'start': 10, 'duration': 2, 'owner': '王五'},
]
create_pdca_gantt(tasks, 'PDCA项目进度', 'gantt.png')
```
