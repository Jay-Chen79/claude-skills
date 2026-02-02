# 统计方法参考

本文档提供验证生成数据时使用的统计方法参考。

---

## 两组比较

### 连续变量

#### 独立样本t检验
- **假设**：正态分布，方差齐性
- **统计量**：t = (x̄1 - x̄2) / SE
- **效应量**：Cohen's d = (x̄1 - x̄2) / Sp

```python
from scipy import stats
t_stat, p_value = stats.ttest_ind(group1, group2)
```

#### Mann-Whitney U检验
- **假设**：独立性
- **适用**：非正态分布或有序变量
- **统计量**：U统计量

```python
from scipy import stats
u_stat, p_value = stats.mannwhitneyu(group1, group2)
```

### 分类变量

#### 卡方检验
- **假设**：期望频数 ≥ 5
- **统计量**：χ² = Σ(O-E)²/E

```python
from scipy import stats
chi2, p_value, dof, expected = stats.chi2_contingency(table)
```

#### Fisher精确检验
- **适用**：小样本或期望频数 < 5
- **精确计算**：基于超几何分布

```python
from scipy import stats
odds_ratio, p_value = stats.fisher_exact(table)
```

---

## 相关分析

### Pearson相关
- **假设**：线性关系，双正态分布
- **统计量**：r = Σ(x-x̄)(y-ȳ) / √[Σ(x-x̄)²Σ(y-ȳ)²]

```python
from scipy import stats
r, p_value = stats.pearsonr(x, y)
```

### Spearman相关
- **假设**：单调关系
- **统计量**：基于秩次的Pearson相关

```python
from scipy import stats
rho, p_value = stats.spearmanr(x, y)
```

### 置信区间（Fisher变换）
```python
import numpy as np
z = np.arctanh(r)
se = 1 / np.sqrt(n - 3)
ci = np.tanh([z - 1.96*se, z + 1.96*se])
```

---

## 回归分析

### 线性回归
- **模型**：Y = β0 + β1X1 + ... + ε
- **假设**：线性、独立、正态、同方差

```python
import statsmodels.api as sm
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())
```

### Logistic回归
- **模型**：logit(p) = β0 + β1X1 + ...
- **效应量**：OR = exp(β)

```python
import statsmodels.api as sm
X = sm.add_constant(X)
model = sm.Logit(y, X).fit()
print(model.summary())
```

### 模型诊断

| 指标 | 含义 | 阈值 |
|-----|-----|-----|
| R² | 解释变异比例 | 视领域而定 |
| VIF | 多重共线性 | < 10 |
| AIC/BIC | 模型比较 | 越小越好 |

---

## 生存分析

### Kaplan-Meier估计
- **用途**：估计生存函数
- **公式**：S(t) = Π[1 - d(ti)/n(ti)]

```python
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()
kmf.fit(time, event)
kmf.plot_survival_function()
```

### Log-rank检验
- **用途**：比较两组生存曲线
- **假设**：比例风险

```python
from lifelines.statistics import logrank_test
result = logrank_test(T1, T2, E1, E2)
print(result.p_value)
```

### Cox比例风险模型
- **模型**：h(t) = h0(t) × exp(β'X)
- **效应量**：HR = exp(β)

```python
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cph.fit(df, duration_col='time', event_col='event')
cph.print_summary()
```

---

## 诊断准确性

### 敏感度和特异度
```
敏感度 = TP / (TP + FN)
特异度 = TN / (TN + FP)
```

### ROC曲线和AUC
```python
from sklearn.metrics import roc_curve, roc_auc_score

fpr, tpr, thresholds = roc_curve(y_true, y_score)
auc = roc_auc_score(y_true, y_score)
```

### 最佳阈值

| 方法 | 计算 |
|-----|------|
| Youden指数 | max(Se + Sp - 1) |
| 距离法 | min(√[(1-Se)² + (1-Sp)²]) |
| 成本最小化 | 考虑FP和FN的相对成本 |

---

## 样本量计算

### 两组均值比较
```
n = 2 × [(Zα + Zβ) × σ / δ]²
```

其中：
- Zα：第一类错误对应的Z值
- Zβ：第二类错误对应的Z值
- σ：标准差
- δ：组间差异

### 两组比例比较
```
n = [Zα√(2p̄q̄) + Zβ√(p1q1 + p2q2)]² / (p1 - p2)²
```

### 相关系数
```
n = [(Zα + Zβ) / (0.5 × ln((1+r)/(1-r)))]² + 3
```

---

## 效应量换算

### Cohen's d 与 r
```
r = d / √(d² + 4)
d = 2r / √(1 - r²)
```

### OR 与 d
```
d = ln(OR) × √3 / π
OR = exp(d × π / √3)
```

### HR 与中位数比
```
HR ≈ median0 / median1  (指数分布)
```

---

## p值校正（多重比较）

| 方法 | 公式 | 特点 |
|-----|------|-----|
| Bonferroni | α' = α/m | 保守 |
| Holm | 逐步调整 | 较Bonferroni有力 |
| FDR (BH) | 控制错误发现率 | 更有力 |

```python
from statsmodels.stats.multitest import multipletests

rejected, p_corrected, _, _ = multipletests(p_values, method='fdr_bh')
```
