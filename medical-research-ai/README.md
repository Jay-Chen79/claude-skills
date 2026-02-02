# Medical Research AI - 医学科研全流程自动化

## 简介

一个自动化的医学科研助手，能够在 10 分钟内完成通常需要 6 个月的科研前期工作：

- ✅ 大规模文献检索（PubMed API）
- ✅ 文献深度分析
- ✅ 研究空白识别
- ✅ 创新性评估
- ✅ 研究方案生成
- ✅ 伦理申请材料

## 安装

```bash
# 依赖 Python 3.7+
pip install requests  # 可选，用于更复杂的请求

# 已包含在 skill 中，直接使用即可
```

## 使用方法

### 方法 1: 在 Claude Code 中使用

直接在对话中提到科研相关话题即可触发：

```
"我想研究干眼症和屏幕时间的关系，帮我做个研究方案"
"近视在儿童青少年中的发病率，有没有创新的研究方向？"
"帮我查一下青光眼的最新研究进展"
```

### 方法 2: 命令行使用

```bash
cd ~/.claude/skills/medical-research-ai
python main.py \
  --topic "干眼症与屏幕时间" \
  --keywords "dry eye" "screen time" "digital device" \
  --mesh "Dry Eye Syndromes" \
  --population "成人" \
  --max-papers 500 \
  --output results.json
```

### 方法 3: Python 代码调用

```python
from main import MedicalResearchAI

# 初始化
ai = MedicalResearchAI()

# 运行完整分析
result = ai.run_full_workflow(
    topic="干眼症与屏幕时间",
    keywords=["dry eye", "screen time", "digital device"],
    mesh_terms=["Dry Eye Syndromes"],
    population="成人",
    max_papers=500
)

# 打印报告
ai.print_summary_report()

# 保存结果
ai.save_to_json("analysis.json")
ai.generate_markdown_report("report.md")
```

## 输出内容

### 1. 文献分析报告

- 检索文献数量
- 发表时间趋势
- 研究类型分布
- 研究人群分析

### 2. 研究空白识别

- 研究人群空白
- 研究设计空白
- 结局指标空白
- 干预措施空白
- 随访时间空白

### 3. 推荐研究方向

按创新性排序的研究方向列表，每个包含：
- 研究题目
- 研究设计
- 创新性评分
- 可行性评分
- 研究描述

### 4. 详细研究方案

Top 3 方向的完整方案：
- 研究设计
- 样本量计算
- 纳入排除标准
- 统计分析计划
- 时间安排

### 5. 伦理申请材料

- 伦理申请表
- 知情同意书模板
- 风险获益评估

## 支持的研究类型

- 队列研究
- 病例对照研究
- 横断面研究
- 随机对照试验 (RCT)
- 诊断准确性研究
- 系统评价/Meta 分析

## 支持的专科领域

目前主要针对眼科/视光领域，涵盖：

- 干眼症
- 近视
- 青光眼
- 白内障
- 糖尿病视网膜病变
- 结膜炎
- 角膜疾病

## PubMed API 配额

- 无 API key: 每秒 3 次请求
- 有 API key: 每秒 10 次请求

申请免费 API key: https://www.ncbi.nlm.nih.gov/account/

## 文件结构

```
medical-research-ai/
├── skill.md              # Skill 说明文件
├── README.md             # 使用说明
├── main.py               # 主流程编排器
├── pubmed_search.py      # PubMed 检索引擎
├── gap_analyzer.py       # Gap 分析器
├── study_designer.py     # 研究设计生成器
└── templates/            # 模板文件（可选）
```

## 限制与说明

1. **全文获取**: 目前主要基于摘要分析，受版权限制无法批量获取全文
2. **创新性保证**: AI 基于现有文献分析，无法保证真正的突破性创新
3. **可行性评估**: 需要人工审核，不了解各医院实际情况
4. **医学专业性**: 眼科/视光优先，其他领域可扩展

## 未来改进方向

- [ ] 接入 Embase、Cochrane 等多数据库
- [ ] 集成全文获取（开放获取期刊）
- [ ] 自动化研究质量评分 (ROBIS, RoB 2.0)
- [ ] 知识图谱可视化
- [ ] 论文初稿生成
- [ ] 投稿期刊推荐

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
