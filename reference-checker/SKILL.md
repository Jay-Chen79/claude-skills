---
name: reference-checker
description: 学术论文参考文献自动检查与验证工具。检查参考文献格式正确性、引用顺序、文献真实性（通过DOI/PubMed/URL验证），生成详细的检查报告和修改建议。触发条件：用户上传论文要求检查参考文献、验证引用真实性、检查引用格式、查找虚假文献等。支持 .docx、.pdf 输入格式。
---

# 参考文献检查器

学术论文参考文献全面检查工具，包含格式检查、真实性验证、相关性分析。

## 快速参考

| 任务 | 方法 |
|------|------|
| 检查 .docx 论文 | 运行 `parse_references.py` 解析 → WebSearch 验证 → `generate_report.py` 生成报告 |
| 检查 .pdf 论文 | 使用 `scientific-skills:pdf` 技能提取文本 → 手动解析 → 验证 → 生成报告 |
| 验证单条文献 | WebSearch 搜索 DOI/标题/作者 |
| 批量验证 | 循环调用验证流程，控制请求频率 |

## 完整工作流程

### 第一步：解析文档

**对于 .docx 文件：**
```bash
python scripts/parse_references.py <论文.docx> [输出.json]
```

**对于 .pdf 文件：**
使用 `scientific-skills:pdf` 技能提取文本，手动识别正文引用和参考文献列表。

**解析输出：**
- 文中所有引用标记 `[1]` `[2]` 及其位置、上下文
- 文末参考文献列表
- 缺失的参考文献（文中引用但列表无）
- 未被引用的参考文献（列表有但文中无）
- 顺序错误的引用

### 第二步：真实性验证（核心）

**验证顺序：**

1. **DOI 验证**（最权威）
   - 使用 WebSearch 搜索 `doi:{DOI号}`
   - 或搜索 `{DOI号} site:doi.org`
   - 检查是否能解析到真实文献页面

2. **PubMed 验证**（医学/生命科学）
   - 搜索 `{文献标题} site:pubmed.ncbi.nlm.nih.gov`
   - 验证 PMID 是否存在
   - 获取 PubMed 链接

3. **书籍验证**
   - 搜索 `{书名} {作者} ISBN`
   - 搜索 `{书名} site:books.google.com` 或 `site:worldcat.org`
   - 提供验证链接

4. **期刊文章验证**
   - 搜索 `"{文献标题}" {作者姓名} {期刊名}`
   - 通过 Google Scholar 或 CrossRef 验证

5. **中文文献验证**
   - 搜索 `{标题} site:cnki.net` 或 `site:wanfangdata.com.cn`
   - CNKI、万方数据库验证

**验证状态分类：**
- `verified`：已验证存在（提供链接）
- `unverified`：无法验证（非虚假，可能数据库未收录）
- `suspicious`：存疑（信息不一致或无法找到）
- `invalid`：明确无效（DOI格式错误、页面404等）

### 第三步：相关性验证

对每个引用：

1. **提取上下文**：获取引用所在句子及前后各1-2句
2. **获取文献摘要**：通过搜索获取被引文献的摘要或主要内容
3. **评估匹配度**：
   - **高度相关**：文献内容直接支持引用处的论点
   - **基本相关**：文献主题相关，但支持程度一般
   - **相关性存疑**：文献与引用上下文关联不明显
   - **明显不相关**：文献内容与引用处论述无关

### 第四步：生成输出

**运行报告生成：**
```bash
python scripts/generate_report.py <原文.docx> <解析.json> <验证.json> [输出前缀]
```

**输出文件：**
1. `{前缀}_report.docx`：详细检查报告
2. `{前缀}_corrected.docx`：标注问题的修改版文档
3. `{前缀}_corrections.json`：机器可读的修改建议

## 报告格式模板

### A. 执行摘要

```
总体评估：[优秀/良好/需修改/存在严重问题]

统计：
- 参考文献总数：X 条
- 验证有效：X 条 (XX%)
- 存疑文献：X 条
- 格式错误：X 处
- 序号问题：X 处

紧急程度：[高/中/低]
- 高：存在虚假文献或严重格式错误
- 中：部分文献无法验证或有格式问题
- 低：仅有轻微问题
```

### B. 详细检查结果表

| 序号 | 原文献信息（摘要） | 检查状态 | DOI/PubMed链接 | 相关性评分 | 问题说明 |
|------|-------------------|---------|---------------|-----------|---------|
| [1]  | Smith et al. 2020... | verified | https://doi.org/... | 高度相关 | 无 |
| [2]  | Wang et al. 2021... | suspicious | - | 存疑 | 无法找到匹配文献 |

### C. 问题分类清单

**虚假/不存在的文献：**
- [X] 原文：...，问题：...

**序号顺序问题：**
- 期望 [3]，实际 [5]

**格式错误：**
- [X] 缺少DOI
- [Y] 作者格式不规范

**相关性存疑：**
- [Z] 上下文与文献内容不匹配

### D. 修改建议

1. 核实并补充/删除以下文献：...
2. 调整引用序号顺序
3. 补充缺失的DOI信息
4. 统一作者姓名格式

### E. 验证链接汇总

所有已验证文献的访问链接，便于作者核实。

## 脚本说明

### parse_references.py

解析 .docx 文件，提取引用和参考文献。

```bash
python scripts/parse_references.py paper.docx output.json
```

输入：.docx 文件
输出：JSON 文件，包含：
- `citations`：引用列表（序号、位置、上下文）
- `references`：参考文献列表（序号、原文、类型、DOI等）
- `missing_refs`：缺失的参考文献序号
- `unused_refs`：未被引用的序号
- `out_of_order`：顺序错误
- `duplicates`：重复引用

### generate_report.py

生成检查报告和修改版文档。

```bash
python scripts/generate_report.py paper.docx parsed.json verified.json output_prefix
```

输入：
- 原始 .docx 文件
- 解析结果 JSON
- 验证结果 JSON

输出：
- `{prefix}_report.docx`：检查报告
- `{prefix}_corrected.docx`：标注问题的文档（红色标记存疑引用）
- `{prefix}_corrections.json`：修改清单

## 在线验证详细方法

### WebSearch 验证策略

**DOI 验证：**
```
搜索：doi:10.1038/s41586-021-03819-2
或：10.1038/s41586-021-03819-2 site:doi.org
```

**PubMed 验证：**
```
搜索：PMID 12345678 site:pubmed.ncbi.nlm.nih.gov
或："{文章标题}" pubmed
```

**书籍验证：**
```
搜索："{书名}" {作者} ISBN
搜索：{书名} site:worldcat.org
搜索：{书名} site:books.google.com
```

**中文文献验证：**
```
搜索："{标题}" site:cnki.net
搜索："{标题}" 万方数据
```

### 验证结果记录

对每条参考文献记录：
- 验证方法（DOI/PubMed/搜索等）
- 验证结果（成功/失败/存疑）
- 验证链接
- 发现的问题

## 支持的引用格式

**引用标记：**
- `[1]` 单篇
- `[1-3]` 连续
- `[1,2,5]` 非连续

**参考文献格式：**
- GB/T 7714-2015（中国国标）
- APA 第7版
- Vancouver（医学）
- 其他编号制格式

详见 [references/citation_formats.md](references/citation_formats.md)

## 限制与注意事项

### 技术限制
- 仅支持数字编号制（`[1]`），不支持作者-年份制（Smith, 2020）
- PDF 解析可能丢失格式信息
- 网络验证受限于数据库收录范围

### 验证准确性
- **通过验证 ≠ 一定真实**：可能存在伪造DOI
- **未通过验证 ≠ 一定虚假**：可能是新文献未被收录、灰色文献等
- 始终需要人工最终确认

### 相关性判断
- 系统提供初步评估，最终判断需人工审核
- 特别注意专业术语的理解差异

## 最佳实践

### 检查前
1. 确保文档格式规范
2. 确认所有引用使用统一格式
3. 检查DOI/PMID是否完整

### 检查中
1. 大量文献（>50条）分批验证
2. 记录验证进度
3. 对存疑文献多次搜索确认

### 检查后
1. 优先处理"明确无效"的文献
2. 逐一核实"存疑"文献
3. 人工审核相关性评分
4. 使用修订模式修改原文

## 依赖

```bash
pip install python-docx
```

PDF 处理需要 `scientific-skills:pdf` 技能。
