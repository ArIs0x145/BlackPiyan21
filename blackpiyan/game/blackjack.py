from typing import Dict, Any, List

from blackpiyan.model.card import Card
from blackpiyan.model.deck import Deck
from blackpiyan.model.dealer import Dealer

class BlackjackGame:
    """21點遊戲類，實現遊戲邏輯"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化21點遊戲
        
        Args:
            config: 遊戲配置
        """
        self.config = config
        num_decks = config.get('game', {}).get('decks', 6)
        reshuffle_threshold = config.get('game', {}).get('reshuffle_threshold', 0.4)
        dealer_hit_until = config.get('dealer', {}).get('hit_until_value', 17)
        
        self.deck = Deck(num_decks=num_decks)
        self.dealer = Dealer(hit_until_value=dealer_hit_until)
        self.reshuffle_threshold = reshuffle_threshold
    
    def play_single_round(self) -> Dict[str, Any]:
        """
        進行一局遊戲
        
        Returns:
            包含遊戲結果的字典，包括:
            - dealer_hand: 莊家的手牌
            - dealer_hand_value: 莊家的手牌點數
            - is_dealer_busted: 莊家是否爆牌
        """
        # 檢查是否需要洗牌
        self.deck.auto_shuffle_if_needed(self.reshuffle_threshold)
        
        # 莊家玩牌
        dealer_hand, dealer_hand_value = self.dealer.play_hand(self.deck)
        is_dealer_busted = self.dealer.is_busted(dealer_hand_value)
        
        # 返回結果
        return {
            'dealer_hand': dealer_hand,
            'dealer_hand_value': dealer_hand_value,
            'is_dealer_busted': is_dealer_busted
        }
    
    def reset(self) -> None:
        """重置遊戲狀態"""
        self.deck.shuffle()
    
    def set_dealer_strategy(self, hit_until_value: int) -> None:
        """
        設置莊家的補牌策略
        
        Args:
            hit_until_value: 莊家補牌策略閾值
        """
        self.dealer.set_strategy(hit_until_value)
        
    def get_dealer_strategy(self) -> int:
        """
        獲取莊家當前的補牌策略
        
        Returns:
            莊家的補牌策略閾值
        """
        return self.dealer.hit_until_value 