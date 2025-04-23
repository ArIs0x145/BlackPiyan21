from typing import List, Tuple

from blackpiyan.model.card import Card
from blackpiyan.model.deck import Deck

class Dealer:
    """
    表示21點遊戲中的莊家
    
    當前已實現標準21點規則，包括：
    - 完整支持 Ace 點數動態計算 (1 或 11)
    - 實現莊家的標準策略（小於特定點數時補牌）
    
    未來可進一步擴展：
    - 支持玩家角色與決策
    - 添加對牌型(如黑傑克、對子等)的判斷
    - 實現更複雜的策略和遊戲規則
    """
    
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
        
        實現標準21點規則中 Ace 可以為 1 或 11 點的邏輯。
        將 Ace 優先視為 11 點，但如果總點數超過 21 點，則將 Ace 視為 1 點。
        
        Args:
            hand: 手牌列表
            
        Returns:
            手牌最優總點數
        """
        # 初始計算，將所有牌按最小值計算
        min_total = sum(card.blackjack_value for card in hand)
        
        # 計算牌中的 Ace 數量
        aces = sum(1 for card in hand if card.value == 1)
        
        # 嘗試將部分 Ace 計為 11 點，但不超過 21 點
        total = min_total
        for _ in range(aces):
            # 嘗試將一個 Ace 從 1 點變為 11 點（增加 10 點）
            if total + 10 <= 21:
                total += 10
            else:
                break
                
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