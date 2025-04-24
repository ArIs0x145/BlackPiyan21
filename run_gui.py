#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BlackPiyan GUI 啟動腳本
運行此腳本以啟動 BlackPiyan 的圖形用戶界面
"""

import sys
import os
import platform
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from blackpiyan.gui.main_window import BlackPiyanGUI

def setup_windows_taskbar_icon():
    """在 Windows 上設置任務欄圖標"""
    try:
        # 僅在 Windows 平台執行
        if platform.system() == "Windows":
            import ctypes
            # 應用程序 ID - 應該是唯一的
            app_id = "BlackPiyanTeam.BlackPiyan.21PointAnalyzer.1.0.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            return True
    except Exception as e:
        print(f"設置 Windows 任務欄圖標時出錯: {str(e)}")
    return False

def main():
    """啟動 BlackPiyan GUI 的主函數，提供給 entry_point 使用"""
    # 為 Windows 設置任務欄圖標
    setup_windows_taskbar_icon()
    
    # 創建 QApplication 實例
    app = QApplication(sys.argv)
    
    # 設置應用程序名稱和組織信息（用於設置存儲）
    app.setApplicationName("BlackPiyan")
    app.setOrganizationName("BlackPiyan Team")
    app.setApplicationDisplayName(" 21點莊家策略分析")  # 設置顯示名稱
    
    # 設置應用程序圖標
    icon_path = os.path.join(os.path.dirname(__file__), "blackpiyan", "gui", "resources", "icons", "piyan.ico")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        print(f"已設置應用程序圖標: {icon_path}")
    else:
        print(f"警告：找不到圖標文件: {icon_path}")
    
    # 創建主窗口
    window = BlackPiyanGUI()
    
    # 顯示窗口
    window.show()
    
    # 進入事件循環 (在 PySide6 中是 exec() 而非 exec_())
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 