"""
连续变量生成模块
用于生成具有指定分布和相关性的连续变量
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Union


class ContinuousVariableGenerator:
    """连续变量生成器"""
    
    def __init__(self, random_seed: Optional[int] = None):
        """
        初始化生成器
        
        Args:
            random_seed: 随机种子，用于结果复现
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def generate_normal(
        self, 
        n: int, 
        mean: float, 
        std: float,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        生成正态分布变量
        
        Args:
            n: 样本量
            mean: 均值
            std: 标准差
            min_val: 最小值截断
            max_val: 最大值截断
            
        Returns:
            生成的数据数组
        """
        data = np.random.normal(mean, std, n)
        
        if min_val is not None or max_val is not None:
            data = self._truncate(data, min_val, max_val)
        
        return data
    
    def generate_lognormal(
        self, 
        n: int, 
        mean: float, 
        std: float,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        生成对数正态分布变量
        
        Args:
            n: 样本量
            mean: 目标均值（原始尺度）
            std: 目标标准差（原始尺度）
            min_val: 最小值截断
            max_val: 最大值截断
            
        Returns:
            生成的数据数组
        """
        # 转换为对数尺度参数
        mu, sigma = self._lognormal_params(mean, std)
        data = np.random.lognormal(mu, sigma, n)
        
        if min_val is not None or max_val is not None:
            data = self._truncate(data, min_val, max_val)
        
        return data
    
    def generate_skewed(
        self, 
        n: int, 
        mean: float, 
        std: float,
        skewness: float = 0.5,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        生成偏态分布变量（使用skewnorm分布）
        
        Args:
            n: 样本量
            mean: 目标均值
            std: 目标标准差
            skewness: 偏度参数（正值右偏，负值左偏）
            min_val: 最小值截断
            max_val: 最大值截断
            
        Returns:
            生成的数据数组
        """
        # 使用skewnorm分布
        a = skewness * 5  # 缩放偏度参数
        data = stats.skewnorm.rvs(a, size=n)
        
        # 标准化到目标均值和标准差
        data = (data - data.mean()) / data.std() * std + mean
        
        if min_val is not None or max_val is not None:
            data = self._truncate(data, min_val, max_val)
        
        return data
    
    def generate_uniform(
        self, 
        n: int, 
        low: float, 
        high: float
    ) -> np.ndarray:
        """
        生成均匀分布变量
        
        Args:
            n: 样本量
            low: 最小值
            high: 最大值
            
        Returns:
            生成的数据数组
        """
        return np.random.uniform(low, high, n)
    
    def generate_correlated_pair(
        self,
        n: int,
        var1_params: Dict,
        var2_params: Dict,
        correlation: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成相关的变量对
        
        Args:
            n: 样本量
            var1_params: 变量1参数 {'mean': float, 'std': float}
            var2_params: 变量2参数 {'mean': float, 'std': float}
            correlation: 目标相关系数
            
        Returns:
            两个相关变量的元组
        """
        # 生成相关的标准正态变量
        cov_matrix = np.array([[1, correlation], [correlation, 1]])
        z = np.random.multivariate_normal([0, 0], cov_matrix, n)
        
        # 转换到目标分布
        var1 = z[:, 0] * var1_params['std'] + var1_params['mean']
        var2 = z[:, 1] * var2_params['std'] + var2_params['mean']
        
        return var1, var2
    
    def generate_multivariate(
        self,
        n: int,
        means: np.ndarray,
        stds: np.ndarray,
        correlation_matrix: np.ndarray
    ) -> np.ndarray:
        """
        生成多元正态分布变量
        
        Args:
            n: 样本量
            means: 各变量均值数组
            stds: 各变量标准差数组
            correlation_matrix: 相关矩阵
            
        Returns:
            生成的数据矩阵 (n, p)
        """
        p = len(means)
        
        # 将相关矩阵转换为协方差矩阵
        cov_matrix = np.outer(stds, stds) * correlation_matrix
        
        # 确保协方差矩阵正定
        cov_matrix = self._ensure_positive_definite(cov_matrix)
        
        # 生成多元正态数据
        data = np.random.multivariate_normal(means, cov_matrix, n)
        
        return data
    
    def generate_group_means(
        self,
        n_per_group: List[int],
        group_means: List[float],
        common_std: float,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成具有指定组间差异的连续变量
        
        Args:
            n_per_group: 各组样本量列表
            group_means: 各组均值列表
            common_std: 组内标准差（假设同方差）
            min_val: 最小值截断
            max_val: 最大值截断
            
        Returns:
            (数据数组, 组别数组)
        """
        data = []
        groups = []
        
        for i, (n, mean) in enumerate(zip(n_per_group, group_means)):
            group_data = np.random.normal(mean, common_std, n)
            data.append(group_data)
            groups.extend([i] * n)
        
        data = np.concatenate(data)
        groups = np.array(groups)
        
        if min_val is not None or max_val is not None:
            data = self._truncate(data, min_val, max_val)
        
        return data, groups
    
    def adjust_effect_size(
        self,
        data: np.ndarray,
        group: np.ndarray,
        target_effect_size: float,
        current_effect_size: Optional[float] = None
    ) -> np.ndarray:
        """
        调整组间效应量
        
        Args:
            data: 原始数据
            group: 组别变量（0/1）
            target_effect_size: 目标效应量（Cohen's d）
            current_effect_size: 当前效应量（如果None则计算）
            
        Returns:
            调整后的数据
        """
        if current_effect_size is None:
            current_effect_size = self._calculate_cohens_d(data, group)
        
        if current_effect_size == 0:
            return data
        
        adjustment_factor = target_effect_size / current_effect_size
        
        # 只调整第1组的数据
        adjusted_data = data.copy()
        group1_mask = group == 1
        pooled_std = np.sqrt(
            (np.var(data[~group1_mask]) + np.var(data[group1_mask])) / 2
        )
        
        mean_diff = data[group1_mask].mean() - data[~group1_mask].mean()
        new_mean_diff = mean_diff * adjustment_factor
        
        adjusted_data[group1_mask] = (
            data[group1_mask] - mean_diff + new_mean_diff
        )
        
        return adjusted_data
    
    def _truncate(
        self, 
        data: np.ndarray, 
        min_val: Optional[float], 
        max_val: Optional[float]
    ) -> np.ndarray:
        """截断数据到指定范围"""
        if min_val is not None:
            data = np.maximum(data, min_val)
        if max_val is not None:
            data = np.minimum(data, max_val)
        return data
    
    def _lognormal_params(
        self, 
        mean: float, 
        std: float
    ) -> Tuple[float, float]:
        """将目标均值和标准差转换为对数正态分布参数"""
        var = std ** 2
        mu = np.log(mean ** 2 / np.sqrt(var + mean ** 2))
        sigma = np.sqrt(np.log(1 + var / mean ** 2))
        return mu, sigma
    
    def _ensure_positive_definite(
        self, 
        matrix: np.ndarray
    ) -> np.ndarray:
        """确保矩阵正定"""
        min_eig = np.min(np.linalg.eigvals(matrix))
        if min_eig < 0:
            matrix = matrix - 1.1 * min_eig * np.eye(matrix.shape[0])
        return matrix
    
    def _calculate_cohens_d(
        self, 
        data: np.ndarray, 
        group: np.ndarray
    ) -> float:
        """计算Cohen's d效应量"""
        group0 = data[group == 0]
        group1 = data[group == 1]
        
        n0, n1 = len(group0), len(group1)
        var0, var1 = np.var(group0, ddof=1), np.var(group1, ddof=1)
        
        pooled_std = np.sqrt(
            ((n0 - 1) * var0 + (n1 - 1) * var1) / (n0 + n1 - 2)
        )
        
        return (group1.mean() - group0.mean()) / pooled_std


def generate_continuous_variable(
    n: int,
    distribution: str = 'normal',
    mean: float = 0,
    std: float = 1,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    skewness: float = 0,
    random_seed: Optional[int] = None,
    **kwargs
) -> np.ndarray:
    """
    便捷函数：生成单个连续变量
    
    Args:
        n: 样本量
        distribution: 分布类型 ('normal', 'lognormal', 'skewed', 'uniform')
        mean: 均值
        std: 标准差
        min_val: 最小值
        max_val: 最大值
        skewness: 偏度（仅用于skewed分布）
        random_seed: 随机种子
        
    Returns:
        生成的数据数组
    """
    generator = ContinuousVariableGenerator(random_seed)
    
    if distribution == 'normal':
        return generator.generate_normal(n, mean, std, min_val, max_val)
    elif distribution == 'lognormal':
        return generator.generate_lognormal(n, mean, std, min_val, max_val)
    elif distribution == 'skewed':
        return generator.generate_skewed(n, mean, std, skewness, min_val, max_val)
    elif distribution == 'uniform':
        low = kwargs.get('low', mean - std * np.sqrt(3))
        high = kwargs.get('high', mean + std * np.sqrt(3))
        return generator.generate_uniform(n, low, high)
    else:
        raise ValueError(f"不支持的分布类型: {distribution}")
