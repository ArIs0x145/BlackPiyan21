#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
跨平台字體管理工具
專注於繁體中文和英文字體的支援
"""

import platform
import logging
from typing import Dict, List, Optional
import matplotlib.font_manager as mpl_fm
from PySide6.QtGui import QFontDatabase, QFont

logger = logging.getLogger(__name__)

class FontManager:
    """跨平台字體管理類，處理GUI和圖表的字體設置，專注於繁體中文和英文支援"""
    
    # 按作業系統定義字體優先級（只保留繁體中文和英文字體）
    SYSTEM_FONTS = {
        'Windows': [
            'Microsoft JhengHei',  # 繁體中文
            'Arial',              # 英文
            'Segoe UI',          # Windows 系統界面字體
        ],
        'Darwin': [  # macOS
            'PingFang TC',        # 繁體中文
            'Heiti TC',           # 繁體中文黑體
            'Apple LiGothic',     # 蘋果儷中黑
            'Helvetica',          # 英文
            'SF Pro Text',        # macOS 系統界面字體
        ],
        'Linux': [
            'Noto Sans CJK TC',   # Google Noto字體 繁體中文
            'DejaVu Sans',        # Linux通用字體
            'Liberation Sans',    # Linux通用英文字體
        ]
    }
    
    # 通用備用字體
    FALLBACK_FONTS = ['sans-serif']
    
    def __init__(self):
        """初始化字體管理器"""
        self.system = platform.system()
        self._qt_fonts: Dict[str, QFont] = {}
        self._mpl_fonts: Dict[str, str] = {}
        
        # 初始化字體
        self._initialize_fonts()
    
    def _initialize_fonts(self) -> None:
        """初始化字體系統，檢測可用字體"""
        # 構建字體優先級列表
        priority_fonts = self.SYSTEM_FONTS.get(self.system, [])
        priority_fonts.extend(self.FALLBACK_FONTS)
        
        # 獲取系統可用字體
        qt_fonts = set(QFontDatabase().families())
        mpl_fonts = set(f.name for f in mpl_fm.fontManager.ttflist)
        
        # 記錄字體可用性
        logger.debug(f"系統: {self.system}")
        logger.debug(f"Qt可用字體數量: {len(qt_fonts)}")
        logger.debug(f"Matplotlib可用字體數量: {len(mpl_fonts)}")
        
        # 選擇第一個可用的字體
        self.primary_font = self._find_first_available_font(priority_fonts, qt_fonts)
        self.primary_mpl_font = self._find_first_available_font(priority_fonts, mpl_fonts)
        
        if not self.primary_font:
            logger.warning("無法找到合適的Qt字體，將使用系統默認字體")
            self.primary_font = 'sans-serif'
            
        if not self.primary_mpl_font:
            logger.warning("無法找到合適的Matplotlib字體，將使用系統默認字體")
            self.primary_mpl_font = 'sans-serif'
            
        logger.info(f"選擇的Qt主要字體: {self.primary_font}")
        logger.info(f"選擇的Matplotlib主要字體: {self.primary_mpl_font}")
    
    def _find_first_available_font(self, priority_list: List[str], available_fonts: set) -> str:
        """從優先級列表中找出第一個可用的字體"""
        for font in priority_list:
            if font in available_fonts:
                return font
        return ''
    
    def get_qt_font(self, size: int = 10, weight: int = -1) -> QFont:
        """
        獲取Qt字體對象
        
        Args:
            size: 字體大小
            weight: 字體粗細 (-1表示默認值)
            
        Returns:
            QFont對象
        """
        key = f"{size}_{weight}"
        if key not in self._qt_fonts:
            font = QFont(self.primary_font, size)
            if weight >= 0:
                font.setWeight(weight)
            self._qt_fonts[key] = font
        return self._qt_fonts[key]
    
    def configure_matplotlib(self) -> None:
        """配置Matplotlib的全局字體設置"""
        import matplotlib.pyplot as plt
        
        # 設置字體家族
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = [self.primary_mpl_font] + self.FALLBACK_FONTS
        
        # 確保負號正確顯示
        plt.rcParams['axes.unicode_minus'] = False
        
        logger.info("Matplotlib字體配置完成")
    
    def get_font_properties(self, size: int = 10) -> mpl_fm.FontProperties:
        """
        獲取Matplotlib的FontProperties對象
        
        Args:
            size: 字體大小
            
        Returns:
            FontProperties對象
        """
        return mpl_fm.FontProperties(
            family=self.primary_mpl_font,
            size=size
        )
    
    @property
    def qt_font_family(self) -> str:
        """獲取Qt字體族名稱"""
        return self.primary_font
    
    @property
    def mpl_font_family(self) -> str:
        """獲取Matplotlib字體族名稱"""
        return self.primary_mpl_font
    
    def get_font_info(self) -> Dict[str, str]:
        """獲取當前字體配置信息"""
        return {
            'system': self.system,
            'qt_font': self.primary_font,
            'mpl_font': self.primary_mpl_font
        } 