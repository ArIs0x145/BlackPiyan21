#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BlackPiyan GUI 啟動腳本
運行此腳本以啟動 BlackPiyan 的圖形用戶界面
支援跨平台（Windows、macOS、Linux）運行
"""

import sys
import os
import platform
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from blackpiyan.gui.main_window import BlackPiyanGUI
from blackpiyan.gui import check_platform_compatibility

# 配置基本日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BlackPiyan.Launcher")

def setup_platform_specific_features():
    """設置平台特定的功能"""
    current_platform = platform.system()
    logger.info(f"檢測到運行平台: {current_platform} ({platform.platform()})")
    
    if current_platform == "Windows":
        setup_windows_features()
    elif current_platform == "Darwin":  # macOS
        setup_macos_features()
    elif current_platform == "Linux":
        setup_linux_features()
    else:
        logger.warning(f"未知平台 {current_platform}，使用通用設定")

def setup_windows_features():
    """設置 Windows 平台特定功能"""
    try:
        # 設置 Windows 任務欄圖標
        import ctypes
        app_id = "BlackPiyanTeam.BlackPiyan.21PointAnalyzer.1.0.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        logger.info("已設置 Windows 任務欄應用程序 ID")
        
        # 其他 Windows 特定設置可以放這裡
    except Exception as e:
        logger.warning(f"設置 Windows 特定功能時出錯: {e}")

def setup_macos_features():
    """設置 macOS 平台特定功能"""
    try:
        # macOS 特定設置，如 Dock 圖標、觸控列支援等
        # 這裡暫時沒有特定設置，但保留此函數以便將來擴展
        pass
    except Exception as e:
        logger.warning(f"設置 macOS 特定功能時出錯: {e}")

def setup_linux_features():
    """設置 Linux 平台特定功能"""
    try:
        # Linux 特定設置，如 X11/Wayland 檢測等
        # 這裡暫時沒有特定設置，但保留此函數以便將來擴展
        pass
    except Exception as e:
        logger.warning(f"設置 Linux 特定功能時出錯: {e}")

def get_app_icon():
    """獲取應用程序圖標，支援多種平台和格式"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_path, "blackpiyan", "gui", "resources", "icons")
    
    # 平台優先的圖標格式
    icon_preferences = {
        "Windows": ["piyan.ico", "piyan.png"],
        "Darwin": ["piyan.icns", "piyan.png", "piyan.ico"],
        "Linux": ["piyan.png", "piyan.ico"]
    }
    
    current_platform = platform.system()
    preferred_icons = icon_preferences.get(current_platform, ["piyan.png", "piyan.ico"])
    
    # 嘗試按優先順序載入圖標
    for icon_name in preferred_icons:
        icon_path = os.path.join(icons_dir, icon_name)
        if os.path.exists(icon_path):
            logger.info(f"找到適用於 {current_platform} 的圖標: {icon_path}")
            return icon_path
    
    # 如果找不到任何特定平台圖標，嘗試通用目錄中的圖標
    fallback_icons = ["piyan.png", "piyan.ico", "piyan.icns"]
    for icon_name in fallback_icons:
        icon_path = os.path.join(icons_dir, icon_name)
        if os.path.exists(icon_path):
            logger.warning(f"使用後備圖標: {icon_path}")
            return icon_path
    
    logger.warning("找不到任何應用程序圖標")
    return None

def main():
    """啟動 BlackPiyan GUI 的主函數"""
    try:
        logger.info("正在啟動 BlackPiyan GUI...")
        
        # 檢查平台兼容性
        compat_info = check_platform_compatibility()
        logger.info(f"平台: {compat_info['platform']}, Python: {compat_info['python_version']}")
        
        if compat_info['issues']:
            for issue in compat_info['issues']:
                logger.warning(f"兼容性警告: {issue}")
        
        # 設置平台特定功能
        setup_platform_specific_features()
        
        # 創建 QApplication 實例
        app = QApplication(sys.argv)
        
        # 設置應用程序名稱和組織信息
        app.setApplicationName("BlackPiyan")
        app.setOrganizationName("BlackPiyan Team")
        app.setApplicationDisplayName("21點莊家策略分析")
        
        # 設置應用程序圖標
        icon_path = get_app_icon()
        if icon_path:
            app_icon = QIcon(icon_path)
            app.setWindowIcon(app_icon)
        
        # 創建主窗口
        window = BlackPiyanGUI()
        
        # 顯示窗口
        window.show()
        logger.info("應用程序已啟動，進入事件循環")
        
        # 進入事件循環
        return app.exec()
    
    except Exception as e:
        logger.error(f"啟動應用程序時發生錯誤: {e}", exc_info=True)
        print(f"啟動失敗: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 