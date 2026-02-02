# 统计结果报告规范

各类统计方法的Methods描述和Results报告模板。

## 一、Methods部分统计方法描述

### 描述性统计

```
【英文模板】
Continuous variables were expressed as mean ± standard deviation (SD) for normally distributed data, or median (interquartile range, IQR) for skewed data. Categorical variables were presented as frequencies (percentages).

【中文模板】
正态分布的连续变量以均数±标准差（mean±SD）表示，偏态分布的连续变量以中位数（四分位距）[M(IQR)]表示。分类变量以频数（百分比）表示。
```

### 正态性检验

```
Normality of continuous variables was assessed using the Shapiro-Wilk test [or Kolmogorov-Smirnov test for n>50].
```

### 两组比较

```
【连续变量】
Comparisons between two groups were performed using independent samples t-test for normally distributed data, or Mann-Whitney U test for non-normally distributed data.

【分类变量】
Categorical variables were compared using chi-square test or Fisher's exact test (when expected frequencies were <5).
```

### 多组比较

```
Comparisons among multiple groups were performed using one-way analysis of variance (ANOVA) with post-hoc Bonferroni correction [or Tukey's test] for normally distributed data, or Kruskal-Wallis H test with post-hoc Dunn's test for non-normally distributed data.
```

### 配对数据

```
Paired comparisons were performed using paired t-test for normally distributed data, or Wilcoxon signed-rank test for non-normally distributed data. McNemar's test was used for paired categorical data.
```

### 相关分析

```
Correlations between continuous variables were evaluated using Pearson correlation coefficient for normally distributed data, or Spearman rank correlation coefficient for non-normally distributed data or ordinal variables.
```

### 回归分析

```
【线性回归】
Multiple linear regression analysis was performed to identify factors associated with [结局变量]. Variables with P < 0.1 in univariate analysis [or clinically relevant variables] were included in the multivariate model.

【Logistic回归】
Binary logistic regression was used to evaluate the association between [暴露] and [结局]. Odds ratios (ORs) and 95% confidence intervals (CIs) were calculated. Multivariate analysis was adjusted for [调整的变量].

【Cox回归】
Cox proportional hazards regression was used to estimate hazard ratios (HRs) and 95% CIs for [结局]. The proportional hazards assumption was tested using Schoenfeld residuals.
```

### 生存分析

```
Survival curves were estimated using the Kaplan-Meier method and compared using the log-rank test. Median survival time with 95% CI was reported.
```

### 诊断试验

```
Sensitivity, specificity, positive predictive value (PPV), negative predictive value (NPV), and area under the receiver operating characteristic curve (AUC) were calculated. The optimal cutoff value was determined using the Youden index [or maximum sensitivity + specificity].
```

### 样本量计算

```
【两组均数比较】
Sample size was calculated based on a two-sided α of 0.05 and a power of 80% [or 90%]. Assuming a mean difference of [X] with a standard deviation of [Y], a minimum of [N] subjects per group was required.

【两组率比较】
Based on previous studies, we assumed a [结局] rate of [X]% in the control group and [Y]% in the intervention group. With α = 0.05 and power = 80%, [N] subjects per group were needed.

【相关性】
To detect a correlation coefficient of [r] with α = 0.05 and power = 80%, a minimum sample size of [N] was required.
```

### 缺失数据处理

```
【完全病例分析】
Analyses were performed on complete cases only.

【多重插补】
Missing data were handled using multiple imputation by chained equations (MICE), generating [5-10] imputed datasets.

【敏感性分析】
Sensitivity analyses were performed to assess the impact of missing data.
```

### 软件声明

```
All statistical analyses were performed using [软件名称] (version [版本号], [公司/组织], [地点]). A two-tailed P value < 0.05 was considered statistically significant.

常用软件：
- SPSS (version 26.0, IBM Corp., Armonk, NY, USA)
- R (version 4.2.0, R Foundation for Statistical Computing, Vienna, Austria)
- Stata (version 17.0, StataCorp LLC, College Station, TX, USA)
- SAS (version 9.4, SAS Institute Inc., Cary, NC, USA)
- GraphPad Prism (version 9.0, GraphPad Software, San Diego, CA, USA)
```

---

## 二、Results部分统计结果报告

### 基本格式规范

```
【P值报告】
✓ P = 0.042（精确值，三位小数）
✓ P < 0.001（不写P = 0.000）
✗ P < 0.05（避免）
✗ P > 0.05 或 NS（避免）

【置信区间】
✓ 95% CI: 1.23-2.45 或 95% CI: 1.23 to 2.45
✓ (95% CI: 1.23-2.45)

【效应量】
✓ OR = 2.15 (95% CI: 1.32-3.50)
✓ HR = 0.72, 95% CI 0.58-0.89
✓ Mean difference = 5.2 (95% CI: 2.1-8.3)
```

### 两组比较结果

```
【t检验-连续变量】
The mean [指标] was significantly higher in the [组1] group compared with the [组2] group (45.3 ± 12.5 vs. 38.2 ± 10.8, P = 0.003).

【Mann-Whitney U检验】
The median [指标] was significantly higher in the [组1] group than in the [组2] group [24 (18-36) vs. 18 (12-25), P = 0.012].

【卡方检验-分类变量】
The proportion of [指标] was significantly higher in the [组1] group than in the [组2] group (45.2% vs. 28.6%, P = 0.008).

【Fisher精确检验】
There was no significant difference in [指标] between the two groups (12.5% vs. 8.3%, P = 0.523, Fisher's exact test).
```

### 多组比较结果

```
【ANOVA】
There was a significant difference in [指标] among the three groups (F = 8.45, P < 0.001). Post-hoc analysis revealed that [组1] had significantly higher [指标] than [组2] (P = 0.002) and [组3] (P = 0.008).

【Kruskal-Wallis】
A significant difference in [指标] was observed among groups (H = 15.23, P = 0.002). Pairwise comparisons showed that [组1] differed significantly from [组2] (P = 0.003).
```

### 相关分析结果

```
【Pearson相关】
There was a significant positive correlation between [变量1] and [变量2] (r = 0.65, P < 0.001).

A moderate negative correlation was observed between [变量1] and [变量2] (r = -0.45, P = 0.008).

【Spearman相关】
[变量1] was significantly correlated with [变量2] (ρ = 0.58, P < 0.001).

相关强度参考：
|r| < 0.3: weak
0.3 ≤ |r| < 0.5: moderate
0.5 ≤ |r| < 0.7: moderately strong
|r| ≥ 0.7: strong
```

### 回归分析结果

```
【线性回归】
In multivariate linear regression, [变量] was independently associated with [结局] (β = 0.35, 95% CI: 0.12-0.58, P = 0.003), after adjusting for age, sex, and BMI.

【Logistic回归】
Multivariate logistic regression showed that [变量] was independently associated with increased odds of [结局] (OR = 2.15, 95% CI: 1.32-3.50, P = 0.002).

After adjustment for potential confounders, [变量] remained significantly associated with [结局] (adjusted OR = 1.85, 95% CI: 1.08-3.16, P = 0.025).

【Cox回归】
In the multivariate Cox model, [变量] was associated with a [X]% increased risk of [结局] (HR = 1.45, 95% CI: 1.12-1.88, P = 0.005).
```

### 生存分析结果

```
【Kaplan-Meier】
The median overall survival was 24 months (95% CI: 18-30) in the [组1] group and 36 months (95% CI: 28-44) in the [组2] group. The difference was statistically significant (log-rank P = 0.008).

The 5-year survival rate was 45.2% (95% CI: 38.5-51.9%) in the [组1] group and 62.3% (95% CI: 55.1-69.5%) in the [组2] group.
```

### 诊断试验结果

```
The [指标] showed good diagnostic performance for [疾病], with an AUC of 0.85 (95% CI: 0.78-0.92). At the optimal cutoff of [X], the sensitivity was 82.5% (95% CI: 75.2-89.8%) and the specificity was 78.3% (95% CI: 70.1-86.5%).

The positive predictive value was 75.6% and the negative predictive value was 84.2%.
```

---

## 三、常见统计错误及纠正

### 错误1：P值报告不当

```
❌ P = 0.000
✓ P < 0.001

❌ P < 0.05 或 P > 0.05
✓ P = 0.042 或 P = 0.156
```

### 错误2：仅报告P值不报告效应量

```
❌ The difference was statistically significant (P = 0.003).
✓ The mean difference was 5.2 (95% CI: 2.1-8.3, P = 0.003).
```

### 错误3：均数±标准差/标准误混淆

```
SD（标准差）：描述数据离散程度，用于描述性统计
SE/SEM（标准误）：描述均数估计精度，用于均数比较

描述样本特征用SD
图中误差棒可用SE或95%CI
```

### 错误4：多重比较未校正

```
❌ 多组比较后直接两两比较未校正
✓ 使用Bonferroni校正或其他事后检验方法
```

### 错误5：相关与因果混淆

```
❌ X causes Y (基于横断面相关分析)
✓ X was associated with Y
✓ X was correlated with Y
```

---

## 四、特殊情况处理

### 小样本

```
当样本量较小时（通常n<30），应使用非参数检验，并在Methods中说明：

Due to the small sample size, non-parametric tests were used for all comparisons.
```

### 多重检验

```
To account for multiple comparisons, the Bonferroni correction was applied, and a P value < [0.05/比较次数] was considered statistically significant.

或使用False Discovery Rate (FDR)校正：
P values were adjusted for multiple comparisons using the Benjamini-Hochberg procedure to control the false discovery rate.
```

### 敏感性分析

```
Sensitivity analyses were performed to test the robustness of our findings:
(1) excluding outliers;
(2) using alternative definitions for [变量];
(3) restricting to [亚组];
(4) using multiple imputation for missing data.

The results remained consistent across all sensitivity analyses.
```
