import os
import yaml
from typing import Any, Dict, Optional, Union

class ConfigManager:
    """配置管理器，負責讀取和管理YAML配置文件"""
    
    def __init__(self, config_path: str):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路徑
        """
        self.config_path = config_path
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        從YAML文件加載配置
        
        Args:
            config_path: 配置文件路徑
            
        Returns:
            配置字典
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config or {}
    
    def get_config(self) -> Dict[str, Any]:
        """
        獲取當前配置
        
        Returns:
            完整配置字典
        """
        return self.config
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        獲取特定配置項的值
        
        Args:
            key_path: 點分隔的配置項路徑，例如 'dealer.hit_until_value'
            default: 如果配置項不存在，返回的默認值
            
        Returns:
            配置項的值，如果不存在則返回默認值
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys:
            if not isinstance(config, dict) or key not in config:
                return default
            config = config[key]
        
        return config
    
    def update_config(self, key_path: str, value: Any) -> None:
        """
        更新配置項
        
        Args:
            key_path: 點分隔的配置項路徑，例如 'dealer.hit_until_value'
            value: 新的配置值
        """
        keys = key_path.split('.')
        config = self.config
        
        # 遍歷路徑到倒數第二個鍵
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            elif not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # 設置最後一個鍵的值
        config[keys[-1]] = value
    
    def save_config(self, path: Optional[str] = None) -> None:
        """
        保存配置到文件
        
        Args:
            path: 保存配置的路徑，如果為None則使用初始化時的路徑
        """
        save_path = path or self.config_path
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True) 