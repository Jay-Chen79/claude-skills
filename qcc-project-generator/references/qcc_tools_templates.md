# QCC工具与图表生成模板

品管圈常用工具的数据结构和图表代码。

## 柏拉图（Pareto Chart）

### 数据结构

```python
# Excel数据格式
columns = ['要因', '次数', '累计次数', '百分比', '累计百分比']

# 示例数据
data = [
    ['如厕时跌倒', 35, 35, 35.0, 35.0],
    ['床边活动跌倒', 28, 63, 28.0, 63.0],
    ['行走时跌倒', 18, 81, 18.0, 81.0],
    ['转移时跌倒', 12, 93, 12.0, 93.0],
    ['其他', 7, 100, 7.0, 100.0],
]
```

### Excel公式模板

```
A列: 要因名称
B列: 次数（手动输入）
C列: 累计次数 =B2（第一行）, =C2+B3（后续行）
D列: 百分比 =B2/$B$总计*100
E列: 累计百分比 =C2/$C$总计*100
```

### 图表生成代码

```python
import matplotlib.pyplot as plt
import numpy as np

def create_pareto_chart(categories, values, title, output_path):
    """生成柏拉图"""
    # 按值排序（降序）
    sorted_indices = np.argsort(values)[::-1]
    categories = [categories[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]
    
    # 计算累计百分比
    total = sum(values)
    cumulative = np.cumsum(values) / total * 100
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # 柱状图
    x = np.arange(len(categories))
    bars = ax1.bar(x, values, color='steelblue', edgecolor='black')
    ax1.set_ylabel('次数', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    
    # 累计百分比折线图
    ax2 = ax1.twinx()
    ax2.plot(x, cumulative, 'ro-', linewidth=2, markersize=8)
    ax2.set_ylabel('累计百分比 (%)', fontsize=12)
    ax2.set_ylim(0, 105)
    
    # 80%参考线
    ax2.axhline(y=80, color='red', linestyle='--', alpha=0.7)
    ax2.text(len(categories)-0.5, 82, '80%', color='red')
    
    # 在柱子上标注数值
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(val), ha='center', va='bottom')
    
    # 在折线上标注累计百分比
    for i, (xi, yi) in enumerate(zip(x, cumulative)):
        ax2.text(xi, yi + 3, f'{yi:.1f}%', ha='center', fontsize=9)
    
    plt.title(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

---

## 鱼骨图（特性要因图）

### 数据结构

```python
fishbone_data = {
    '人 (Man)': {
        '知识不足': ['培训频次低', '内容不系统'],
        '意识薄弱': ['重视程度不够', '存在侥幸心理'],
        '人力不足': ['护患比不达标', '夜班人员少']
    },
    '机 (Machine)': {
        '设备因素': ['床栏松动', '呼叫系统故障'],
        '工具缺乏': ['助行器不足', '轮椅数量少']
    },
    '料 (Material)': {
        '物资问题': ['防滑垫缺失', '标识不清晰'],
        '药物因素': ['镇静药物使用', '降压药影响']
    },
    '法 (Method)': {
        '流程缺陷': ['评估不完善', '交接班遗漏'],
        '制度问题': ['巡视频次不够', '健康宣教不到位']
    },
    '环 (Environment)': {
        '物理环境': ['地面湿滑', '光线不足'],
        '时间因素': ['夜间发生率高', '交接班时段']
    }
}
```

### 文档输出格式

```
特性要因图（鱼骨图）

主题：降低住院患者跌倒发生率

┌─────────────────────────────────────────────────────────┐
│                                                         │
│    人                机                料               │
│    │                │                │               │
│    ├─知识不足        ├─设备因素        ├─物资问题       │
│    │  └培训频次低    │  └床栏松动      │  └防滑垫缺失   │
│    │                │                │               │
│    ├─意识薄弱        ├─工具缺乏        ├─药物因素       │
│    │  └重视不够      │  └助行器不足    │  └镇静药使用   │
│    │                │                │               │
│────┴────────────────┴────────────────┴───────────────→ 跌倒
│    │                │                                  │
│    ├─流程缺陷        ├─物理环境                        │
│    │  └评估不完善    │  └地面湿滑                      │
│    │                │                                │
│    ├─制度问题        ├─时间因素                        │
│    │  └巡视不够      │  └夜间高发                      │
│    │                │                                │
│    法                环                                │
│                                                       │
└─────────────────────────────────────────────────────────┘

★ 圈选真因：
1. 评估不完善 ✓
2. 防滑垫缺失 ✓
3. 健康宣教不到位 ✓
4. 夜间巡视不足 ✓
```

---

## 甘特图（活动计划）

### 数据结构

```python
gantt_data = [
    {'步骤': '主题选定', '负责人': '张三', '开始周': 1, '持续周': 2},
    {'步骤': '计划拟定', '负责人': '李四', '开始周': 3, '持续周': 1},
    {'步骤': '现状把握', '负责人': '王五', '开始周': 4, '持续周': 5},
    {'步骤': '目标设定', '负责人': '张三', '开始周': 9, '持续周': 1},
    {'步骤': '解析', '负责人': '李四', '开始周': 10, '持续周': 4},
    {'步骤': '对策拟定', '负责人': '王五', '开始周': 14, '持续周': 2},
    {'步骤': '对策实施', '负责人': '全体', '开始周': 16, '持续周': 6},
    {'步骤': '效果确认', '负责人': '张三', '开始周': 22, '持续周': 3},
    {'步骤': '标准化', '负责人': '李四', '开始周': 25, '持续周': 2},
    {'步骤': '检讨改进', '负责人': '全体', '开始周': 27, '持续周': 1},
]
```

### 图表生成代码

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_gantt_chart(tasks, title, output_path):
    """生成甘特图"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(tasks)))
    
    for i, task in enumerate(tasks):
        ax.barh(i, task['持续周'], left=task['开始周']-1, 
               height=0.6, color=colors[i], edgecolor='black')
        
        # 标注持续时间
        mid = task['开始周'] - 1 + task['持续周'] / 2
        ax.text(mid, i, f"{task['持续周']}周", ha='center', va='center', fontsize=9)
    
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t['步骤'] for t in tasks])
    ax.set_xlabel('周次')
    ax.set_title(title)
    ax.set_xlim(0, max(t['开始周'] + t['持续周'] for t in tasks) + 1)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

---

## 雷达图（无形成果）

### 数据结构

```python
radar_data = {
    '维度': ['QCC手法', '团队凝聚力', '沟通协调', '责任感', 
            '解决问题能力', '工作积极性', '专业知识', '品质意识'],
    '改善前': [2.5, 2.8, 3.0, 3.2, 2.7, 3.0, 3.5, 2.8],
    '改善后': [4.2, 4.5, 4.3, 4.6, 4.4, 4.5, 4.2, 4.7]
}
```

### 图表生成代码

```python
import numpy as np
import matplotlib.pyplot as plt

def create_radar_chart(categories, before, after, title, output_path):
    """生成雷达图"""
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    
    # 闭合图形
    before = before + [before[0]]
    after = after + [after[0]]
    angles = angles + [angles[0]]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    ax.plot(angles, before, 'o-', linewidth=2, label='改善前', color='#ff7f0e')
    ax.fill(angles, before, alpha=0.25, color='#ff7f0e')
    
    ax.plot(angles, after, 'o-', linewidth=2, label='改善后', color='#1f77b4')
    ax.fill(angles, after, alpha=0.25, color='#1f77b4')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'])
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.set_title(title, fontsize=14, y=1.08)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

---

## 改善前后对比折线图

### 数据结构

```python
trend_data = {
    '时间点': ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月'],
    '阶段': ['改善前', '改善前', '改善前', '实施中', '实施中', '改善后', '改善后', '改善后'],
    '指标值': [0.65, 0.58, 0.62, 0.45, 0.38, 0.28, 0.25, 0.22]
}
```

### 图表生成代码

```python
def create_trend_chart(time_points, values, phases, target, title, ylabel, output_path):
    """生成改善趋势图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 背景分区
    phase_colors = {'改善前': '#ffcccc', '实施中': '#ffffcc', '改善后': '#ccffcc'}
    
    # 绘制折线
    ax.plot(time_points, values, 'bo-', linewidth=2, markersize=8, label='实际值')
    
    # 目标线
    ax.axhline(y=target, color='red', linestyle='--', linewidth=2, label=f'目标值: {target}')
    
    # 标注数值
    for i, (x, y) in enumerate(zip(time_points, values)):
        ax.annotate(f'{y:.2f}', (x, y), textcoords="offset points", 
                   xytext=(0, 10), ha='center')
    
    ax.set_xlabel('时间')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
```

---

## 对策效果确认表

### Excel模板结构

```
| 真因 | 对策 | 负责人 | 完成时间 | 效果确认 | 结果 |
|------|------|--------|----------|----------|------|
| 评估不完善 | 修订评估量表 | 张三 | 第5周 | 评估准确率提高至95% | ✓有效 |
| 防滑垫缺失 | 采购并铺设防滑垫 | 李四 | 第6周 | 100%病房已铺设 | ✓有效 |
| 宣教不到位 | 制作宣教视频+手册 | 王五 | 第7周 | 知晓率从60%→92% | ✓有效 |
```

---

## 统计检验模板

### 卡方检验（计数资料）

```python
from scipy import stats

def chi_square_test(before_events, before_total, after_events, after_total):
    """改善前后率的比较（卡方检验）"""
    # 构建四格表
    table = [
        [before_events, before_total - before_events],
        [after_events, after_total - after_events]
    ]
    
    chi2, p_value, dof, expected = stats.chi2_contingency(table)
    
    return {
        'chi2': chi2,
        'p_value': p_value,
        'before_rate': before_events / before_total,
        'after_rate': after_events / after_total,
        'conclusion': '差异有统计学意义' if p_value < 0.05 else '差异无统计学意义'
    }
```

### t检验（计量资料）

```python
def t_test_comparison(before_data, after_data):
    """改善前后均值比较（独立样本t检验）"""
    t_stat, p_value = stats.ttest_ind(before_data, after_data)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'before_mean': np.mean(before_data),
        'after_mean': np.mean(after_data),
        'before_std': np.std(before_data),
        'after_std': np.std(after_data),
        'conclusion': '差异有统计学意义' if p_value < 0.05 else '差异无统计学意义'
    }
```
