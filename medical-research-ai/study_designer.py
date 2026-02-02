#!/usr/bin/env python3
"""
研究设计生成器 - 基于分析结果生成详细研究方案
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class StudyDesigner:
    """研究设计方案生成器"""

    # 眼科常用测量指标库
    OPHTHALMOLOGY_OUTCOMES = {
        "干眼症": {
            "primary": [
                "泪膜破裂时间 (TBUT)",
                "Schirmer I 试验",
                "角膜荧光素染色评分",
                "眼表疾病指数 (OSDI 问卷)",
            ],
            "secondary": [
                "泪液渗透压",
                "泪河高度",
                "睑板腺形态评估",
                "结膜充血评分",
                "视力相关生活质量问卷 (NEI-VFQ-25)",
            ]
        },
        "近视": {
            "primary": [
                "等效球镜 (SE)",
                "眼轴长度 (AL)",
                "角膜曲率 (K)",
            ],
            "secondary": [
                "最佳矫正视力 (BCVA)",
                "脉络膜厚度 (OCT)",
                "调节力",
                "集合功能",
                "户外活动时间",
            ]
        },
        "青光眼": {
            "primary": [
                "眼压 (IOP)",
                "视野指数 (MD, PSD)",
                "视网膜神经纤维层厚度 (RNFL)",
            ],
            "secondary": [
                "视乳头结构参数",
                "角膜中央厚度",
                "视力",
                "生活质量",
            ]
        },
        "白内障": {
            "primary": [
                "最佳矫正视力 (BCVA)",
                "晶状体混浊分级 (LOCS III)",
            ],
            "secondary": [
                "对比敏感度",
                "眩光测试",
                "生活质量问卷 (Catquest-9SF)",
                "手术并发症率",
            ]
        },
        "糖尿病视网膜病变": {
            "primary": [
                "DR 分期 (ETDRS 标准)",
                "黄斑中心凹厚度 (CMT, OCT)",
                "最佳矫正视力 (BCVA)",
            ],
            "secondary": [
                "微血管瘤数量",
                "出血面积",
                "硬性渗出范围",
                "血管无灌注区面积 (FA)",
            ]
        },
    }

    # 样本量计算参数
    SAMPLE_SIZE_PARAMETERS = {
        "队列研究": {
            "formula": "n = (Zα+Zβ)² × 2×p×(1-p) / d²",
            "default": {
                "alpha": 0.05,
                "power": 0.80,
                "p": 0.5,  # 预期事件发生率
                "d": 0.15,  # 最小检测差异
            }
        },
        "RCT": {
            "formula": "n = 2×(Zα+Zβ)² × σ² / Δ²",
            "default": {
                "alpha": 0.05,
                "power": 0.80,
                "sigma": 1.0,  # 标准差
                "delta": 0.5,  # 组间差异
            }
        },
        "横断面研究": {
            "formula": "n = Z² × p × (1-p) / d²",
            "default": {
                "alpha": 0.05,
                "p": 0.5,  # 预期患病率
                "d": 0.05,  # 精度
            }
        },
        "病例对照研究": {
            "formula": "n = (Zα+Zβ)² × (p1×(1-p1) + p2×(1-p2)) / (p1-p2)²",
            "default": {
                "alpha": 0.05,
                "power": 0.80,
                "or": 2.0,  # 预期 OR 值
                "exposure": 0.2,  # 暴露率
            }
        },
        "诊断准确性研究": {
            "formula": "n = (Zα+Zβ)² × Se×(1-Se) / d²",
            "default": {
                "alpha": 0.05,
                "power": 0.80,
                "sensitivity": 0.85,  # 预期灵敏度
                "d": 0.10,  # 精度
            }
        },
    }

    # 纳入排除标准模板
    INCLUSION_EXCLUSION_TEMPLATES = {
        "成人": {
            "inclusion": [
                "年龄 ≥ 18 岁",
                "理解并签署知情同意书",
                "能够配合完成各项检查",
            ],
            "exclusion": [
                "妊娠或哺乳期妇女",
                "伴有严重全身性疾病（如未控制的糖尿病、高血压）",
                "有眼部手术史",
                "无法配合研究者",
            ]
        },
        "儿童青少年": {
            "inclusion": [
                "年龄 6-18 岁",
                "监护人签署知情同意书",
                "患儿本人签署知情同意书（如≥12岁）",
                "能够配合完成各项检查",
            ],
            "exclusion": [
                "伴有先天性眼部异常",
                "有眼部外伤史",
                "伴有全身性疾病影响眼部",
                "正在参与其他临床研究",
            ]
        },
        "老年人": {
            "inclusion": [
                "年龄 ≥ 65 岁",
                "理解并签署知情同意书（或监护人签署）",
                "生活能够基本自理",
            ],
            "exclusion": [
                "伴有严重认知障碍",
                "预期寿命 < 1 年",
                "伴有严重全身疾病",
                "长期卧床",
            ]
        },
    }

    def __init__(self, topic: str, study_design: str, population: str):
        """
        Args:
            topic: 研究主题（如：干眼症、近视、青光眼）
            study_design: 研究设计类型（如：队列研究、RCT、横断面研究）
            population: 研究人群（如：成人、儿童青少年、老年人）
        """
        self.topic = topic
        self.study_design = study_design
        self.population = population
        self.outcomes = self._get_outcomes_for_topic(topic)

    def _get_outcomes_for_topic(self, topic: str) -> Dict:
        """获取研究主题对应的结局指标"""
        for key, value in self.OPHTHALMOLOGY_OUTCOMES.items():
            if key in topic or topic in key:
                return value
        # 默认返回通用指标
        return {
            "primary": ["视力", "症状评分"],
            "secondary": ["生活质量", "满意度"],
        }

    def calculate_sample_size(self, **kwargs) -> Dict:
        """计算样本量"""
        params = self.SAMPLE_SIZE_PARAMETERS.get(self.study_design, {})
        if not params:
            return {"note": "暂不支持该研究设计的样本量计算"}

        # 使用默认参数或用户提供的参数
        calculation_params = params["default"].copy()
        calculation_params.update(kwargs)

        # 简化计算（实际应用中应使用统计软件）
        if self.study_design == "横断面研究":
            n = 384  # 常用经验值，p=0.5, d=0.05
        elif self.study_design == "队列研究":
            n = 400  # 经验值
        elif self.study_design == "RCT":
            n = 128  # 每组，经验值
            n = n * 2  # 两组
        elif self.study_design == "病例对照研究":
            n = 200  # 每组，经验值
            n = n * 2  # 病例+对照
        elif self.study_design == "诊断准确性研究":
            n = 150  # 经验值（病例+对照）
        else:
            n = 200  # 默认值

        # 考虑失访率
        attrition_rate = 0.15
        final_n = int(n * (1 + attrition_rate))

        return {
            "calculated_n": n,
            "with_attrition": final_n,
            "attrition_rate": f"{attrition_rate*100}%",
            "parameters_used": calculation_params,
            "note": "建议使用 PASS 或 G*Power 进行精确计算",
        }

    def generate_inclusion_exclusion(self) -> Dict:
        """生成纳入排除标准"""
        base = self.INCLUSION_EXCLUSION_TEMPLATES.get(self.population,
                                                      self.INCLUSION_EXCLUSION_TEMPLATES["成人"])

        # 根据研究主题添加特定标准
        topic_specific = self._get_topic_specific_criteria()

        inclusion = base["inclusion"] + topic_specific.get("inclusion", [])
        exclusion = base["exclusion"] + topic_specific.get("exclusion", [])

        return {
            "inclusion": inclusion,
            "exclusion": exclusion,
        }

    def _get_topic_specific_criteria(self) -> Dict:
        """获取研究主题特定的纳入排除标准"""
        criteria = {
            "干眼症": {
                "inclusion": [
                    "符合干眼症诊断标准",
                    "OSDI 评分 ≥ 23 分",
                ],
                "exclusion": [
                    "正在使用人工泪液以外的眼科药物",
                    "有眼部活动性炎症",
                    "近期有眼部手术计划",
                ]
            },
            "近视": {
                "inclusion": [
                    "等效球镜 ≤ -6.00D（高度近视）或 -0.50D ~ -6.00D（中低度近视）",
                ],
                "exclusion": [
                    "有病理性近视改变",
                    "有角膜屈光手术史",
                    "伴有弱视或斜视",
                ]
            },
            "青光眼": {
                "inclusion": [
                    "符合青光眼诊断标准",
                    "眼压 ≤ 21 mmHg（治疗后）",
                ],
                "exclusion": [
                    "晚期青光眼（MD < -15dB）",
                    "有其他视神经疾病",
                ]
            },
            "白内障": {
                "inclusion": [
                    "LOCS III 分级 ≥ NO2 或 NC2",
                    "BCVA < 0.5（LogMAR > 0.3）",
                ],
                "exclusion": [
                    "伴有其他影响视力的眼病",
                    "有玻璃体视网膜手术史",
                ]
            },
        }

        for key, value in criteria.items():
            if key in self.topic or self.topic in key:
                return value

        return {"inclusion": [], "exclusion": []}

    def generate_statistical_plan(self) -> Dict:
        """生成统计分析计划"""
        plans = {
            "队列研究": {
                "descriptive": "描述性分析：均数±标准差或中位数（四分位数）描述连续变量，频数（百分比）描述分类变量",
                "univariate": "单因素分析：t检验、Mann-Whitney U检验或卡方检验",
                "multivariate": "多因素分析：Cox比例风险模型或Logistic回归分析",
                "adjustment": "调整年龄、性别、基线严重程度等混杂因素",
            },
            "RCT": {
                "primary_analysis": "主要终点：意向性分析（ITT），组间比较采用t检验或Mann-Whitney U检验",
                "secondary_analysis": "次要终点：重复测量方差分析或混合效应模型",
                "subgroup": "亚组分析：按年龄、基线严重程度分层",
                "safety": "安全性分析：描述不良事件发生率",
            },
            "横断面研究": {
                "descriptive": "描述性分析：计算患病率及其95%置信区间",
                "association": "关联性分析：Logistic回归分析危险因素",
                "correlation": "相关性分析：Pearson或Spearman相关分析",
            },
            "病例对照研究": {
                "matching": "匹配因素：年龄（±3岁）、性别",
                "univariate": "单因素分析：比较病例组和对照组的暴露差异",
                "multivariate": "多因素分析：条件Logistic回归计算OR值及95%CI",
            },
            "诊断准确性研究": {
                "primary_analysis": "主要终点：计算灵敏度、特异度、阳性预测值、阴性预测值",
                "accuracy": "准确性评估：绘制ROC曲线，计算AUC及其95%CI",
                "comparison": "比较分析：与金标准一致性检验（Kappa值）",
                "sample_size": "样本量：基于预期灵敏度和特异度计算",
            },
        }

        plan = plans.get(self.study_design, {}).copy()

        plan["statistical_software"] = "SAS 9.4 或 R 4.0+"
        plan["significance_level"] = "α = 0.05（双侧检验）"
        plan["missing_data"] = "缺失数据处理：多重插补法或完整案例分析"

        return plan

    def generate_timeline(self, total_months: int = 24) -> List[Dict]:
        """生成研究时间表"""
        phases = []

        if self.study_design == "RCT":
            phases = [
                {"phase": "准备阶段", "duration": 3, "activities": [
                    "方案制定与伦理审批",
                    "CRF表设计",
                    "研究者培训",
                    "中心启动",
                ]},
                {"phase": "入组阶段", "duration": total_months // 3, "activities": [
                    "受试者筛选",
                    "知情同意",
                    "基线评估",
                    "随机分组",
                ]},
                {"phase": "干预与随访", "duration": total_months // 3, "activities": [
                    "干预实施",
                    "定期随访",
                    "安全性监测",
                ]},
                {"phase": "数据分析与报告", "duration": 3, "activities": [
                    "数据清理",
                    "统计分析",
                    "报告撰写",
                ]},
            ]
        else:
            phases = [
                {"phase": "准备阶段", "duration": 3, "activities": [
                    "方案制定与伦理审批",
                    "研究团队培训",
                ]},
                {"phase": "数据收集", "duration": total_months - 6, "activities": [
                    "受试者招募",
                    "基线与随访评估",
                    "质量控制",
                ]},
                {"phase": "数据分析与报告", "duration": 3, "activities": [
                    "数据清理与分析",
                    "论文撰写",
                ]},
            ]

        return phases

    def generate_full_protocol(self) -> Dict:
        """生成完整研究方案"""
        return {
            "basic_info": {
                "title": f"{self.topic}{self.study_design}研究",
                "study_design": self.study_design,
                "population": self.population,
                "research_center": "单中心" if self.study_design in ["横断面研究", "病例对照研究"] else "单中心（可扩展为多中心）",
            },
            "background": {
                "research_question": f"探索{self.topic}在{self.population}群体中的流行病学特征/危险因素/预后",
                "clinical_significance": f"研究结果将有助于{self.population}群体{self.topic}的早期识别、预防和治疗",
            },
            "objectives": {
                "primary": f"评估{self.topic}在{self.population}群体中的患病率/发生率/预后因素",
                "secondary": [
                    f"分析{self.topic}的危险因素",
                    f"探索{self.topic}对生活质量的影响",
                    f"建立{self.topic}的预测模型",
                ],
            },
            "endpoints": {
                "primary_endpoint": self.outcomes["primary"][0] if self.outcomes["primary"] else "主要研究终点",
                "secondary_endpoints": self.outcomes["secondary"],
            },
            "sample_size": self.calculate_sample_size(),
            "inclusion_exclusion": self.generate_inclusion_exclusion(),
            "study_procedures": {
                "screening": ["知情同意", " eligibility评估", "基线资料收集"],
                "baseline": self.outcomes["primary"] + self.outcomes["secondary"][:2],
                "followup": "每3-6个月随访一次，收集终点事件",
            },
            "statistical_analysis": self.generate_statistical_plan(),
            "timeline": self.generate_timeline(),
            "ethics": {
                "ethical_considerations": [
                    "本研究遵循《赫尔辛基宣言》",
                    "需经伦理委员会审批",
                    "所有受试者需签署知情同意书",
                    "受试者可随时退出研究",
                ],
                "risk_benefit": {
                    "risks": [
                        "检查不适：部分眼部检查可能引起轻微不适",
                        "时间成本：每次随访约需1-2小时",
                    ],
                    "benefits": [
                        "获得详细的眼部检查",
                        "及时了解眼部健康状况",
                        "为后续临床实践提供依据",
                    ],
                },
            },
            "quality_control": {
                "training": "研究开始前对所有研究者进行统一培训",
                "monitoring": "定期监查，确保数据质量",
                "auditing": "独立稽查员定期稽查",
            },
        }

    def print_protocol_summary(self):
        """打印方案摘要"""
        protocol = self.generate_full_protocol()

        print("\n" + "="*70)
        print("📋 研究方案摘要")
        print("="*70)

        print(f"\n标题: {protocol['basic_info']['title']}")
        print(f"设计: {protocol['basic_info']['study_design']}")
        print(f"人群: {protocol['basic_info']['population']}")

        print(f"\n研究目的:")
        print(f"  主要目的: {protocol['objectives']['primary']}")
        print(f"  次要目的:")
        for obj in protocol['objectives']['secondary']:
            print(f"    • {obj}")

        print(f"\n主要终点:")
        print(f"  • {protocol['endpoints']['primary_endpoint']}")

        print(f"\n次要终点:")
        for endpoint in protocol['endpoints']['secondary_endpoints']:
            print(f"  • {endpoint}")

        print(f"\n样本量:")
        sample = protocol['sample_size']
        print(f"  • 计算样本量: {sample['calculated_n']}")
        print(f"  • 考虑失访率后: {sample['with_attrition']}")
        print(f"  • 失访率: {sample['attrition_rate']}")

        print(f"\n纳入标准:")
        for i, criteria in enumerate(protocol['inclusion_exclusion']['inclusion'], 1):
            print(f"  {i}. {criteria}")

        print(f"\n排除标准:")
        for i, criteria in enumerate(protocol['inclusion_exclusion']['exclusion'], 1):
            print(f"  {i}. {criteria}")

        print(f"\n研究时间表:")
        for phase in protocol['timeline']:
            print(f"\n  {phase['phase']} ({phase['duration']}个月):")
            for activity in phase['activities']:
                print(f"    • {activity}")


if __name__ == "__main__":
    # 示例用法
    designer = StudyDesigner(
        topic="干眼症",
        study_design="队列研究",
        population="成人"
    )

    designer.print_protocol_summary()

    # 生成完整 JSON
    protocol = designer.generate_full_protocol()
    print("\n\n完整方案 (JSON):")
    print(json.dumps(protocol, indent=2, ensure_ascii=False))
