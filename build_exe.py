#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BlackPiyan GUI 打包腳本
此腳本用於將 BlackPiyan GUI 打包為獨立的可執行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """檢查是否已安裝 PyInstaller"""
    try:
        import PyInstaller
        print("已檢測到 PyInstaller")
        return True
    except ImportError:
        print("未檢測到 PyInstaller，正在安裝...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return False

def clean_previous_build():
    """清理之前的構建文件"""
    paths_to_clean = ['dist', 'build', '*.spec']
    for path in paths_to_clean:
        if '*' in path:  # 通配符路徑
            import glob
            for file_path in glob.glob(path):
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"已刪除: {file_path}")
        else:  # 目錄路徑
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"已刪除: {path}")

def ensure_icons_folder():
    """確保圖標文件夾存在"""
    icons_dir = Path("gui/resources/icons")
    if not icons_dir.exists():
        print(f"創建圖標目錄: {icons_dir}")
        icons_dir.mkdir(parents=True, exist_ok=True)
    
    # 檢查圖標文件
    icon_file = icons_dir / "piyan.ico"
    if not icon_file.exists():
        print(f"警告: 圖標文件 {icon_file} 不存在!")
        print("打包的應用程序將使用默認圖標")
    else:
        print(f"檢測到圖標文件: {icon_file}")
    
    return str(icon_file) if icon_file.exists() else None

def build_exe():
    """構建可執行文件"""
    print("開始構建 BlackPiyan GUI 可執行文件...")
    
    # 確認 PyInstaller 已安裝
    check_pyinstaller()
    
    # 清理之前的構建
    clean_previous_build()
    
    # 確保圖標目錄存在
    icon_path = ensure_icons_folder()
    
    # 構建命令
    cmd = [
        "pyinstaller",
        "--name=BlackPiyan",
        "--windowed",  # 不顯示控制台窗口
        "--noconfirm",  # 覆蓋現有文件
        "--clean",      # 清理臨時文件
        "--add-data=gui/resources;gui/resources",  # 添加資源文件
        "--add-data=configs;configs",              # 添加配置文件
    ]
    
    # 如果有圖標，添加圖標
    if icon_path:
        cmd.append(f"--icon={icon_path}")
    
    # 添加主程序文件
    cmd.append("run_gui.py")
    
    # 執行構建
    print("執行命令:", " ".join(cmd))
    subprocess.call(cmd)
    
    print("\n構建完成!")
    print(f"可執行文件位於 dist/BlackPiyan 目錄下")

if __name__ == "__main__":
    build_exe() 