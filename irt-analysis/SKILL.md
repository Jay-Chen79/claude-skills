---
name: irt-analysis
description: >
  Comprehensive Rasch and IRT analysis workflow using R packages.
  Handles data intake, dimensionality assessment (PCAR, ECV, Omega),
  Rasch analysis with Winsteps-style outputs, multidimensional IRT,
  and DIF analysis. Triggers: psychometric analysis, item response
  theory, scale validation, Rasch model.
---

# Rasch分析技能 (Rasch Analysis Skill)

使用R语言包进行完整的Rasch分析工作流程。

## 工作流程概览

```
1. 数据接收与确认 → 2. 维度检验 → 3. 分析路径决策 → 4. Rasch/MIRT分析 → 5. 输出报告
```

## 第一步：数据接收与需求确认

### 必须确认的信息

收到数据后，**必须**通过问答方式明确以下信息：

#### 基本数据结构
- **条目数量**: 量表/问卷包含多少个条目(items)?
- **受试者数量**: 共有多少名受试者(persons/subjects)?
- **数据格式**: 确认Excel格式，检查数据排列方式（受试者×条目）

#### 一般资料变量
- **人口学变量**: 包含哪些一般资料?（年龄、性别、教育程度、职业等）
- **年龄数据**: 是连续变量还是已分组? 如需DIF分析，如何分组?
- **其他分组变量**: 是否有其他需要进行DIF分析的分组变量?

#### DIF分析需求
**必须询问**: "是否需要进行DIF（差异项目功能）分析？"

如需DIF分析，明确：
- 按哪些变量进行DIF检验?（性别、年龄组、教育程度等）
- 年龄分组方案（如需要）：
  - 中位数分组
  - 按特定年龄界值分组（如≤40 vs >40）
  - 按年龄段分组（如青年/中年/老年）

### 数据质量检查清单

```r
# 数据检查要点
# 1. 缺失值检查
# 2. 异常值检查
# 3. 数据编码确认（如1-5分制）
# 4. ID唯一性检查
# 5. 变量类型确认
```

执行以下检查：
- [ ] 检查缺失值比例（单个条目>20%需报告）
- [ ] 确认计分方式（几点量表）
- [ ] 检查是否有反向计分条目
- [ ] 验证数据范围合理性
- [ ] 检查受试者完成率

## 第二步：维度性检验

### 使用R包
- **主包**: `psych`, `mirt`, `lavaan`
- **辅助包**: `nFactors`, `EFAtools`

### 三项核心检验

#### 1. 残差主成分分析 (PCAR)

```r
# 使用包: mirt
library(mirt)

# 拟合单维Rasch模型
rasch_model <- mirt(data, 1, itemtype = 'Rasch')

# 提取残差主成分
residuals <- residuals(rasch_model, type = 'Q3')

# PCAR分析
# 判断标准: 
# - 第一主成分特征值 < 2.0（理想 < 1.5）
# - 第一主成分解释方差 < 10%
```

**判断标准**:
| 指标 | 单维性支持 | 警示值 |
|------|-----------|--------|
| 第一对比成分特征值 | < 2.0 | ≥ 3.0 |
| 第一对比成分方差解释 | < 5% | ≥ 10% |

#### 2. 解释共同方差 (ECV)

```r
# 使用包: psych, EFAtools
library(psych)

# 双因素模型或层次因素分析
omega_result <- omega(data, nfactors = 3, sl = TRUE)

# ECV计算
# ECV = 一般因素解释方差 / 总解释方差

# 或使用EFAtools
library(EFAtools)
ecv_result <- ECV(omega_result)
```

**判断标准**:
| ECV值 | 解释 |
|-------|------|
| ≥ 0.85 | 强单维性 |
| 0.70-0.84 | 基本单维 |
| 0.60-0.69 | 边缘单维 |
| < 0.60 | 多维性 |

#### 3. 分层Omega系数 (ωh)

```r
# 使用包: psych
library(psych)

# 计算omega层次系数
omega_h <- omega(data, nfactors = 3)

# 提取omega hierarchical
omega_h$omega_h  # 分层omega

# 判断标准:
# ωh ≥ 0.75: 总分可解释为单一构念
# ωh ≥ 0.80: 强单维性支持
```

**判断标准**:
| ωh值 | 解释 |
|------|------|
| ≥ 0.80 | 强单维性 |
| 0.75-0.79 | 可接受单维 |
| 0.50-0.74 | 弱单维 |
| < 0.50 | 多维性明显 |

### 维度检验汇总报告模板

```
========================================
          维度性检验结果汇总
========================================

1. PCAR结果:
   - 第一对比成分特征值: [值]
   - 第一对比成分方差解释: [值]%
   - 判断: [单维/多维]

2. ECV结果:
   - ECV值: [值]
   - 判断: [单维/多维]

3. Omega Hierarchical结果:
   - ωh值: [值]
   - 判断: [单维/多维]

----------------------------------------
综合判断: [单维性成立 / 存在多维性]
建议分析方案: [继续Rasch / 询问用户]
========================================
```

## 第三步：分析路径决策

### 情况A：单维性成立

直接进入Rasch分析流程（第四步）。

### 情况B：多维性存在

**必须询问用户选择**:

```
检测到量表存在多维性，请选择后续分析方案:

方案1: 拆分维度分析
- 将量表按理论维度拆分
- 对每个维度分别进行Rasch分析
- 优点: 符合传统Rasch假设
- 缺点: 无法获得整体量表信息

方案2: 多维IRT模型分析
- 使用MIRT包进行多维IRT分析
- 同时估计多个潜在特质
- 优点: 保留维度间相关信息
- 缺点: 模型复杂度增加

请选择: [1/2]
```

## 第四步：Rasch分析（单维情况）

### 使用R包
- **主包**: `eRm`, `TAM`, `mirt`
- **推荐**: `TAM`（输出最接近Winsteps格式）

### 核心分析内容

#### 4.1 模型拟合

```r
# 使用TAM包
library(TAM)

# Rasch模型拟合
mod <- tam(data)

# 或使用eRm包
library(eRm)
mod <- RM(data)
```

#### 4.2 条目分析 (Winsteps格式输出)

```r
# TAM包输出条目统计
item_stats <- tam.fit(mod)

# 需要输出的指标 (仿Winsteps格式):
# - MEASURE (条目难度/logit)
# - MODEL S.E. (标准误)
# - INFIT MNSQ (加权拟合)
# - INFIT ZSTD (标准化加权拟合)
# - OUTFIT MNSQ (非加权拟合)
# - OUTFIT ZSTD (标准化非加权拟合)
# - PTMEASURE-A CORR (点测量相关)
```

**条目拟合判断标准**:
| 指标 | 理想范围 | 可接受范围 | 需关注 |
|------|----------|-----------|--------|
| INFIT MNSQ | 0.7-1.3 | 0.5-1.5 | <0.5或>1.5 |
| OUTFIT MNSQ | 0.7-1.3 | 0.5-1.5 | <0.5或>2.0 |
| ZSTD | -2.0~+2.0 | -2.5~+2.5 | |z|>2.5 |

#### 4.3 受试者分析

```r
# 个人能力估计
person_stats <- tam.wle(mod)

# 输出内容:
# - theta (能力估计值)
# - error (标准误)
# - WLE可靠性
```

#### 4.4 必须输出的图表 (Winsteps风格)

**图1: 条目难度分布图 (Wright Map/Item-Person Map)**
```r
# TAM包
plot(mod, type = "items")

# 或自定义绘图
library(ggplot2)
# [自定义Wright Map代码]
```

**图2: 条目特征曲线 (ICC)**
```r
# 所有条目ICC
plot(mod, type = "items", export = FALSE)

# 单个条目ICC
plot(mod, items = 1)
```

**图3: 条目信息函数 (IIF)**
```r
# 条目信息曲线
plot(mod, type = "info")
```

**图4: 测验信息函数 (TIF)**
```r
# 测验信息曲线
test_info <- tam.fit(mod)
```

**图5: 类别概率曲线 (Category Probability Curves)**
```r
# 对于polytomous data
plot(mod, type = "expected")
```

**图6: 条目拟合图**
```r
# Infit/Outfit散点图
fit_data <- data.frame(
  item = rownames(item_stats),
  infit = item_stats$Infit,
  outfit = item_stats$Outfit
)
# 绘制气泡图或散点图
```

#### 4.5 标准表格输出

**表1: 条目难度与拟合统计表**
```
+-------+----------+-------+-------+-------+-------+-------+-------+
| Item  | Measure  | S.E.  | INFIT | INFIT | OUTFIT| OUTFIT| PT-M  |
|       | (logit)  |       | MNSQ  | ZSTD  | MNSQ  | ZSTD  | CORR  |
+-------+----------+-------+-------+-------+-------+-------+-------+
| item1 |  -0.52   | 0.12  | 1.02  | 0.3   | 0.98  | -0.1  | 0.65  |
| item2 |   0.31   | 0.11  | 0.95  | -0.5  | 0.92  | -0.8  | 0.71  |
| ...   |   ...    | ...   | ...   | ...   | ...   | ...   | ...   |
+-------+----------+-------+-------+-------+-------+-------+-------+
| Mean  |   0.00   | 0.11  | 1.00  | 0.0   | 1.00  | 0.0   |       |
| S.D.  |   0.85   | 0.02  | 0.15  | 1.2   | 0.18  | 1.4   |       |
+-------+----------+-------+-------+-------+-------+-------+-------+
```

**表2: 分离度与信度指标**
```
+------------------+----------+----------+
|       指标       |   条目   |   个人   |
+------------------+----------+----------+
| 分离度 (Separation) |  [值]   |  [值]   |
| 信度 (Reliability)  |  [值]   |  [值]   |
| Strata            |  [值]   |  [值]   |
+------------------+----------+----------+
```

**表3: 评分等级/阈值分析 (Rating Scale)**
```
+----------+----------+----------+----------+----------+
| Category | Observed | Average  | Infit    | Outfit   |
|          | Count    | Measure  | MNSQ     | MNSQ     |
+----------+----------+----------+----------+----------+
| 1        | [n]      | [值]     | [值]     | [值]     |
| 2        | [n]      | [值]     | [值]     | [值]     |
| ...      | ...      | ...      | ...      | ...      |
+----------+----------+----------+----------+----------+
```

### 4.6 DIF分析

```r
# 使用TAM包进行DIF分析
library(TAM)

# 按性别进行DIF
dif_gender <- tam.mml.mfr(data, formulaA = ~ item + item:gender)

# 按年龄组进行DIF
dif_age <- tam.mml.mfr(data, formulaA = ~ item + item:age_group)

# DIF效应量判断 (Winsteps标准)
# |DIF contrast| < 0.43 logits: 轻微
# |DIF contrast| 0.43-0.64 logits: 中等
# |DIF contrast| > 0.64 logits: 显著
```

**DIF结果表**
```
+-------+----------+----------+----------+----------+---------+
| Item  | Group 1  | Group 2  | DIF      | DIF      | DIF     |
|       | Measure  | Measure  | Contrast | S.E.     | t-value |
+-------+----------+----------+----------+----------+---------+
```

## 第五步：多维IRT分析（备选路径）

### 使用R包
- **主包**: `mirt`

```r
library(mirt)

# 定义维度结构
spec <- '
  F1 = 1-5
  F2 = 6-10
  F3 = 11-15
  COV = F1*F2, F1*F3, F2*F3
'

# 多维模型拟合
mod_mirt <- mirt(data, model = spec, itemtype = 'graded')

# 模型拟合指标
M2(mod_mirt)
fitIndices(mod_mirt)

# 条目参数
coef(mod_mirt, simplify = TRUE)

# 因素相关
summary(mod_mirt)
```

### 多维分析输出
- 各维度条目参数
- 维度间相关矩阵
- 多维信息曲面
- 模型拟合指标 (CFI, TLI, RMSEA, SRMR)

## 数据核查与复核

### 核查清单

**分析前核查**:
- [ ] 数据导入正确性（维度匹配）
- [ ] 编码一致性
- [ ] 缺失值处理方案确定

**分析中核查**:
- [ ] 模型收敛状态
- [ ] 参数估计合理性（条目难度范围通常-3~+3 logits）
- [ ] 异常拟合值标记

**分析后核查**:
- [ ] 分离度>2.0
- [ ] 信度>0.80
- [ ] 无严重误拟合条目（或已报告）

### 复核运算

对关键指标进行多包交叉验证:
```r
# TAM结果
mod_tam <- tam(data)

# eRm结果
mod_erm <- RM(data)

# mirt结果
mod_mirt <- mirt(data, 1, itemtype = 'Rasch')

# 比较条目难度估计相关
cor(tam_difficulties, erm_difficulties)  # 应 > 0.99
```

## 输出文件结构

```
[分析项目名]/
├── 数据/
│   ├── 原始数据.xlsx
│   ├── 清洗后数据.xlsx
│   └── 数据说明.txt
├── 维度检验/
│   ├── PCAR结果.xlsx
│   ├── ECV_Omega结果.xlsx
│   └── 维度检验报告.docx
├── Rasch分析/
│   ├── 条目统计表.xlsx
│   ├── 个人估计表.xlsx
│   ├── 图表/
│   │   ├── WrightMap.png
│   │   ├── ICC_all.png
│   │   ├── ICC_individual/
│   │   ├── ItemInfoFunction.png
│   │   ├── TestInfoFunction.png
│   │   ├── CategoryProbability.png
│   │   └── FitPlot.png
│   └── DIF分析.xlsx (如适用)
├── R代码/
│   ├── 01_数据处理.R
│   ├── 02_维度检验.R
│   ├── 03_Rasch分析.R
│   └── 04_DIF分析.R
└── 分析报告.docx
```

## R包版本要求

```r
# 核心包及推荐版本
install.packages(c(
  "TAM",      # >= 4.1-4  (主要Rasch分析包)
  "eRm",      # >= 1.0-2  (Rasch分析备选)
  "mirt",     # >= 1.38   (IRT/MIRT分析)
  "psych",    # >= 2.3.3  (Omega/EFA)
  "lavaan",   # >= 0.6-15 (CFA)
  "EFAtools", # >= 0.4.4  (ECV计算)
  "ggplot2",  # >= 3.4.0  (绑图)
  "openxlsx", # >= 4.2.5  (Excel输出)
  "knitr",    # >= 1.42   (报告生成)
  "rmarkdown" # >= 2.21   (报告生成)
))
```

## 常见问题处理

### 模型不收敛
1. 检查是否有全对/全错的受试者
2. 检查是否有全部选同一选项的条目
3. 尝试减少迭代精度要求

### 严重误拟合条目
1. 报告用户
2. 讨论是否删除或合并
3. 进行敏感性分析

### DIF检测阳性
1. 报告效应量
2. 讨论实质意义
3. 提供是否保留建议

## 关键提醒

1. **所有分析必须使用R语言包，不使用Winsteps软件本身**
2. **每次使用包时必须明确告知包名称**
3. **输出格式尽量模仿Winsteps标准格式**
4. **关键计算需进行多包交叉验证**
5. **维度检验必须在Rasch分析之前完成**
6. **发现多维性必须询问用户处理方案**
