"""測試21點模擬功能"""

import os
import unittest
import tempfile
import shutil
from pathlib import Path

from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.game.blackjack import BlackjackGame
from blackpiyan.simulation.simulator import Simulator
from blackpiyan.analysis.analyzer import Analyzer
from blackpiyan.visualization.visualizer import Visualizer

class TestSimulation(unittest.TestCase):
    """測試模擬功能"""
    
    def setUp(self):
        """設置測試環境"""
        # 使用測試配置
        self.config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
        self.config_manager = ConfigManager(self.config_path)
        self.config = self.config_manager.get_config()
        
        # 創建臨時目錄用於測試輸出
        self.temp_dir = tempfile.mkdtemp()
        self.config['output']['data_dir'] = os.path.join(self.temp_dir, 'data')
        self.config['output']['charts_dir'] = os.path.join(self.temp_dir, 'charts')
        
        # 創建輸出目錄
        os.makedirs(self.config['output']['data_dir'], exist_ok=True)
        os.makedirs(self.config['output']['charts_dir'], exist_ok=True)
    
    def tearDown(self):
        """清理測試環境"""
        # 移除臨時目錄
        shutil.rmtree(self.temp_dir)
    
    def test_blackjack_game(self):
        """測試21點遊戲類"""
        game = BlackjackGame(self.config)
        
        # 測試默認設置
        self.assertEqual(game.dealer.hit_until_value, 17)
        
        # 設置不同的策略
        game.set_dealer_strategy(16)
        self.assertEqual(game.get_dealer_strategy(), 16)
        
        # 測試單局遊戲
        result = game.play_single_round()
        self.assertIn('dealer_hand', result)
        self.assertIn('dealer_hand_value', result)
        self.assertIn('is_dealer_busted', result)
        
        # 重置遊戲
        game.reset()
    
    def test_simulator(self):
        """測試模擬器"""
        simulator = Simulator(self.config)
        
        # 測試單一策略模擬
        num_games = 10
        strategy = 17
        results = simulator.run_simulation(strategy, num_games)
        
        # 檢查模擬結果
        self.assertEqual(len(results), num_games)
        for result in results:
            self.assertEqual(result['strategy'], strategy)
            self.assertIn('game_id', result)
            self.assertIn('dealer_hand_value', result)
            self.assertIn('is_dealer_busted', result)
        
        # 測試多策略模擬
        strategies = [16, 17]
        all_results = simulator.run_multiple_strategies(strategies, num_games)
        
        # 檢查每個策略的結果
        self.assertEqual(len(all_results), len(strategies))
        for strategy in strategies:
            self.assertIn(strategy, all_results)
            self.assertEqual(len(all_results[strategy]), num_games)
    
    def test_analyzer(self):
        """測試分析器"""
        # 先跑模擬產生數據
        simulator = Simulator(self.config)
        strategies = [16, 17]
        results = simulator.run_multiple_strategies(strategies, 10)
        
        # 創建分析器
        analyzer = Analyzer(results)
        
        # 測試基本統計
        for strategy in strategies:
            stats = analyzer.calculate_statistics(strategy)
            self.assertIn('count', stats)
            self.assertIn('bust_rate', stats)
            self.assertIn('mean', stats)
            self.assertIn('median', stats)
            self.assertIn('value_counts', stats)
        
        # 測試分布獲取
        for strategy in strategies:
            dist = analyzer.get_distribution(strategy)
            self.assertIsInstance(dist, dict)
        
        # 測試所有分布獲取
        all_dist = analyzer.get_all_distributions()
        self.assertEqual(len(all_dist), len(strategies))
        
        # 測試策略比較
        comparison = analyzer.compare_strategies()
        self.assertEqual(len(comparison), len(strategies))
    
    def test_visualizer(self):
        """測試視覺化器"""
        # 先跑模擬產生數據
        simulator = Simulator(self.config)
        strategies = [16, 17]
        results = simulator.run_multiple_strategies(strategies, 10)
        
        # 創建分析器
        analyzer = Analyzer(results)
        
        # 創建視覺化器
        visualizer = Visualizer(analyzer, self.config)
        
        # 測試單一策略分布圖
        for strategy in strategies:
            output_path = os.path.join(self.config['output']['charts_dir'], f"test_{strategy}.png")
            visualizer.plot_distribution(strategy, output_path)
            self.assertTrue(os.path.exists(output_path))
        
        # 測試比較圖
        comparison_path = os.path.join(self.config['output']['charts_dir'], "test_comparison.png")
        visualizer.plot_comparison(comparison_path)
        self.assertTrue(os.path.exists(comparison_path))

class TestEndToEnd(unittest.TestCase):
    """端到端測試完整流程"""
    
    def setUp(self):
        """設置測試環境"""
        # 使用測試配置
        self.config_path = os.path.join(os.path.dirname(__file__), 'test_config.yaml')
        self.config_manager = ConfigManager(self.config_path)
        self.config = self.config_manager.get_config()
        
        # 創建臨時目錄用於測試輸出
        self.temp_dir = tempfile.mkdtemp()
        self.config['output']['data_dir'] = os.path.join(self.temp_dir, 'data')
        self.config['output']['charts_dir'] = os.path.join(self.temp_dir, 'charts')
        
        # 創建輸出目錄
        os.makedirs(self.config['output']['data_dir'], exist_ok=True)
        os.makedirs(self.config['output']['charts_dir'], exist_ok=True)
    
    def tearDown(self):
        """清理測試環境"""
        # 移除臨時目錄
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """測試完整流程，從模擬到視覺化"""
        # 獲取設置
        strategies = self.config['simulation']['strategies']
        games_per_strategy = 5  # 使用較少的局數加速測試
        
        # 模擬
        simulator = Simulator(self.config)
        results = simulator.run_multiple_strategies(strategies, games_per_strategy)
        
        # 分析
        analyzer = Analyzer(results)
        
        # 生成視覺化
        visualizer = Visualizer(analyzer, self.config)
        
        # 檢查每個策略的輸出
        for strategy in strategies:
            visualizer.plot_distribution(strategy)
            output_path = os.path.join(self.config['output']['charts_dir'], f"strategy_{strategy}_distribution.png")
            self.assertTrue(os.path.exists(output_path))
        
        # 檢查比較圖
        visualizer.plot_comparison()
        output_path = os.path.join(self.config['output']['charts_dir'], "strategy_comparison.png")
        self.assertTrue(os.path.exists(output_path))
        
        # 檢查輸出內容
        chart_files = os.listdir(self.config['output']['charts_dir'])
        self.assertEqual(len(chart_files), len(strategies) + 1)  # 每個策略一個圖 + 一個比較圖

if __name__ == "__main__":
    unittest.main() 