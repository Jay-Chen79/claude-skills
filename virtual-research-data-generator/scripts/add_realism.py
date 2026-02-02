"""
真实性增强模块
用于添加缺失值、离群值、测量误差等真实世界特征
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum


class MissingMechanism(Enum):
    """缺失机制"""
    MCAR = "mcar"  # 完全随机缺失
    MAR = "mar"    # 随机缺失
    MNAR = "mnar"  # 非随机缺失


class RealismEnhancer:
    """真实性增强器"""
    
    def __init__(self, random_seed: Optional[int] = None):
        """
        初始化增强器
        
        Args:
            random_seed: 随机种子
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def add_missing_values(
        self,
        data: np.ndarray,
        missing_rate: float = 0.05,
        mechanism: MissingMechanism = MissingMechanism.MCAR,
        related_var: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        添加缺失值
        
        Args:
            data: 原始数据
            missing_rate: 缺失比例
            mechanism: 缺失机制
            related_var: 相关变量（用于MAR/MNAR）
            
        Returns:
            含缺失值的数据（使用np.nan表示）
        """
        n = len(data)
        result = data.astype(float).copy()
        
        if mechanism == MissingMechanism.MCAR:
            # 完全随机缺失
            missing_mask = np.random.random(n) < missing_rate
            
        elif mechanism == MissingMechanism.MAR:
            # 随机缺失：缺失概率与相关变量相关
            if related_var is None:
                raise ValueError("MAR机制需要提供related_var")
            
            # 根据相关变量的分位数决定缺失概率
            quantiles = np.percentile(related_var, [25, 50, 75])
            missing_probs = np.zeros(n)
            missing_probs[related_var <= quantiles[0]] = missing_rate * 0.5
            missing_probs[(related_var > quantiles[0]) & (related_var <= quantiles[1])] = missing_rate
            missing_probs[(related_var > quantiles[1]) & (related_var <= quantiles[2])] = missing_rate * 1.5
            missing_probs[related_var > quantiles[2]] = missing_rate * 2
            
            missing_mask = np.random.random(n) < missing_probs
            
        elif mechanism == MissingMechanism.MNAR:
            # 非随机缺失：缺失概率与缺失值本身相关
            # 高值更容易缺失
            quantiles = np.percentile(data, [25, 50, 75])
            missing_probs = np.zeros(n)
            missing_probs[data <= quantiles[0]] = missing_rate * 0.5
            missing_probs[(data > quantiles[0]) & (data <= quantiles[1])] = missing_rate
            missing_probs[(data > quantiles[1]) & (data <= quantiles[2])] = missing_rate * 1.5
            missing_probs[data > quantiles[2]] = missing_rate * 2.5
            
            missing_mask = np.random.random(n) < missing_probs
        else:
            raise ValueError(f"不支持的缺失机制: {mechanism}")
        
        result[missing_mask] = np.nan
        return result
    
    def add_measurement_error(
        self,
        data: np.ndarray,
        error_sd: float = 0.1,
        error_type: str = 'additive'
    ) -> np.ndarray:
        """
        添加测量误差
        
        Args:
            data: 原始数据
            error_sd: 误差标准差（相对于数据范围）
            error_type: 误差类型 ('additive', 'multiplicative')
            
        Returns:
            含误差的数据
        """
        n = len(data)
        
        if error_type == 'additive':
            # 加性误差
            data_range = np.nanstd(data)
            error = np.random.normal(0, error_sd * data_range, n)
            result = data + error
            
        elif error_type == 'multiplicative':
            # 乘性误差
            error = np.random.normal(1, error_sd, n)
            result = data * error
        else:
            raise ValueError(f"不支持的误差类型: {error_type}")
        
        return result
    
    def add_outliers(
        self,
        data: np.ndarray,
        outlier_rate: float = 0.02,
        outlier_type: str = 'extreme',
        multiplier: float = 3.0
    ) -> np.ndarray:
        """
        添加离群值
        
        Args:
            data: 原始数据
            outlier_rate: 离群值比例
            outlier_type: 离群值类型 ('extreme', 'mild', 'clinical')
            multiplier: 离群值倍数
            
        Returns:
            含离群值的数据
        """
        n = len(data)
        result = data.copy()
        
        # 选择要变成离群值的观测
        outlier_mask = np.random.random(n) < outlier_rate
        n_outliers = outlier_mask.sum()
        
        if n_outliers == 0:
            return result
        
        mean = np.nanmean(data)
        std = np.nanstd(data)
        
        if outlier_type == 'extreme':
            # 极端离群值：距离均值3+个标准差
            directions = np.random.choice([-1, 1], n_outliers)
            offsets = np.random.uniform(multiplier, multiplier + 1, n_outliers)
            outlier_values = mean + directions * offsets * std
            
        elif outlier_type == 'mild':
            # 温和离群值：距离均值2-3个标准差
            directions = np.random.choice([-1, 1], n_outliers)
            offsets = np.random.uniform(2, multiplier, n_outliers)
            outlier_values = mean + directions * offsets * std
            
        elif outlier_type == 'clinical':
            # 临床离群值：在可能但罕见的范围内
            # 使用数据的1%和99%分位数扩展
            q01, q99 = np.nanpercentile(data, [1, 99])
            range_ext = (q99 - q01) * 0.5
            outlier_values = np.random.uniform(
                q01 - range_ext, q99 + range_ext, n_outliers
            )
        else:
            raise ValueError(f"不支持的离群值类型: {outlier_type}")
        
        result[outlier_mask] = outlier_values
        return result
    
    def add_misclassification(
        self,
        data: np.ndarray,
        error_rate: float = 0.02,
        categories: Optional[List] = None
    ) -> np.ndarray:
        """
        添加分类错误
        
        Args:
            data: 原始分类数据
            error_rate: 错误分类比例
            categories: 可能的类别列表
            
        Returns:
            含错误分类的数据
        """
        result = data.copy()
        n = len(data)
        
        if categories is None:
            categories = np.unique(data)
        
        # 选择要错误分类的观测
        error_mask = np.random.random(n) < error_rate
        n_errors = error_mask.sum()
        
        if n_errors == 0:
            return result
        
        # 为每个错误分类的观测随机选择一个不同的类别
        for i in np.where(error_mask)[0]:
            current_cat = result[i]
            other_cats = [c for c in categories if c != current_cat]
            if len(other_cats) > 0:
                result[i] = np.random.choice(other_cats)
        
        return result
    
    def round_to_precision(
        self,
        data: np.ndarray,
        precision: float = 1.0,
        method: str = 'round'
    ) -> np.ndarray:
        """
        调整数据精度
        
        Args:
            data: 原始数据
            precision: 精度（如0.1表示保留一位小数，1表示整数）
            method: 舍入方法 ('round', 'floor', 'ceil')
            
        Returns:
            调整精度后的数据
        """
        if method == 'round':
            result = np.round(data / precision) * precision
        elif method == 'floor':
            result = np.floor(data / precision) * precision
        elif method == 'ceil':
            result = np.ceil(data / precision) * precision
        else:
            raise ValueError(f"不支持的舍入方法: {method}")
        
        return result
    
    def enforce_range(
        self,
        data: np.ndarray,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> np.ndarray:
        """
        强制值在合理范围内
        
        Args:
            data: 原始数据
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            范围内的数据
        """
        result = data.copy()
        
        if min_val is not None:
            result = np.maximum(result, min_val)
        if max_val is not None:
            result = np.minimum(result, max_val)
        
        return result
    
    def add_dropout(
        self,
        data: Dict[str, np.ndarray],
        dropout_rate: float = 0.1,
        dropout_mechanism: str = 'random'
    ) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
        """
        添加失访/脱落
        
        Args:
            data: 数据字典
            dropout_rate: 脱落率
            dropout_mechanism: 脱落机制 ('random', 'related')
            
        Returns:
            (过滤后的数据字典, 脱落指示变量)
        """
        n = len(list(data.values())[0])
        
        if dropout_mechanism == 'random':
            # 随机脱落
            dropout_mask = np.random.random(n) < dropout_rate
        elif dropout_mechanism == 'related':
            # 与暴露或结局相关的脱落
            # 这里简化处理，实际应根据具体变量调整
            dropout_mask = np.random.random(n) < dropout_rate
        else:
            raise ValueError(f"不支持的脱落机制: {dropout_mechanism}")
        
        retained_mask = ~dropout_mask
        
        filtered_data = {}
        for key, values in data.items():
            filtered_data[key] = values[retained_mask]
        
        return filtered_data, dropout_mask
    
    def ensure_logical_consistency(
        self,
        data: Dict[str, np.ndarray],
        rules: List[Dict]
    ) -> Dict[str, np.ndarray]:
        """
        确保逻辑一致性
        
        Args:
            data: 数据字典
            rules: 规则列表，每条规则包含 {var1, var2, relation, action}
            
        Returns:
            调整后的数据字典
        """
        result = {k: v.copy() for k, v in data.items()}
        
        for rule in rules:
            var1 = rule['var1']
            var2 = rule['var2']
            relation = rule['relation']
            action = rule.get('action', 'adjust_var2')
            
            if var1 not in result or var2 not in result:
                continue
            
            if relation == 'var1_less_than_var2':
                # var1 应该小于 var2
                mask = result[var1] >= result[var2]
                if action == 'adjust_var2':
                    result[var2][mask] = result[var1][mask] + np.abs(
                        np.random.normal(1, 0.5, mask.sum())
                    )
                elif action == 'adjust_var1':
                    result[var1][mask] = result[var2][mask] - np.abs(
                        np.random.normal(1, 0.5, mask.sum())
                    )
            
            elif relation == 'derived':
                # var2 是从 var1 派生的
                formula = rule.get('formula')
                if formula:
                    # 这里简化处理，实际应解析公式
                    pass
        
        return result
    
    def generate_unique_ids(
        self,
        n: int,
        prefix: str = 'ID',
        digits: int = 6
    ) -> np.ndarray:
        """
        生成唯一ID
        
        Args:
            n: 样本量
            prefix: ID前缀
            digits: 数字位数
            
        Returns:
            ID数组
        """
        ids = [f"{prefix}{str(i+1).zfill(digits)}" for i in range(n)]
        return np.array(ids)


def enhance_realism(
    data: np.ndarray,
    missing_rate: float = 0.03,
    outlier_rate: float = 0.02,
    measurement_error: float = 0.05,
    precision: Optional[float] = None,
    value_range: Optional[Tuple[float, float]] = None,
    random_seed: Optional[int] = None
) -> np.ndarray:
    """
    便捷函数：一次性添加所有真实性特征
    
    Args:
        data: 原始数据
        missing_rate: 缺失率
        outlier_rate: 离群值率
        measurement_error: 测量误差
        precision: 精度
        value_range: 值范围 (min, max)
        random_seed: 随机种子
        
    Returns:
        增强后的数据
    """
    enhancer = RealismEnhancer(random_seed)
    
    result = data.copy()
    
    # 添加测量误差
    if measurement_error > 0:
        result = enhancer.add_measurement_error(result, measurement_error)
    
    # 添加离群值
    if outlier_rate > 0:
        result = enhancer.add_outliers(result, outlier_rate, 'clinical')
    
    # 调整精度
    if precision is not None:
        result = enhancer.round_to_precision(result, precision)
    
    # 强制范围
    if value_range is not None:
        result = enhancer.enforce_range(result, value_range[0], value_range[1])
    
    # 添加缺失值（最后添加）
    if missing_rate > 0:
        result = enhancer.add_missing_values(result, missing_rate)
    
    return result
