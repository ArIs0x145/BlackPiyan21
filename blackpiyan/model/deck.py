import random
from typing import List, Optional

from blackpiyan.model.card import Card

class Deck:
    """表示一個牌組，可以包含多副牌"""
    
    def __init__(self, num_decks: int = 6):
        """
        初始化牌組
        
        Args:
            num_decks: 牌組中包含的標準撲克牌副數，默認為6
        """
        if num_decks <= 0:
            raise ValueError(f"Number of decks must be positive, got {num_decks}")
        
        self.num_decks = num_decks
        self.initial_cards_count = num_decks * 52
        self.cards = self._create_decks(num_decks)
        self.shuffle()
    
    def _create_decks(self, num_decks: int) -> List[Card]:
        """創建多副牌"""
        cards = []
        for _ in range(num_decks):
            for suit in Card.SUITS:
                for value in range(1, 14):
                    cards.append(Card(value, suit))
        return cards
    
    def shuffle(self) -> None:
        """洗牌"""
        self.cards = self._create_decks(self.num_decks)
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        """
        從牌組中抽取一張牌
        
        Returns:
            抽取的牌
            
        Raises:
            RuntimeError: 如果牌組已空
        """
        if not self.cards:
            raise RuntimeError("Cannot draw from an empty deck")
        return self.cards.pop()
    
    def get_remaining_percentage(self) -> float:
        """
        返回牌組中剩餘牌的百分比
        
        Returns:
            剩餘牌佔總牌數的百分比 (0.0-1.0)
        """
        return len(self.cards) / self.initial_cards_count
    
    def auto_shuffle_if_needed(self, threshold: float = 0.4) -> bool:
        """
        如果剩餘牌數低於閾值則自動洗牌
        
        Args:
            threshold: 洗牌閾值，默認為40%
            
        Returns:
            是否進行了洗牌
        """
        if self.get_remaining_percentage() < threshold:
            self.shuffle()
            return True
        return False
    
    def __len__(self) -> int:
        """返回牌組中剩餘的牌數"""
        return len(self.cards) 