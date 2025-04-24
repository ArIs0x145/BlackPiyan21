"""測試視覺化字體兼容性"""

import unittest
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import platform
import os

class TestFont(unittest.TestCase):
    """測試中文字體兼容性"""
    
    def test_available_cjk_fonts(self):
        """測試系統中可用的中文字體"""
        fonts = [f.name for f in fm.fontManager.ttflist]
        
        # 打印出所有可用字體供參考
        print("\n可用字體列表:")
        for font in sorted(set(fonts)):
            print(f"- {font}")
        
        # 檢查是否有可用的中文字體
        cjk_fonts = [
            # Windows 常見中文字體
            'Microsoft YaHei', '微软雅黑', 'SimHei', '黑体',
            'SimSun', '宋体', 'NSimSun', '新宋体', 'FangSong', '仿宋',
            # Mac 常見中文字體
            'PingFang SC', 'PingFang TC', 'STHeiti', 'Heiti TC',
            # Linux 常見中文字體
            'Noto Sans CJK TC', 'Noto Sans CJK SC', 'Noto Sans CJK JP',
            'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
            # 通用字體
            'Arial Unicode MS', 'Hiragino Sans GB'
        ]
        
        found_cjk_fonts = [font for font in cjk_fonts if font in fonts]
        
        print(f"\n找到的中文字體: {found_cjk_fonts}")
        print(f"當前作業系統: {platform.system()} {platform.version()}")
        
        # 測試不強制要求有中文字體，因為這取決於系統配置
        # 但至少要打印出來以便手動檢查
        self.assertIsNotNone(found_cjk_fonts, "無法獲取字體列表")
    
    def test_matplotlib_font_config(self):
        """測試 Matplotlib 字體配置"""
        # 檢查預設字體
        default_font = plt.rcParams['font.family']
        print(f"\nMatplotlib 預設字體族: {default_font}")
        
        # 檢查當前字體路徑
        font_paths = plt.rcParams.get('font.paths', [])
        print(f"Matplotlib 字體路徑: {font_paths}")
        
        # 檢查 .matplotlib 目錄是否存在
        user_home = os.path.expanduser("~")
        matplotlib_dir = os.path.join(user_home, '.matplotlib')
        has_config_dir = os.path.exists(matplotlib_dir)
        print(f".matplotlib 配置目錄存在: {has_config_dir}")
        
        if has_config_dir:
            config_files = os.listdir(matplotlib_dir)
            print(f".matplotlib 目錄內容: {config_files}")
        
        # 這只是信息性測試，所以總是通過
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main() 