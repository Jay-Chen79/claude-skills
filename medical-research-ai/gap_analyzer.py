#!/usr/bin/env python3
"""
Gap 分析器 - 识别研究空白，评估创新性
"""

import re
from typing import List, Dict, Tuple
from collections import defaultdict, Counter


class GapAnalyzer:
    """研究空白分析器"""

    def __init__(self, literature_summaries: List[Dict]):
        """
        Args:
            literature_summaries: 文献摘要列表（来自 PubMedSearcher.fetch_summaries）
        """
        self.summaries = literature_summaries
        self.analysis = self._perform_deep_analysis()

    def _perform_deep_analysis(self) -> Dict:
        """执行深度文献分析"""
        return {
            "population_analysis": self._analyze_populations(),
            "design_analysis": self._analyze_designs(),
            "outcome_analysis": self._analyze_outcomes(),
            "intervention_analysis": self._analyze_interventions(),
            "followup_analysis": self._analyze_followup(),
            "methodology_trends": self._analyze_methodology_trends(),
        }

    def _analyze_populations(self) -> Dict:
        """分析研究人群"""
        age_groups = defaultdict(list)
        sample_sizes = []
        conditions = defaultdict(list)

        for s in self.summaries:
            title = s.get("title", "").lower()
            abstract = s.get("abstract", "").lower()

            # 年龄组识别
            if any(w in title + abstract for w in ["pediatric", "children", "child", "adolescent", "teenager", "青少年", "儿童"]):
                age_groups["儿童青少年"].append(s["pmid"])
            elif any(w in title + abstract for w in ["elderly", "older", "aging", "senior", "老年"]):
                age_groups["老年人"].append(s["pmid"])
            else:
                age_groups["成人"].append(s["pmid"])

            # 样本量提取（从摘要中提取数字）
            numbers = re.findall(r"n\s*=\s*(\d+)", abstract)
            if numbers:
                sample_sizes.append(int(numbers[0]))

            # 疾病状况识别
            if "healthy" in title + abstract or "control" in abstract:
                conditions["健康对照"].append(s["pmid"])

        return {
            "age_distribution": {k: len(v) for k, v in age_groups.items()},
            "sample_size_range": f"{min(sample_sizes) if sample_sizes else 0}-{max(sample_sizes) if sample_sizes else 0}",
            "median_sample_size": sorted(sample_sizes)[len(sample_sizes)//2] if sample_sizes else 0,
        }

    def _analyze_designs(self) -> Dict:
        """分析研究设计"""
        designs = defaultdict(list)

        for s in self.summaries:
            pubtypes = s.get("publication_types", [])
            title = s.get("title", "").lower()
            abstract = s.get("abstract", "").lower()

            for pt in pubtypes:
                pt_lower = pt.lower()
                if "randomized" in pt_lower and "clinical trial" in pt_lower:
                    designs["RCT"].append(s["pmid"])
                elif "cohort" in pt_lower:
                    designs["队列研究"].append(s["pmid"])
                elif "case-control" in pt_lower:
                    designs["病例对照研究"].append(s["pmid"])
                elif "cross-sectional" in pt_lower:
                    designs["横断面研究"].append(s["pmid"])
                elif "case series" in pt_lower:
                    designs["病例系列"].append(s["pmid"])
                elif "review" in pt_lower:
                    designs["综述"].append(s["pmid"])

        return dict(designs)

    def _analyze_outcomes(self) -> Dict:
        """分析结局指标"""
        # 眼科常见指标
        ophthalmology_outcomes = {
            "视力相关": ["visual acuity", "va", "bcva", "logmar", "snellen", "视力"],
            "眼压": ["iop", "intraocular pressure", "眼压", "tonometry"],
            "屈光": ["refraction", "sphere", "cylinder", "se", "屈光", "等效球镜"],
            "泪液": ["tear break-up time", "tbu", "schirmer", "泪膜", "泪液", "干眼"],
            "角膜": ["corneal", "topography", "pachymetry", "角膜", "厚度", "地形图"],
            "视网膜": ["retina", "oct", "thickness", "macula", "视网膜", "黄斑", "OCT"],
            "生活质量": ["quality of life", "qol", "questionnaire", "问卷", "生活质量"],
        }

        outcome_usage = defaultdict(list)

        for s in self.summaries:
            abstract = s.get("abstract", "").lower()
            title = s.get("title", "").lower()
            text = title + " " + abstract

            for category, keywords in ophthalmology_outcomes.items():
                if any(kw in text for kw in keywords):
                    outcome_usage[category].append(s["pmid"])

        return {k: len(set(v)) for k, v in outcome_usage.items()}

    def _analyze_interventions(self) -> Dict:
        """分析干预措施"""
        interventions = defaultdict(list)

        for s in self.summaries:
            abstract = s.get("abstract", "").lower()
            title = s.get("title", "").lower()
            text = title + " " + abstract

            # 手术干预
            if any(w in text for w in ["surgery", "surgical", "operat", "手术", "植入"]):
                interventions["手术干预"].append(s["pmid"])

            # 药物干预
            if any(w in text for w in ["medication", "drug", "eye drop", "ointment", "药物", "眼药水", "眼膏"]):
                interventions["药物治疗"].append(s["pmid"])

            # 物理治疗
            if any(w in text for w in ["laser", "phototherapy", "ipl", "thermal", "激光", "热疗"]):
                interventions["物理治疗"].append(s["pmid"])

            # 生活方式
            if any(w in text for w in ["exercise", "diet", "sleep", "screen time", "运动", "饮食", "睡眠", "屏幕"]):
                interventions["生活方式"].append(s["pmid"])

        return {k: len(set(v)) for k, v in interventions.items()}

    def _analyze_followup(self) -> Dict:
        """分析随访时间"""
        followup_durations = []

        for s in self.summaries:
            abstract = s.get("abstract", "").lower()

            # 提取随访时间
            patterns = [
                r"(\d+)\s*month\s*follow-up",
                r"follow-up\s*of\s*(\d+)\s*month",
                r"(\d+)-month",
                r"随访\s*(\d+)\s*月",
            ]

            for pattern in patterns:
                matches = re.findall(pattern, abstract)
                if matches:
                    followup_durations.extend([int(m) for m in matches])

        if not followup_durations:
            return {"message": "未提取到明确的随访时间信息"}

        return {
            "min_months": min(followup_durations),
            "max_months": max(followup_durations),
            "median_months": sorted(followup_durations)[len(followup_durations)//2],
            "long_term_studies": sum(1 for d in followup_durations if d >= 12),
        }

    def _analyze_methodology_trends(self) -> Dict:
        """分析方法学趋势"""
        recent = [s for s in self.summaries if self._is_recent(s.get("pubdate", ""), years=3)]
        older = [s for s in self.summaries if not self._is_recent(s.get("pubdate", ""), years=3)]

        return {
            "recent_studies": len(recent),
            "recent_vs_older_ratio": f"{len(recent)}/{len(older)}" if older else f"{len(recent)}/0",
        }

    def _is_recent(self, pubdate: str, years: int = 3) -> bool:
        """判断是否是最近几年的文献"""
        from datetime import datetime
        year_match = re.search(r"(\d{4})", pubdate)
        if year_match:
            pub_year = int(year_match.group(1))
            current_year = datetime.now().year
            return pub_year >= current_year - years
        return False

    def identify_gaps(self) -> List[Dict]:
        """识别研究空白"""
        gaps = []

        # 人群空白
        pop_analysis = self.analysis["population_analysis"]
        age_dist = pop_analysis["age_distribution"]

        if age_dist.get("儿童青少年", 0) < age_dist.get("成人", 0) * 0.2:
            gaps.append({
                "type": "研究人群",
                "gap": "儿童青少年群体研究不足",
                "evidence": f"成人研究 {age_dist.get('成人', 0)} 篇 vs 儿童青少年 {age_dist.get('儿童青少年', 0)} 篇",
                "potential": "★★★★★",
            })

        if age_dist.get("老年人", 0) < age_dist.get("成人", 0) * 0.3:
            gaps.append({
                "type": "研究人群",
                "gap": "老年人群研究不足",
                "evidence": f"成人研究 {age_dist.get('成人', 0)} 篇 vs 老年人 {age_dist.get('老年人', 0)} 篇",
                "potential": "★★★★☆",
            })

        # 研究设计空白
        design_analysis = self.analysis["design_analysis"]
        rct_count = len(design_analysis.get("RCT", []))
        observational = sum(len(v) for k, v in design_analysis.items()
                           if k in ["队列研究", "横断面研究", "病例对照研究"])

        if rct_count < observational * 0.2:
            gaps.append({
                "type": "研究设计",
                "gap": "干预性 RCT 研究缺乏",
                "evidence": f"RCT 仅 {rct_count} 篇，观察性研究 {observational} 篇",
                "potential": "★★★★★",
            })

        # 随访时间空白
        followup = self.analysis["followup_analysis"]
        if "median_months" in followup and followup["median_months"] < 12:
            gaps.append({
                "type": "随访时间",
                "gap": "长期随访数据缺乏",
                "evidence": f"中位随访时间仅 {followup['median_months']} 个月",
                "potential": "★★★★☆",
            })

        # 结局指标空白
        outcome_analysis = self.analysis["outcome_analysis"]
        low_usage_outcomes = [k for k, v in outcome_analysis.items() if v < len(self.summaries) * 0.1]

        for outcome in low_usage_outcomes:
            gaps.append({
                "type": "结局指标",
                "gap": f"{outcome}相关研究不足",
                "evidence": f"仅 {outcome_analysis[outcome]} 篇文献涉及",
                "potential": "★★★☆☆",
            })

        # 干预措施空白
        intervention_analysis = self.analysis["intervention_analysis"]
        intervention_types = ["手术干预", "药物治疗", "物理治疗", "生活方式"]

        for it in intervention_types:
            if intervention_analysis.get(it, 0) < len(self.summaries) * 0.15:
                gaps.append({
                    "type": "干预措施",
                    "gap": f"{it}相关研究不足",
                    "evidence": f"仅 {intervention_analysis.get(it, 0)} 篇文献涉及",
                    "potential": "★★★☆☆",
                })

        return sorted(gaps, key=lambda x: x["potential"], reverse=True)

    def generate_research_directions(self, topic: str) -> List[Dict]:
        """基于 gap 生成研究方向"""
        gaps = self.identify_gaps()
        directions = []

        # 为每个 gap 生成对应研究方向
        for gap in gaps[:5]:  # 取 top 5 gaps
            direction = self._create_direction_from_gap(gap, topic)
            directions.append(direction)

        return directions

    def _create_direction_from_gap(self, gap: Dict, topic: str) -> Dict:
        """将 gap 转换为研究方向"""
        gap_type = gap["type"]
        gap_desc = gap["gap"]

        # 根据不同类型生成不同的研究设计
        if gap_type == "研究人群":
            target_pop = "儿童青少年" if "儿童" in gap_desc else "老年人"
            return {
                "title": f"{topic}在{target_pop}群体中的临床研究",
                "design": "队列研究",
                "population": target_pop,
                "innovation": gap_desc,
                "innovation_score": gap["potential"],
                "feasibility": "★★★☆☆",
                "description": f"针对{target_pop}这一特殊群体，系统评估{topic}的流行病学特征、危险因素和临床结局",
            }

        elif gap_type == "研究设计":
            return {
                "title": f"{topic}的随机对照临床试验",
                "design": "RCT",
                "population": "成人",
                "innovation": gap_desc,
                "innovation_score": gap["potential"],
                "feasibility": "★★☆☆☆",
                "description": f"通过严格的随机对照设计，评估干预措施对{topic}的效果",
            }

        elif gap_type == "随访时间":
            return {
                "title": f"{topic}的长期预后研究",
                "design": "前瞻性队列研究",
                "population": "成人",
                "innovation": gap_desc,
                "innovation_score": gap["potential"],
                "feasibility": "★★★★☆",
                "description": f"对{topic}患者进行 5 年以上的长期随访，评估远期结局和并发症",
            }

        elif gap_type == "结局指标":
            outcome_name = gap_desc.replace("相关研究不足", "")
            return {
                "title": f"基于{outcome_name}评估{topic}的新方法",
                "design": "诊断准确性研究",
                "population": "成人",
                "innovation": gap_desc,
                "innovation_score": gap["potential"],
                "feasibility": "★★★★☆",
                "description": f"引入{outcome_name}作为新的评估指标，提高诊断准确性",
            }

        else:  # 干预措施
            intervention_name = gap_desc.replace("相关研究不足", "")
            return {
                "title": f"{intervention_name}干预{topic}的疗效研究",
                "design": "RCT",
                "population": "成人",
                "innovation": gap_desc,
                "innovation_score": gap["potential"],
                "feasibility": "★★★☆☆",
                "description": f"探索{intervention_name}作为新的干预手段，评估其对{topic}的疗效",
            }

    def print_summary(self):
        """打印分析摘要"""
        print("\n" + "="*60)
        print("📊 文献深度分析报告")
        print("="*60)

        print("\n👥 研究人群分析:")
        for k, v in self.analysis["population_analysis"]["age_distribution"].items():
            print(f"  • {k}: {v} 篇")

        print("\n🔬 研究设计分析:")
        for k, v in self.analysis["design_analysis"].items():
            print(f"  • {k}: {len(v)} 篇")

        print("\n📏 结局指标分析:")
        for k, v in self.analysis["outcome_analysis"].items():
            print(f"  • {k}: {v} 篇")

        print("\n💉 干预措施分析:")
        for k, v in self.analysis["intervention_analysis"].items():
            print(f"  • {k}: {v} 篇")

        print("\n⏱️  随访时间分析:")
        followup = self.analysis["followup_analysis"]
        if "median_months" in followup:
            print(f"  • 中位随访时间: {followup['median_months']} 个月")
            print(f"  • 范围: {followup['min_months']}-{followup['max_months']} 个月")
        else:
            print(f"  • {followup.get('message', '无数据')}")

        print("\n🔍 识别的研究空白:")
        gaps = self.identify_gaps()
        for i, gap in enumerate(gaps, 1):
            print(f"\n  {i}. [{gap['type']}] {gap['gap']}")
            print(f"     证据: {gap['evidence']}")
            print(f"     潜力: {gap['potential']}")


if __name__ == "__main__":
    # 示例用法
    from pubmed_search import PubMedSearcher

    searcher = PubMedSearcher()
    query = searcher.build_ophthalmology_query(
        keywords=["dry eye", "screen time"],
    )

    pmids = searcher.search(query, max_results=50)
    summaries = searcher.fetch_summaries(pmids)

    analyzer = GapAnalyzer(summaries)
    analyzer.print_summary()

    print("\n💡 生成的研究方向:")
    directions = analyzer.generate_research_directions("干眼症与屏幕时间")
    for i, d in enumerate(directions, 1):
        print(f"\n{i}. {d['title']}")
        print(f"   设计: {d['design']}")
        print(f"   创新性: {d['innovation_score']}")
        print(f"   可行性: {d['feasibility']}")
        print(f"   描述: {d['description']}")
