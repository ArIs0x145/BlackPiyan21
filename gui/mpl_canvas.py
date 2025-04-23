#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Matplotlib 畫布類，用於在 PySide6 控件中嵌入 Matplotlib 圖表"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        初始化 Matplotlib 畫布
        
        Args:
            parent: 父控件
            width: 圖形寬度（英寸）
            height: 圖形高度（英寸）
            dpi: 圖形分辨率（每英寸點數）
        """
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.logger = logging.getLogger(__name__)
        
        # 設置尺寸策略，使圖表自適應父控件大小
        FigureCanvas.setSizePolicy(self,
                                  QtWidgets.QSizePolicy.Policy.Expanding,
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # 為中文顯示設置默認字體
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題 

    def draw(self):
        """
        重寫 draw 方法，添加錯誤處理
        """
        try:
            super().draw()
        except Exception as e:
            error_msg = str(e)
            error_detail = traceback.format_exc()
            self.logger.error(f"Matplotlib 渲染錯誤: {error_msg}\n{error_detail}")
            # 嘗試清除圖形並顯示錯誤信息
            try:
                self.axes.clear()
                self.axes.text(0.5, 0.5, f"渲染錯誤: {error_msg}",
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=10, color='red')
                super().draw()
            except Exception as inner_error:
                # 如果連錯誤顯示都失敗，只能記錄日誌
                self.logger.error(f"無法顯示渲染錯誤信息: {str(inner_error)}")

# 直接使用現有的 NavigationToolbar2QT 作為 NavigationToolbar
NavigationToolbar = NavigationToolbar