#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.utils.logger import Logger
from blackpiyan.simulation.simulator import Simulator
from blackpiyan.analysis.analyzer import Analyzer
from blackpiyan.visualization.visualizer import Visualizer

def main():
    """主程序入口"""
    # 載入配置
    config_path = 'configs/default.yaml'
    if not os.path.exists(config_path):
        print(f"錯誤: 找不到配置文件 {config_path}")
        sys.exit(1)
    
    config_manager = ConfigManager(config_path)
    config = config_manager.get_config()
    
    # 初始化日誌
    logger = Logger(config).get_logger("main")
    logger.info("開始BlackPiyan模擬")
    
    # 獲取模擬配置
    strategies = config.get('simulation', {}).get('strategies', [16, 17, 18])
    min_games = config.get('simulation', {}).get('min_games_per_strategy', 1000)
    
    logger.info(f"將模擬策略: {strategies}，每種策略 {min_games} 局")
    
    # 執行模擬
    start_time = time.time()
    simulator = Simulator(config)
    results = simulator.run_multiple_strategies(strategies, min_games)
    
    # 分析結果
    logger.info("模擬完成，開始分析結果")
    analyzer = Analyzer(results)
    
    # 輸出基本統計
    for strategy in strategies:
        stats = analyzer.calculate_statistics(strategy)
        logger.info(f"策略 {strategy} 統計:")
        logger.info(f"  總局數: {stats['count']}")
        logger.info(f"  爆牌率: {stats['bust_rate']*100:.2f}%")
        logger.info(f"  平均點數: {stats['mean']:.2f}")
        logger.info(f"  中位數點數: {stats['median']}")
    
    # 比較策略
    comparison = analyzer.compare_strategies()
    logger.info(f"策略比較: \n{comparison}")
    
    # 生成視覺化
    logger.info("生成視覺化圖表")
    visualizer = Visualizer(analyzer, config)
    
    # 為每個策略生成分布圖
    for strategy in strategies:
        visualizer.plot_distribution(strategy)
    
    # 生成策略比較圖
    visualizer.plot_comparison()
    
    elapsed_time = time.time() - start_time
    logger.info(f"模擬和分析完成，總用時: {elapsed_time:.2f} 秒")
    logger.info(f"結果圖表已保存到 {config.get('output', {}).get('charts_dir', 'results/charts')}")

if __name__ == "__main__":
    main() 