from typing import List, Tuple

from blackpiyan.model.card import Card
from blackpiyan.model.deck import Deck

class Dealer:
    """表示21點遊戲中的莊家"""
    
    def __init__(self, hit_until_value: int = 17):
        """
        初始化莊家
        
        Args:
            hit_until_value: 莊家補牌策略，當點數小於此值時補牌
        """
        self.hit_until_value = hit_until_value
    
    def set_strategy(self, hit_until_value: int) -> None:
        """
        設置補牌策略
        
        Args:
            hit_until_value: 莊家補牌策略，當點數小於此值時補牌
        """
        if hit_until_value < 12 or hit_until_value > 21:
            raise ValueError(f"Hit until value should be between 12 and 21, got {hit_until_value}")
        self.hit_until_value = hit_until_value
    
    def should_hit(self, hand_value: int) -> bool:
        """
        決定是否需要補牌
        
        Args:
            hand_value: 當前手牌點數
            
        Returns:
            是否應該補牌
        """
        return hand_value < self.hit_until_value
    
    def calculate_hand_value(self, hand: List[Card]) -> int:
        """
        計算手牌總點數
        
        Args:
            hand: 手牌列表
            
        Returns:
            手牌總點數
        """
        total = sum(card.blackjack_value for card in hand)
        return total
    
    def play_hand(self, deck: Deck) -> Tuple[List[Card], int]:
        """
        莊家玩一手牌
        
        Args:
            deck: 用於抽牌的牌組
            
        Returns:
            一個包含兩個元素的元組:
            - 莊家最終的手牌列表
            - 莊家最終的點數
        """
        # 初始抽兩張牌
        hand = [deck.draw(), deck.draw()]
        hand_value = self.calculate_hand_value(hand)
        
        # 根據策略決定是否繼續補牌
        while self.should_hit(hand_value):
            # 檢查剩餘牌數，如有必要則洗牌
            deck.auto_shuffle_if_needed()
            
            # 補牌
            hand.append(deck.draw())
            hand_value = self.calculate_hand_value(hand)
        
        return hand, hand_value
    
    def is_busted(self, hand_value: int) -> bool:
        """
        判斷是否爆牌
        
        Args:
            hand_value: 手牌點數
            
        Returns:
            是否爆牌
        """
        return hand_value > 21 