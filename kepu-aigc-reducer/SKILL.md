---
name: kepu-aigc-reducer
description: >
  中文医学科普文 AIGC 降率工具。针对已用 AI 辅助写作的医学科普文章（.docx），通过人性化改写降低 AIGC 检测工具的疑似率。
  支持两种模式：(1) 提供 AIGC 检测报告 PDF，精准定位高风险段落后改写；(2) 无报告时，根据 AI 写作特征自动扫描改写。
  输出改写后的新 docx 文件，保留原文结构、格式和医学准确性。
  触发词：'降AI率'、'降低AI检测'、'AIGC检测'、'去AI味'、'AI疑似率'、'人工智能检测'、'降重'（AIGC方向）、
  '科普文被检测'、'医学科普降AI'
---

# 医学科普文 AIGC 降率工具

## 工具链依赖

```bash
# 文本提取
pandoc <input.docx> -t plain

# PDF 读取检测报告
python3 -c "import pdfplumber; ..."

# DOCX 编辑（unpack → edit XML → repack）
python3 ~/.claude/skills/docx/scripts/office/unpack.py <input.docx> <unpacked_dir>/
python3 ~/.claude/skills/docx/scripts/office/pack.py <unpacked_dir>/ <output.docx> --original <input.docx>
```

> **注意**：pack.py 需要 Python 3.10+，macOS 请用 `/opt/homebrew/bin/python3`

---

## 工作流程

### Step 1：提取文章内容

```bash
pandoc "<input.docx>" -t plain 2>/dev/null
```

### Step 2：读取 AIGC 检测报告（如有）

用 pdfplumber 提取报告文本，找出每段落的 AI 疑似概率。
**重点改写阈值：≥ 60% 的段落为高优先级，40-60% 为中优先级。**

若无报告，跳至 Step 3b。

```python
import pdfplumber
with pdfplumber.open("检测报告.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

报告中关键字段：
- `该段落可能为AI生成的概率为：XX%` → 段落级别疑似率
- `高度疑似AI占全文比` → 整体疑似率概览

### Step 3a：有报告 → 精准定位改写目标

按报告中的段落顺序，将疑似率 ≥ 60% 的段落标记为必改，40-60% 为选改。
跳过 ≤ 40% 的段落（改写风险高于收益）。

### Step 3b：无报告 → 扫描 AI 写作特征

对全文逐段判断，含以下特征的段落优先改写（详见 `references/humanization-patterns.md`）：
- 完美对仗的并列结构（"不仅…更是…"、"一方面…另一方面…"）
- 连续多个"这就好比…"类比
- 每段都以"总结句"收尾
- 主语长期为"我们"或"患者"

### Step 4：改写高 AI 段落

**改写原则**（详见 `references/humanization-patterns.md`）：
1. 注入第一人称临床视角（护士/医生"我"的经历）
2. 加入具体患者场景（年龄、行为、对话）
3. 打破对称句式，混合长短句
4. 用口语化结尾替代书面总结句
5. 替换 AI 惯用连接词

**保留原则**：
- 医学术语和数据准确性不变
- 原文结构（标题、Q&A、要点列表）不变
- 低 AI 段落（≤ 40%）不动

### Step 5：应用改写到 DOCX

```bash
# 1. 解包
python3 ~/.claude/skills/docx/scripts/office/unpack.py "<input.docx>" /tmp/docx_work/

# 2. 定位目标段落的 XML 行
grep -n "<关键词>" /tmp/docx_work/word/document.xml

# 3. 用 Edit 工具替换 <w:t> 内容（不改 <w:rPr> 格式标签）
# 注意：引号使用 XML 实体 &#x201C; &#x201D; &#x2018; &#x2019;

# 4. 重新打包
/opt/homebrew/bin/python3 ~/.claude/skills/docx/scripts/office/pack.py \
    /tmp/docx_work/ "<output_降AI版.docx>" --original "<input.docx>"
```

输出文件命名规范：`原文件名_降AI版.docx`，保存在原文件同目录。

### Step 6：输出改写摘要

完成后向用户报告：
- 改写段落数 / 总段落数
- 各段改写前后预估 AI 率变化
- 主要改写手法说明

---

## 参考资料

- **改写模式详情**：见 `references/humanization-patterns.md`
  - 完整 AI 写作特征识别清单
  - 分类改写策略（句式、词汇、视角）
  - 改写前后对照示例（来自真实案例）
