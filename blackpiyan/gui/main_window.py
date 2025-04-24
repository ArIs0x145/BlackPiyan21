#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import matplotlib.pyplot as plt
import traceback
import time
import os

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Signal, Slot, QThread, QObject
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem

# 導入生成的UI類
from .ui_main_window import Ui_MainWindow
# 導入Matplotlib嵌入類
from .mpl_canvas import MplCanvas, NavigationToolbar
# 導入工作線程類
from .worker import SimulationWorker

# 導入BlackPiyan核心類
from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.analysis.analyzer import Analyzer
from blackpiyan.utils.font_manager import FontManager

# --- 日誌處理器 ---
class QtLogHandler(logging.Handler, QObject):
    """將日誌重定向到Qt文本控件的處理器"""
    
    log_signal = Signal(str)

    def __init__(self, parent):
        logging.Handler.__init__(self)
        QObject.__init__(self)
        self.parent_widget = parent
        self.log_signal.connect(self.parent_widget.append_log)  # 連接到主窗口的槽

    def emit(self, record):
        """發送日誌記錄"""
        msg = self.format(record)
        self.log_signal.emit(msg)


# --- 主窗口類 ---
class BlackPiyanGUI(QMainWindow):
    """BlackPiyan GUI 主窗口"""
    
    # 定義信號
    simulation_complete = Signal(object)   # 模擬完成信號
    progress_update = Signal(int, str)     # 進度更新信號 (百分比, 狀態消息)
    error_occurred = Signal(str, str)      # 錯誤信號 (錯誤標題, 錯誤詳情)

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 加載配置
        try:
            self.config_manager = ConfigManager('configs/default.yaml')
            self.config = self.config_manager.get_config()
        except Exception as e:
            QMessageBox.critical(self, "配置加載錯誤", f"無法加載配置文件: {e}")
            self.config = {'simulation': {'min_games_per_strategy': 1000, 'strategies': [16, 17, 18]},
                           'game': {'decks': 6, 'reshuffle_threshold': 0.4}}

        # 初始化字體管理器
        self.font_manager = FontManager()
        
        # 設置應用程序字體
        app = QApplication.instance()
        if app:
            app.setFont(self.font_manager.get_qt_font())

        # 設置應用程序圖標
        try:
            # 使用絕對路徑獲取圖標
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "resources", "icons", "piyan.ico")
            
            if os.path.exists(icon_path):
                self.setWindowIcon(QtGui.QIcon(icon_path))
                logging.info(f"已設置窗口圖標: {icon_path}")
            else:
                logging.warning(f"圖標文件不存在: {icon_path}")
        except Exception as e:
            logging.warning(f"設置應用程序圖標時出錯: {str(e)}")

        # 初始化UI組件
        self.setup_matplotlib_widgets()
        self.setup_logging()
        self.load_initial_config()

        # 連接信號和槽
        self.connect_signals()

        # 初始化狀態
        self.worker_thread = None
        self.simulator_worker = None
        self.ui.stopButton.setEnabled(False)
        
        # 設置窗口標題
        self.setWindowTitle(f"BlackPiyan v1.0.0")
        
        # 更新狀態欄
        self.ui.statusbar.showMessage("就緒")
        
        # 安裝全局異常處理器
        self.install_global_exception_handler()

    def setup_matplotlib_widgets(self):
        """設置 Matplotlib 圖表控件"""
        # 配置 Matplotlib 字體
        self.font_manager.configure_matplotlib()
        
        # 為分佈圖創建Canvas
        self.dist_canvas = MplCanvas(self.ui.distributionPlotWidget, width=5, height=4, dpi=100)
        dist_layout = QtWidgets.QVBoxLayout()
        dist_layout.addWidget(self.dist_canvas)
        # 添加導航工具欄（可選）
        self.dist_toolbar = NavigationToolbar(self.dist_canvas, self)
        dist_layout.addWidget(self.dist_toolbar)
        self.ui.distributionPlotWidget.setLayout(dist_layout)

        # 為策略比較頁創建Canvas
        self.comp_canvas = MplCanvas(self.ui.comparisonTabPlotWidget, width=5, height=4, dpi=100)
        comp_layout = QtWidgets.QVBoxLayout()
        comp_layout.addWidget(self.comp_canvas)
        # 添加導航工具欄（可選）
        self.comp_toolbar = NavigationToolbar(self.comp_canvas, self)
        comp_layout.addWidget(self.comp_toolbar)
        self.ui.comparisonTabPlotWidget.setLayout(comp_layout)
        
        # 初始化繪圖區域
        self.dist_canvas.axes.text(0.5, 0.5, '尚無數據', 
                                  horizontalalignment='center', 
                                  verticalalignment='center',
                                  fontsize=14)
        self.comp_canvas.axes.text(0.5, 0.5, '尚無數據', 
                                  horizontalalignment='center',
                                  verticalalignment='center',
                                  fontsize=14)
        self.dist_canvas.draw()
        self.comp_canvas.draw()

    def setup_logging(self):
        """設置日誌處理"""
        # 獲取根logger
        log = logging.getLogger()  # 獲取根logger
        # 創建Qt Handler
        self.log_handler = QtLogHandler(self)
        # 設置格式
        log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.log_handler.setFormatter(log_format)
        # 添加Handler
        log.addHandler(self.log_handler)
        # 設置級別
        log.setLevel(logging.INFO)
        self.log_handler.setLevel(logging.INFO)
        
        # 添加第一條日誌
        self.append_log("BlackPiyan GUI 初始化完成，系統就緒。")

    def load_initial_config(self):
        """從配置加載初始值到UI控件"""
        sim_config = self.config.get('simulation', {})
        game_config = self.config.get('game', {})

        # 設置模擬參數
        self.ui.gamesSpinBox.setValue(sim_config.get('min_games_per_strategy', 1000))
        strategies_str = ", ".join(map(str, sim_config.get('strategies', [16, 17, 18])))
        self.ui.strategiesLineEdit.setText(strategies_str)
        
        # 設置牌庫參數
        self.ui.decksSpinBox.setValue(game_config.get('decks', 6))
        self.ui.reshuffleSpinBox.setValue(game_config.get('reshuffle_threshold', 0.4))
        
        # 設置實時更新參數
        realtime_config = sim_config.get('realtime_update', {})
        if 'enabled' in realtime_config:
            self.ui.realtimeUpdateCheck.setChecked(realtime_config.get('enabled', True))
        if 'update_interval' in realtime_config:
            self.ui.updateIntervalSpinBox.setValue(realtime_config.get('update_interval', 100))
        if 'auto_adjust' in realtime_config:
            self.ui.autoAdjustCheck.setChecked(realtime_config.get('auto_adjust', True))

    def connect_signals(self):
        """連接信號和槽"""
        # 按鈕點擊
        self.ui.runButton.clicked.connect(self.start_simulation)
        self.ui.stopButton.clicked.connect(self.stop_simulation)
        self.ui.resetButton.clicked.connect(self.reset_parameters)
        
        # 實時更新設置變化
        self.ui.realtimeUpdateCheck.stateChanged.connect(self.update_realtime_config)
        self.ui.autoAdjustCheck.stateChanged.connect(self.update_realtime_config)
        self.ui.updateIntervalSpinBox.valueChanged.connect(self.update_realtime_config)
        
        # 菜單動作
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.show_about_dialog)
        
        # 策略選擇下拉框變更
        self.ui.strategyDistCombo.currentIndexChanged.connect(self.update_distribution_plot)
        
        # 自定義信號
        self.simulation_complete.connect(self.handle_simulation_results)
        self.progress_update.connect(self.update_progress)
        self.error_occurred.connect(self.handle_error)

    @Slot(str)
    def append_log(self, message):
        """添加日誌到日誌文本框"""
        self.ui.logTextEdit.append(message)
        # 自動滾動到底部
        scrollbar = self.ui.logTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot()
    def update_realtime_config(self):
        """當UI中的實時更新設置變化時更新配置"""
        if not hasattr(self, 'config'):
            return
            
        # 確保配置中有必要的節點
        if 'simulation' not in self.config:
            self.config['simulation'] = {}
        if 'realtime_update' not in self.config['simulation']:
            self.config['simulation']['realtime_update'] = {}
            
        # 更新配置
        rt_config = self.config['simulation']['realtime_update']
        rt_config['enabled'] = self.ui.realtimeUpdateCheck.isChecked()
        rt_config['update_interval'] = self.ui.updateIntervalSpinBox.value()
        rt_config['auto_adjust'] = self.ui.autoAdjustCheck.isChecked()
        
        # 調整UI狀態
        self.ui.updateIntervalSpinBox.setEnabled(self.ui.realtimeUpdateCheck.isChecked())
        self.ui.autoAdjustCheck.setEnabled(self.ui.realtimeUpdateCheck.isChecked())
        
        # 記錄變更
        self.append_log(f"更新實時配置: 啟用={rt_config['enabled']}, "
                       f"間隔={rt_config['update_interval']}, "
                       f"自動調整={rt_config['auto_adjust']}")

    def get_parameters_from_ui(self):
        """從UI控件獲取參數"""
        params = {}
        try:
            # 獲取模擬參數
            params['min_games_per_strategy'] = self.ui.gamesSpinBox.value()
            
            # 解析策略列表
            strategies_text = self.ui.strategiesLineEdit.text()
            strategies = []
            for s in strategies_text.split(','):
                if s.strip():
                    strategies.append(int(s.strip()))
            params['strategies'] = strategies
            
            # 獲取牌庫設置
            params['decks'] = self.ui.decksSpinBox.value()
            params['reshuffle_threshold'] = self.ui.reshuffleSpinBox.value()
            
            # 獲取模擬時間設置
            params['sim_time_seconds'] = self.ui.simTimeSpinBox.value()
            
            # 獲取實時更新設置
            params['realtime_update'] = {
                'enabled': self.ui.realtimeUpdateCheck.isChecked(),
                'update_interval': self.ui.updateIntervalSpinBox.value(),
                'auto_adjust': self.ui.autoAdjustCheck.isChecked()
            }

            # 參數驗證
            if not params['strategies']:
                raise ValueError("策略列表不能為空")
            if params['min_games_per_strategy'] <= 0:
                raise ValueError("模擬局數必須大於0")
            if params['decks'] <= 0:
                raise ValueError("牌副數必須大於0")
            if not (0 < params['reshuffle_threshold'] < 1):
                 raise ValueError("洗牌閾值必須在0和1之間")
            if params['sim_time_seconds'] <= 0:
                raise ValueError("模擬時間必須大於0")

        except ValueError as e:
            QMessageBox.warning(self, "參數錯誤", f"輸入參數無效: {e}")
            return None
        
        return params

    def install_global_exception_handler(self):
        """安裝全局異常處理器來捕獲未捕獲的異常"""
        def excepthook(exc_type, exc_value, exc_traceback):
            # 獲取詳細錯誤訊息
            error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            # 發送錯誤信號到主視窗
            self.error_occurred.emit("未捕獲的異常", error_msg)
            # 保持原有的異常處理
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        
        # 安裝全局異常處理器
        sys.excepthook = excepthook
        
    @Slot(str, str)
    def handle_error(self, title, message):
        """處理來自任何來源的錯誤"""
        # 記錄錯誤
        logging.error(f"{title}: {message}")
        self.append_log(f"錯誤: {title}")
        
        # 在介面顯示錯誤
        QMessageBox.critical(self, title, message)
        
        # 更新狀態
        self.ui.statusbar.showMessage(f"發生錯誤")
        self.ui.statusLabel.setText(f"出錯: {title}")
        
        # 確保按鈕狀態恢復
        self.ui.runButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

    @Slot()
    def start_simulation(self):
        """開始模擬"""
        # 獲取並驗證參數
        params = self.get_parameters_from_ui()
        if params is None:
            return

        # 更新配置對象
        self.config['simulation']['min_games_per_strategy'] = params['min_games_per_strategy']
        self.config['simulation']['strategies'] = params['strategies']
        self.config['simulation']['sim_time_seconds'] = params['sim_time_seconds']
        self.config['game']['decks'] = params['decks']
        self.config['game']['reshuffle_threshold'] = params['reshuffle_threshold']
        
        # 更新實時更新配置
        if 'realtime_update' in params:
            self.config['simulation']['realtime_update'] = params['realtime_update']

        # 更新UI狀態
        self.ui.runButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.progressBar.setValue(0)
        self.ui.statusLabel.setText("正在準備模擬...")
        self.append_log("--- 開始模擬 ---")
        self.ui.statusbar.showMessage("模擬中...")

        # 清空策略選擇下拉框
        self.ui.strategyDistCombo.clear()
        
        # 準備實時更新的數據結構
        self.current_strategy = None
        self.intermediate_results = {}

        try:
            # 創建工作線程
            self.worker_thread = QThread()
            self.simulator_worker = SimulationWorker(self.config)
            self.simulator_worker.moveToThread(self.worker_thread)

            # 連接線程信號
            self.worker_thread.started.connect(self.simulator_worker.run)
            self.simulator_worker.finished.connect(self.worker_thread.quit)
            self.simulator_worker.finished.connect(self.simulator_worker.deleteLater)
            self.worker_thread.finished.connect(self.worker_thread.deleteLater)
            self.simulator_worker.result_ready.connect(self.simulation_complete)
            self.simulator_worker.progress.connect(self.progress_update)
            self.simulator_worker.error_signal.connect(lambda title, msg: self.error_occurred.emit(title, msg))
            
            # 連接中間結果信號
            self.simulator_worker.intermediate_result.connect(self.handle_intermediate_results)

            # 啟動線程
            self.worker_thread.start()
        except Exception as e:
            error_msg = f"啟動模擬時出錯: {str(e)}\n{traceback.format_exc()}"
            self.error_occurred.emit("模擬錯誤", error_msg)

    @Slot()
    def stop_simulation(self):
        """停止模擬"""
        if self.simulator_worker:
            self.append_log("請求停止模擬...")
            self.ui.statusLabel.setText("正在停止模擬...")
            self.ui.statusbar.showMessage("停止中...")
            self.simulator_worker.request_stop()
            
        self.ui.stopButton.setEnabled(False)

    @Slot()
    def reset_parameters(self):
        """重置參數到默認值"""
        self.load_initial_config()
        
        # 記住當前活動的頁面索引
        current_tab_index = self.ui.tabWidget.currentIndex()
        
        # 清除結果顯示
        self.ui.summaryTable.setRowCount(0)
        
        # 重置分佈圖
        self.dist_canvas.axes.clear()
        self.dist_canvas.axes.text(0.5, 0.5, '尚無數據', 
                                 horizontalalignment='center', 
                                 verticalalignment='center',
                                 fontsize=14)
        self.dist_canvas.draw()
        
        # 重置策略比較圖
        self.comp_canvas.figure.clear()
        self.comp_canvas.axes = self.comp_canvas.figure.add_subplot(111)
        self.comp_canvas.axes.text(0.5, 0.5, '尚無數據', 
                                 horizontalalignment='center',
                                 verticalalignment='center',
                                 fontsize=14)
        self.comp_canvas.draw()
        
        # 切換到策略比較頁面以確保其被正確更新
        self.ui.tabWidget.setCurrentIndex(2)  # 假設策略比較頁是索引2
        QApplication.processEvents()  # 處理界面事件
        
        # 切回原始頁面
        self.ui.tabWidget.setCurrentIndex(current_tab_index)
        
        # 清除策略下拉框
        self.ui.strategyDistCombo.clear()
        
        # 重置進度條和狀態
        self.ui.progressBar.setValue(0)
        self.ui.statusLabel.setText("參數已重置")
        
        # 清除任何保存的結果和分析器
        if hasattr(self, 'simulation_results'):
            self.simulation_results = None
        if hasattr(self, 'analyzer'):
            self.analyzer = None
        if hasattr(self, 'intermediate_results'):
            self.intermediate_results = None
        
        self.append_log("--- 參數已重置 ---")
        self.ui.statusbar.showMessage("就緒")

    @Slot(int, str)
    def update_progress(self, value, message):
        """更新進度顯示"""
        self.ui.progressBar.setValue(value)
        self.ui.statusLabel.setText(message)
        self.ui.statusbar.showMessage(f"模擬進度: {value}%")

    @Slot(object)
    def handle_simulation_results(self, results):
        """處理模擬結果"""
        self.append_log("--- 模擬完成，正在處理結果 ---")
        self.ui.statusLabel.setText("正在分析結果...")
        self.ui.statusbar.showMessage("處理結果中...")
        QApplication.processEvents()  # 處理界面事件，避免卡頓

        if isinstance(results, str):  # 如果是錯誤信息
            QMessageBox.critical(self, "模擬出錯", results)
            self.append_log(f"模擬出錯: {results}")
            self.ui.statusbar.showMessage("模擬出錯")
        elif results:
            try:
                # 保存模擬結果，以便其他方法可以使用
                self.simulation_results = results
                
                # 1. 分析結果
                analyzer = Analyzer(results)
                self.analyzer = analyzer  # 保存分析器實例
                comparison_df = analyzer.compare_strategies()

                # 2. 更新統計表格
                self.update_summary_table(comparison_df)

                # 3. 填充策略選擇下拉框
                self.ui.strategyDistCombo.clear()
                for strategy in sorted(results.keys()):
                    self.ui.strategyDistCombo.addItem(f"策略 {strategy}", strategy)
                
                # 4. 更新分佈圖
                if self.ui.strategyDistCombo.count() > 0:
                    self.ui.strategyDistCombo.setCurrentIndex(0)  # 觸發選擇變更
                else:
                    self.dist_canvas.axes.clear()
                    self.dist_canvas.axes.text(0.5, 0.5, '無策略數據', 
                                               horizontalalignment='center', 
                                               verticalalignment='center',
                                               fontsize=14)
                    self.dist_canvas.draw()
                
                # 5. 更新策略比較頁的比較圖
                self.plot_comparison_gui(analyzer, comparison_df)

                self.append_log("--- 結果處理完成 ---")
                self.ui.statusLabel.setText("模擬和分析完成")
                self.ui.statusbar.showMessage("完成")

            except Exception as e:
                QMessageBox.critical(self, "分析出錯", f"處理結果時發生錯誤: {e}")
                self.append_log(f"分析出錯: {e}")
                logging.exception("分析結果時出錯")
                self.ui.statusbar.showMessage("分析失敗")

        else:
            self.append_log("模擬未產生有效結果。")
            self.ui.statusLabel.setText("模擬完成但無結果")
            self.ui.statusbar.showMessage("無結果")

        # 恢復按鈕狀態
        self.ui.runButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.progressBar.setValue(100)  # 標記完成

    def update_summary_table(self, df):
        """更新摘要表格"""
        # 清空表格
        self.ui.summaryTable.setRowCount(0)
        
        if df.empty:
            return
            
        # 設置表格行數和列數
        self.ui.summaryTable.setRowCount(len(df))
        self.ui.summaryTable.setColumnCount(len(df.columns))
        
        # 設置列標題
        self.ui.summaryTable.setHorizontalHeaderLabels(df.columns)

        # 填充數據
        for i, row in enumerate(df.itertuples(index=False)):
            for j, value in enumerate(row):
                # 格式化數值
                if isinstance(value, float):
                    if 'rate' in df.columns[j].lower():
                        item_text = f"{value:.2%}"  # 百分比格式
                    else:
                        item_text = f"{value:.4f}"  # 保留4位小數
                else:
                    item_text = str(value)
                    
                # 創建表格項
                item = QTableWidgetItem(item_text)
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # 居中顯示
                self.ui.summaryTable.setItem(i, j, item)

        # 自動調整列寬
        self.ui.summaryTable.resizeColumnsToContents()
        
        # 確保最後一列拉伸填滿
        header = self.ui.summaryTable.horizontalHeader()
        header.setStretchLastSection(True)

    @Slot()
    def update_distribution_plot(self):
        """更新分佈圖顯示"""
        try:
            # 獲取當前選中的策略
            current_idx = self.ui.strategyDistCombo.currentIndex()
            if current_idx < 0:
                # 沒有選中項，可能是下拉列表為空
                logging.warning("無法更新分佈圖：沒有選中的策略")
                return
                
            strategy = self.ui.strategyDistCombo.itemData(current_idx)
            if strategy is None:
                logging.warning("無法更新分佈圖：策略值為 None")
                return
                
            # 繪製圖形
            self.plot_distribution_gui(strategy)
        except Exception as e:
            logging.exception(f"更新分佈圖時出錯: {str(e)}")
            self.error_occurred.emit("更新圖表失敗", f"更新分佈圖時出錯: {str(e)}\n\n{traceback.format_exc()}")

    def plot_distribution_gui(self, strategy):
        """繪製特定策略的點數分佈圖"""
        # 清除圖形
        self.dist_canvas.figure.clear()
        self.dist_canvas.axes = self.dist_canvas.figure.add_subplot(111)
        
        try:
            # 嘗試獲取分析器
            if hasattr(self, 'analyzer') and self.analyzer is not None:
                # 優先使用已存在的分析器
                analyzer = self.analyzer
            elif hasattr(self, 'simulation_results') and self.simulation_results is not None:
                # 使用已保存的模擬結果創建新的分析器
                analyzer = Analyzer(self.simulation_results)
            elif hasattr(self, 'simulator_worker') and hasattr(self.simulator_worker, 'results') and self.simulator_worker.results is not None:
                # 兜底：從模擬工作器獲取結果
                analyzer = Analyzer(self.simulator_worker.results)
            else:
                self.dist_canvas.axes.text(0.5, 0.5, '無模擬結果數據', 
                                        horizontalalignment='center', 
                                        verticalalignment='center',
                                        fontsize=14)
                self.dist_canvas.draw()
                logging.warning("無法繪製分佈圖：模擬結果不可用")
                return
            
            # 確認分析器有數據可用
            if not analyzer.strategies:
                self.dist_canvas.axes.text(0.5, 0.5, '分析器沒有策略數據', 
                                        horizontalalignment='center', 
                                        verticalalignment='center',
                                        fontsize=14)
                self.dist_canvas.draw()
                logging.warning("無法繪製分佈圖：分析器沒有策略數據")
                return
                
            distribution = analyzer.get_distribution(strategy)
            stats = analyzer.calculate_statistics(strategy)
            
            # 如果沒有數據，顯示提示並退出
            if not distribution:
                self.dist_canvas.axes.text(0.5, 0.5, f'策略 {strategy} 沒有分佈數據', 
                                        horizontalalignment='center', 
                                        verticalalignment='center',
                                        fontsize=14)
                self.dist_canvas.draw()
                return
                
            bust_rate = stats['bust_rate'] * 100
            
            # 繪圖
            x = list(distribution.keys())
            y = list(distribution.values())
            colors = ['red' if val > 21 else 'steelblue' for val in x]
            
            # 創建條形圖
            self.dist_canvas.axes.bar(range(len(x)), y, color=colors)
            
            # 設置軸和標題
            self.dist_canvas.axes.set_xticks(range(len(x)))
            self.dist_canvas.axes.set_xticklabels([str(val) if val <= 21 else 'Bust' for val in x])
            self.dist_canvas.axes.set_title(f"策略 {strategy} 點數分佈 (爆牌率: {bust_rate:.2f}%)")
            self.dist_canvas.axes.set_xlabel("手牌點數")
            self.dist_canvas.axes.set_ylabel("局數")
            self.dist_canvas.axes.grid(True, axis='y')
            
        except Exception as e:
            error_msg = str(e)
            error_detail = traceback.format_exc()
            self.dist_canvas.axes.text(0.5, 0.5, f'繪圖錯誤: {error_msg}', 
                                    horizontalalignment='center', 
                                    verticalalignment='center',
                                    fontsize=12)
            logging.exception("繪製分佈圖時出錯")
            # 使用錯誤處理器顯示詳細錯誤
            self.error_occurred.emit("繪圖錯誤", f"繪製分佈圖時出錯:\n{error_msg}\n\n詳細信息:\n{error_detail}")

        # 刷新Canvas
        try:
            self.dist_canvas.draw()
        except Exception as e:
            logging.exception("繪圖渲染時出錯")
            self.error_occurred.emit("繪圖渲染錯誤", f"無法渲染分佈圖: {str(e)}\n{traceback.format_exc()}")

    def plot_comparison_gui(self, analyzer=None, comparison_df=None):
        """繪製策略比較圖"""
        # 清除圖形
        self.comp_canvas.figure.clear()

        try:
            # 檢查傳入的參數
            if analyzer is None or comparison_df is None:
                # 嘗試通過已有數據創建
                if hasattr(self, 'analyzer') and self.analyzer is not None and self.analyzer.strategies:
                    analyzer = self.analyzer
                    comparison_df = analyzer.compare_strategies()
                elif hasattr(self, 'simulation_results') and self.simulation_results is not None:
                    analyzer = Analyzer(self.simulation_results)
                    if analyzer.strategies:
                        comparison_df = analyzer.compare_strategies()
                    else:
                        self.comp_canvas.figure.clear()
                        ax = self.comp_canvas.figure.add_subplot(111)
                        ax.text(0.5, 0.5, '無比較數據：分析器沒有策略數據', 
                            horizontalalignment='center', 
                            verticalalignment='center',
                            fontsize=14)
                        self.comp_canvas.draw()
                        return
                else:
                    self.comp_canvas.figure.clear()
                    ax = self.comp_canvas.figure.add_subplot(111)
                    ax.text(0.5, 0.5, '無比較數據', 
                        horizontalalignment='center', 
                        verticalalignment='center',
                        fontsize=14)
                    self.comp_canvas.draw()
                    return
            
            # 設置 Figure 的比例和大小
            # 使用子圖佈局，但不使用 gridspec，而是明確設置每個子圖的位置
            fig = self.comp_canvas.figure
            fig.subplots_adjust(wspace=0.6, hspace=0.5, left=0.1, right=0.95, top=0.85, bottom=0.15)
            
            # 添加總標題
            fig.suptitle("策略比較", fontsize=14, fontweight='bold', y=0.98)
            
            # 1. 爆牌率比較 (左)
            ax1 = fig.add_subplot(131)  # 1行3列的第1個
            if not comparison_df.empty:
                strategies = comparison_df['strategy'].astype(str)
                bust_rates = comparison_df['bust_rate']
                
                # 創建條形圖
                width = 0.6  # 減小條形寬度
                bars = ax1.bar(strategies, bust_rates, color='skyblue', width=width)
                
                # 設置標題和軸
                ax1.set_title("爆牌率比較", fontsize=12, pad=10)
                ax1.set_xlabel("策略", fontsize=10)
                ax1.set_ylabel("爆牌率", fontsize=10)
                
                # 設置百分比格式
                ax1.yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
                
                # 添加數值標籤
                for bar in bars:
                    yval = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2.0, 
                            yval, 
                            f'{yval:.2%}', 
                            va='bottom', 
                            ha='center',
                            fontsize=9,
                            fontweight='bold')
                
                # 添加網格線
                ax1.grid(True, axis='y', alpha=0.3)
                
                # 設置 y 軸範圍以便更好地比較
                ax1.set_ylim(0, max(bust_rates) * 1.1)
            
            # 2. 平均點數比較 (中)
            ax2 = fig.add_subplot(132)  # 1行3列的第2個
            if not comparison_df.empty:
                strategies = comparison_df['strategy'].astype(str)
                mean_values = comparison_df['mean_value']
                
                # 創建條形圖
                width = 0.6  # 減小條形寬度
                bars = ax2.bar(strategies, mean_values, color='lightgreen', width=width)
                
                # 設置標題和軸
                ax2.set_title("平均點數比較", fontsize=12, pad=10)
                ax2.set_xlabel("策略", fontsize=10)
                ax2.set_ylabel("平均點數", fontsize=10)
                
                # 添加數值標籤
                for bar in bars:
                    yval = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2.0, 
                            yval, 
                            f'{yval:.2f}', 
                            va='bottom', 
                            ha='center',
                            fontsize=9,
                            fontweight='bold')
                
                # 添加網格線
                ax2.grid(True, axis='y', alpha=0.3)
                
                # 設置 y 軸範圍，使視覺效果更佳
                min_val = max(0, min(mean_values) * 0.9)
                ax2.set_ylim(min_val, max(mean_values) * 1.05)
            
            # 3. 標準差比較 (右)
            ax3 = fig.add_subplot(133)  # 1行3列的第3個
            if not comparison_df.empty:
                strategies = comparison_df['strategy'].astype(str)
                std_devs = comparison_df['std_dev']
                
                # 創建條形圖
                width = 0.6  # 減小條形寬度
                bars = ax3.bar(strategies, std_devs, color='coral', width=width)
                
                # 設置標題和軸
                ax3.set_title("標準差比較", fontsize=12, pad=10)
                ax3.set_xlabel("策略", fontsize=10)
                ax3.set_ylabel("標準差", fontsize=10)
                
                # 添加數值標籤
                for bar in bars:
                    yval = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2.0, 
                            yval, 
                            f'{yval:.2f}', 
                            va='bottom', 
                            ha='center',
                            fontsize=9,
                            fontweight='bold')
                
                # 添加網格線
                ax3.grid(True, axis='y', alpha=0.3)
                
                # 設置 y 軸範圍
                min_val = max(0, min(std_devs) * 0.9)
                ax3.set_ylim(min_val, max(std_devs) * 1.05)
                
        except Exception as e:
            error_msg = str(e)
            error_detail = traceback.format_exc()
            self.comp_canvas.figure.clear()
            ax = self.comp_canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'繪圖錯誤: {error_msg}', 
                   horizontalalignment='center', 
                   verticalalignment='center',
                   fontsize=12)
            logging.exception("繪製比較圖時出錯")
            # 使用錯誤處理器顯示詳細錯誤
            self.error_occurred.emit("繪圖錯誤", f"繪製比較圖時出錯:\n{error_msg}\n\n詳細信息:\n{error_detail}")

        # 刷新Canvas
        try:
            self.comp_canvas.draw()
        except Exception as e:
            logging.exception("繪圖渲染時出錯")
            self.error_occurred.emit("繪圖渲染錯誤", f"無法渲染比較圖: {str(e)}\n{traceback.format_exc()}")

    @Slot()
    def show_about_dialog(self):
        """顯示關於對話框"""
        about_text = """
        <h3>BlackPiyan v1.0.0</h3>
        <p>專業的21點(Blackjack)莊家策略模擬與分析工具</p>
        <p>Copyright © 2025 BlackPiyan Team</p>
        <p>使用 MIT 許可證</p>
        """
        QMessageBox.about(self, "關於 BlackPiyan", about_text)

    def closeEvent(self, event):
        """關閉窗口時的事件處理"""
        # 首先禁用所有按鈕，防止用戶在關閉過程中進行新的操作
        try:
            self.ui.runButton.setEnabled(False)
            self.ui.stopButton.setEnabled(False)
            self.ui.resetButton.setEnabled(False)
        except:
            pass  # 忽略可能的錯誤
        
        # 記錄關閉事件
        try:
            self.append_log("應用程序正在關閉...")
            logging.info("用戶發起關閉應用程序")
        except:
            pass  # 忽略可能的錯誤
        
        # 主要關閉邏輯
        try:
            # 停止所有可能的 Qt 計時器
            try:
                for obj in self.findChildren(QtCore.QObject):
                    if isinstance(obj, QtCore.QTimer):
                        try:
                            if obj.isActive():
                                obj.stop()
                                logging.info(f"停止計時器: {obj.objectName()}")
                        except:
                            pass
            except:
                pass
            
            # 停止正在進行的模擬
            if hasattr(self, 'simulator_worker') and self.simulator_worker:
                try:
                    self.simulator_worker.request_stop()
                    logging.info("已請求停止模擬工作")
                except:
                    logging.warning("請求停止模擬工作時出錯")
            
            # 如果工作線程還在運行，嘗試終止它
            if hasattr(self, 'worker_thread') and self.worker_thread:
                try:
                    # 先檢查 worker_thread 是否是有效的物件，並且未被刪除
                    if self.worker_thread and not self.worker_thread.parent() is None:
                        if self.worker_thread.isRunning():
                            logging.info("工作線程仍在運行，嘗試終止")
                            # 嘗試安全終止線程
                            try:
                                # 先確保停止工作器
                                if hasattr(self, 'simulator_worker') and self.simulator_worker:
                                    self.simulator_worker.request_stop()
                                
                                # 等待一小段時間
                                time.sleep(0.2)
                                
                                # 嘗試正常退出
                                if self.worker_thread and not self.worker_thread.parent() is None:
                                    if self.worker_thread.isRunning():
                                        # 記得使用 deleteLater 而不是直接刪除
                                        self.worker_thread.quit()
                                        # 等待一段時間
                                        successful = self.worker_thread.wait(1000)
                                        
                                        # 如果仍未退出，則嘗試強制終止
                                        if not successful and self.worker_thread and not self.worker_thread.parent() is None:
                                            if self.worker_thread.isRunning():
                                                logging.warning("線程未能通過 quit() 終止，嘗試強制終止")
                                                self.worker_thread.terminate()
                                                self.worker_thread.wait(500)
                            except Exception as e:
                                logging.error(f"終止線程的標準方法失敗: {str(e)}")
                                
                                # 回退方案：使用強制終止
                                try:
                                    if hasattr(self, 'worker_thread') and self.worker_thread and not self.worker_thread.parent() is None:
                                        if self.worker_thread.isRunning():
                                            self.worker_thread.terminate()
                                            self.worker_thread.wait(500)
                                except:
                                    logging.error("強制終止線程失敗")
                except Exception as e:
                    logging.error(f"終止工作線程時出錯: {str(e)}")
                
                # 安全地清除線程引用
                try:
                    # 使用 None 而不是刪除對象
                    if hasattr(self, 'simulator_worker'):
                        self.simulator_worker = None
                    if hasattr(self, 'worker_thread'):
                        self.worker_thread = None
                except Exception as e:
                    logging.error(f"清除線程引用時出錯: {str(e)}")
                    pass
            
            # 斷開所有可能的信號連接
            try:
                # 嘗試斷開Qt信號連接
                if hasattr(self, 'ui'):
                    # 斷開按鈕信號
                    for btn_name in ['runButton', 'stopButton', 'resetButton']:
                        try:
                            btn = getattr(self.ui, btn_name, None)
                            if btn:
                                btn.clicked.disconnect()
                        except:
                            pass
                    
                    # 斷開下拉框信號
                    try:
                        if hasattr(self.ui, 'strategyDistCombo'):
                            self.ui.strategyDistCombo.currentIndexChanged.disconnect()
                    except:
                        pass
            except:
                pass
            
            # 清理圖形資源
            try:
                # 確保關閉所有matplotlib圖形
                plt.close('all')
                
                # 清理具體的圖形對象
                for canvas_name in ['dist_canvas', 'comp_canvas']:
                    if hasattr(self, canvas_name):
                        canvas = getattr(self, canvas_name)
                        if canvas:
                            try:
                                # 清理圖形
                                if hasattr(canvas, 'figure'):
                                    canvas.figure.clear()
                                # 將引用設為None
                                setattr(self, canvas_name, None)
                            except:
                                logging.warning(f"清理 {canvas_name} 時出錯")
                
                # 清理導航工具條
                for toolbar_name in ['dist_toolbar', 'comp_toolbar']:
                    if hasattr(self, toolbar_name):
                        toolbar = getattr(self, toolbar_name)
                        if toolbar:
                            try:
                                toolbar.setParent(None)
                                setattr(self, toolbar_name, None)
                            except:
                                logging.warning(f"清理 {toolbar_name} 時出錯")
            except Exception as e:
                logging.error(f"清理圖形資源時出錯: {str(e)}")
            
            # 清理其他資源和引用
            for attr_name in ['simulation_results', 'analyzer', 'intermediate_results']:
                if hasattr(self, attr_name):
                    try:
                        setattr(self, attr_name, None)
                    except:
                        pass
            
            # 關閉日誌處理器
            if hasattr(self, 'log_handler') and self.log_handler:
                try:
                    handler = self.log_handler
                    # 先將handler從logger移除
                    logger = logging.getLogger()
                    if handler in logger.handlers:
                        logger.removeHandler(handler)
                    # 嘗試關閉handler
                    try:
                        handler.close()
                    except:
                        pass
                    # 清除引用
                    self.log_handler = None
                except Exception as e:
                    logging.error(f"關閉日誌處理器時出錯: {str(e)}")
            
            # 強制進行垃圾收集
            try:
                import gc
                gc.collect()
            except:
                pass
            
            # 處理所有待處理的事件
            QApplication.processEvents()
            
            # 最後一步，接受關閉事件
            event.accept()
            logging.info("應用程序關閉完成")
            
        except Exception as e:
            # 捕獲整個關閉過程中的任何錯誤
            try:
                error_msg = f"關閉時發生未捕獲的錯誤: {str(e)}\n{traceback.format_exc()}"
                logging.critical(error_msg)
                print(error_msg)  # 確保即使logging失敗也能看到錯誤
            except:
                pass
            
            # 無論發生什麼錯誤，都接受關閉事件
            event.accept()

    @Slot(object, int)
    def handle_intermediate_results(self, intermediate_data, current_strategy):
        """處理模擬過程中的中間結果，更新圖表"""
        try:
            # 保存中間結果和當前策略
            self.intermediate_results = intermediate_data
            self.current_strategy = current_strategy
            
            # 確保下拉框包含所有已知策略
            strategies = list(intermediate_data.keys())
            for strategy in sorted(strategies):
                if self.ui.strategyDistCombo.findData(strategy) == -1:  # 如果策略不在下拉框中
                    self.ui.strategyDistCombo.addItem(f"策略 {strategy}", strategy)
            
            # 選擇當前策略
            index = self.ui.strategyDistCombo.findData(current_strategy)
            if index >= 0 and self.ui.strategyDistCombo.currentIndex() != index:
                self.ui.strategyDistCombo.setCurrentIndex(index)
            elif self.ui.strategyDistCombo.count() > 0 and self.ui.strategyDistCombo.currentIndex() < 0:
                self.ui.strategyDistCombo.setCurrentIndex(0)
            
            # 使用中間結果更新圖表
            self.update_charts_with_intermediate_results()
            
            # 更新介面
            QApplication.processEvents()  # 確保 UI 能響應
            
        except Exception as e:
            error_msg = f"處理中間結果時出錯: {str(e)}"
            error_detail = traceback.format_exc()
            self.error_occurred.emit("中間結果錯誤", f"{error_msg}\n\n{error_detail}")
            logging.exception("處理中間結果時出錯")
    
    def update_charts_with_intermediate_results(self):
        """根據中間結果更新圖表"""
        try:
            # 獲取中間結果並創建分析器
            if not hasattr(self, 'intermediate_results') or self.intermediate_results is None:
                logging.warning("中間結果不可用，無法更新圖表")
                return

            # 確保結果不為空
            if not self.intermediate_results:
                logging.warning("中間結果為空，無法更新圖表")
                return
                
            # 創建分析器
            self.analyzer = Analyzer(self.intermediate_results)
            
            # 如果沒有策略數據，則退出
            if not self.analyzer.strategies:
                logging.warning("中間結果中沒有策略數據，無法更新圖表")
                return
                
            # 獲取當前選中的策略
            strategy = self.ui.strategyDistCombo.currentData()
            if strategy is None and self.analyzer.strategies:
                # 如果沒有選中的策略但有可用的策略，則使用第一個
                strategy = self.analyzer.strategies[0]
                
            # 1. 更新分佈圖
            if strategy is not None:
                self.plot_distribution_gui(strategy)
                
            # 2. 更新策略比較頁的比較圖
            comparison_df = self.analyzer.compare_strategies()
            self.plot_comparison_gui(self.analyzer, comparison_df)
            
            # 3. 更新表格
            self.update_summary_table(comparison_df)
            
        except Exception as e:
            logging.exception(f"更新中間結果圖表時出錯: {str(e)}")
            # 顯示錯誤對話框
            self.error_occurred.emit("更新圖表錯誤", f"無法更新圖表: {str(e)}\n\n{traceback.format_exc()}")