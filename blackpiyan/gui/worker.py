#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal, Slot
import time
import logging
import traceback
import copy

# 導入核心類
from blackpiyan.simulation.simulator import Simulator

class SimulationWorker(QObject):
    """模擬工作線程類，用於在背景執行模擬任務"""
    
    # 信號定義
    finished = Signal()              # 任務完成信號
    result_ready = Signal(object)    # 結果準備好信號 (傳遞結果字典或錯誤信息)
    progress = Signal(int, str)      # 進度更新信號 (百分比, 狀態消息)
    error_signal = Signal(str, str)  # 錯誤信號 (錯誤標題, 錯誤詳情)
    intermediate_result = Signal(object, int)  # 中間結果信號 (部分結果字典, 當前策略)

    def __init__(self, config):
        """
        初始化工作線程
        
        Args:
            config: 模擬配置字典
        """
        super().__init__()
        self.config = config
        self._is_running = True
        self._stop_requested = False
        self.logger = logging.getLogger(__name__)
        self.results = None  # 添加 results 屬性用於儲存模擬結果
        
        # 從配置中獲取實時更新設置
        self._setup_realtime_update_config()
        
        # 累積的模擬結果
        self.accumulated_results = {}

    def _setup_realtime_update_config(self):
        """設置實時更新配置"""
        # 默認值
        self.realtime_update_enabled = True
        self.update_interval = 100
        self.min_update_interval = 50
        self.max_update_interval = 500
        self.auto_adjust = True
        
        # 從配置讀取，如果存在
        if 'simulation' in self.config and 'realtime_update' in self.config['simulation']:
            rt_config = self.config['simulation']['realtime_update']
            
            if 'enabled' in rt_config:
                self.realtime_update_enabled = rt_config['enabled']
                
            if 'update_interval' in rt_config:
                self.update_interval = rt_config['update_interval']
                
            if 'min_update_interval' in rt_config:
                self.min_update_interval = rt_config['min_update_interval']
                
            if 'max_update_interval' in rt_config:
                self.max_update_interval = rt_config['max_update_interval']
                
            if 'auto_adjust' in rt_config:
                self.auto_adjust = rt_config['auto_adjust']
        
        self.logger.info(f"實時更新設置: 啟用={self.realtime_update_enabled}, "
                        f"更新間隔={self.update_interval}, 自動調整={self.auto_adjust}")

    def _calculate_update_interval(self, total_games):
        """
        根據總局數計算合適的更新間隔
        
        Args:
            total_games: 總模擬局數
            
        Returns:
            計算後的更新間隔
        """
        if not self.auto_adjust:
            return self.update_interval
            
        # 自動調整邏輯: 總局數越大，更新間隔越大
        # 但確保更新間隔在最小和最大值之間
        # 使用總局數的平方根來進行調整，這樣大規模模擬時不會更新過於頻繁
        adjusted_interval = int(self.update_interval * (total_games / 1000) ** 0.5)
        
        # 限制在配置的範圍內
        adjusted_interval = max(self.min_update_interval, 
                              min(self.max_update_interval, adjusted_interval))
        
        self.logger.debug(f"自動調整更新間隔: 總局數={total_games}, 調整後間隔={adjusted_interval}")
        return adjusted_interval

    @Slot()
    def run(self):
        """主工作方法，執行模擬任務"""
        self.logger.info("工作線程啟動，開始模擬...")
        results = {}
        error_message = None
        try:
            simulator = Simulator(self.config)  # 在線程內創建Simulator實例
            strategies = self.config['simulation']['strategies']
            games_per_strategy = self.config['simulation']['min_games_per_strategy']
            sim_time_seconds = self.config.get('simulation', {}).get('sim_time_seconds', 10)
            total_strategies = len(strategies)
            
            # 計算本次模擬總局數，用於自動調整更新間隔
            total_games = games_per_strategy * total_strategies
            update_interval = self._calculate_update_interval(total_games)
            self.logger.info(f"總模擬局數: {total_games}, 實時更新間隔: {update_interval}, 目標模擬時間: {sim_time_seconds}秒")

            for i, strategy in enumerate(strategies):
                if self._stop_requested:
                    self.logger.info(f"檢測到停止請求，終止策略 {strategy} 的模擬。")
                    error_message = "用戶請求停止"
                    break

                self.logger.info(f"線程: 開始模擬策略 {strategy}")
                strategy_progress_base = (i / total_strategies) * 100
                strategy_progress_step = 100 / total_strategies
                self.progress.emit(int(strategy_progress_base), f"正在模擬策略 {strategy}...")

                # 初始化此策略的結果列表
                results[strategy] = []
                self.accumulated_results[strategy] = []
                
                try:
                    # 計算每個策略的目標模擬時間
                    strategy_sim_time = sim_time_seconds / total_strategies
                    start_time = time.time()
                    
                    # 計算基於目標時間的批次大小
                    batch_count = max(20, min(100, int(games_per_strategy / 20)))  # 至少分成20批，最多100批
                    base_batch_size = max(10, games_per_strategy // batch_count)
                    
                    # 初始化模擬進度
                    completed_games = 0
                    last_update_time = time.time()
                    
                    # 計算每批次應該的時間
                    time_per_batch = strategy_sim_time / batch_count
                    
                    for batch_num in range(batch_count):
                        if self._stop_requested:
                            break
                        
                        # 計算本批次應該模擬的局數
                        remaining = games_per_strategy - completed_games
                        if batch_num == batch_count - 1:  # 最後一批
                            current_batch = remaining
                        else:
                            current_batch = min(base_batch_size, remaining)
                        
                        # 記錄批次開始時間
                        batch_start = time.time()
                        
                        # 執行一批模擬
                        batch_results = simulator.run_simulation(strategy, current_batch)
                        results[strategy].extend(batch_results)
                        self.accumulated_results[strategy].extend(batch_results)
                        completed_games += current_batch
                        
                        # 計算批次耗時
                        batch_elapsed = time.time() - batch_start
                        
                        # 計算並發送進度
                        batch_progress = completed_games / games_per_strategy * strategy_progress_step
                        current_progress = int(strategy_progress_base + batch_progress)
                        self.progress.emit(current_progress, 
                                         f"策略 {strategy}: 已完成 {completed_games}/{games_per_strategy} 局")
                        
                        # 發送中間結果用於實時顯示
                        if self.realtime_update_enabled and len(self.accumulated_results[strategy]) > 0:
                            # 檢查是否需要更新 (避免過於頻繁的更新)
                            current_time = time.time()
                            time_since_last_update = current_time - last_update_time
                            
                            # 至少間隔0.5秒發送一次更新，避免GUI過載
                            if time_since_last_update >= 0.5:
                                # 創建當前累積結果的副本以避免競態條件
                                intermediate_data = copy.deepcopy(self.accumulated_results)
                                self.intermediate_result.emit(intermediate_data, strategy)
                                last_update_time = current_time
                                self.logger.debug(f"發送實時更新: 策略={strategy}, 已完成={completed_games}")
                        
                        # 調整速度以符合目標時間
                        # 如果批次執行太快，則等待一段時間
                        if batch_elapsed < time_per_batch and batch_num < batch_count - 1:
                            sleep_time = time_per_batch - batch_elapsed
                            time.sleep(sleep_time)
                            self.logger.debug(f"批次{batch_num}執行時間{batch_elapsed:.3f}秒，休眠{sleep_time:.3f}秒")
                    
                    # 最後一次更新，確保顯示最終結果
                    if self.realtime_update_enabled:
                        intermediate_data = copy.deepcopy(self.accumulated_results)
                        self.intermediate_result.emit(intermediate_data, strategy)
                    
                    # 計算實際耗時
                    strategy_elapsed = time.time() - start_time
                    self.logger.info(f"策略 {strategy} 模擬完成, 實際耗時: {strategy_elapsed:.2f}秒 (目標: {strategy_sim_time:.2f}秒)")
                    
                    # 更新進度
                    strategy_progress = strategy_progress_base + strategy_progress_step
                    self.progress.emit(int(strategy_progress), f"策略 {strategy} 模擬完成")
                    self.logger.info(f"線程: 策略 {strategy} 模擬完成")
                    
                except Exception as e:
                    # 捕獲單個策略模擬中的錯誤
                    error_detail = traceback.format_exc()
                    error_msg = f"模擬策略 {strategy} 時出錯: {str(e)}"
                    self.logger.exception(error_msg)
                    self.error_signal.emit(f"模擬策略 {strategy} 錯誤", f"{error_msg}\n\n{error_detail}")
                    # 繼續模擬其他策略
                    continue

            if not self._stop_requested:
                 self.progress.emit(100, "所有模擬完成")

        except Exception as e:
            error_detail = traceback.format_exc()
            error_msg = f"模擬過程中發生錯誤: {str(e)}"
            self.logger.exception(error_msg)
            self.error_signal.emit("模擬錯誤", f"{error_msg}\n\n{error_detail}")
            error_message = error_msg
            results = None  # 出錯時不返回部分結果

        finally:
            self._is_running = False
            # 儲存結果到實例變數
            self.results = results
            # 發送結果或錯誤信息
            self.result_ready.emit(results if error_message is None else error_message)
            self.finished.emit()
            self.logger.info("工作線程結束。")

    def request_stop(self):
        """請求停止模擬任務"""
        self.logger.info("收到停止請求")
        self._stop_requested = True 