# 貢獻指南

感謝您考慮為 BlackPiyan 專案做出貢獻！以下是一些指南，旨在讓貢獻過程更加順暢。

## 目錄
1. [行為準則](#行為準則)
2. [開發環境設置](#開發環境設置)
3. [如何貢獻](#如何貢獻)
4. [提交 Pull Request](#提交-pull-request)
5. [編碼規範](#編碼規範)
6. [測試](#測試)
7. [文檔貢獻](#文檔貢獻)
8. [問題報告](#問題報告)
9. [功能請求](#功能請求)

## 行為準則

本專案採用貢獻者公約（Contributor Covenant）作為其行為準則。透過參與，您需要遵守此行為準則。請報告不可接受的行為。

## 開發環境設置

1. Fork 本倉庫
2. Clone 您的 fork 到本地
```bash
git clone https://github.com/YOUR_USERNAME/BlackPiyan.git
cd BlackPiyan
```

3. 創建並激活虛擬環境
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

4. 安裝依賴庫
```bash
pip install -r requirements.txt

# 安裝開發依賴
pip install -r requirements-dev.txt  # 如果存在
```

5. 創建新分支進行開發
```bash
git checkout -b feature/your-feature-name
```

## 如何貢獻

您可以透過多種方式貢獻：

- **修復 Bug**：查看 Issues 區域中標記為「bug」的問題
- **添加新功能**：實現標記為「enhancement」的功能請求
- **改進文檔**：幫助完善或翻譯文檔
- **提交測試案例**：為現有功能增加測試覆蓋率
- **報告問題**：報告您發現的問題或建議改進

## 提交 Pull Request

1. 確保您的代碼符合[編碼規範](#編碼規範)
2. 確保所有測試通過
```bash
python -m unittest discover blackpiyan.tests
```

3. 提交您的更改
```bash
git add .
git commit -m "簡短描述您的更改"
```

4. 推送到您的分支
```bash
git push origin feature/your-feature-name
```

5. 從 GitHub 界面創建 Pull Request

## 編碼規範

- 遵循 PEP 8 風格指南
- 使用有意義的變數名和函數名
- 使用類型提示
- 提供詳細的文檔字符串
- 每個函數和類都應該有明確的單一責任
- 對複雜邏輯添加注釋

## 測試

- 為新功能添加測試
- 確保測試覆蓋關鍵路徑和邊界情況
- 在提交前運行測試以確保沒有破壞現有功能
```bash
python -m unittest discover blackpiyan.tests
```

### 測試組織

測試文件位於 `tests/` 目錄，針對不同模組提供相應的測試：
- `test_model.py`：數據模型測試
- `test_simulation.py`：模擬引擎測試
- `test_font.py`：字體支持測試

## 文檔貢獻

- 文檔位於 `docs/` 目錄中
- 更新 API 文檔以反映代碼更改
- 使用 Markdown 格式
- 提供清晰的範例和說明
- 添加截圖或圖表以增強理解

## 問題報告

提交問題報告時，請包含：

- 清晰的問題描述
- 重現步驟
- 預期行為
- 實際行為
- 環境信息（操作系統、Python 版本等）
- 截圖或錯誤日誌

## 功能請求

提交功能建議時，請包含：

- 清晰的功能描述
- 為什麼這個功能對項目有益的理由
- 可能的實現方法
- 與現有功能的關係
- 使用場景示例

## 發布流程

如果您有發布權限：

1. 更新版本號（在 `blackpiyan/__init__.py` 中）
2. 更新 CHANGELOG.md（如果存在）
3. 創建一個新的版本標籤：
```bash
git tag -a v1.x.x -m "版本 1.x.x"
git push origin v1.x.x
```

4. 在 GitHub 上創建正式發布，附上版本說明

---

再次感謝您的貢獻！您的參與對 BlackPiyan 的發展至關重要。如有任何問題，請隨時聯繫項目維護者。