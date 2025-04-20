import logging
import os
from typing import Dict, Any, Optional

class Logger:
    """日誌工具類，提供統一的日誌配置和獲取方法"""
    
    # 單例模式，確保全局只有一個日誌配置
    _instance = None
    
    def __new__(cls, config: Optional[Dict[str, Any]] = None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._loggers = {}
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # 如果已經初始化過，則跳過
        if self._initialized:
            return
        
        self.config = config or {}
        self._setup_logging()
        self._initialized = True
    
    def _setup_logging(self) -> None:
        """設置日誌配置"""
        log_level = self._get_log_level()
        log_format = self.config.get('logging', {}).get(
            'format', 
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        log_file = self.config.get('logging', {}).get('file', 'logs/blackpiyan.log')
        
        # 確保日誌目錄存在
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # 配置根日誌記錄器
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # 清除可能存在的處理器
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 創建文件處理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # 創建控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    def _get_log_level(self) -> int:
        """從配置中獲取日誌級別"""
        level_str = self.config.get('logging', {}).get('level', 'INFO').upper()
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(level_str, logging.INFO)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        獲取特定名稱的日誌記錄器
        
        Args:
            name: 日誌記錄器名稱
            
        Returns:
            配置好的日誌記錄器
        """
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)
        
        return self._loggers[name]
    
    def set_level(self, level: str) -> None:
        """
        設置日誌級別
        
        Args:
            level: 日誌級別字符串 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        level_str = level.upper()
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        log_level = level_map.get(level_str, logging.INFO)
        
        # 設置根日誌記錄器級別
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # 設置所有處理器的級別
        for handler in root_logger.handlers:
            handler.setLevel(log_level) 