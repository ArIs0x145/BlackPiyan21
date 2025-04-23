from typing import Literal, Optional

class Card:
    """表示一張撲克牌"""
    
    SUITS = ["♥", "♦", "♣", "♠"]
    VALUES = {
        1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
        8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K"
    }
    
    def __init__(self, value: int, suit: str):
        """
        初始化一張卡牌
        
        Args:
            value: 牌的點數值 (1-13)
            suit: 牌的花色
        """
        if value < 1 or value > 13:
            raise ValueError(f"Card value must be between 1 and 13, got {value}")
        if suit not in self.SUITS:
            raise ValueError(f"Suit must be one of {self.SUITS}, got {suit}")
        
        self.value = value
        self.suit = suit
    
    @property
    def blackjack_value(self) -> int:
        """
        返回這張牌在21點遊戲中的點數
        
        在標準21點規則中，J/Q/K 算10點，Ace 預設計為 1 點。
        在計算總點數時，應該動態決定 Ace 是計為 1 點還是 11 點。
        
        Returns:
            牌的點數值（Ace 為 1，J/Q/K 為 10，其他按面值）
        """
        if self.value == 1:  # Ace
            return 1  # Ace 預設為 1 點，在計算總點數時再決定是否算為 11 點
        elif self.value >= 11:  # Face cards (J/Q/K)
            return 10
        else:
            return self.value
    
    def __str__(self) -> str:
        """返回牌的字符串表示，如 A♥"""
        return f"{self.VALUES[self.value]}{self.suit}"
    
    def __repr__(self) -> str:
        """返回牌的詳細表示"""
        return f"Card({self.value}, '{self.suit}')" 