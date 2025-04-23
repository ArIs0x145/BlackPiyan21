from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import logging

class Analyzer:
    """分析器類，用於分析21點模擬結果"""
    
    def __init__(self, results: Optional[Dict[int, List[Dict[str, Any]]]] = None):
        """
        初始化分析器
        
        Args:
            results: 模擬結果字典，鍵為策略值，值為該策略的結果列表
        """
        self.results = results if results is not None else {}
        self.strategies = list(self.results.keys()) if self.results else []
        
        # 將結果轉換為DataFrame以便分析
        self.dataframes = {}
        if self.results:
            for strategy, strategy_results in self.results.items():
                self.dataframes[strategy] = pd.DataFrame(strategy_results)
    
    def calculate_statistics(self, strategy: Optional[int] = None) -> Dict[str, Any]:
        """
        計算特定策略的統計數據
        
        Args:
            strategy: 要分析的策略，如不指定則計算所有策略的合併統計
            
        Returns:
            包含統計數據的字典
        """
        if strategy is not None:
            # 分析單一策略
            if strategy not in self.dataframes:
                logging.warning(f"無結果找到（策略 {strategy}）")
                # 返回默認值
                return {
                    'count': 0,
                    'bust_count': 0,
                    'bust_rate': 0.0,
                    'mean': 0.0,
                    'median': 0.0,
                    'std': 0.0,
                    'min': 0,
                    'max': 0,
                    'percentile_25': 0.0,
                    'percentile_75': 0.0,
                    'value_counts': {}
                }
            df = self.dataframes[strategy]
        else:
            # 分析所有策略
            if not self.dataframes:
                logging.warning("無結果數據可分析")
                return {
                    'count': 0,
                    'bust_count': 0,
                    'bust_rate': 0.0,
                    'mean': 0.0,
                    'median': 0.0,
                    'std': 0.0,
                    'min': 0,
                    'max': 0,
                    'percentile_25': 0.0,
                    'percentile_75': 0.0,
                    'value_counts': {}
                }
            df = pd.concat(list(self.dataframes.values()))
        
        # 計算統計數據
        stats = {
            'count': len(df),
            'bust_count': df['is_dealer_busted'].sum(),
            'bust_rate': df['is_dealer_busted'].mean(),
            'mean': df['dealer_hand_value'].mean(),
            'median': df['dealer_hand_value'].median(),
            'std': df['dealer_hand_value'].std(),
            'min': df['dealer_hand_value'].min(),
            'max': df['dealer_hand_value'].max(),
            # 百分位數
            'percentile_25': df['dealer_hand_value'].quantile(0.25),
            'percentile_75': df['dealer_hand_value'].quantile(0.75),
            # 點數分布
            'value_counts': df['dealer_hand_value'].value_counts().sort_index().to_dict()
        }
        
        return stats
    
    def get_distribution(self, strategy: int) -> Dict[int, int]:
        """
        獲取特定策略的點數分布
        
        Args:
            strategy: 要分析的策略
            
        Returns:
            點數到局數的映射字典，若策略不存在則返回空字典
        """
        if strategy not in self.dataframes:
            logging.warning(f"無結果找到（策略 {strategy}）")
            return {}
        
        df = self.dataframes[strategy]
        return df['dealer_hand_value'].value_counts().sort_index().to_dict()
    
    def get_all_distributions(self) -> Dict[int, Dict[int, int]]:
        """
        獲取所有策略的點數分布
        
        Returns:
            策略到點數分布的嵌套字典
        """
        distributions = {}
        for strategy in self.strategies:
            distributions[strategy] = self.get_distribution(strategy)
        return distributions
    
    def compare_strategies(self) -> pd.DataFrame:
        """
        比較不同策略的關鍵指標
        
        Returns:
            包含各策略關鍵指標的DataFrame
        """
        if not self.strategies:
            logging.warning("沒有策略可比較")
            return pd.DataFrame()
            
        comparison = []
        for strategy in self.strategies:
            stats = self.calculate_statistics(strategy)
            comparison.append({
                'strategy': strategy,
                'sample_size': stats['count'],
                'bust_rate': stats['bust_rate'],
                'mean_value': stats['mean'],
                'median_value': stats['median'],
                'std_dev': stats['std']
            })
        
        return pd.DataFrame(comparison) 