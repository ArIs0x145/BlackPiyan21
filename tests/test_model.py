"""測試21點模型層的功能"""

import unittest
from blackpiyan.model.card import Card
from blackpiyan.model.deck import Deck
from blackpiyan.model.dealer import Dealer

class TestCard(unittest.TestCase):
    """測試Card類"""
    
    def test_card_initialization(self):
        """測試卡牌初始化"""
        card = Card(1, "♥")
        self.assertEqual(card.value, 1)
        self.assertEqual(card.suit, "♥")
        
    def test_invalid_card_value(self):
        """測試無效的卡牌點數"""
        with self.assertRaises(ValueError):
            Card(0, "♥")
        with self.assertRaises(ValueError):
            Card(14, "♥")
    
    def test_invalid_card_suit(self):
        """測試無效的卡牌花色"""
        with self.assertRaises(ValueError):
            Card(1, "X")
    
    def test_blackjack_value(self):
        """測試21點中的牌值計算"""
        # A應該為1點
        self.assertEqual(Card(1, "♥").blackjack_value, 1)
        # 2-10應該為相應點數
        self.assertEqual(Card(2, "♥").blackjack_value, 2)
        self.assertEqual(Card(10, "♥").blackjack_value, 10)
        # J/Q/K應該為10點
        self.assertEqual(Card(11, "♥").blackjack_value, 10)
        self.assertEqual(Card(12, "♥").blackjack_value, 10)
        self.assertEqual(Card(13, "♥").blackjack_value, 10)
    
    def test_string_representation(self):
        """測試卡牌的字符串表示"""
        self.assertEqual(str(Card(1, "♥")), "A♥")
        self.assertEqual(str(Card(11, "♠")), "J♠")
        self.assertEqual(str(Card(13, "♦")), "K♦")

class TestDeck(unittest.TestCase):
    """測試Deck類"""
    
    def test_deck_initialization(self):
        """測試牌組初始化"""
        deck = Deck(num_decks=1)
        self.assertEqual(len(deck.cards), 52)
        
        deck = Deck(num_decks=6)
        self.assertEqual(len(deck.cards), 312)
    
    def test_invalid_num_decks(self):
        """測試無效的牌副數量"""
        with self.assertRaises(ValueError):
            Deck(num_decks=0)
        with self.assertRaises(ValueError):
            Deck(num_decks=-1)
    
    def test_draw_card(self):
        """測試抽牌功能"""
        deck = Deck(num_decks=1)
        initial_count = len(deck.cards)
        card = deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.cards), initial_count - 1)
    
    def test_empty_deck(self):
        """測試從空牌組抽牌"""
        deck = Deck(num_decks=1)
        # 抽光所有牌
        for _ in range(52):
            deck.draw()
            
        # 下一次抽牌應該拋出異常
        with self.assertRaises(RuntimeError):
            deck.draw()
    
    def test_remaining_percentage(self):
        """測試剩餘牌數百分比計算"""
        deck = Deck(num_decks=1)
        self.assertEqual(deck.get_remaining_percentage(), 1.0)
        
        # 抽掉一半的牌
        for _ in range(26):
            deck.draw()
        
        self.assertEqual(deck.get_remaining_percentage(), 0.5)
    
    def test_auto_shuffle(self):
        """測試自動洗牌功能"""
        deck = Deck(num_decks=1)
        
        # 抽掉70%的牌
        for _ in range(36):
            deck.draw()
        
        # 剩餘30%，低於默認閾值40%，應該自動洗牌
        shuffled = deck.auto_shuffle_if_needed()
        self.assertTrue(shuffled)
        self.assertEqual(len(deck.cards), 52)  # 洗牌後恢復到完整牌組
        
        # 現在是100%，高於閾值，不應該洗牌
        shuffled = deck.auto_shuffle_if_needed()
        self.assertFalse(shuffled)

class TestDealer(unittest.TestCase):
    """測試Dealer類"""
    
    def test_dealer_initialization(self):
        """測試莊家初始化"""
        dealer = Dealer()
        self.assertEqual(dealer.hit_until_value, 17)
        
        dealer = Dealer(hit_until_value=16)
        self.assertEqual(dealer.hit_until_value, 16)
    
    def test_set_strategy(self):
        """測試設置補牌策略"""
        dealer = Dealer()
        dealer.set_strategy(16)
        self.assertEqual(dealer.hit_until_value, 16)
        
        # 測試無效的策略值
        with self.assertRaises(ValueError):
            dealer.set_strategy(11)
        with self.assertRaises(ValueError):
            dealer.set_strategy(22)
    
    def test_should_hit(self):
        """測試補牌決策"""
        dealer = Dealer(hit_until_value=17)
        
        # 16點應該補牌
        self.assertTrue(dealer.should_hit(16))
        
        # 17點不應該補牌
        self.assertFalse(dealer.should_hit(17))
        
        # 大於17點也不應該補牌
        self.assertFalse(dealer.should_hit(18))
    
    def test_calculate_hand_value(self):
        """測試手牌點數計算"""
        dealer = Dealer()
        
        # 空手牌應該為0點
        self.assertEqual(dealer.calculate_hand_value([]), 0)
        
        # A + 10 = 11點
        hand = [Card(1, "♥"), Card(10, "♠")]
        self.assertEqual(dealer.calculate_hand_value(hand), 11)
        
        # A + J + Q = 21點
        hand = [Card(1, "♥"), Card(11, "♠"), Card(12, "♦")]
        self.assertEqual(dealer.calculate_hand_value(hand), 21)
    
    def test_is_busted(self):
        """測試爆牌判斷"""
        dealer = Dealer()
        
        # 21點不爆
        self.assertFalse(dealer.is_busted(21))
        
        # 22點爆
        self.assertTrue(dealer.is_busted(22))
    
    def test_play_hand(self):
        """測試完整的玩牌過程"""
        dealer = Dealer(hit_until_value=17)
        deck = Deck(num_decks=1)
        
        hand, hand_value = dealer.play_hand(deck)
        
        # 手牌應該至少有2張
        self.assertGreaterEqual(len(hand), 2)
        
        # 手牌點數應該>=17（除非初始兩張牌就爆了）
        if hand_value <= 21:
            self.assertGreaterEqual(hand_value, 17)

if __name__ == "__main__":
    unittest.main() 