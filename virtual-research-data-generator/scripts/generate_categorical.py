"""
分类变量生成模块
用于生成具有指定比例和关联性的分类变量
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Union


class CategoricalVariableGenerator:
    """分类变量生成器"""
    
    def __init__(self, random_seed: Optional[int] = None):
        """
        初始化生成器
        
        Args:
            random_seed: 随机种子，用于结果复现
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def generate_binary(
        self, 
        n: int, 
        probability: float = 0.5,
        labels: Tuple[int, int] = (0, 1)
    ) -> np.ndarray:
        """
        生成二分类变量
        
        Args:
            n: 样本量
            probability: 阳性（标签1）的概率
            labels: 两个类别的标签
            
        Returns:
            生成的分类数组
        """
        data = np.random.binomial(1, probability, n)
        return np.where(data == 1, labels[1], labels[0])
    
    def generate_multinomial(
        self, 
        n: int, 
        categories: List[Union[int, str]],
        probabilities: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        生成多分类变量
        
        Args:
            n: 样本量
            categories: 类别列表
            probabilities: 各类别的概率（如果None则均匀分布）
            
        Returns:
            生成的分类数组
        """
        k = len(categories)
        
        if probabilities is None:
            probabilities = [1/k] * k
        
        # 确保概率和为1
        probabilities = np.array(probabilities)
        probabilities = probabilities / probabilities.sum()
        
        indices = np.random.choice(k, size=n, p=probabilities)
        return np.array([categories[i] for i in indices])
    
    def generate_ordinal(
        self, 
        n: int, 
        levels: int,
        probabilities: Optional[List[float]] = None,
        distribution: str = 'uniform'
    ) -> np.ndarray:
        """
        生成有序分类变量
        
        Args:
            n: 样本量
            levels: 等级数量
            probabilities: 各等级的概率（如果None则使用distribution）
            distribution: 分布类型 ('uniform', 'normal', 'skewed_low', 'skewed_high')
            
        Returns:
            生成的有序分类数组（1到levels）
        """
        if probabilities is not None:
            probabilities = np.array(probabilities)
            probabilities = probabilities / probabilities.sum()
        else:
            if distribution == 'uniform':
                probabilities = np.ones(levels) / levels
            elif distribution == 'normal':
                # 中间等级概率更高
                x = np.linspace(-2, 2, levels)
                probabilities = stats.norm.pdf(x)
                probabilities = probabilities / probabilities.sum()
            elif distribution == 'skewed_low':
                # 低等级概率更高
                probabilities = np.linspace(levels, 1, levels).astype(float)
                probabilities = probabilities / probabilities.sum()
            elif distribution == 'skewed_high':
                # 高等级概率更高
                probabilities = np.linspace(1, levels, levels).astype(float)
                probabilities = probabilities / probabilities.sum()
            else:
                raise ValueError(f"不支持的分布类型: {distribution}")
        
        categories = list(range(1, levels + 1))
        indices = np.random.choice(levels, size=n, p=probabilities)
        return np.array([categories[i] for i in indices])
    
    def generate_count(
        self, 
        n: int, 
        mean: float,
        distribution: str = 'poisson',
        dispersion: float = 1.0,
        max_count: Optional[int] = None
    ) -> np.ndarray:
        """
        生成计数变量
        
        Args:
            n: 样本量
            mean: 均值
            distribution: 分布类型 ('poisson', 'negative_binomial')
            dispersion: 过度离散参数（仅用于负二项分布）
            max_count: 最大值截断
            
        Returns:
            生成的计数数组
        """
        if distribution == 'poisson':
            data = np.random.poisson(mean, n)
        elif distribution == 'negative_binomial':
            # 参数转换：均值=n*p/(1-p)，方差=n*p/(1-p)^2
            # 给定均值和过度离散参数，计算n和p
            var = mean * dispersion
            p = mean / var
            r = mean * p / (1 - p)
            data = np.random.negative_binomial(r, p, n)
        else:
            raise ValueError(f"不支持的分布类型: {distribution}")
        
        if max_count is not None:
            data = np.minimum(data, max_count)
        
        return data
    
    def generate_binary_with_odds_ratio(
        self,
        n: int,
        exposure: np.ndarray,
        baseline_probability: float,
        odds_ratio: float
    ) -> np.ndarray:
        """
        根据暴露变量生成具有指定OR的二分类结局
        
        Args:
            n: 样本量
            exposure: 暴露变量（0/1）
            baseline_probability: 非暴露组的阳性概率
            odds_ratio: 目标比值比
            
        Returns:
            生成的结局变量
        """
        # 计算暴露组的概率
        baseline_odds = baseline_probability / (1 - baseline_probability)
        exposed_odds = baseline_odds * odds_ratio
        exposed_probability = exposed_odds / (1 + exposed_odds)
        
        # 根据暴露状态生成结局
        outcome = np.zeros(n, dtype=int)
        
        unexposed_mask = exposure == 0
        exposed_mask = exposure == 1
        
        outcome[unexposed_mask] = np.random.binomial(
            1, baseline_probability, unexposed_mask.sum()
        )
        outcome[exposed_mask] = np.random.binomial(
            1, exposed_probability, exposed_mask.sum()
        )
        
        return outcome
    
    def generate_binary_with_risk_ratio(
        self,
        n: int,
        exposure: np.ndarray,
        baseline_probability: float,
        risk_ratio: float
    ) -> np.ndarray:
        """
        根据暴露变量生成具有指定RR的二分类结局
        
        Args:
            n: 样本量
            exposure: 暴露变量（0/1）
            baseline_probability: 非暴露组的阳性概率
            risk_ratio: 目标风险比
            
        Returns:
            生成的结局变量
        """
        exposed_probability = min(baseline_probability * risk_ratio, 0.999)
        
        outcome = np.zeros(n, dtype=int)
        
        unexposed_mask = exposure == 0
        exposed_mask = exposure == 1
        
        outcome[unexposed_mask] = np.random.binomial(
            1, baseline_probability, unexposed_mask.sum()
        )
        outcome[exposed_mask] = np.random.binomial(
            1, exposed_probability, exposed_mask.sum()
        )
        
        return outcome
    
    def generate_binary_logistic(
        self,
        covariates: np.ndarray,
        coefficients: np.ndarray,
        intercept: float = 0
    ) -> np.ndarray:
        """
        根据逻辑回归模型生成二分类结局
        
        Args:
            covariates: 协变量矩阵 (n, p)
            coefficients: 回归系数
            intercept: 截距
            
        Returns:
            生成的结局变量
        """
        n = covariates.shape[0]
        
        # 计算线性预测值
        linear_pred = intercept + covariates @ coefficients
        
        # 转换为概率
        probabilities = 1 / (1 + np.exp(-linear_pred))
        
        # 生成二分类结局
        outcome = np.random.binomial(1, probabilities, n)
        
        return outcome
    
    def generate_correlated_binary(
        self,
        n: int,
        prob1: float,
        prob2: float,
        correlation: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成相关的二分类变量对
        
        Args:
            n: 样本量
            prob1: 变量1的阳性概率
            prob2: 变量2的阳性概率
            correlation: 目标相关系数（phi系数）
            
        Returns:
            两个相关二分类变量的元组
        """
        # 使用latent variable方法
        # 生成相关的标准正态变量
        cov_matrix = np.array([[1, correlation], [correlation, 1]])
        
        # 确保正定
        min_eig = np.min(np.linalg.eigvals(cov_matrix))
        if min_eig < 0:
            cov_matrix = cov_matrix - 1.1 * min_eig * np.eye(2)
        
        z = np.random.multivariate_normal([0, 0], cov_matrix, n)
        
        # 根据阈值截断
        threshold1 = stats.norm.ppf(1 - prob1)
        threshold2 = stats.norm.ppf(1 - prob2)
        
        var1 = (z[:, 0] > threshold1).astype(int)
        var2 = (z[:, 1] > threshold2).astype(int)
        
        return var1, var2
    
    def generate_group_proportions(
        self,
        n_per_group: List[int],
        group_proportions: List[float]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成具有指定组间比例差异的二分类变量
        
        Args:
            n_per_group: 各组样本量列表
            group_proportions: 各组的阳性比例列表
            
        Returns:
            (结局数组, 组别数组)
        """
        outcome = []
        groups = []
        
        for i, (n, prop) in enumerate(zip(n_per_group, group_proportions)):
            group_outcome = np.random.binomial(1, prop, n)
            outcome.append(group_outcome)
            groups.extend([i] * n)
        
        outcome = np.concatenate(outcome)
        groups = np.array(groups)
        
        return outcome, groups
    
    def adjust_odds_ratio(
        self,
        outcome: np.ndarray,
        exposure: np.ndarray,
        target_or: float,
        max_iterations: int = 100
    ) -> np.ndarray:
        """
        调整数据以达到目标OR（通过翻转部分结局）
        
        Args:
            outcome: 原始结局变量
            exposure: 暴露变量
            target_or: 目标比值比
            max_iterations: 最大迭代次数
            
        Returns:
            调整后的结局变量
        """
        adjusted = outcome.copy()
        
        for _ in range(max_iterations):
            current_or = self._calculate_odds_ratio(adjusted, exposure)
            
            if current_or is None:
                break
            
            # 检查是否足够接近目标
            if abs(np.log(current_or) - np.log(target_or)) < 0.1:
                break
            
            # 决定调整方向
            if current_or < target_or:
                # 需要增加OR：翻转暴露组的一些0为1，或非暴露组的一些1为0
                exposed_zeros = np.where((exposure == 1) & (adjusted == 0))[0]
                if len(exposed_zeros) > 0:
                    flip_idx = np.random.choice(exposed_zeros)
                    adjusted[flip_idx] = 1
            else:
                # 需要减少OR：翻转暴露组的一些1为0，或非暴露组的一些0为1
                exposed_ones = np.where((exposure == 1) & (adjusted == 1))[0]
                if len(exposed_ones) > 0:
                    flip_idx = np.random.choice(exposed_ones)
                    adjusted[flip_idx] = 0
        
        return adjusted
    
    def _calculate_odds_ratio(
        self, 
        outcome: np.ndarray, 
        exposure: np.ndarray
    ) -> Optional[float]:
        """计算比值比"""
        a = np.sum((exposure == 1) & (outcome == 1))
        b = np.sum((exposure == 1) & (outcome == 0))
        c = np.sum((exposure == 0) & (outcome == 1))
        d = np.sum((exposure == 0) & (outcome == 0))
        
        if b == 0 or c == 0:
            return None
        
        return (a * d) / (b * c)


def generate_categorical_variable(
    n: int,
    var_type: str = 'binary',
    probability: float = 0.5,
    categories: Optional[List] = None,
    probabilities: Optional[List[float]] = None,
    levels: int = 5,
    random_seed: Optional[int] = None,
    **kwargs
) -> np.ndarray:
    """
    便捷函数：生成单个分类变量
    
    Args:
        n: 样本量
        var_type: 变量类型 ('binary', 'multinomial', 'ordinal', 'count')
        probability: 阳性概率（用于binary）
        categories: 类别列表（用于multinomial）
        probabilities: 各类别概率
        levels: 等级数（用于ordinal）
        random_seed: 随机种子
        
    Returns:
        生成的分类数组
    """
    generator = CategoricalVariableGenerator(random_seed)
    
    if var_type == 'binary':
        return generator.generate_binary(n, probability)
    elif var_type == 'multinomial':
        if categories is None:
            categories = list(range(3))
        return generator.generate_multinomial(n, categories, probabilities)
    elif var_type == 'ordinal':
        distribution = kwargs.get('distribution', 'uniform')
        return generator.generate_ordinal(n, levels, probabilities, distribution)
    elif var_type == 'count':
        mean = kwargs.get('mean', 5)
        distribution = kwargs.get('distribution', 'poisson')
        return generator.generate_count(n, mean, distribution)
    else:
        raise ValueError(f"不支持的变量类型: {var_type}")
