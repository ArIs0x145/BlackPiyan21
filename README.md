# BlackPiyan

21點（Blackjack）遊戲中莊家補牌策略的模擬和分析工具

## 功能特點

- 模擬21點遊戲中莊家的不同補牌策略
- 使用6副牌（312張）進行遊戲
- 自動在剩餘牌數低於40%時洗牌
- 收集並分析各種補牌策略下莊家的點數分布
- 生成各種策略的比較圖表和統計數據

## 安裝與使用

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 運行模擬

```bash
python main.py
```

## 配置說明

配置文件位於 `configs/default.yaml`，可自定義以下設置：

- 使用的牌副數量
- 洗牌閾值
- 要測試的莊家補牌策略
- 每種策略的模擬局數
- 日誌設置
- 結果輸出路徑

## 配置示例

```yaml
game:
  decks: 6                  # 使用的牌副數量
  reshuffle_threshold: 0.4  # 當剩餘牌數低於此閾值時洗牌

dealer:
  hit_until_value: 17       # 莊家補牌策略值 (小於此值就補牌)

simulation:
  min_games_per_strategy: 1000  # 每種策略至少模擬的局數
  strategies:                   # 要測試的所有策略值
    - 16
    - 17
    - 18
```

## 輸出結果

模擬結果將以兩種形式呈現：

1. 控制台和日誌文件中的統計信息
2. `results/charts/` 目錄下的圖表:
   - 每種策略的點數分布圖
   - 不同策略的比較圖

## 開發者

BlackPiyan Team 

## 運行測試

BlackPiyan 提供了完整的測試套件：

```bash
# 運行所有測試
python -m unittest discover tests

# 運行特定測試模塊
python -m unittest tests.test_model
python -m unittest tests.test_simulation

# 運行單個測試類
python -m unittest tests.test_model.TestCard
```

## 系統需求

- Python 3.8 或更高版本
- 依賴庫: 見 requirements.txt 