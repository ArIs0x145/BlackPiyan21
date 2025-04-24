#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BlackPiyan GUI 模組
提供圖形使用者界面功能
"""

import platform
import logging
import os

logger = logging.getLogger(__name__)

def check_platform_compatibility():
    """
    檢查當前平台與GUI兼容性
    
    Returns:
        dict: 包含平台兼容性信息
    """
    system = platform.system()
    platform_info = platform.platform()
    python_version = platform.python_version()
    
    # 獲取當前目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(current_dir, "resources")
    icons_dir = os.path.join(resources_dir, "icons")
    
    # 檢查資源目錄
    has_resources_dir = os.path.exists(resources_dir)
    has_icons_dir = os.path.exists(icons_dir)
    
    # 檢查圖標文件
    icon_files = []
    if has_icons_dir:
        icon_files = [f for f in os.listdir(icons_dir) 
                     if os.path.isfile(os.path.join(icons_dir, f))]
    
    # 檢查常見問題
    issues = []
    
    if system == "Windows":
        try:
            import ctypes
            # 檢查 Windows 特定庫
        except ImportError:
            issues.append("無法導入 ctypes 模塊，某些 Windows 特定功能可能無法使用")
    
    elif system == "Darwin":  # macOS
        # 檢查 macOS 版本
        mac_version = platform.mac_ver()[0]
        if mac_version and mac_version < "10.13":
            issues.append(f"檢測到 macOS 版本 {mac_version}，建議使用 10.13 或更高版本")
        
        # 檢查 icns 圖標
        if not any(f.endswith('.icns') for f in icon_files):
            issues.append("缺少 macOS 圖標文件 (.icns)")
    
    elif system == "Linux":
        # 檢查常見的 Linux 圖形庫
        try:
            from PySide6.QtGui import QGuiApplication
            # 檢查 X11/Wayland
        except ImportError:
            issues.append("無法完全初始化 Qt GUI 系統，可能缺少某些圖形庫")
    
    return {
        "system": system,
        "platform": platform_info,
        "python_version": python_version,
        "has_resources_dir": has_resources_dir,
        "has_icons_dir": has_icons_dir,
        "icon_files": icon_files,
        "issues": issues,
        "compatible": len(issues) == 0
    }

__version__ = "1.0.0" 