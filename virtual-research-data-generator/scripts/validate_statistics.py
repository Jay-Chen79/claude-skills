"""
统计验证模块
用于验证生成的数据是否符合预期的统计特性
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果数据类"""
    passed: bool
    metric_name: str
    expected_value: float
    actual_value: float
    tolerance: float
    p_value: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    message: str = ""
    
    def __str__(self):
        status = "✓ 通过" if self.passed else "✗ 未通过"
        return (
            f"{status} | {self.metric_name}: "
            f"预期={self.expected_value:.3f}, 实际={self.actual_value:.3f} "
            f"(容差±{self.tolerance*100:.0f}%)"
        )


class StatisticalValidator:
    """统计验证器"""
    
    def __init__(self, tolerance: float = 0.2):
        """
        初始化验证器
        
        Args:
            tolerance: 效应量容差（默认±20%）
        """
        self.tolerance = tolerance
        self.results: List[ValidationResult] = []
    
    def validate_mean_difference(
        self,
        data: np.ndarray,
        group: np.ndarray,
        expected_diff: float,
        expected_significant: bool = True,
        alpha: float = 0.05
    ) -> ValidationResult:
        """
        验证两组均值差异
        
        Args:
            data: 数据数组
            group: 组别变量（0/1）
            expected_diff: 预期均值差（组1-组0）
            expected_significant: 预期是否显著
            alpha: 显著性水平
            
        Returns:
            验证结果
        """
        group0 = data[group == 0]
        group1 = data[group == 1]
        
        actual_diff = np.mean(group1) - np.mean(group0)
        
        # t检验
        t_stat, p_value = stats.ttest_ind(group1, group0)
        
        # 95%置信区间
        se = np.sqrt(np.var(group0)/len(group0) + np.var(group1)/len(group1))
        ci = (actual_diff - 1.96*se, actual_diff + 1.96*se)
        
        # 验证效应量
        diff_ok = self._check_value(actual_diff, expected_diff)
        
        # 验证显著性
        if expected_significant:
            sig_ok = p_value < alpha
        else:
            sig_ok = p_value >= alpha
        
        passed = diff_ok and sig_ok
        
        result = ValidationResult(
            passed=passed,
            metric_name="均值差异",
            expected_value=expected_diff,
            actual_value=actual_diff,
            tolerance=self.tolerance,
            p_value=p_value,
            confidence_interval=ci,
            message=f"t={t_stat:.2f}, p={p_value:.4f}"
        )
        
        self.results.append(result)
        return result
    
    def validate_odds_ratio(
        self,
        outcome: np.ndarray,
        exposure: np.ndarray,
        expected_or: float,
        expected_significant: bool = True,
        alpha: float = 0.05
    ) -> ValidationResult:
        """
        验证比值比
        
        Args:
            outcome: 结局变量（0/1）
            exposure: 暴露变量（0/1）
            expected_or: 预期OR
            expected_significant: 预期是否显著
            alpha: 显著性水平
            
        Returns:
            验证结果
        """
        # 2x2表
        a = np.sum((exposure == 1) & (outcome == 1))
        b = np.sum((exposure == 1) & (outcome == 0))
        c = np.sum((exposure == 0) & (outcome == 1))
        d = np.sum((exposure == 0) & (outcome == 0))
        
        # OR计算
        if b == 0 or c == 0:
            actual_or = np.inf if a * d > 0 else 0
        else:
            actual_or = (a * d) / (b * c)
        
        # log(OR)的标准误
        if a > 0 and b > 0 and c > 0 and d > 0:
            se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
            log_or = np.log(actual_or)
            
            # 95% CI
            ci_log = (log_or - 1.96*se_log_or, log_or + 1.96*se_log_or)
            ci = (np.exp(ci_log[0]), np.exp(ci_log[1]))
            
            # 简单z检验
            z = log_or / se_log_or
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        else:
            ci = (None, None)
            p_value = None
        
        # 验证效应量
        or_ok = self._check_value(actual_or, expected_or)
        
        # 验证显著性
        if p_value is not None:
            if expected_significant:
                sig_ok = p_value < alpha
            else:
                sig_ok = p_value >= alpha
        else:
            sig_ok = False
        
        passed = or_ok and sig_ok
        
        result = ValidationResult(
            passed=passed,
            metric_name="比值比(OR)",
            expected_value=expected_or,
            actual_value=actual_or,
            tolerance=self.tolerance,
            p_value=p_value,
            confidence_interval=ci,
            message=f"OR={actual_or:.2f}, 95%CI=({ci[0]:.2f}, {ci[1]:.2f})" if ci[0] else ""
        )
        
        self.results.append(result)
        return result
    
    def validate_correlation(
        self,
        var1: np.ndarray,
        var2: np.ndarray,
        expected_r: float,
        expected_significant: bool = True,
        alpha: float = 0.05,
        method: str = 'pearson'
    ) -> ValidationResult:
        """
        验证相关系数
        
        Args:
            var1: 变量1
            var2: 变量2
            expected_r: 预期相关系数
            expected_significant: 预期是否显著
            alpha: 显著性水平
            method: 相关系数类型
            
        Returns:
            验证结果
        """
        if method == 'pearson':
            actual_r, p_value = stats.pearsonr(var1, var2)
        elif method == 'spearman':
            actual_r, p_value = stats.spearmanr(var1, var2)
        else:
            raise ValueError(f"不支持的相关类型: {method}")
        
        # Fisher z变换置信区间
        n = len(var1)
        z = np.arctanh(actual_r)
        se = 1 / np.sqrt(n - 3)
        ci_z = (z - 1.96*se, z + 1.96*se)
        ci = (np.tanh(ci_z[0]), np.tanh(ci_z[1]))
        
        # 验证效应量
        r_ok = self._check_value(actual_r, expected_r)
        
        # 验证显著性
        if expected_significant:
            sig_ok = p_value < alpha
        else:
            sig_ok = p_value >= alpha
        
        passed = r_ok and sig_ok
        
        result = ValidationResult(
            passed=passed,
            metric_name=f"{method}相关系数",
            expected_value=expected_r,
            actual_value=actual_r,
            tolerance=self.tolerance,
            p_value=p_value,
            confidence_interval=ci,
            message=f"r={actual_r:.3f}, p={p_value:.4f}"
        )
        
        self.results.append(result)
        return result
    
    def validate_hazard_ratio(
        self,
        time: np.ndarray,
        event: np.ndarray,
        exposure: np.ndarray,
        expected_hr: float,
        expected_significant: bool = True,
        alpha: float = 0.05
    ) -> ValidationResult:
        """
        验证风险比（基于中位数估计）
        
        Args:
            time: 观察时间
            event: 事件指示变量
            exposure: 暴露变量
            expected_hr: 预期HR
            expected_significant: 预期是否显著
            alpha: 显著性水平
            
        Returns:
            验证结果
        """
        # 简化估计：基于事件时间的中位数比
        time0 = time[(exposure == 0) & (event == 1)]
        time1 = time[(exposure == 1) & (event == 1)]
        
        if len(time0) > 0 and len(time1) > 0:
            median0 = np.median(time0)
            median1 = np.median(time1)
            # HR ≈ median0 / median1 (对于指数分布)
            actual_hr = median0 / median1 if median1 > 0 else np.inf
        else:
            actual_hr = 1.0
        
        # Log-rank检验
        try:
            from scipy.stats import mannwhitneyu
            # 使用Mann-Whitney作为简化替代
            stat, p_value = mannwhitneyu(
                time[exposure == 0], time[exposure == 1], 
                alternative='two-sided'
            )
        except:
            p_value = None
        
        # 验证效应量
        hr_ok = self._check_value(actual_hr, expected_hr)
        
        # 验证显著性
        if p_value is not None:
            if expected_significant:
                sig_ok = p_value < alpha
            else:
                sig_ok = p_value >= alpha
        else:
            sig_ok = False
        
        passed = hr_ok and sig_ok
        
        result = ValidationResult(
            passed=passed,
            metric_name="风险比(HR)",
            expected_value=expected_hr,
            actual_value=actual_hr,
            tolerance=self.tolerance,
            p_value=p_value,
            confidence_interval=None,
            message=f"HR≈{actual_hr:.2f} (基于中位数估计)"
        )
        
        self.results.append(result)
        return result
    
    def validate_auc(
        self,
        y_true: np.ndarray,
        y_score: np.ndarray,
        expected_auc: float,
        expected_significant: bool = True
    ) -> ValidationResult:
        """
        验证ROC曲线下面积
        
        Args:
            y_true: 真实标签
            y_score: 预测分数
            expected_auc: 预期AUC
            expected_significant: 预期是否显著（>0.5）
            
        Returns:
            验证结果
        """
        # 计算AUC（Mann-Whitney U统计量）
        pos_scores = y_score[y_true == 1]
        neg_scores = y_score[y_true == 0]
        
        n_pos, n_neg = len(pos_scores), len(neg_scores)
        
        # U统计量
        U = 0
        for pos in pos_scores:
            U += np.sum(pos > neg_scores) + 0.5 * np.sum(pos == neg_scores)
        
        actual_auc = U / (n_pos * n_neg)
        
        # AUC的标准误（DeLong方法简化）
        se = np.sqrt((actual_auc * (1 - actual_auc) + 
                     (n_pos - 1) * (actual_auc / (2 - actual_auc) - actual_auc**2) +
                     (n_neg - 1) * (2 * actual_auc**2 / (1 + actual_auc) - actual_auc**2)) / 
                    (n_pos * n_neg))
        
        ci = (actual_auc - 1.96*se, actual_auc + 1.96*se)
        
        # z检验（H0: AUC = 0.5）
        z = (actual_auc - 0.5) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        # 验证效应量
        auc_ok = self._check_value(actual_auc, expected_auc)
        
        # 验证显著性
        if expected_significant:
            sig_ok = p_value < 0.05 and actual_auc > 0.5
        else:
            sig_ok = p_value >= 0.05 or actual_auc <= 0.5
        
        passed = auc_ok and sig_ok
        
        result = ValidationResult(
            passed=passed,
            metric_name="AUC",
            expected_value=expected_auc,
            actual_value=actual_auc,
            tolerance=self.tolerance,
            p_value=p_value,
            confidence_interval=ci,
            message=f"AUC={actual_auc:.3f}, 95%CI=({ci[0]:.3f}, {ci[1]:.3f})"
        )
        
        self.results.append(result)
        return result
    
    def validate_group_balance(
        self,
        data: np.ndarray,
        group: np.ndarray,
        threshold: float = 0.05
    ) -> ValidationResult:
        """
        验证两组基线平衡（适用于RCT）
        
        Args:
            data: 数据数组
            group: 组别变量
            threshold: p值阈值（应>threshold表示平衡）
            
        Returns:
            验证结果
        """
        group0 = data[group == 0]
        group1 = data[group == 1]
        
        # 如果是连续变量使用t检验
        if len(np.unique(data)) > 10:
            t_stat, p_value = stats.ttest_ind(group0, group1)
            actual_diff = np.mean(group1) - np.mean(group0)
        else:
            # 分类变量使用卡方检验
            contingency = np.array([
                [np.sum(group0 == v) for v in np.unique(data)],
                [np.sum(group1 == v) for v in np.unique(data)]
            ])
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            actual_diff = chi2
        
        passed = p_value > threshold
        
        result = ValidationResult(
            passed=passed,
            metric_name="组间平衡",
            expected_value=0,
            actual_value=actual_diff,
            tolerance=self.tolerance,
            p_value=p_value,
            message=f"p={p_value:.4f} ({'平衡' if passed else '不平衡'})"
        )
        
        self.results.append(result)
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """获取验证摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        return {
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'all_passed': passed == total,
            'results': self.results
        }
    
    def generate_report(self) -> str:
        """生成验证报告"""
        lines = ["# 统计验证报告", ""]
        
        summary = self.get_summary()
        lines.append(f"## 摘要")
        lines.append(f"- 总验证项: {summary['total']}")
        lines.append(f"- 通过: {summary['passed']}")
        lines.append(f"- 未通过: {summary['failed']}")
        lines.append(f"- 通过率: {summary['pass_rate']*100:.1f}%")
        lines.append("")
        
        lines.append("## 详细结果")
        lines.append("")
        
        for result in self.results:
            status = "✓" if result.passed else "✗"
            lines.append(f"### {status} {result.metric_name}")
            lines.append(f"- 预期值: {result.expected_value:.4f}")
            lines.append(f"- 实际值: {result.actual_value:.4f}")
            if result.p_value is not None:
                lines.append(f"- p值: {result.p_value:.4f}")
            if result.confidence_interval and result.confidence_interval[0]:
                lines.append(
                    f"- 95%CI: ({result.confidence_interval[0]:.4f}, "
                    f"{result.confidence_interval[1]:.4f})"
                )
            if result.message:
                lines.append(f"- 备注: {result.message}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _check_value(self, actual: float, expected: float) -> bool:
        """检查值是否在容差范围内"""
        if expected == 0:
            return abs(actual) < self.tolerance
        
        relative_error = abs(actual - expected) / abs(expected)
        return relative_error <= self.tolerance


def validate_effect(
    data: Dict[str, np.ndarray],
    effect_type: str,
    expected_value: float,
    expected_significant: bool = True,
    tolerance: float = 0.2,
    **kwargs
) -> ValidationResult:
    """
    便捷函数：验证效应
    
    Args:
        data: 数据字典
        effect_type: 效应类型 ('mean_diff', 'or', 'hr', 'r', 'auc')
        expected_value: 预期效应值
        expected_significant: 预期是否显著
        tolerance: 容差
        
    Returns:
        验证结果
    """
    validator = StatisticalValidator(tolerance)
    
    if effect_type == 'mean_diff':
        return validator.validate_mean_difference(
            data['outcome'], data['group'], expected_value, expected_significant
        )
    elif effect_type == 'or':
        return validator.validate_odds_ratio(
            data['outcome'], data['exposure'], expected_value, expected_significant
        )
    elif effect_type == 'hr':
        return validator.validate_hazard_ratio(
            data['time'], data['event'], data['exposure'], 
            expected_value, expected_significant
        )
    elif effect_type == 'r':
        return validator.validate_correlation(
            data['var1'], data['var2'], expected_value, expected_significant
        )
    elif effect_type == 'auc':
        return validator.validate_auc(
            data['y_true'], data['y_score'], expected_value, expected_significant
        )
    else:
        raise ValueError(f"不支持的效应类型: {effect_type}")
