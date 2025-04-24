# BlackPiyan 跨平台字體支持

本文檔提供在不同操作系統上正確顯示中文字體的指南，確保 BlackPiyan 生成的圖表中的中文文字能夠正常顯示。

## 目錄

1. [字體配置基礎](#字體配置基礎)
2. [常見中文字體](#常見中文字體)
3. [各操作系統字體支持](#各操作系統字體支持)
   - [Windows](#windows)
   - [macOS](#macos)
   - [Linux](#linux)
4. [自定義字體設置](#自定義字體設置)
5. [字體測試工具](#字體測試工具)
6. [故障排除](#故障排除)

## 字體配置基礎

BlackPiyan 使用 Matplotlib 繪製圖表，因此字體支持由 Matplotlib 的字體處理機制控制。配置文件中的字體設置會被傳遞給 Matplotlib：

```yaml
font:
  family: "Microsoft JhengHei"  # 首選字體
  fallback: "DejaVu Sans"       # 後備字體
```

當首選字體不可用時，系統會自動使用後備字體。

## 常見中文字體

以下是各操作系統上常見的中文字體：

### Windows 常見中文字體
- Microsoft JhengHei (微軟正黑體)
- Microsoft YaHei (微軟雅黑)
- SimSun (宋體)
- SimHei (黑體)
- KaiTi (楷體)
- FangSong (仿宋)

### macOS 常見中文字體
- PingFang TC (蘋方-繁)
- PingFang SC (蘋方-簡)
- Heiti TC (黑體-繁中)
- Heiti SC (黑體-簡中)
- STHeiti (華文黑體)
- Hiragino Sans CNS (冬青黑體繁中)

### Linux 常見中文字體
- Noto Sans CJK TC (思源黑體-繁)
- Noto Sans CJK SC (思源黑體-簡)
- Noto Serif CJK TC (思源宋體-繁)
- WenQuanYi Micro Hei (文泉驛微米黑)
- WenQuanYi Zen Hei (文泉驛正黑)
- Droid Sans Fallback

## 各操作系統字體支持

### Windows

Windows 系統通常已預裝多種中文字體，默認配置應能正常工作。如果需要更改字體：

1. 打開 `configs/default.yaml`
2. 修改 `font` 部分：
   ```yaml
   font:
     family: "Microsoft YaHei"  # 改為其他中文字體
     fallback: "Arial"
   ```

### macOS

macOS 的中文支持也很完善，但字體名稱與 Windows 不同：

1. 打開 `configs/default.yaml`
2. 使用 macOS 特有的字體名稱：
   ```yaml
   font:
     family: "PingFang TC"
     fallback: "Helvetica"
   ```

### Linux

Linux 系統需要安裝額外的中文字體包：

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install fonts-noto-cjk fonts-noto-cjk-extra fonts-wqy-microhei fonts-wqy-zenhei
```

#### Fedora
```bash
sudo dnf install google-noto-sans-cjk-fonts google-noto-serif-cjk-fonts wqy-microhei-fonts wqy-zenhei-fonts
```

#### Arch Linux
```bash
sudo pacman -S noto-fonts-cjk wqy-microhei wqy-zenhei
```

配置文件設置：
```yaml
font:
  family: "Noto Sans CJK TC"
  fallback: "WenQuanYi Micro Hei"
```

## 自定義字體設置

如果您有特定喜好的字體，可以按以下步驟進行設置：

1. 確保您的系統已安裝該字體
2. 打開 `configs/default.yaml`
3. 修改字體設置：
   ```yaml
   font:
     family: "您的字體名稱"
     fallback: "後備字體名稱"
   ```
4. 保存文件並重新運行程序

## 字體測試工具

BlackPiyan 提供了一個字體測試工具，可以幫助您確認哪些字體可以正確顯示：

```bash
python -m blackpiyan.tests.test_font
```

這將生成一個測試圖表，顯示系統中可用的中文字體。結果保存在 `results/font_tests/` 目錄下。

對於跨平台測試：

```bash
python -m blackpiyan.tests.test_cross_platform_font
```

這將測試常見的跨平台中文字體，幫助您選擇在不同系統上都能正常顯示的字體。

## 故障排除

### 問題：中文顯示為方框或亂碼

**可能原因與解決方案**：
- 系統未安裝指定的字體 → 安裝字體或使用已安裝的字體
- 配置文件中的字體名稱錯誤 → 確保字體名稱拼寫正確，包括大小寫
- Python 環境問題 → 確保 matplotlib 版本正確且安裝完整

### 問題：部分中文正常，部分中文異常

**可能原因與解決方案**：
- 字體不支持全部中文字符 → 使用更完整的中文字體如 Noto CJK
- 多字體混用 → 確保配置只指定一種主要字體

### 問題：GUI 界面與圖表字體不一致

**可能原因與解決方案**：
- GUI 使用系統字體，圖表使用配置指定的字體 → 在配置中使用與系統相同的字體

如果您仍然遇到字體問題，可以嘗試：
1. 使用字體測試工具確定可用的中文字體
2. 檢查系統字體目錄中已安裝的字體
3. 更新 matplotlib 和相關依賴庫