# BlackPiyan 安裝指南

本文檔提供 BlackPiyan（21點莊家策略模擬工具）的詳細安裝說明。根據您的操作系統，按照相應的安裝步驟進行操作。

## 目錄

1. [系統要求](#系統要求)
2. [Python 環境設置](#python-環境設置)
3. [BlackPiyan 安裝](#blackpiyan-安裝)
4. [依賴庫安裝](#依賴庫安裝)
5. [字體安裝](#字體安裝)
6. [驗證安裝](#驗證安裝)
7. [常見安裝問題](#常見安裝問題)

## 系統要求

BlackPiyan 可運行於以下環境：

- **作業系統**：
  - Windows 10/11
  - macOS 10.14 (Mojave) 或更高版本
  - 主流 Linux 發行版 (Ubuntu 18.04+, Fedora 30+, CentOS 8+)

- **硬件需求**：
  - 至少 2GB RAM
  - 至少 100MB 磁盤空間

- **軟件需求**：
  - Python 3.8 或更高版本
  - pip (Python 包管理器)

## Python 環境設置

### Windows

1. 從 [Python 官網](https://www.python.org/downloads/windows/) 下載最新版 Python 安裝包
2. 運行安裝程序，選擇「Add Python to PATH」選項
3. 完成安裝後，打開命令提示符，輸入以下命令驗證安裝：
   ```cmd
   python --version
   pip --version
   ```

### macOS

1. 使用 Homebrew 安裝 Python（如未安裝 Homebrew，請先訪問 [brew.sh](https://brew.sh) 安裝）：
   ```bash
   brew install python
   ```
2. 安裝完成後，驗證 Python 安裝：
   ```bash
   python3 --version
   pip3 --version
   ```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Fedora
```bash
sudo dnf install python3 python3-pip
```

#### Arch Linux
```bash
sudo pacman -S python python-pip
```

## BlackPiyan 安裝

### 方法一：使用 Git 克隆倉庫

```bash
# 克隆倉庫
git clone https://github.com/yourusername/blackpiyan.git
cd blackpiyan

# 創建並激活虛擬環境 (推薦)
python -m venv .venv

# Windows 激活虛擬環境
.venv\Scripts\activate  # Windows
# macOS/Linux 激活虛擬環境
source .venv/bin/activate  # macOS/Linux
```

### 方法二：下載發布包

1. 訪問 [GitHub Releases 頁面](https://github.com/yourusername/blackpiyan/releases)
2. 下載最新版本的發布包 (.zip 或 .tar.gz)
3. 解壓文件到您想要的位置
4. 進入解壓後的目錄

## 依賴庫安裝

BlackPiyan 依賴一些 Python 庫來進行模擬、數據分析和可視化。使用以下命令安裝所需依賴：

```bash
pip install -r requirements.txt
```

主要依賴包括：

- **matplotlib**：用於生成圖表
- **numpy**：用於數值計算
- **pandas**：用於數據分析
- **seaborn**：用於高級可視化
- **pyyaml**：用於解析配置文件

## 字體安裝

BlackPiyan 使用中文字體渲染圖表。不同操作系統需要不同的安裝步驟：

### Windows

Windows 系統通常已預裝所需的中文字體（如 Microsoft JhengHei、Microsoft YaHei 等）。

### macOS

macOS 系統已內置中文字體支持。如需安裝其他中文字體：

1. 下載需要的字體文件（.ttf 或 .otf 格式）
2. 雙擊字體文件安裝到系統

### Linux

請參考[跨平台字體支持](./font_support.md)文檔中的 Linux 字體安裝說明。

## 驗證安裝

安裝完成後，執行以下命令驗證 BlackPiyan 是否正確安裝：

```bash
python main.py
```

如果安裝成功，程序將執行，並在控制台顯示進度信息，最後在 `results/charts/` 目錄下生成可視化圖表。

## 常見安裝問題

### 問題：安裝依賴時出現錯誤

**解決方案**：
- 確保您的 pip 是最新版本：
  ```bash
  python -m pip install --upgrade pip
  ```
- 如果某個包安裝失敗，嘗試單獨安裝：
  ```bash
  pip install package_name
  ```

### 問題：matplotlib 無法正常顯示中文

**解決方案**：
- 參考[跨平台字體支持](./font_support.md)文檔安裝並配置中文字體

### 問題：找不到模塊 'blackpiyan'

**解決方案**：
- 確保您在正確的目錄下運行程序
- 如果仍然有問題，嘗試將項目路徑添加到 Python 路徑：
  ```python
  import sys
  sys.path.insert(0, '/path/to/blackpiyan')
  ```

### 問題：虛擬環境無法激活

**解決方案**：
- Windows：確保PowerShell執行策略允許運行腳本
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Linux/macOS：確保 .venv/bin/activate 有執行權限
  ```bash
  chmod +x .venv/bin/activate
  ```

---

如果您在安裝過程中遇到其他問題，請查閱[故障排除](./troubleshooting.md)文檔，或在 GitHub 項目頁面提交 Issue。 