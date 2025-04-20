#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
測試跨平台字體兼容性
"""

import os
import sys
import platform
import logging
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import unittest
import matplotlib

from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.visualization.visualizer import Visualizer

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("font_test")

class TestCrossPlatformFont(unittest.TestCase):
    """測試跨平台字體兼容性的測試類"""
    
    def setUp(self):
        """測試初始化"""
        # 載入配置
        config_path = 'configs/default.yaml'
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        
        # 創建輸出目錄
        self.output_dir = "results/font_tests"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def test_font_availability(self):
        """測試各種中文字體在當前系統的可用性"""
        # 準備常見的中文字體列表
        common_cjk_fonts = [
            # Windows 字體
            "Microsoft JhengHei", "Microsoft YaHei", "SimSun", "SimHei", "MingLiU", "NSimSun",
            # macOS 字體
            "PingFang TC", "PingFang SC", "Heiti TC", "Heiti SC", "Apple LiGothic", "Hiragino Sans GB",
            # Linux 字體
            "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP", 
            "WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Droid Sans Fallback",
            # 通用字體
            "Arial Unicode MS", "DejaVu Sans"
        ]
        
        # 獲取當前系統上所有可用的字體
        available_fonts = set([f.name for f in fm.fontManager.ttflist])
        
        # 檢查每個常見中文字體是否可用
        found_cjk_fonts = []
        for font in common_cjk_fonts:
            if font in available_fonts:
                found_cjk_fonts.append(font)
                logger.info(f"✓ 已找到字體: {font}")
            else:
                logger.info(f"✗ 未找到字體: {font}")
        
        # 輸出系統信息
        logger.info(f"作業系統: {platform.system()} {platform.version()}")
        logger.info(f"Python 版本: {platform.python_version()}")
        logger.info(f"Matplotlib 版本: {matplotlib.__version__}")
        logger.info(f"找到的中文字體數量: {len(found_cjk_fonts)}")
        
        # 驗證至少找到一個中文字體
        self.assertTrue(len(found_cjk_fonts) > 0, "找不到任何中文字體，這可能會導致中文顯示問題")
        
        return found_cjk_fonts
    
    def test_font_rendering(self):
        """測試字體渲染中文的效果"""
        # 獲取可用字體
        fonts = self.test_font_availability()
        if not fonts:
            self.skipTest("沒有找到可用的中文字體，跳過渲染測試")
            return
        
        # 準備測試文本
        test_text = "測試中文字體與負號 (-10)"
        
        # 為每個字體創建測試圖表
        for i, font in enumerate(fonts[:min(3, len(fonts))]):  # 最多測試3個字體
            plt.figure(figsize=(10, 3))
            plt.text(0.5, 0.5, test_text, fontsize=16, ha='center', va='center',
                    fontproperties=fm.FontProperties(family=font))
            plt.title(f"字體測試: {font}", fontproperties=fm.FontProperties(family=font))
            plt.axis('off')
            
            # 保存測試圖表
            save_path = os.path.join(self.output_dir, f"font_test_{i}_{font.replace(' ', '_')}.png")
            plt.savefig(save_path, dpi=200)
            plt.close()
            logger.info(f"已生成字體測試圖表: {save_path}")
        
        # 確認文件生成
        self.assertTrue(os.path.exists(save_path), "未能生成字體測試圖表")
    
    def test_visualizer_font_handling(self):
        """測試Visualizer類對不同字體的處理"""
        # 創建基本圖表
        plt.figure(figsize=(10, 6))
        x = np.linspace(-10, 10, 100)
        y = np.sin(x)
        
        # 使用Visualizer處理字體
        analyzer = None  # 這裡不需要真正的分析器
        visualizer = Visualizer(analyzer, self.config)
        
        # 顯示Visualizer選擇的字體
        logger.info(f"Visualizer選擇的字體: {visualizer.font_family}")
        logger.info(f"Matplotlib字體族: {plt.rcParams['font.family']}")
        
        # 確認Visualizer找到了字體
        self.assertIsNotNone(visualizer.font_family, "Visualizer未能選擇字體")
        
        # 創建測試圖表
        plt.plot(x, y)
        plt.title("測試中文字體與負號 (-10 到 10)", fontproperties=visualizer.font_prop)
        plt.xlabel("X軸 (負值測試)", fontproperties=visualizer.font_prop)
        plt.ylabel("Y軸", fontproperties=visualizer.font_prop)
        plt.grid(True)
        
        # 保存測試圖表
        save_path = os.path.join(self.output_dir, "visualizer_font_test.png")
        plt.savefig(save_path, dpi=300)
        plt.close()
        logger.info(f"已生成Visualizer字體測試圖表: {save_path}")
        
        # 確認文件生成
        self.assertTrue(os.path.exists(save_path), "未能生成Visualizer字體測試圖表")
    
    def test_cross_platform_compatibility(self):
        """測試不同平台的字體兼容性"""
        # 獲取當前作業系統
        system = platform.system()
        logger.info(f"當前作業系統: {system}")
        
        # 模擬不同作業系統的字體列表
        test_configs = {
            'windows': {'family': 'Microsoft JhengHei'},
            'macos': {'family': 'PingFang TC'},
            'linux': {'family': 'Noto Sans CJK TC'}
        }
        
        # 使用當前平台測試
        analyzer = None
        plt.figure(figsize=(10, 4))
        
        # 創建Visualizer實例模擬不同平台
        for i, (platform_name, font_config) in enumerate(test_configs.items()):
            # 復制配置並設置模擬的字體
            custom_config = self.config.copy()
            custom_config['font'] = font_config
            
            # 創建Visualizer實例
            vis = Visualizer(analyzer, custom_config)
            
            # 記錄結果
            logger.info(f"模擬平台: {platform_name}")
            logger.info(f"配置字體: {font_config['family']}")
            logger.info(f"選擇的字體: {vis.font_family}")
            
            # 驗證Visualizer總能找到字體
            self.assertIsNotNone(vis.font_family, f"在模擬{platform_name}時，Visualizer未能找到替代字體")
        
        self.assertTrue(True, "跨平台字體測試完成")

if __name__ == "__main__":
    unittest.main() 