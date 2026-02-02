"""
生存数据生成模块
用于生成具有指定风险比的生存时间数据
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Union


class SurvivalDataGenerator:
    """生存数据生成器"""
    
    def __init__(self, random_seed: Optional[int] = None):
        """
        初始化生成器
        
        Args:
            random_seed: 随机种子，用于结果复现
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def generate_exponential(
        self, 
        n: int, 
        median_survival: float,
        max_time: Optional[float] = None
    ) -> np.ndarray:
        """
        生成指数分布的生存时间
        
        Args:
            n: 样本量
            median_survival: 中位生存时间
            max_time: 最大随访时间（用于截断）
            
        Returns:
            生存时间数组
        """
        # 从中位数计算 lambda: median = ln(2) / lambda
        lambda_param = np.log(2) / median_survival
        
        # 生成指数分布的生存时间
        survival_time = np.random.exponential(1 / lambda_param, n)
        
        if max_time is not None:
            survival_time = np.minimum(survival_time, max_time)
        
        return survival_time
    
    def generate_weibull(
        self, 
        n: int, 
        median_survival: float,
        shape: float = 1.0,
        max_time: Optional[float] = None
    ) -> np.ndarray:
        """
        生成Weibull分布的生存时间
        
        Args:
            n: 样本量
            median_survival: 中位生存时间
            shape: 形状参数（>1递增风险，<1递减风险，=1指数分布）
            max_time: 最大随访时间
            
        Returns:
            生存时间数组
        """
        # 从中位数和形状参数计算尺度参数
        # median = scale * (ln(2))^(1/shape)
        scale = median_survival / (np.log(2) ** (1 / shape))
        
        # 生成Weibull分布的生存时间
        survival_time = scale * np.random.weibull(shape, n)
        
        if max_time is not None:
            survival_time = np.minimum(survival_time, max_time)
        
        return survival_time
    
    def generate_with_hazard_ratio(
        self,
        n: int,
        exposure: np.ndarray,
        baseline_median: float,
        hazard_ratio: float,
        distribution: str = 'exponential',
        shape: float = 1.0,
        max_time: Optional[float] = None
    ) -> np.ndarray:
        """
        根据暴露变量生成具有指定HR的生存时间
        
        Args:
            n: 样本量
            exposure: 暴露变量（0/1）
            baseline_median: 非暴露组的中位生存时间
            hazard_ratio: 目标风险比（>1表示暴露组风险更高）
            distribution: 分布类型 ('exponential', 'weibull')
            shape: Weibull形状参数
            max_time: 最大随访时间
            
        Returns:
            生存时间数组
        """
        survival_time = np.zeros(n)
        
        unexposed_mask = exposure == 0
        exposed_mask = exposure == 1
        
        # 非暴露组的生存时间
        if distribution == 'exponential':
            survival_time[unexposed_mask] = self.generate_exponential(
                unexposed_mask.sum(), baseline_median, max_time
            )
        else:
            survival_time[unexposed_mask] = self.generate_weibull(
                unexposed_mask.sum(), baseline_median, shape, max_time
            )
        
        # 暴露组的中位生存时间（HR调整）
        # HR = h1/h0 = lambda1/lambda0 (指数分布)
        # 中位数与lambda成反比，所以 median1 = median0 / HR
        exposed_median = baseline_median / hazard_ratio
        
        if distribution == 'exponential':
            survival_time[exposed_mask] = self.generate_exponential(
                exposed_mask.sum(), exposed_median, max_time
            )
        else:
            survival_time[exposed_mask] = self.generate_weibull(
                exposed_mask.sum(), exposed_median, shape, max_time
            )
        
        return survival_time
    
    def generate_censoring(
        self,
        survival_time: np.ndarray,
        censoring_rate: float = 0.2,
        censoring_type: str = 'random',
        max_followup: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成删失数据
        
        Args:
            survival_time: 真实生存时间
            censoring_rate: 删失比例
            censoring_type: 删失类型 ('random', 'administrative', 'mixed')
            max_followup: 最大随访时间
            
        Returns:
            (观察时间, 事件指示变量)
        """
        n = len(survival_time)
        
        if censoring_type == 'random':
            # 随机删失：删失时间服从均匀分布
            if max_followup is None:
                max_followup = np.max(survival_time) * 1.5
            
            # 调整删失分布以达到目标删失率
            censoring_time = np.random.uniform(0, max_followup * 2, n)
            
        elif censoring_type == 'administrative':
            # 行政删失：所有删失发生在同一时间点
            if max_followup is None:
                max_followup = np.percentile(survival_time, 100 * (1 - censoring_rate))
            censoring_time = np.full(n, max_followup)
            
        elif censoring_type == 'mixed':
            # 混合删失：部分随机，部分行政
            if max_followup is None:
                max_followup = np.max(survival_time) * 1.2
            
            random_censor = np.random.uniform(0, max_followup * 2, n)
            admin_censor = np.full(n, max_followup)
            
            # 50%随机删失，50%行政删失
            mix_probs = np.random.binomial(1, 0.5, n)
            censoring_time = np.where(mix_probs, random_censor, admin_censor)
        else:
            raise ValueError(f"不支持的删失类型: {censoring_type}")
        
        # 计算观察时间和事件指示
        observed_time = np.minimum(survival_time, censoring_time)
        event = (survival_time <= censoring_time).astype(int)
        
        return observed_time, event
    
    def generate_cox_survival(
        self,
        covariates: np.ndarray,
        coefficients: np.ndarray,
        baseline_median: float,
        distribution: str = 'exponential',
        shape: float = 1.0,
        max_time: Optional[float] = None
    ) -> np.ndarray:
        """
        根据Cox比例风险模型生成生存时间
        
        Args:
            covariates: 协变量矩阵 (n, p)
            coefficients: 回归系数（log(HR)）
            baseline_median: 基线中位生存时间
            distribution: 基线风险分布
            shape: Weibull形状参数
            max_time: 最大时间
            
        Returns:
            生存时间数组
        """
        n = covariates.shape[0]
        
        # 计算相对风险
        linear_pred = covariates @ coefficients
        relative_hazard = np.exp(linear_pred)
        
        # 调整每个个体的中位生存时间
        individual_median = baseline_median / relative_hazard
        
        # 生成生存时间
        survival_time = np.zeros(n)
        for i in range(n):
            if distribution == 'exponential':
                lambda_param = np.log(2) / individual_median[i]
                survival_time[i] = np.random.exponential(1 / lambda_param)
            else:
                scale = individual_median[i] / (np.log(2) ** (1 / shape))
                survival_time[i] = scale * np.random.weibull(shape)
        
        if max_time is not None:
            survival_time = np.minimum(survival_time, max_time)
        
        return survival_time
    
    def generate_competing_risks(
        self,
        n: int,
        cause_medians: List[float],
        cause_names: Optional[List[str]] = None,
        max_time: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成竞争风险数据
        
        Args:
            n: 样本量
            cause_medians: 各原因的中位时间列表
            cause_names: 原因名称列表
            max_time: 最大时间
            
        Returns:
            (观察时间, 事件类型)
        """
        k = len(cause_medians)
        
        if cause_names is None:
            cause_names = [f'cause_{i+1}' for i in range(k)]
        
        # 为每个原因生成潜在事件时间
        potential_times = np.zeros((n, k))
        for j, median in enumerate(cause_medians):
            potential_times[:, j] = self.generate_exponential(n, median, max_time)
        
        # 选择最先发生的事件
        observed_time = np.min(potential_times, axis=1)
        event_type = np.argmin(potential_times, axis=1)
        
        # 转换为事件名称
        event_names = np.array([cause_names[i] for i in event_type])
        
        if max_time is not None:
            censored = observed_time >= max_time
            observed_time[censored] = max_time
            event_names[censored] = 'censored'
        
        return observed_time, event_names
    
    def adjust_hazard_ratio(
        self,
        survival_time: np.ndarray,
        exposure: np.ndarray,
        target_hr: float,
        current_hr: Optional[float] = None
    ) -> np.ndarray:
        """
        调整数据以达到目标HR
        
        Args:
            survival_time: 原始生存时间
            exposure: 暴露变量
            target_hr: 目标风险比
            current_hr: 当前风险比（如果None则估计）
            
        Returns:
            调整后的生存时间
        """
        if current_hr is None:
            current_hr = self._estimate_hazard_ratio(survival_time, exposure)
        
        if current_hr is None or current_hr == 0:
            return survival_time
        
        # 调整暴露组的生存时间
        # HR = h1/h0，对于指数分布 median1/median0 = h0/h1 = 1/HR
        adjustment_factor = current_hr / target_hr
        
        adjusted = survival_time.copy()
        exposed_mask = exposure == 1
        adjusted[exposed_mask] = survival_time[exposed_mask] * adjustment_factor
        
        return adjusted
    
    def _estimate_hazard_ratio(
        self, 
        survival_time: np.ndarray, 
        exposure: np.ndarray
    ) -> Optional[float]:
        """简单估计风险比（基于中位数比值）"""
        median0 = np.median(survival_time[exposure == 0])
        median1 = np.median(survival_time[exposure == 1])
        
        if median1 == 0:
            return None
        
        # HR ≈ median0 / median1 (对于指数分布)
        return median0 / median1


def generate_survival_data(
    n: int,
    median_survival: float,
    censoring_rate: float = 0.2,
    distribution: str = 'exponential',
    shape: float = 1.0,
    max_time: Optional[float] = None,
    random_seed: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    便捷函数：生成生存数据
    
    Args:
        n: 样本量
        median_survival: 中位生存时间
        censoring_rate: 删失比例
        distribution: 分布类型
        shape: Weibull形状参数
        max_time: 最大时间
        random_seed: 随机种子
        
    Returns:
        (观察时间, 事件指示变量)
    """
    generator = SurvivalDataGenerator(random_seed)
    
    if distribution == 'exponential':
        survival_time = generator.generate_exponential(n, median_survival, max_time)
    elif distribution == 'weibull':
        survival_time = generator.generate_weibull(n, median_survival, shape, max_time)
    else:
        raise ValueError(f"不支持的分布类型: {distribution}")
    
    observed_time, event = generator.generate_censoring(
        survival_time, censoring_rate, 'mixed', max_time
    )
    
    return observed_time, event
