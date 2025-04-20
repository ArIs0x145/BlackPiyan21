# 跨平台字體支持文檔

## 目錄

1. [概述](#概述)
2. [字體配置](#字體配置)
3. [支持的字體](#支持的字體)
4. [操作系統特定說明](#操作系統特定說明)
5. [圖表中文顯示問題](#圖表中文顯示問題)
6. [字體測試](#字體測試)
7. [高級設置](#高級設置)
8. [常見問題與解決方案](#常見問題與解決方案)

## 概述

BlackPiyan 支持在不同作業系統（Windows、macOS 和 Linux）上正確顯示中文字體。系統通過智能字體選擇和自動回退機制確保圖表中的中文文字能夠正確顯示，即使在某些平台上沒有安裝指定的字體。

本文檔詳細說明如何配置字體、測試字體顯示效果，以及解決常見的字體顯示問題。

## 字體配置

### 基本配置

在 `configs/default.yaml` 文件中，可以設置字體相關配置：

```yaml
# 字體配置
font:
  family: "Microsoft JhengHei"     # 中文顯示字體
  fallback: "DejaVu Sans"       # 後備字體 
```

### 配置項說明

- `family`: 首選字體，用於顯示中文字符。建議使用系統內置的中文字體。
- `fallback`: 當首選字體無法顯示某些字符時使用的後備字體。

### 動態字體選擇機制

BlackPiyan 採用了智能字體選擇機制，按照以下順序選擇字體：

1. 首先嘗試配置文件中指定的 `family` 字體
2. 如果不可用，則根據當前操作系統選擇合適的系統內置中文字體
3. 如果系統內置中文字體都不可用，嘗試使用後備字體 `fallback`
4. 如果後備字體也不可用，則回退到 'sans-serif' 通用字體族

## 支持的字體

### Windows 推薦字體

- Microsoft JhengHei (微軟正黑體)
- Microsoft YaHei (微軟雅黑)
- SimSun (宋體)
- SimHei (黑體)
- MingLiU (細明體)

### macOS 推薦字體

- PingFang TC
- PingFang SC
- Heiti TC
- Hiragino Sans GB

### Linux 推薦字體

- Noto Sans CJK TC
- Noto Sans CJK SC
- WenQuanYi Micro Hei
- Droid Sans Fallback

## 操作系統特定說明

### Windows

Windows 系統通常已預裝多種中文字體，如 Microsoft JhengHei、Microsoft YaHei 等，無需額外安裝即可正常顯示中文。

### macOS

macOS 系統內置 PingFang 和 Heiti 等中文字體。如果需要使用其他中文字體，可以通過以下步驟安裝：

1. 下載所需中文字體（TTF 或 OTF 格式）
2. 雙擊字體文件安裝
3. 在系統偏好設置中的「字體册」中確認字體已安裝

### Linux

大多數 Linux 發行版需要手動安裝中文字體：

#### Ubuntu/Debian:

```bash
# 安裝 Noto CJK 字體
sudo apt-get install fonts-noto-cjk

# 安裝文泉驛字體
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei
```

#### Fedora/CentOS:

```bash
# 安裝 Noto CJK 字體
sudo dnf install google-noto-sans-cjk-ttc-fonts

# 安裝文泉驛字體
sudo dnf install wqy-microhei-fonts wqy-zenhei-fonts
```

#### Arch Linux:

```bash
# 安裝 Noto CJK 字體
sudo pacman -S noto-fonts-cjk

# 安裝文泉驛字體
sudo pacman -S wqy-microhei wqy-zenhei
```

## 圖表中文顯示問題

### 負號顯示問題

中文環境下，matplotlib 可能會將負號顯示為方框或其他符號。BlackPiyan 通過設置 `axes.unicode_minus` 解決了這個問題：

```python
plt.rcParams['axes.unicode_minus'] = False  # 正確顯示負號
```

### 中文顯示為方框

如果中文字符顯示為方框或亂碼，通常是因為所選字體不支持中文字符。解決方法：

1. 確認配置文件中指定的字體已在系統中安裝
2. 嘗試使用系統內置的中文字體
3. 運行字體測試（見下文）診斷問題

## 字體測試

BlackPiyan 提供了全面的字體測試工具，用於檢測系統中可用的中文字體並測試它們的渲染效果。

### 運行字體測試

```bash
# 運行完整字體測試套件
python -m unittest tests.test_cross_platform_font

# 僅測試字體可用性
python -m unittest tests.test_cross_platform_font.TestCrossPlatformFont.test_font_availability

# 僅測試字體渲染效果
python -m unittest tests.test_cross_platform_font.TestCrossPlatformFont.test_font_rendering
```

### 測試輸出

字體測試會生成以下輸出：

1. 控制台日誌，列出系統中可用的中文字體
2. `results/font_tests/` 目錄下的測試圖表：
   - 各種字體渲染的中文文本示例
   - Visualizer 使用的字體效果

## 高級設置

### 自定義字體路徑

如果需要使用系統未安裝的自定義字體，可以手動設置字體路徑：

```python
import matplotlib.font_manager as fm

# 添加字體文件
font_path = '/path/to/your/custom_font.ttf'
fm.fontManager.addfont(font_path)

# 使用自定義字體
plt.rcParams['font.family'] = ['Custom Font Name', 'sans-serif']
```

### 程序內嵌入字體

為確保跨平台一致性，可以考慮在程序中嵌入開源中文字體：

1. 在項目中創建 `fonts` 目錄
2. 將開源中文字體（如 Noto Sans CJK）放入該目錄
3. 在代碼中動態加載該字體：

```python
import os
import matplotlib.font_manager as fm

# 獲取字體路徑
font_path = os.path.join(os.path.dirname(__file__), 'fonts/NotoSansCJK-Regular.ttc')

# 註冊字體
custom_font = fm.FontProperties(fname=font_path)

# 在繪圖時使用該字體
plt.title("中文標題", fontproperties=custom_font)
```

## 常見問題與解決方案

### 問題：安裝了字體但程序無法識別

**解決方案**：
1. 重新啟動應用程序
2. 清除 matplotlib 字體緩存：

```python
import matplotlib.font_manager as fm
fm.fontManager.addfont('/path/to/font.ttf')  # 添加字體
fm._load_fontmanager()  # 重新加載字體管理器
```

### 問題：字體顯示不正確或顯示為方框

**解決方案**：
1. 確認系統中已安裝該字體
2. 嘗試使用絕對路徑指定字體文件
3. 檢查字體是否支持需要顯示的字符

### 問題：不同作業系統顯示效果不一致

**解決方案**：
1. 使用程序內嵌的字體確保一致性
2. 為每個平台定義特定的字體配置
3. 使用廣泛支持的開源字體，如 Noto Sans CJK

### 問題：負號(-) 顯示不正確

**解決方案**：
確保設置了 `plt.rcParams['axes.unicode_minus'] = False`

### 問題：字體渲染模糊或鋸齒明顯

**解決方案**：
1. 調整保存圖表時的 DPI 設置：`plt.savefig('output.png', dpi=300)`
2. 使用矢量格式保存圖表：`plt.savefig('output.svg')`
3. 嘗試不同的字體，某些字體在特定大小時渲染效果更好 