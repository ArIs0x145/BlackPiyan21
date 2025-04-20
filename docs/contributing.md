# 貢獻指南

感謝您考慮為 BlackPiyan 專案做出貢獻！以下是一些指南，旨在讓貢獻過程更加順暢。

## 目錄

1. [行為準則](#行為準則)
2. [如何貢獻](#如何貢獻)
3. [開發環境設置](#開發環境設置)
4. [提交 Pull Request](#提交-pull-request)
5. [編碼規範](#編碼規範)
6. [測試](#測試)
7. [文檔貢獻](#文檔貢獻)
8. [問題報告](#問題報告)

## 行為準則

本專案參與者應遵循開放、尊重和包容的原則。尊重各種觀點和經驗，對他人保持善意和耐心。不接受任何形式的騷擾或冒犯性言論。

## 如何貢獻

您可以通過多種方式為 BlackPiyan 做出貢獻：

1. **修復 Bug**：如果您發現了 Bug，請提交詳細的問題報告，或者更好的是，提交包含修復的 Pull Request。
2. **添加新功能**：如果您有新功能想法，請先開 Issue 討論，獲得同意後再實施。
3. **改進文檔**：幫助我們完善文檔，無論是修正錯誤還是添加更多示例。
4. **優化代碼**：改進性能、代碼結構或測試覆蓋率。

## 開發環境設置

1. **Fork 倉庫**：首先，在 GitHub 上 Fork 本倉庫到您的賬號下。

2. **克隆您的 Fork**：
   ```bash
   git clone https://github.com/YOUR_USERNAME/BlackPiyan.git
   cd BlackPiyan
   ```

3. **添加上游倉庫**：
   ```bash
   git remote add upstream https://github.com/CornHub114514/BlackPiyan.git
   ```

4. **創建虛擬環境**：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # 或
   .venv\Scripts\activate  # Windows
   ```

5. **安裝開發依賴**：
   ```bash
   pip install -r requirements.txt
   pip install -e .  # 安裝可編輯模式
   ```

6. **創建功能分支**：
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 提交 Pull Request

1. **保持分支最新**：
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **提交您的更改**：
   ```bash
   git add .
   git commit -m "描述性的提交消息"
   git push origin feature/your-feature-name
   ```

3. **創建 Pull Request**：通過 GitHub 界面從您的分支到主倉庫的 `main` 分支創建 Pull Request。

4. **PR 描述**：在 PR 描述中，清晰說明：
   - 您的更改解決了什麼問題
   - 實現方法的概述
   - 任何需要審核者特別注意的地方

5. **等待審核**：維護者會審核您的 PR，可能會提出修改建議。

## 編碼規範

我們遵循以下編碼規範：

1. **PEP 8**：遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 的 Python 代碼風格指南。
2. **文檔字符串**：所有公共函數、類和方法必須有 docstring，遵循 [Google 風格](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)。
3. **類型提示**：盡可能使用 [類型提示](https://docs.python.org/3/library/typing.html)。
4. **命名約定**：
   - 類名使用 `CamelCase`
   - 函數和變量使用 `snake_case`
   - 常量使用 `UPPER_CASE`

## 測試

所有新功能或 Bug 修復都應包含適當的測試：

- 單元測試位於 `tests/` 目錄中
- 運行測試：`python -m unittest discover tests`
- 確保所有測試都通過
- 盡量提高測試覆蓋率

## 文檔貢獻

文檔貢獻非常受歡迎：

- 更新或添加文檔位於 `docs/` 目錄中
- 確保您的文檔格式一致，使用 Markdown
- 更新主 README.md 以反映任何重大更改
- 如果添加新功能，請更新相關文檔或創建新文檔

## 問題報告

如果您發現 Bug 或有功能請求，請在提交 Issue 時提供以下信息：

- 簡明的問題標題
- 重現步驟或詳細描述
- 預期行為 vs. 實際行為
- 環境信息（操作系統、Python 版本等）
- 可能的原因或解決方案（如果有）

---

感謝您的貢獻，讓 BlackPiyan 變得更好！ 