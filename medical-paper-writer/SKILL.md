---
name: medical-paper-writer
description: "辅助医学科研论文写作的全流程工具。当用户提到'论文写作'、'SCI写作'、'论文润色'、'摘要撰写'、'Methods写作'、'Discussion写作'、'审稿意见回复'、'Cover Letter'、'投稿'、'CONSORT'、'STROBE'、'PRISMA'等时使用此skill。支持：各部分写作模板、报告规范checklist、统计结果描述、学术英语表达、投稿材料准备等。"
---

# 医学科研论文写作助手

辅助医学论文从构思到投稿的全流程写作。

## 工作流程概述

```
1. 确认研究信息 → 2. 匹配报告规范 → 3. 提供写作指导 → 4. 生成模板/润色
```

## Step 1: 信息收集

收到论文写作请求后，询问关键信息：

### 必问信息
- **研究类型**：RCT / 队列研究 / 病例对照 / 横断面 / Meta分析 / 病例报告 / 基础研究
- **目标期刊级别**：SCI / 中文核心 / 普通期刊（或具体期刊名）
- **语言**：英文 / 中文
- **当前阶段**：
  - 从头写作
  - 部分完成需补充
  - 初稿润色
  - 回复审稿意见

### 可选信息
- 研究主题/标题
- 已有材料（数据、初稿）
- 字数/格式要求
- 截止时间

## Step 2: 报告规范匹配

根据研究类型自动匹配报告规范：

| 研究类型 | 报告规范 | 核心条目数 |
|----------|----------|------------|
| 随机对照试验（RCT） | CONSORT | 25项 |
| 队列/病例对照/横断面 | STROBE | 22项 |
| 系统综述/Meta分析 | PRISMA | 27项 |
| 诊断准确性研究 | STARD | 25项 |
| 病例报告 | CARE | 13项 |
| 动物实验 | ARRIVE | 21项 |
| 质量改进研究 | SQUIRE | 18项 |

详细checklist见 references/reporting_guidelines.md

## Step 3: 各部分写作指导

### 3.1 Title（标题）

**结构模板**：

```
【RCT】
[干预措施] for [疾病/人群]: A Randomized Controlled Trial
Effect of [干预] on [结局] in Patients with [疾病]: A Randomized, [盲法], [对照类型] Trial

【队列研究】
Association between [暴露] and [结局] in [人群]: A [前瞻性/回顾性] Cohort Study
[暴露] and Risk of [结局]: A [数据库名] Cohort Study

【病例对照】
[暴露因素] and [疾病]: A Case-Control Study
Risk Factors for [疾病] in [人群]: A Hospital-Based Case-Control Study

【横断面】
Prevalence and Risk Factors of [疾病] among [人群]: A Cross-Sectional Study

【Meta分析】
[干预/暴露] and [结局]: A Systematic Review and Meta-Analysis
Efficacy and Safety of [干预] for [疾病]: A Meta-Analysis of Randomized Controlled Trials

【病例报告】
[罕见情况/特殊表现] in a Patient with [疾病]: A Case Report
[治疗方法] for [罕见疾病]: A Case Report and Literature Review
```

**标题原则**：
- 简洁明确，通常不超过20个单词
- 包含研究设计类型
- 避免缩写（除非广泛认知如DNA、MRI）
- 避免"研究"、"观察"等冗余词

---

### 3.2 Abstract（摘要）

**结构式摘要模板（英文）**：

```
Background/Purpose:
[1-2句背景] + [研究目的，以"This study aimed to..."或"We aimed to..."开头]

Methods:
[研究设计] + [研究对象] + [干预/暴露] + [主要结局指标] + [统计方法]

Results:
[样本量] + [主要结果，含具体数据] + [次要结果]

Conclusions:
[主要结论] + [临床意义/研究意义]
```

**字数控制**：
- 大多数期刊：250-300词
- BMJ/Lancet等：300-400词
- 中文摘要：400-500字

**时态规则**：
- Background：现在时（陈述已知事实）
- Methods/Results：过去时
- Conclusions：现在时或现在完成时

---

### 3.3 Introduction（引言）

**漏斗式结构**：

```
第1段：大背景（What is known）
- 疾病/问题的重要性
- 发病率、危害、负担
- 当前治疗/研究现状

第2段：研究空白（What is unknown）
- 现有研究的局限性
- 存在的争议或空白
- 为什么需要本研究

第3段：研究目的（What this study adds）
- 本研究目的
- 简要说明研究方法
- 可选：假设
```

**常用句型**：

```
【背景句型】
- [疾病] is a leading cause of [后果] worldwide.
- [疾病] affects approximately [数字] million people globally.
- The prevalence of [疾病] has increased dramatically over the past decades.
- [治疗/因素] has been widely used/recognized as...

【研究空白句型】
- However, the [relationship/effect/mechanism] remains unclear.
- Previous studies have yielded inconsistent results.
- Limited data are available regarding...
- To date, no study has investigated...
- Whether [因素] is associated with [结局] remains controversial.

【研究目的句型】
- Therefore, this study aimed to investigate/evaluate/assess...
- The purpose of this study was to determine...
- We conducted this study to examine...
- In the present study, we sought to...
```

**长度**：通常3-4段，占全文10-15%

---

### 3.4 Methods（方法）

**标准结构**：

```
1. Study Design and Setting
   - 研究设计类型
   - 研究地点和时间
   - 伦理批准声明

2. Participants/Subjects
   - 纳入标准
   - 排除标准
   - 样本量及计算依据

3. Interventions/Exposures（如适用）
   - 干预措施详细描述
   - 对照组处理
   - 随机化和盲法（RCT）

4. Outcomes/Variables
   - 主要结局指标（定义、测量方法）
   - 次要结局指标
   - 其他变量

5. Data Collection
   - 数据收集方法
   - 使用的工具/量表
   - 质量控制

6. Statistical Analysis
   - 描述性统计方法
   - 推断性统计方法
   - 软件和显著性水平
```

**伦理声明模板**：

```
【英文】
This study was approved by the Institutional Review Board/Ethics Committee of [机构名称] (Approval No. [编号]). Written informed consent was obtained from all participants [or their legal guardians].

This study was conducted in accordance with the Declaration of Helsinki.

【中文】
本研究经[机构名称]伦理委员会批准（批准文号：[编号]），所有参与者[或其监护人]均签署知情同意书。
```

**统计方法描述模板**：
见 references/statistical_reporting.md

---

### 3.5 Results（结果）

**呈现顺序**：

```
1. 研究流程（Flow diagram描述）
   - 筛选过程
   - 排除原因
   - 最终纳入数量

2. 基线特征（Table 1）
   - 人口学特征
   - 临床特征
   - 组间可比性（如适用）

3. 主要结局
   - 先给主要发现
   - 具体数据支持
   - 图表引用

4. 次要结局
   - 按重要性排序

5. 亚组分析/敏感性分析（如有）

6. 不良事件（如适用）
```

**数据报告规范**：

```
【连续变量-正态分布】
mean ± SD 或 mean (SD)
示例：The mean age was 45.3 ± 12.5 years.

【连续变量-偏态分布】
median (IQR) 或 median (Q1-Q3)
示例：The median follow-up was 24 (18-36) months.

【分类变量】
n (%)
示例：Diabetes was present in 45 patients (32.1%).

【比较结果】
差值/比值 (95% CI), P值
示例：
- OR = 2.15 (95% CI: 1.32-3.50), P = 0.002
- HR = 0.72 (95% CI: 0.58-0.89), P = 0.003
- Mean difference = 5.2 (95% CI: 2.1-8.3), P = 0.001

【P值报告】
- P < 0.001（不写P = 0.000）
- 精确到小数点后三位，如P = 0.042
- 不显著时：P = 0.156（不写P > 0.05或NS）
```

**结果描述句型**：
见 references/results_phrases.md

---

### 3.6 Discussion（讨论）

**标准结构**：

```
第1段：主要发现（Key Findings）
- 开门见山陈述主要结果
- 不重复Results的数据细节
- 1段，3-5句

第2-4段：与既往研究比较（Comparison with Literature）
- 与已发表研究对比
- 一致性：支持/验证
- 不一致：可能原因解释
- 每个主要发现1段

第5段：可能机制（Potential Mechanisms）
- 生物学/病理生理学解释
- 引用基础研究支持
- 可以是推测但要注明

第6段：优势与局限（Strengths and Limitations）
- 优势：2-3点
- 局限：3-5点（诚实但不过度贬低）
- 如何缓解局限性

第7段：临床/研究意义（Implications）
- 对临床实践的启示
- 对未来研究的建议

第8段：结论（Conclusion）
- 简洁总结主要发现
- 呼应研究目的
- 避免过度外推
```

**常用句型**：

```
【主要发现】
- In this [study type], we found that...
- The main finding of this study was that...
- Our results demonstrated that...

【与文献比较-一致】
- Our findings are consistent with previous studies showing...
- In line with [Author et al.], we observed...
- This result confirms earlier reports that...

【与文献比较-不一致】
- In contrast to [Author et al.], we found...
- Our results differ from those of [study], which may be explained by...
- The discrepancy between our findings and previous studies might be due to...

【机制解释】
- Several mechanisms may explain this finding.
- One possible explanation is that...
- This observation could be attributed to...

【局限性】
- This study has several limitations.
- First, the [retrospective/cross-sectional] design limits causal inference.
- Second, we could not adjust for [unmeasured confounders].
- Third, the generalizability may be limited due to...

【临床意义】
- These findings have important clinical implications.
- Our results suggest that clinicians should consider...
- This study provides evidence supporting...

【结论】
- In conclusion, our study demonstrates that...
- Taken together, these findings indicate...
```

---

### 3.7 References（参考文献）

**Vancouver格式**（医学期刊最常用）：

```
【期刊文章】
Author AA, Author BB, Author CC. Title of article. Journal Name. Year;Volume(Issue):Pages. doi:xx

示例：
Smith J, Johnson M, Williams K. Effect of aspirin on cardiovascular outcomes. N Engl J Med. 2023;388(15):1234-1245. doi:10.1056/NEJMoa2301234

【超过6位作者】
列出前6位作者后加"et al."

【书籍章节】
Author AA. Chapter title. In: Editor BB, ed. Book Title. Edition. Publisher; Year:Pages.
```

**引用原则**：
- 优先引用近5年文献
- 优先引用高质量期刊
- 引用原始研究而非综述（除非讨论综述结论）
- 避免过度自引

## Step 4: 投稿材料

### Cover Letter模板

```
Dear Editor,

We are pleased to submit our manuscript entitled "[Title]" for consideration for publication in [Journal Name].

[1-2句研究背景和重要性]

In this [study type], we [简述研究内容和主要发现]. Our findings suggest that [主要结论和意义].

We believe this work will be of interest to the readers of [Journal Name] because [与期刊scope的匹配度].

This manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission to [Journal Name].

We have no conflicts of interest to declare. [或具体声明利益冲突]

Thank you for your consideration. We look forward to hearing from you.

Sincerely,

[Corresponding Author Name]
[Title, Department]
[Institution]
[Email]
[Phone]
```

### 审稿意见回复模板

```
Dear Editor and Reviewers,

We would like to thank you for the opportunity to revise our manuscript (Manuscript ID: XXX) entitled "[Title]". We appreciate the constructive comments from the reviewers, which have helped us improve the manuscript significantly.

We have carefully addressed all the comments point by point. Below please find our detailed responses. All changes in the revised manuscript are highlighted in [yellow/tracked changes].

---

REVIEWER #1

Comment 1: [原文引用审稿人意见]

Response: We thank the reviewer for this insightful comment. [具体回应]. We have revised the manuscript accordingly (Page X, Lines XX-XX):

"[修改后的原文引用]"

Comment 2: [原文引用]

Response: [回应]

---

REVIEWER #2

[同样格式]

---

We hope the revised manuscript now meets the standards for publication in [Journal Name]. Please do not hesitate to contact us if any further revisions are needed.

Sincerely,
[Authors]
```

**回复原则**：
- 逐条回复，不遗漏
- 先感谢，再解释
- 明确标注修改位置
- 不同意时礼貌说明理由并提供证据
- 重大修改需详细解释

## 学术写作注意事项

### 避免的表达

```
❌ 口语化
- a lot of → numerous, substantial, considerable
- get → obtain, acquire, achieve
- show → demonstrate, indicate, reveal
- big/small → large/substantial, minor/minimal

❌ 主观化
- We believe → The findings suggest
- Obviously → The data indicate
- Interestingly → Notably

❌ 绝对化
- prove → support, suggest
- always/never → generally, rarely
- must → may, might, could
```

### 时态使用

| 部分 | 时态 | 示例 |
|------|------|------|
| Abstract-Background | 现在时 | Diabetes is a major health concern. |
| Abstract-Methods | 过去时 | We conducted a cohort study. |
| Abstract-Results | 过去时 | The mean age was 45 years. |
| Abstract-Conclusion | 现在时 | These findings suggest... |
| Introduction | 现在时为主 | Previous studies have shown... |
| Methods | 过去时 | Patients were enrolled... |
| Results | 过去时 | The incidence rate was... |
| Discussion | 混合 | Our study found (过去) + This suggests (现在) |

## 输出格式

根据需求提供：
- Word文档（带模板结构）
- 纯文本（可复制）
- Checklist（报告规范核对）
- 修改建议（批注形式）
