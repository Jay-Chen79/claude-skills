"""
Excel导出模块
用于将生成的数据导出为Excel格式，包含数据字典和汇总统计
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime


class ExcelExporter:
    """Excel导出器"""
    
    def __init__(self):
        """初始化导出器"""
        self.data_df: Optional[pd.DataFrame] = None
        self.data_dict: List[Dict] = []
        self.metadata: Dict[str, Any] = {}
    
    def set_data(
        self,
        data: Dict[str, np.ndarray],
        variable_info: Optional[List[Dict]] = None
    ):
        """
        设置数据
        
        Args:
            data: 数据字典 {变量名: 数据数组}
            variable_info: 变量信息列表
        """
        self.data_df = pd.DataFrame(data)
        
        if variable_info:
            self.data_dict = variable_info
        else:
            # 自动推断变量信息
            self.data_dict = self._infer_variable_info(data)
    
    def _infer_variable_info(self, data: Dict[str, np.ndarray]) -> List[Dict]:
        """自动推断变量信息"""
        info_list = []
        
        for var_name, values in data.items():
            # 处理缺失值
            valid_values = values[~np.isnan(values) if np.issubdtype(values.dtype, np.floating) else np.ones(len(values), dtype=bool)]
            
            # 推断类型
            unique_count = len(np.unique(valid_values))
            
            if unique_count <= 2:
                var_type = "二分类"
            elif unique_count <= 10:
                if np.issubdtype(values.dtype, np.integer):
                    var_type = "分类"
                else:
                    var_type = "连续"
            else:
                var_type = "连续"
            
            # 推断范围
            if np.issubdtype(values.dtype, np.number):
                val_range = f"{np.nanmin(values):.2f} - {np.nanmax(values):.2f}"
            else:
                val_range = ", ".join([str(v) for v in np.unique(valid_values)[:5]])
            
            info_list.append({
                '变量名': var_name,
                '变量标签': var_name,
                '变量类型': var_type,
                '取值范围': val_range,
                '单位': '',
                '说明': ''
            })
        
        return info_list
    
    def set_metadata(
        self,
        study_name: str = "虚拟研究数据",
        generation_params: Optional[Dict] = None,
        random_seed: Optional[int] = None,
        notes: Optional[str] = None
    ):
        """
        设置元数据
        
        Args:
            study_name: 研究名称
            generation_params: 生成参数
            random_seed: 随机种子
            notes: 备注
        """
        self.metadata = {
            '研究名称': study_name,
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '样本量': len(self.data_df) if self.data_df is not None else 0,
            '变量数': len(self.data_df.columns) if self.data_df is not None else 0,
            '随机种子': random_seed if random_seed else '未记录',
            '备注': notes if notes else ''
        }
        
        if generation_params:
            self.metadata['生成参数'] = str(generation_params)
    
    def _create_summary_sheet(self) -> pd.DataFrame:
        """创建汇总统计表"""
        if self.data_df is None:
            return pd.DataFrame()
        
        summary_data = []
        
        for col in self.data_df.columns:
            values = self.data_df[col]
            
            row = {'变量名': col}
            
            # 基本统计
            row['样本量'] = len(values)
            row['缺失'] = values.isna().sum()
            row['缺失率'] = f"{values.isna().mean()*100:.1f}%"
            
            # 根据类型计算不同统计量
            valid = values.dropna()
            
            if pd.api.types.is_numeric_dtype(values):
                unique_count = valid.nunique()
                
                if unique_count <= 10:
                    # 可能是分类变量
                    row['统计类型'] = '频数'
                    value_counts = valid.value_counts()
                    for v, c in value_counts.head(5).items():
                        row[f'值{v}'] = f"{c} ({c/len(valid)*100:.1f}%)"
                else:
                    # 连续变量
                    row['统计类型'] = '描述性'
                    row['均值'] = f"{valid.mean():.2f}"
                    row['标准差'] = f"{valid.std():.2f}"
                    row['中位数'] = f"{valid.median():.2f}"
                    row['最小值'] = f"{valid.min():.2f}"
                    row['最大值'] = f"{valid.max():.2f}"
                    row['Q1'] = f"{valid.quantile(0.25):.2f}"
                    row['Q3'] = f"{valid.quantile(0.75):.2f}"
            else:
                # 字符串变量
                row['统计类型'] = '频数'
                value_counts = valid.value_counts()
                for v, c in value_counts.head(5).items():
                    row[f'值{v}'] = f"{c} ({c/len(valid)*100:.1f}%)"
            
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def _create_metadata_sheet(self) -> pd.DataFrame:
        """创建元数据表"""
        meta_rows = []
        for key, value in self.metadata.items():
            meta_rows.append({'属性': key, '值': value})
        return pd.DataFrame(meta_rows)
    
    def export(
        self,
        filepath: str,
        include_summary: bool = True,
        include_dictionary: bool = True,
        include_metadata: bool = True
    ):
        """
        导出到Excel文件
        
        Args:
            filepath: 文件路径
            include_summary: 是否包含汇总统计
            include_dictionary: 是否包含数据字典
            include_metadata: 是否包含元数据
        """
        if self.data_df is None:
            raise ValueError("请先设置数据")
        
        filepath = Path(filepath)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 原始数据
            self.data_df.to_excel(writer, sheet_name='Raw_Data', index=False)
            
            # 数据字典
            if include_dictionary and self.data_dict:
                dict_df = pd.DataFrame(self.data_dict)
                dict_df.to_excel(writer, sheet_name='Data_Dictionary', index=False)
            
            # 汇总统计
            if include_summary:
                summary_df = self._create_summary_sheet()
                summary_df.to_excel(writer, sheet_name='Summary_Statistics', index=False)
            
            # 元数据
            if include_metadata and self.metadata:
                meta_df = self._create_metadata_sheet()
                meta_df.to_excel(writer, sheet_name='Metadata', index=False)
        
        print(f"数据已导出到: {filepath}")
    
    def export_validation_report(
        self,
        filepath: str,
        validation_results: List[Dict]
    ):
        """
        导出验证报告
        
        Args:
            filepath: 文件路径
            validation_results: 验证结果列表
        """
        filepath = Path(filepath)
        
        # 转换验证结果为DataFrame
        results_data = []
        for r in validation_results:
            results_data.append({
                '验证项': r.get('metric_name', ''),
                '预期值': r.get('expected_value', ''),
                '实际值': r.get('actual_value', ''),
                'p值': r.get('p_value', ''),
                '95%CI下限': r.get('ci_lower', ''),
                '95%CI上限': r.get('ci_upper', ''),
                '通过': '✓' if r.get('passed', False) else '✗',
                '备注': r.get('message', '')
            })
        
        results_df = pd.DataFrame(results_data)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            results_df.to_excel(writer, sheet_name='Validation_Results', index=False)
        
        print(f"验证报告已导出到: {filepath}")


def export_to_excel(
    data: Dict[str, np.ndarray],
    filepath: str,
    variable_info: Optional[List[Dict]] = None,
    study_name: str = "虚拟研究数据",
    random_seed: Optional[int] = None,
    notes: Optional[str] = None
):
    """
    便捷函数：导出数据到Excel
    
    Args:
        data: 数据字典
        filepath: 文件路径
        variable_info: 变量信息
        study_name: 研究名称
        random_seed: 随机种子
        notes: 备注
    """
    exporter = ExcelExporter()
    exporter.set_data(data, variable_info)
    exporter.set_metadata(study_name, None, random_seed, notes)
    exporter.export(filepath)


def create_data_dictionary(
    variables: List[str],
    labels: Optional[List[str]] = None,
    types: Optional[List[str]] = None,
    ranges: Optional[List[str]] = None,
    units: Optional[List[str]] = None,
    descriptions: Optional[List[str]] = None
) -> List[Dict]:
    """
    创建数据字典
    
    Args:
        variables: 变量名列表
        labels: 变量标签列表
        types: 变量类型列表
        ranges: 取值范围列表
        units: 单位列表
        descriptions: 说明列表
        
    Returns:
        数据字典列表
    """
    n = len(variables)
    
    if labels is None:
        labels = variables
    if types is None:
        types = [''] * n
    if ranges is None:
        ranges = [''] * n
    if units is None:
        units = [''] * n
    if descriptions is None:
        descriptions = [''] * n
    
    return [
        {
            '变量名': variables[i],
            '变量标签': labels[i],
            '变量类型': types[i],
            '取值范围': ranges[i],
            '单位': units[i],
            '说明': descriptions[i]
        }
        for i in range(n)
    ]
