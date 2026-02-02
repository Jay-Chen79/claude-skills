#!/usr/bin/env python3
"""
Medical Research AI - 主流程编排器
整合文献检索、Gap分析、研究设计生成，实现端到端自动化
"""

import sys
import json
from typing import Dict, List, Optional

# 导入各模块
from pubmed_search import PubMedSearcher
from gap_analyzer import GapAnalyzer
from study_designer import StudyDesigner


class MedicalResearchAI:
    """医学科研全流程自动化系统"""

    def __init__(self, api_key: str = "", email: str = ""):
        """
        Args:
            api_key: NCBI API key (可选，提高请求配额)
            email: 联系邮箱 (NCBI 要求)
        """
        self.searcher = PubMedSearcher(api_key=api_key, email=email)
        self.current_analysis = None

    def run_full_workflow(self, topic: str, keywords: List[str],
                          mesh_terms: List[str] = None,
                          population: str = "成人",
                          study_type_preference: str = None,
                          max_papers: int = 500) -> Dict:
        """
        运行完整工作流

        Args:
            topic: 研究主题（如：干眼症、近视、青光眼）
            keywords: 关键词列表
            mesh_terms: MeSH 词列表（可选）
            population: 目标人群（成人/儿童青少年/老年人）
            study_type_preference: 研究类型偏好
            max_papers: 最大检索文献数

        Returns:
            完整分析结果字典
        """
        print("\n" + "="*70)
        print("🔬 Medical Research AI - 医学科研全流程自动化")
        print("="*70)

        # ============ Phase 1: 文献检索 ============
        print("\n📚 Phase 1: 大规模文献检索...")
        print(f"   研究主题: {topic}")
        print(f"   目标人群: {population}")

        query = self.searcher.build_ophthalmology_query(
            keywords=keywords,
            mesh_terms=mesh_terms,
            study_type=study_type_preference
        )

        print(f"   检索式: {query[:100]}...")

        pmids = self.searcher.search(query, max_results=max_papers)
        print(f"   ✓ 检索到 {len(pmids)} 篇相关文献")

        if not pmids:
            print("   ⚠️ 未检索到文献，请调整检索词")
            return {"error": "未检索到文献"}

        # ============ Phase 2: 获取文献摘要 ============
        print(f"\n📖 Phase 2: 获取文献摘要...")
        summaries = self.searcher.fetch_summaries(pmids)
        print(f"   ✓ 成功获取 {len(summaries)} 篇摘要")

        # ============ Phase 3: 文献分析 ============
        print(f"\n📊 Phase 3: 文献深度分析...")

        pub_trend = self.searcher.analyze_publication_dates(summaries)
        study_types = self.searcher.analyze_study_types(summaries)

        print(f"   发表时间范围: {pub_trend.get('year_range', 'N/A')}")
        print(f"   总文献数: {pub_trend.get('total', 0)}")
        print(f"   近5年发表: {pub_trend.get('recent_5_years', 0)} 篇")

        print(f"\n   研究类型分布:")
        for st, count in study_types.items():
            if count > 0:
                print(f"     • {st}: {count} 篇")

        # ============ Phase 4: Gap 分析 ============
        print(f"\n🔍 Phase 4: 识别研究空白...")
        analyzer = GapAnalyzer(summaries)
        gaps = analyzer.identify_gaps()

        print(f"   ✓ 识别出 {len(gaps)} 个研究空白")

        # ============ Phase 5: 生成研究方向 ============
        print(f"\n💡 Phase 5: 生成研究方向...")
        directions = analyzer.generate_research_directions(topic)

        print(f"   ✓ 生成 {len(directions)} 个研究方向")

        # ============ Phase 6: 生成详细方案 ============
        print(f"\n📋 Phase 6: 生成详细研究方案...")

        protocols = []
        for i, direction in enumerate(directions[:3], 1):  # 取 top 3
            print(f"   [{i}] {direction['title']}")
            designer = StudyDesigner(
                topic=topic,
                study_design=direction['design'],
                population=direction.get('population', population)
            )
            protocol = designer.generate_full_protocol()
            protocol['innovation'] = direction.get('innovation', '')
            protocol['innovation_score'] = direction.get('innovation_score', '')
            protocols.append(protocol)

        # ============ Phase 7: 生成伦理材料 ============
        print(f"\n⚖️  Phase 7: 生成伦理申请材料...")

        ethics_materials = []
        for protocol in protocols:
            ethics = self._generate_ethics_materials(protocol)
            ethics_materials.append(ethics)

        # ============ 汇总结果 ============
        self.current_analysis = {
            "topic": topic,
            "population": population,
            "literature_search": {
                "query": query,
                "total_found": len(pmids),
                "abstracts_obtained": len(summaries),
                "publication_trend": pub_trend,
                "study_types": study_types,
            },
            "gap_analysis": {
                "gaps_identified": gaps,
                "total_gaps": len(gaps),
            },
            "research_directions": directions,
            "detailed_protocols": protocols,
            "ethics_materials": ethics_materials,
        }

        print(f"\n✅ 工作流完成！")

        return self.current_analysis

    def _generate_ethics_materials(self, protocol: Dict) -> Dict:
        """生成伦理申请材料"""
        basic_info = protocol['basic_info']

        return {
            "伦理申请表": {
                "项目名称": basic_info['title'],
                "研究类型": basic_info['study_design'],
                "研究者": "[待填写]",
                "单位": "[待填写]",
                "研究期限": f"{sum(p['duration'] for p in protocol['timeline'])}个月",
                "研究目的": protocol['objectives']['primary'],
                "研究人群": basic_info['population'],
                "样本量": protocol['sample_size'].get('with_attrition', protocol['sample_size'].get('calculated_n', '待定')),
                "主要风险": protocol['ethics']['risk_benefit']['risks'],
                "预期获益": protocol['ethics']['risk_benefit']['benefits'],
            },
            "知情同意书": {
                "标题": f"{basic_info['title']}知情同意书",
                "研究说明": self._generate_consent_content(protocol),
                "风险告知": protocol['ethics']['risk_benefit']['risks'],
                "获益说明": protocol['ethics']['risk_benefit']['benefits'],
                "自愿声明": "我已充分了解本研究的内容和风险，自愿参加研究。",
                "联系方式": "[待填写研究者联系方式]",
            },
        }

    def _generate_consent_content(self, protocol: Dict) -> str:
        """生成知情同意书正文"""
        return f"""
本研究旨在{protocol['objectives']['primary']}。

研究大约需要{sum(p['duration'] for p in protocol['timeline'])}个月完成，
需要您配合完成以下检查：
{', '.join(protocol['study_procedures']['baseline'][:5])}等。

参与本研究的风险包括：{'; '.join(protocol['ethics']['risk_benefit']['risks'])}。

参与本研究的获益包括：{'; '.join(protocol['ethics']['risk_benefit']['benefits'])}。

您的所有资料都将严格保密，研究结果将用于科学发表。
您有权在任何时候退出研究，这不会影响您的正常治疗。
"""

    def print_summary_report(self):
        """打印摘要报告"""
        if not self.current_analysis:
            print("请先运行 run_full_workflow()")
            return

        analysis = self.current_analysis

        print("\n\n" + "="*70)
        print("📊 Medical Research AI - 分析报告摘要")
        print("="*70)

        print(f"\n研究主题: {analysis['topic']}")
        print(f"目标人群: {analysis['population']}")

        print(f"\n{'─'*70}")
        print("📚 文献检索结果")
        print(f"{'─'*70}")
        lit = analysis['literature_search']
        print(f"检索文献数: {lit['total_found']} 篇")
        print(f"获取摘要: {lit['abstracts_obtained']} 篇")
        print(f"发表年份: {lit['publication_trend'].get('year_range', 'N/A')}")
        print(f"近5年发表: {lit['publication_trend'].get('recent_5_years', 0)} 篇")

        print(f"\n研究类型分布:")
        for st, count in lit['study_types'].items():
            if count > 0:
                print(f"  • {st}: {count} 篇 ({count/lit['abstracts_obtained']*100:.1f}%)")

        print(f"\n{'─'*70}")
        print("🔍 识别的研究空白")
        print(f"{'─'*70}")
        for i, gap in enumerate(analysis['gap_analysis']['gaps_identified'][:5], 1):
            print(f"\n{i}. [{gap['type']}] {gap['gap']}")
            print(f"   证据: {gap['evidence']}")
            print(f"   潜力: {gap['potential']}")

        print(f"\n{'─'*70}")
        print("💡 推荐研究方向 (按创新性排序)")
        print(f"{'─'*70}")
        for i, direction in enumerate(analysis['research_directions'][:5], 1):
            print(f"\n{i}. {direction['title']}")
            print(f"   设计: {direction['design']}")
            print(f"   创新性: {direction['innovation_score']}")
            print(f"   可行性: {direction['feasibility']}")
            print(f"   描述: {direction['description']}")

        print(f"\n{'─'*70}")
        print("📋 详细研究方案 (Top 3)")
        print(f"{'─'*70}")
        for i, protocol in enumerate(analysis['detailed_protocols'], 1):
            print(f"\n【方案 {i}】{protocol['basic_info']['title']}")
            print(f"  设计类型: {protocol['basic_info']['study_design']}")
            print(f"  研究人群: {protocol['basic_info']['population']}")
            print(f"  主要终点: {protocol['endpoints']['primary_endpoint']}")
            print(f"  样本量: {protocol['sample_size']['with_attrition']}")
            print(f"  创新性: {protocol['innovation_score']}")
            print(f"  创新点: {protocol['innovation']}")

        print(f"\n{'─'*70}")
        print("⚖️  伦理材料")
        print(f"{'─'*70}")
        print("已生成以下材料:")
        for i, ethics in enumerate(analysis['ethics_materials'], 1):
            print(f"  {i}. 方案{i}: 伦理申请表、知情同意书")

        print("\n" + "="*70)
        print("✅ 报告生成完成")
        print("="*70)

    def save_to_json(self, filepath: str = None):
        """保存分析结果到 JSON 文件"""
        if not self.current_analysis:
            print("请先运行 run_full_workflow()")
            return

        if filepath is None:
            topic = self.current_analysis['topic']
            filepath = f"research_analysis_{topic.replace(' ', '_')}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_analysis, f, ensure_ascii=False, indent=2)

        print(f"\n💾 分析结果已保存至: {filepath}")

    def generate_markdown_report(self, filepath: str = None) -> str:
        """生成 Markdown 格式报告"""
        if not self.current_analysis:
            print("请先运行 run_full_workflow()")
            return ""

        analysis = self.current_analysis
        topic = analysis['topic']

        md_content = f"""# {topic} - 科研项目自动化分析报告

**生成时间**: {self._get_current_time()}
**目标人群**: {analysis['population']}

---

## 📚 一、文献检索结果

### 1.1 检索概况

| 项目 | 数值 |
|------|------|
| 检索文献数 | {analysis['literature_search']['total_found']} 篇 |
| 获取摘要数 | {analysis['literature_search']['abstracts_obtained']} 篇 |
| 发表年份范围 | {analysis['literature_search']['publication_trend'].get('year_range', 'N/A')} |
| 近5年发表 | {analysis['literature_search']['publication_trend'].get('recent_5_years', 0)} 篇 |

### 1.2 研究类型分布

"""

        # 研究类型表格
        total = analysis['literature_search']['abstracts_obtained']
        for st, count in analysis['literature_search']['study_types'].items():
            if count > 0:
                md_content += f"- **{st}**: {count} 篇 ({count/total*100:.1f}%)\n"

        md_content += f"""

---

## 🔍 二、研究空白分析

共识别 **{analysis['gap_analysis']['total_gaps']}** 个研究空白：

"""

        for i, gap in enumerate(analysis['gap_analysis']['gaps_identified'], 1):
            md_content += f"""
### {i}. {gap['gap']}

- **类型**: {gap['type']}
- **证据**: {gap['evidence']}
- **研究潜力**: {gap['potential']}
"""

        md_content += """

---

## 💡 三、推荐研究方向

"""

        for i, direction in enumerate(analysis['research_directions'], 1):
            md_content += f"""
### {i}. {direction['title']}

- **研究设计**: {direction['design']}
- **目标人群**: {direction.get('population', '成人')}
- **创新性**: {direction['innovation_score']}
- **可行性**: {direction['feasibility']}
- **研究描述**: {direction['description']}
- **创新点**: {direction['innovation']}
"""

        md_content += """

---

## 📋 四、详细研究方案

"""

        for i, protocol in enumerate(analysis['detailed_protocols'], 1):
            md_content += f"""
### 方案 {i}: {protocol['basic_info']['title']}

**基本信息**
- 研究设计: {protocol['basic_info']['study_design']}
- 研究人群: {protocol['basic_info']['population']}
- 研究中心: {protocol['basic_info']['research_center']}

**研究目的**
- 主要目的: {protocol['objectives']['primary']}

**研究终点**
- 主要终点: {protocol['endpoints']['primary_endpoint']}
- 次要终点: {', '.join(protocol['endpoints']['secondary_endpoints'][:3])}

**样本量**
- 计算样本量: {protocol['sample_size'].get('calculated_n', 'N/A')}
- 考虑失访: {protocol['sample_size'].get('with_attrition', 'N/A')}

**纳入标准**
"""
            for criteria in protocol['inclusion_exclusion']['inclusion'][:5]:
                md_content += f"- {criteria}\n"

            md_content += "**排除标准**\n"
            for criteria in protocol['inclusion_exclusion']['exclusion'][:5]:
                md_content += f"- {criteria}\n"

        md_content += """

---

## ⚖️ 五、伦理申请材料

已生成以下材料，可用于伦理委员会申请：
- 伦理申请表
- 知情同意书模板
- 研究方案摘要

---

*本报告由 Medical Research AI 自动生成，建议由专业研究人员审核后使用。*
"""

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"📄 Markdown 报告已保存至: {filepath}")

        return md_content

    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日 %H:%M")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Medical Research AI - 医学科研全流程自动化")
    parser.add_argument("--topic", required=True, help="研究主题（如：干眼症、近视）")
    parser.add_argument("--keywords", nargs="+", required=True, help="检索关键词")
    parser.add_argument("--mesh", nargs="*", help="MeSH 词")
    parser.add_argument("--population", default="成人", help="目标人群")
    parser.add_argument("--max-papers", type=int, default=500, help="最大检索文献数")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    # 运行分析
    ai = MedicalResearchAI()
    result = ai.run_full_workflow(
        topic=args.topic,
        keywords=args.keywords,
        mesh_terms=args.mesh,
        population=args.population,
        max_papers=args.max_papers
    )

    # 打印报告
    ai.print_summary_report()

    # 保存结果
    if args.output:
        ai.save_to_json(args.output)
        md_path = args.output.replace('.json', '.md')
        ai.generate_markdown_report(md_path)


if __name__ == "__main__":
    # 示例运行
    if len(sys.argv) == 1:
        print("Medical Research AI - 医学科研全流程自动化")
        print("\n示例: 分析干眼症与屏幕时间的关系")
        print("-" * 50)

        ai = MedicalResearchAI()
        result = ai.run_full_workflow(
            topic="干眼症与屏幕时间",
            keywords=["dry eye", "screen time", "digital device", "computer vision syndrome"],
            mesh_terms=["Dry Eye Syndromes"],
            population="成人",
            max_papers=100  # 示例用少量文献
        )

        ai.print_summary_report()
        ai.save_to_json()
        ai.generate_markdown_report()

    else:
        main()
