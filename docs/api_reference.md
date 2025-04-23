# BlackPiyan API 參考文檔 (v1.0.0)

本文檔提供 BlackPiyan 各模塊的詳細 API 說明，幫助開發者理解和擴展系統功能。

## 目錄

1. [核心模塊](#核心模塊)
   - [ConfigManager](#configmanager)
   - [Logger](#logger)
2. [遊戲邏輯](#遊戲邏輯)
   - [BlackjackGame](#blackjackgame)
   - [Card](#card)
   - [Deck](#deck)
   - [Dealer](#dealer)
3. [模擬引擎](#模擬引擎)
   - [Simulator](#simulator)
4. [數據分析](#數據分析)
   - [Analyzer](#analyzer)
5. [可視化](#可視化)
   - [Visualizer](#visualizer)

---

## 核心模塊

### ConfigManager

`blackpiyan.config.config_manager.ConfigManager`

處理配置文件加載和訪問。

#### 初始化

```python
def __init__(self, config_path: str)
```

**參數**:
- `config_path`: 配置文件路徑

#### 方法

```python
def get_config(self) -> Dict[str, Any]
```
返回配置字典。

**返回**:
- 包含所有配置項的字典

```python
def validate_config(self) -> bool
```
驗證配置是否有效。

**返回**:
- 配置有效時返回 True，否則拋出異常

### Logger

`blackpiyan.utils.logger.Logger`

提供整個應用程序的日誌功能。

#### 初始化

```python
def __init__(self, config: Dict[str, Any])
```

**參數**:
- `config`: 配置字典，包含日誌設置

#### 方法

```python
def get_logger(self, name: str) -> logging.Logger
```
獲取指定名稱的日誌記錄器。

**參數**:
- `name`: 日誌記錄器名稱

**返回**:
- 配置好的 Logger 實例

---

## 遊戲邏輯

### BlackjackGame

`blackpiyan.game.blackjack.BlackjackGame`

實現 21 點遊戲核心邏輯，管理牌組和莊家動作。

#### 初始化

```python
def __init__(self, config: Dict[str, Any])
```

**參數**:
- `config`: 遊戲配置

#### 方法

```python
def play_single_round(self) -> Dict[str, Any]
```
模擬一局 21 點遊戲。

**返回**:
- 包含遊戲結果的字典，包括莊家手牌、點數和是否爆牌

```python
def reset(self) -> None
```
重置遊戲狀態，洗牌。

```python
def set_dealer_strategy(self, hit_until_value: int) -> None
```
設置莊家的補牌策略。

**參數**:
- `hit_until_value`: 莊家補牌策略閾值

```python
def get_dealer_strategy(self) -> int
```
獲取莊家當前的補牌策略閾值。

**返回**:
- 莊家的補牌策略閾值

### Card

`blackpiyan.model.card.Card`

表示一張撲克牌。

#### 初始化

```python
def __init__(self, value: int, suit: str)
```

**參數**:
- `value`: 牌的點數值 (1-13)
- `suit`: 牌的花色 (♥, ♦, ♣, ♠)

#### 屬性

```python
@property
def blackjack_value(self) -> int
```
返回這張牌在 21 點遊戲中的點數。

**返回**:
- 21 點遊戲中的點數值

### Deck

`blackpiyan.model.deck.Deck`

表示一副或多副撲克牌。

#### 初始化

```python
def __init__(self, num_decks: int = 1)
```

**參數**:
- `num_decks`: 牌組數量，默認為 1

#### 方法

```python
def shuffle(self) -> None
```
洗牌。

```python
def deal_card(self) -> Card
```
發一張牌。

**返回**:
- 一個 Card 對象

```python
def remaining(self) -> int
```
獲取剩餘牌數。

**返回**:
- 剩餘牌數

```python
def auto_shuffle_if_needed(self, threshold: float) -> bool
```
如果剩餘牌數低於閾值，則自動洗牌。

**參數**:
- `threshold`: 洗牌閾值 (0-1)

**返回**:
- 是否執行了洗牌操作

### Dealer

`blackpiyan.model.dealer.Dealer`

模擬 21 點遊戲中的莊家行為。

#### 初始化

```python
def __init__(self, hit_until_value: int = 17)
```

**參數**:
- `hit_until_value`: 莊家補牌策略閾值

#### 方法

```python
def play_hand(self, deck: Deck) -> Tuple[List[Card], int]
```
模擬莊家玩一手牌。

**參數**:
- `deck`: 牌組

**返回**:
- 包含手牌列表和最終點數的元組

```python
def set_strategy(self, hit_until_value: int) -> None
```
設置莊家的補牌策略。

**參數**:
- `hit_until_value`: 新的補牌策略閾值

```python
def is_busted(self, hand_value: int) -> bool
```
判斷是否爆牌。

**參數**:
- `hand_value`: 手牌點數

**返回**:
- 是否爆牌

```python
def calculate_dynamic_hand_value(self, hand: List[Card]) -> int
```
計算手牌總點數，動態處理 Ace 點數。

**參數**:
- `hand`: 手牌列表

**返回**:
- 手牌最優總點數（Ace 可為 1 或 11，以獲得最佳點數且不超過 21 點）

```python
def should_hit(self, hand_value: int) -> bool
```
決定是否需要補牌。

**參數**:
- `hand_value`: 當前手牌點數

**返回**:
- 是否應該補牌

```python
def calculate_hand_value(self, hand: List[Card]) -> int
```
計算手牌總點數。

**參數**:
- `hand`: 手牌列表

**返回**:
- 手牌總點數

---

## 模擬引擎

### Simulator

`blackpiyan.simulation.simulator.Simulator`

執行 21 點遊戲模擬，收集不同策略下的結果數據。

#### 初始化

```python
def __init__(self, config: Dict[str, Any])
```

**參數**:
- `config`: 配置字典

#### 方法

```python
def run_single_strategy(self, strategy: int, min_games: int) -> List[Dict[str, Any]]
```
模擬指定策略的多局遊戲。

**參數**:
- `strategy`: 莊家補牌策略閾值
- `min_games`: 最少模擬局數

**返回**:
- 包含每局遊戲結果的列表

```python
def run_multiple_strategies(self, strategies: List[int], min_games_per_strategy: int) -> Dict[int, List[Dict[str, Any]]]
```
模擬多種策略，每種策略多局遊戲。

**參數**:
- `strategies`: 策略列表
- `min_games_per_strategy`: 每種策略的最少模擬局數

**返回**:
- 以策略值為鍵，遊戲結果列表為值的字典

---

## 數據分析

### Analyzer

`blackpiyan.analysis.analyzer.Analyzer`

分析模擬結果，計算統計數據和比較不同策略。

#### 初始化

```python
def __init__(self, results: Dict[int, List[Dict[str, Any]]])
```

**參數**:
- `results`: 模擬結果，以策略值為鍵，遊戲結果列表為值

#### 方法

```python
def calculate_statistics(self, strategy: int) -> Dict[str, Any]
```
計算指定策略的統計數據。

**參數**:
- `strategy`: 策略值

**返回**:
- 包含統計信息的字典（總局數、平均點數、中位數、爆牌率等）

```python
def get_distribution(self, strategy: int) -> Dict[int, int]
```
獲取指定策略的點數分布。

**參數**:
- `strategy`: 策略值

**返回**:
- 以點數為鍵，次數為值的字典

```python
def compare_strategies(self) -> pd.DataFrame
```
比較不同策略的表現。

**返回**:
- 包含各策略統計數據的 DataFrame

---

## 可視化

### Visualizer

`blackpiyan.visualization.visualizer.Visualizer`

將分析結果可視化為圖表。

#### 初始化

```python
def __init__(self, analyzer: Analyzer, config: Dict[str, Any])
```

**參數**:
- `analyzer`: 分析器實例
- `config`: 配置字典

#### 方法

```python
def plot_distribution(self, strategy: int) -> None
```
繪製指定策略的點數分布圖。

**參數**:
- `strategy`: 策略值

```python
def plot_comparison(self) -> None
```
繪製不同策略的比較圖表。

```python
def save_figure(self, fig, filename: str) -> str
```
保存圖表到文件。

**參數**:
- `fig`: 圖表對象
- `filename`: 文件名

**返回**:
- 保存的文件路徑

---

## 使用示例

### 基本使用

```python
from blackpiyan.config.config_manager import ConfigManager
from blackpiyan.simulation.simulator import Simulator
from blackpiyan.analysis.analyzer import Analyzer
from blackpiyan.visualization.visualizer import Visualizer

# 加載配置
config_manager = ConfigManager('configs/default.yaml')
config = config_manager.get_config()

# 執行模擬
simulator = Simulator(config)
strategies = [16, 17, 18]
results = simulator.run_multiple_strategies(strategies, 1000)

# 分析結果
analyzer = Analyzer(results)
stats = analyzer.calculate_statistics(17)
print(f"策略 17 爆牌率: {stats['bust_rate']*100:.2f}%")

# 生成圖表
visualizer = Visualizer(analyzer, config)
visualizer.plot_distribution(17)
visualizer.plot_comparison()
```

### 自定義策略模擬

```python
# 自定義策略列表
custom_strategies = [15, 16, 17, 18, 19]
results = simulator.run_multiple_strategies(custom_strategies, 2000)

# 分析和可視化
analyzer = Analyzer(results)
visualizer = Visualizer(analyzer, config)
visualizer.plot_comparison()
``` 