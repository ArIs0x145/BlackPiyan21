from typing import Dict, Any, List, Optional
import time

from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.game.blackjack import BlackjackGame
from blackpiyan.utils.logger import Logger

class Simulator:
    """模擬器類，用於運行大量21點遊戲並收集數據"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化模擬器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.logger = Logger(config).get_logger(__name__)
        self.game = BlackjackGame(config)
    
    def run_simulation(self, strategy_value: int, num_games: int) -> List[Dict[str, Any]]:
        """
        使用指定策略運行多局遊戲
        
        Args:
            strategy_value: 莊家補牌策略值
            num_games: 要運行的遊戲局數
            
        Returns:
            遊戲結果列表
        """
        self.logger.info(f"開始模擬策略 {strategy_value}，共 {num_games} 局")
        start_time = time.time()
        
        # 設置莊家策略
        self.game.set_dealer_strategy(strategy_value)
        
        # 運行模擬並收集結果
        results = []
        for i in range(num_games):
            result = self.game.play_single_round()
            results.append({
                'strategy': strategy_value,
                'game_id': i + 1,
                'dealer_hand_value': result['dealer_hand_value'],
                'is_dealer_busted': result['is_dealer_busted']
            })
            
            # 每1000局記錄進度
            if (i + 1) % 1000 == 0:
                self.logger.debug(f"策略 {strategy_value} 已完成 {i + 1} 局")
        
        elapsed_time = time.time() - start_time
        self.logger.info(f"策略 {strategy_value} 模擬完成，用時 {elapsed_time:.2f} 秒")
        
        return results
    
    def run_multiple_strategies(self, strategies: List[int], games_per_strategy: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        模擬多個策略
        
        Args:
            strategies: 要測試的補牌策略列表
            games_per_strategy: 每個策略要模擬的局數
            
        Returns:
            策略映射到結果列表的字典
        """
        results = {}
        
        for strategy in strategies:
            self.logger.info(f"模擬策略 {strategy}")
            strategy_results = self.run_simulation(strategy, games_per_strategy)
            results[strategy] = strategy_results
            
            # 重置遊戲狀態，準備下一個策略
            self.game.reset()
        
        return results 