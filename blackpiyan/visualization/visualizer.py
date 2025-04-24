from typing import Dict, Any, List, Optional
import os
import platform
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import logging

from blackpiyan.analysis.analyzer import Analyzer
from blackpiyan.utils.font_manager import FontManager

# 獲取日誌記錄器
logger = logging.getLogger(__name__)

class Visualizer:
    """視覺化類，用於生成21點模擬分析圖表"""
    
    def __init__(self, analyzer: Analyzer, config: Optional[Dict[str, Any]] = None):
        """
        初始化視覺化器
        
        Args:
            analyzer: 分析器實例
            config: 配置字典
        """
        self.analyzer = analyzer
        self.config = config or {}
        
        # 初始化字體管理器
        self.font_manager = FontManager()
        self.font_manager.configure_matplotlib()
        
        # 設置圖表風格
        sns.set_style("whitegrid")
        
        # 圖表輸出目錄
        self.charts_dir = self.config.get('output', {}).get('charts_dir', 'results/charts')
        os.makedirs(self.charts_dir, exist_ok=True)
    
    def plot_distribution(self, strategy: int, save_path: Optional[str] = None) -> None:
        """
        繪製單一策略的點數分布圖
        
        Args:
            strategy: 要繪製的策略
            save_path: 保存圖表的路徑，如果為None則使用默認路徑
        """
        # 獲取點數分布
        distribution = self.analyzer.get_distribution(strategy)
        
        # 轉換為DataFrame以便繪圖
        df = pd.DataFrame({
            'hand_value': list(distribution.keys()),
            'count': list(distribution.values())
        })
        
        # 計算爆牌率
        stats = self.analyzer.calculate_statistics(strategy)
        bust_rate = stats['bust_rate'] * 100
        
        # 設置圖表尺寸
        plt.figure(figsize=(12, 6))
        
        # 繪製柱狀圖，區分爆牌和非爆牌
        ax = sns.barplot(
            x='hand_value', 
            y='count', 
            data=df,
            hue='hand_value',
            palette=['red' if x > 21 else 'steelblue' for x in df['hand_value']],
            legend=False
        )
        
        # 添加標題和標籤
        plt.title(f"莊家點數分布 (補到 {strategy} 點停牌，爆牌率: {bust_rate:.2f}%)", 
                 fontsize=16, fontproperties=self.font_manager.get_font_properties(16))
        plt.xlabel("手牌點數", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        plt.ylabel("局數", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        
        # 為每個柱添加數字標籤
        for p in ax.patches:
            ax.annotate(
                f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=10
            )
        
        # 添加中位數和平均值線
        median_value = stats['median']
        median_index = np.abs(np.array(df['hand_value']) - median_value).argmin()
        plt.axvline(x=median_index, color='green', linestyle='--', 
                   label=f"中位數: {median_value}")
        
        # 查找最接近平均值的索引
        mean_value = stats['mean']
        mean_index = np.abs(np.array(df['hand_value']) - mean_value).argmin()
        plt.axvline(x=mean_index, color='purple', linestyle=':', 
                   label=f"平均值: {mean_value:.2f}")
        
        # 設置圖例字體
        plt.legend(prop=self.font_manager.get_font_properties())
        plt.tight_layout()
        
        # 保存圖表
        if save_path is None:
            save_path = os.path.join(self.charts_dir, f"strategy_{strategy}_distribution.png")
        
        plt.savefig(save_path, dpi=300)
        plt.close()
    
    def plot_comparison(self, save_path: Optional[str] = None) -> None:
        """
        繪製不同策略的比較圖
        
        Args:
            save_path: 保存圖表的路徑，如果為None則使用默認路徑
        """
        # 獲取比較數據
        comparison_df = self.analyzer.compare_strategies()
        
        # 創建子圖
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 爆牌率比較
        sns.barplot(x='strategy', y='bust_rate', data=comparison_df, ax=axes[0, 0])
        axes[0, 0].set_title("不同策略的爆牌率比較", fontsize=16, fontproperties=self.font_manager.get_font_properties(16))
        axes[0, 0].set_xlabel("策略 (補到X點停牌)", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        axes[0, 0].set_ylabel("爆牌率", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        
        # 為每個柱添加百分比標籤
        for p in axes[0, 0].patches:
            axes[0, 0].annotate(
                f'{p.get_height()*100:.2f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12
            )
        
        # 平均點數比較
        sns.barplot(x='strategy', y='mean_value', data=comparison_df, ax=axes[0, 1])
        axes[0, 1].set_title("不同策略的平均點數比較", fontsize=16, fontproperties=self.font_manager.get_font_properties(16))
        axes[0, 1].set_xlabel("策略 (補到X點停牌)", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        axes[0, 1].set_ylabel("平均點數", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        
        # 為每個柱添加數值標籤
        for p in axes[0, 1].patches:
            axes[0, 1].annotate(
                f'{p.get_height():.2f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12
            )
        
        # 點數分布比較
        distributions = self.analyzer.get_all_distributions()
        
        # 將所有分布合併到一個DataFrame中以便繪圖
        distribution_data = []
        for strategy, dist in distributions.items():
            for hand_value, count in dist.items():
                distribution_data.append({
                    'strategy': f'補到{strategy}點停',
                    'hand_value': hand_value,
                    'count': count
                })
        
        dist_df = pd.DataFrame(distribution_data)
        
        # 分布比較 - 只顯示特定範圍的點數
        plot_df = dist_df[dist_df['hand_value'].between(16, 26)]
        sns.lineplot(
            x='hand_value', 
            y='count', 
            hue='strategy', 
            data=plot_df, 
            markers=True, 
            dashes=False,
            ax=axes[1, 0]
        )
        
        axes[1, 0].set_title("不同策略的點數分布比較 (16-26點)", fontsize=16, fontproperties=self.font_manager.get_font_properties(16))
        axes[1, 0].set_xlabel("手牌點數", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        axes[1, 0].set_ylabel("局數", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        
        # 設置圖例字體
        legend = axes[1, 0].legend(title="策略")
        plt.setp(legend.get_title(), fontproperties=self.font_manager.get_font_properties())
        plt.setp(legend.get_texts(), fontproperties=self.font_manager.get_font_properties())
        
        # 標準差比較
        sns.barplot(x='strategy', y='std_dev', data=comparison_df, ax=axes[1, 1])
        axes[1, 1].set_title("不同策略的點數標準差比較", fontsize=16, fontproperties=self.font_manager.get_font_properties(16))
        axes[1, 1].set_xlabel("策略 (補到X點停牌)", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        axes[1, 1].set_ylabel("標準差", fontsize=14, fontproperties=self.font_manager.get_font_properties(14))
        
        # 為每個柱添加數值標籤
        for p in axes[1, 1].patches:
            axes[1, 1].annotate(
                f'{p.get_height():.2f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12
            )
        
        plt.tight_layout()
        
        # 保存圖表
        if save_path is None:
            save_path = os.path.join(self.charts_dir, "strategy_comparison.png")
        
        plt.savefig(save_path, dpi=300)
        plt.close() 