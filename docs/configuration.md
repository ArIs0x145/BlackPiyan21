# BlackPiyan 配置說明

本文檔詳細說明 BlackPiyan 的配置選項和自定義設置，幫助用戶根據自己的需求定制模擬參數。

## 目錄

1. [配置文件位置](#配置文件位置)
2. [配置格式](#配置格式)
3. [配置項詳解](#配置項詳解)
   - [遊戲配置](#遊戲配置)
   - [莊家配置](#莊家配置)
   - [模擬配置](#模擬配置)
   - [日誌配置](#日誌配置)
   - [輸出配置](#輸出配置)
   - [字體配置](#字體配置)
4. [配置示例](#配置示例)
5. [高級配置](#高級配置)
6. [故障排除](#故障排除)

## 配置文件位置

BlackPiyan 默認使用 `configs/default.yaml` 作為配置文件。您可以：

- 直接修改 `default.yaml` 文件
- 創建自己的配置文件，並使用命令行參數指定：
  ```bash
  python main.py --config configs/my_config.yaml
  ```
- 在 GUI 中直接調整參數（無需手動修改配置文件）

## 配置格式

BlackPiyan 使用 YAML 格式的配置文件，其結構清晰易讀。YAML 是一種人類友好的數據序列化標準，使用縮進表示層級關係。

基本語法：
- 使用冒號分隔鍵和值：`key: value`
- 使用縮進表示嵌套結構
- 列表項使用連字符開頭：`- item`
- 支持字符串、數字、布爾值和複合數據類型

示例：
```yaml
# 這是頂層鍵
top_level:
  # 這是嵌套鍵
  nested_key: value
  # 這是列表
  list_key:
    - item1
    - item2
  # 這是帶有嵌套結構的列表
  complex_list:
    - name: item1
      value: 10
    - name: item2
      value: 20
```

## 配置項詳解

### 遊戲配置

`game` 部分控制 21 點遊戲的基本設置。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `decks` | 整數 | 6 | 使用的牌副數量，標準 21 點通常使用 6-8 副 |
| `reshuffle_threshold` | 浮點數 | 0.4 | 當剩餘牌數低於總牌數的此比例時洗牌，範圍 0.0-1.0 |

```yaml
game:
  decks: 6
  reshuffle_threshold: 0.4
```

### 莊家配置

`dealer` 部分控制莊家的行為。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `hit_until_value` | 整數 | 17 | 莊家的補牌策略值，當手牌點數小於此值時補牌，否則停牌 |

```yaml
dealer:
  hit_until_value: 17
```

### 模擬配置

`simulation` 部分控制模擬的運行參數。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `min_games_per_strategy` | 整數 | 1000 | 每種策略至少模擬的局數 |
| `total_min_games` | 整數 | 2000 | 總共至少模擬的局數 |
| `strategies` | 整數列表 | [16, 17, 18] | 要測試的莊家補牌策略值列表 |

```yaml
simulation:
  min_games_per_strategy: 1000
  total_min_games: 2000
  strategies:
    - 16
    - 17
    - 18
```

#### 實時更新配置

`realtime_update` 是 `simulation` 的子配置，控制實時更新圖表的行為。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `enabled` | 布爾值 | true | 是否啟用實時更新 |
| `update_interval` | 整數 | 100 | 每模擬多少局更新一次圖表 |
| `min_update_interval` | 整數 | 50 | 最小更新間隔（局數） |
| `max_update_interval` | 整數 | 500 | 最大更新間隔（局數） |
| `auto_adjust` | 布爾值 | true | 是否根據總局數自動調整更新間隔 |

```yaml
simulation:
  # 其他配置...
  realtime_update:
    enabled: true
    update_interval: 100
    min_update_interval: 50
    max_update_interval: 500
    auto_adjust: true
```

### 日誌配置

`logging` 部分控制日誌記錄的行為。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `level` | 字符串 | "INFO" | 日誌級別，可選 "DEBUG", "INFO", "WARNING", "ERROR" |
| `file` | 字符串 | "logs/blackpiyan.log" | 日誌文件路徑 |
| `format` | 字符串 | "%(asctime)s..." | 日誌格式 |

```yaml
logging:
  level: INFO
  file: logs/blackpiyan.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### 輸出配置

`output` 部分控制結果的保存位置。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `data_dir` | 字符串 | "results/data" | 結果數據保存目錄 |
| `charts_dir` | 字符串 | "results/charts" | 圖表保存目錄 |

```yaml
output:
  data_dir: results/data
  charts_dir: results/charts
```

### 字體配置

`font` 部分控制圖表中的字體設置，對於非英文環境尤為重要。

| 配置項 | 類型 | 默認值 | 說明 |
|------|------|-------|------|
| `family` | 字符串 | "Microsoft JhengHei" | 首選字體，用於顯示中文字符 |
| `fallback` | 字符串 | "DejaVu Sans" | 後備字體，當首選字體不可用時使用 |

```yaml
font:
  family: "Microsoft JhengHei"
  fallback: "DejaVu Sans"
```

更多字體設置信息，請參閱 [跨平台字體支持](./font_support.md)。

## 配置示例

以下是一個完整的配置文件示例：

```yaml
---
# BlackPiyan 配置文件

# 遊戲配置
game:
  decks: 6                  # 使用的牌副數量
  reshuffle_threshold: 0.4  # 當剩餘牌數低於此閾值時洗牌

# 莊家配置
dealer:
  hit_until_value: 17       # 莊家補牌策略值 (小於此值就補牌)

# 模擬配置
simulation:
  min_games_per_strategy: 1000  # 每種策略至少模擬的局數
  total_min_games: 2000         # 總共至少模擬的局數
  strategies:                   # 要測試的所有策略值
    - 16
    - 17
    - 18
  # 實時更新配置
  realtime_update:
    enabled: true               # 是否啟用實時更新
    update_interval: 100        # 每多少局更新一次圖表
    min_update_interval: 50     # 最小更新間隔 (局數)
    max_update_interval: 500    # 最大更新間隔 (局數)
    auto_adjust: true           # 是否根據總局數自動調整更新間隔

# 日誌配置
logging:
  level: INFO                  # 日誌級別 (DEBUG, INFO, WARNING, ERROR)
  file: logs/blackpiyan.log    # 日誌文件
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 結果輸出配置
output:
  data_dir: results/data        # 結果數據存儲目錄
  charts_dir: results/charts    # 圖表輸出目錄 
  
# 字體配置
font:
  family: "Microsoft JhengHei"  # 中文顯示字體
  fallback: "DejaVu Sans"       # 後備字體 
```

## 高級配置

### 自定義策略範圍

如果要測試更廣泛的策略範圍，可以修改 `strategies` 項：

```yaml
simulation:
  strategies:
    - 15
    - 16
    - 17
    - 18
    - 19
```

### 增加模擬局數

對於更精確的結果，可以增加模擬局數：

```yaml
simulation:
  min_games_per_strategy: 10000  # 增加到 10,000 局
```

### 自定義圖表輸出

如果需要將圖表保存到特定位置：

```yaml
output:
  charts_dir: "my_results/blackpiyan_charts"
```

## 故障排除

### 配置文件未找到

如果遇到「配置文件未找到」錯誤：

- 確認 `configs/default.yaml` 文件存在
- 如果使用自定義配置，確保路徑正確：
  ```bash
  python main.py --config configs/my_config.yaml
  ```

### 配置選項無效

如果遇到「配置選項無效」錯誤：

- 檢查 YAML 格式是否正確（縮進、冒號等）
- 確保所有必需的配置項都存在
- 確保數值在有效範圍內（如 `reshuffle_threshold` 應在 0.0-1.0 之間）

### 字體問題

如果圖表中的中文顯示為方框或亂碼，請：
- 檢查系統中是否安裝了指定的字體
- 嘗試使用系統已安裝的其他中文字體
- 參考 [跨平台字體支持](./font_support.md) 文檔