#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout, 
    QLabel, QLineEdit, QMenu, QMenuBar, QProgressBar, QPushButton, 
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar, QTabWidget, 
    QTableWidget, QTextEdit, QVBoxLayout, QWidget
)


class Ui_MainWindow(object):
    """BlackPiyan GUI UI設置類"""
    
    def setupUi(self, MainWindow):
        """設置主窗口UI"""
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        # 左側面板（參數設置和日誌）
        self.leftPanel = QFrame(self.centralwidget)
        self.leftPanel.setObjectName(u"leftPanel")
        self.leftPanel.setMinimumSize(QSize(350, 0))
        self.leftPanel.setMaximumSize(QSize(350, 16777215))
        self.leftPanel.setFrameShape(QFrame.StyledPanel)
        self.leftPanel.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.leftPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 參數組
        self.parametersGroup = QGroupBox(self.leftPanel)
        self.parametersGroup.setObjectName(u"parametersGroup")
        self.parametersLayout = QVBoxLayout(self.parametersGroup)
        self.parametersLayout.setObjectName(u"parametersLayout")
        self.parametersLayout.setContentsMargins(9, 9, 9, 9) 
        self.parametersLayout.setSpacing(6) 
        
        # 遊戲設置
        self.gameSettingsGroup = QGroupBox(self.parametersGroup)
        self.gameSettingsGroup.setObjectName(u"gameSettingsGroup")
        self.verticalLayout_3 = QVBoxLayout(self.gameSettingsGroup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)  
        self.verticalLayout_3.setSpacing(4)  
        
        # 牌副數
        self.decksLabel = QLabel(self.gameSettingsGroup)
        self.decksLabel.setObjectName(u"decksLabel")
        self.verticalLayout_3.addWidget(self.decksLabel)
        self.decksSpinBox = QSpinBox(self.gameSettingsGroup)
        self.decksSpinBox.setObjectName(u"decksSpinBox")
        self.decksSpinBox.setMinimum(1)
        self.decksSpinBox.setMaximum(12)
        self.decksSpinBox.setValue(6)
        self.verticalLayout_3.addWidget(self.decksSpinBox)
        
        # 洗牌閾值
        self.reshuffleLabel = QLabel(self.gameSettingsGroup)
        self.reshuffleLabel.setObjectName(u"reshuffleLabel")
        self.verticalLayout_3.addWidget(self.reshuffleLabel)
        self.reshuffleSpinBox = QDoubleSpinBox(self.gameSettingsGroup)
        self.reshuffleSpinBox.setObjectName(u"reshuffleSpinBox")
        self.reshuffleSpinBox.setDecimals(2)
        self.reshuffleSpinBox.setMinimum(0.10)
        self.reshuffleSpinBox.setMaximum(0.90)
        self.reshuffleSpinBox.setSingleStep(0.05)
        self.reshuffleSpinBox.setValue(0.40)
        self.verticalLayout_3.addWidget(self.reshuffleSpinBox)
        
        # 添加到參數佈局
        self.parametersLayout.addWidget(self.gameSettingsGroup)
        
        # 模擬設置
        self.simulationSettingsGroup = QGroupBox(self.parametersGroup)
        self.simulationSettingsGroup.setObjectName(u"simulationSettingsGroup")
        self.verticalLayout_4 = QVBoxLayout(self.simulationSettingsGroup)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)  
        self.verticalLayout_4.setSpacing(4)  
        
        # 每策略局數
        self.gamesLabel = QLabel(self.simulationSettingsGroup)
        self.gamesLabel.setObjectName(u"gamesLabel")
        self.verticalLayout_4.addWidget(self.gamesLabel)
        self.gamesSpinBox = QSpinBox(self.simulationSettingsGroup)
        self.gamesSpinBox.setObjectName(u"gamesSpinBox")
        self.gamesSpinBox.setMinimum(100)
        self.gamesSpinBox.setMaximum(1000000)
        self.gamesSpinBox.setSingleStep(100)
        self.gamesSpinBox.setValue(1000)
        self.verticalLayout_4.addWidget(self.gamesSpinBox)
        
        # 策略列表
        self.strategiesLabel = QLabel(self.simulationSettingsGroup)
        self.strategiesLabel.setObjectName(u"strategiesLabel")
        self.verticalLayout_4.addWidget(self.strategiesLabel)
        self.strategiesLineEdit = QLineEdit(self.simulationSettingsGroup)
        self.strategiesLineEdit.setObjectName(u"strategiesLineEdit")
        self.verticalLayout_4.addWidget(self.strategiesLineEdit)
        
        # 模擬時間設置
        self.simTimeLabel = QLabel(self.simulationSettingsGroup)
        self.simTimeLabel.setObjectName(u"simTimeLabel")
        self.verticalLayout_4.addWidget(self.simTimeLabel)
        self.simTimeSpinBox = QSpinBox(self.simulationSettingsGroup)
        self.simTimeSpinBox.setObjectName(u"simTimeSpinBox")
        self.simTimeSpinBox.setMinimum(1)
        self.simTimeSpinBox.setMaximum(300)
        self.simTimeSpinBox.setSingleStep(1)
        self.simTimeSpinBox.setValue(10)
        self.simTimeSpinBox.setSuffix(" 秒")
        self.verticalLayout_4.addWidget(self.simTimeSpinBox)
        
        # 定義 font1，修復錯誤
        font1 = QFont()
        font1.setBold(True)
        
        # 實時更新設置 (整合到模擬設置中)
        self.realtimeUpdateLabel = QLabel(self.simulationSettingsGroup)
        self.realtimeUpdateLabel.setObjectName(u"realtimeUpdateLabel")
        self.realtimeUpdateLabel.setFont(font1)
        self.verticalLayout_4.addWidget(self.realtimeUpdateLabel)
        
        # 實時更新設置水平佈局
        self.realtimeUpdateLayout = QHBoxLayout()
        self.realtimeUpdateLayout.setObjectName(u"realtimeUpdateLayout")
        self.realtimeUpdateLayout.setSpacing(4)  
        
        # 啟用實時更新
        self.realtimeUpdateCheck = QCheckBox(self.simulationSettingsGroup)
        self.realtimeUpdateCheck.setObjectName(u"realtimeUpdateCheck")
        self.realtimeUpdateCheck.setChecked(True)
        self.realtimeUpdateLayout.addWidget(self.realtimeUpdateCheck)
        
        # 自動調整
        self.autoAdjustCheck = QCheckBox(self.simulationSettingsGroup)
        self.autoAdjustCheck.setObjectName(u"autoAdjustCheck")
        self.autoAdjustCheck.setChecked(True)
        self.realtimeUpdateLayout.addWidget(self.autoAdjustCheck)
        
        # 添加到模擬設置佈局
        self.verticalLayout_4.addLayout(self.realtimeUpdateLayout)
        
        # 更新間隔
        self.updateIntervalLayout = QHBoxLayout()
        self.updateIntervalLayout.setObjectName(u"updateIntervalLayout")
        self.updateIntervalLayout.setSpacing(4) 
        
        self.updateIntervalLabel = QLabel(self.simulationSettingsGroup)
        self.updateIntervalLabel.setObjectName(u"updateIntervalLabel")
        self.updateIntervalLayout.addWidget(self.updateIntervalLabel)
        
        self.updateIntervalSpinBox = QSpinBox(self.simulationSettingsGroup)
        self.updateIntervalSpinBox.setObjectName(u"updateIntervalSpinBox")
        self.updateIntervalSpinBox.setMinimum(10)
        self.updateIntervalSpinBox.setMaximum(1000)
        self.updateIntervalSpinBox.setSingleStep(10)
        self.updateIntervalSpinBox.setValue(100)
        self.updateIntervalLayout.addWidget(self.updateIntervalSpinBox)
        
        # 添加到模擬設置佈局
        self.verticalLayout_4.addLayout(self.updateIntervalLayout)
        
        # 添加到參數佈局
        self.parametersLayout.addWidget(self.simulationSettingsGroup)
        
        # 控制按鈕
        self.controlsGroup = QGroupBox(self.parametersGroup)
        self.controlsGroup.setObjectName(u"controlsGroup")
        self.horizontalLayout_2 = QHBoxLayout(self.controlsGroup)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)  
        self.horizontalLayout_2.setSpacing(4)  
        
        self.runButton = QPushButton(self.controlsGroup)
        self.runButton.setObjectName(u"runButton")
        self.horizontalLayout_2.addWidget(self.runButton)
        self.stopButton = QPushButton(self.controlsGroup)
        self.stopButton.setObjectName(u"stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        self.resetButton = QPushButton(self.controlsGroup)
        self.resetButton.setObjectName(u"resetButton")
        self.horizontalLayout_2.addWidget(self.resetButton)
        
        # 添加到參數佈局
        self.parametersLayout.addWidget(self.controlsGroup)
        
        # 進度狀態
        self.statusFrame = QFrame(self.parametersGroup)
        self.statusFrame.setObjectName(u"statusFrame")
        self.statusFrame.setFrameShape(QFrame.StyledPanel)
        self.statusFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.statusFrame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)  
        self.verticalLayout_5.setSpacing(4)  
        
        self.statusLabel = QLabel(self.statusFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_5.addWidget(self.statusLabel)
        self.progressBar = QProgressBar(self.statusFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout_5.addWidget(self.progressBar)
        
        # 添加到參數佈局
        self.parametersLayout.addWidget(self.statusFrame)
        
        # 垂直間隔
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.parametersLayout.addItem(self.verticalSpacer)
        
        # 添加參數組到左側面板
        self.verticalLayout.addWidget(self.parametersGroup)
        
        # 日誌組
        self.logGroup = QGroupBox(self.leftPanel)
        self.logGroup.setObjectName(u"logGroup")
        self.verticalLayout_2 = QVBoxLayout(self.logGroup)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)  
        self.verticalLayout_2.setSpacing(4)  
        
        self.logTextEdit = QTextEdit(self.logGroup)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setReadOnly(True)
        self.verticalLayout_2.addWidget(self.logTextEdit)
        
        # 添加日誌組到左側面板
        self.verticalLayout.addWidget(self.logGroup)
        
        # 添加左側面板到主佈局
        self.horizontalLayout.addWidget(self.leftPanel)
        
        # 右側面板（圖表和結果）
        self.rightPanel = QFrame(self.centralwidget)
        self.rightPanel.setObjectName(u"rightPanel")
        self.rightPanel.setFrameShape(QFrame.StyledPanel)
        self.rightPanel.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.rightPanel)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        
        # 定義標題字體
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        
        # 結果標籤
        self.resultsLabel = QLabel(self.rightPanel)
        self.resultsLabel.setObjectName(u"resultsLabel")
        self.resultsLabel.setFont(font)
        self.resultsLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout_6.addWidget(self.resultsLabel)
        
        # 標籤控件
        self.tabWidget = QTabWidget(self.rightPanel)
        self.tabWidget.setObjectName(u"tabWidget")
        
        # 圖表標籤頁
        self.chartsTab = QWidget()
        self.chartsTab.setObjectName(u"chartsTab")
        self.verticalLayout_7 = QVBoxLayout(self.chartsTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        
        # 分佈圖佈局
        self.distributionLayout = QVBoxLayout()
        self.distributionLayout.setObjectName(u"distributionLayout")
        
        # 分佈圖標題和下拉框佈局
        self.distributionHeaderLayout = QHBoxLayout()
        self.distributionHeaderLayout.setObjectName(u"distributionHeaderLayout")
        
        # 分佈圖標題
        self.distributionLabel = QLabel(self.chartsTab)
        self.distributionLabel.setObjectName(u"distributionLabel")
        self.distributionLabel.setFont(font1)
        self.distributionHeaderLayout.addWidget(self.distributionLabel)
        
        # 分佈圖策略選擇
        self.strategyDistLabel = QLabel(self.chartsTab)
        self.strategyDistLabel.setObjectName(u"strategyDistLabel")
        self.distributionHeaderLayout.addWidget(self.strategyDistLabel)
        self.strategyDistCombo = QComboBox(self.chartsTab)
        self.strategyDistCombo.setObjectName(u"strategyDistCombo")
        self.distributionHeaderLayout.addWidget(self.strategyDistCombo)
        
        # 水平間隔
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.distributionHeaderLayout.addItem(self.horizontalSpacer)
        
        # 添加到分佈圖佈局
        self.distributionLayout.addLayout(self.distributionHeaderLayout)
        
        # 分佈圖
        self.distributionPlotWidget = QWidget(self.chartsTab)
        self.distributionPlotWidget.setObjectName(u"distributionPlotWidget")
        self.distributionPlotWidget.setMinimumSize(QSize(0, 250))
        self.distributionLayout.addWidget(self.distributionPlotWidget)
        
        # 添加到標籤頁佈局
        self.verticalLayout_7.addLayout(self.distributionLayout)
        
        # 添加圖表標籤頁到標籤控件
        self.tabWidget.addTab(self.chartsTab, "")
        
        # 表格標籤頁
        self.tableTab = QWidget()
        self.tableTab.setObjectName(u"tableTab")
        self.verticalLayout_8 = QVBoxLayout(self.tableTab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        
        # 表格
        self.summaryTable = QTableWidget(self.tableTab)
        self.summaryTable.setObjectName(u"summaryTable")
        
        # 添加到標籤頁佈局
        self.verticalLayout_8.addWidget(self.summaryTable)
        
        # 添加表格標籤頁到標籤控件
        self.tabWidget.addTab(self.tableTab, "")
        
        # 策略比較標籤頁
        self.comparisonTab = QWidget()
        self.comparisonTab.setObjectName(u"comparisonTab")
        self.verticalLayout_9 = QVBoxLayout(self.comparisonTab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        
        # 策略比較圖
        self.comparisonTabLayout = QVBoxLayout()
        self.comparisonTabLayout.setObjectName(u"comparisonTabLayout")
        self.comparisonTabLabel = QLabel(self.comparisonTab)
        self.comparisonTabLabel.setObjectName(u"comparisonTabLabel")
        self.comparisonTabLabel.setFont(font1)
        self.comparisonTabLayout.addWidget(self.comparisonTabLabel)
        self.comparisonTabPlotWidget = QWidget(self.comparisonTab)
        self.comparisonTabPlotWidget.setObjectName(u"comparisonTabPlotWidget")
        self.comparisonTabPlotWidget.setMinimumSize(QSize(0, 500))
        self.comparisonTabLayout.addWidget(self.comparisonTabPlotWidget)
        
        # 添加到標籤頁佈局
        self.verticalLayout_9.addLayout(self.comparisonTabLayout)
        
        # 添加策略比較標籤頁到標籤控件
        self.tabWidget.addTab(self.comparisonTab, "")
        
        # 添加標籤控件到右側面板
        self.verticalLayout_6.addWidget(self.tabWidget)
        
        # 添加右側面板到主佈局
        self.horizontalLayout.addWidget(self.rightPanel)
        
        # 設置中央窗口
        MainWindow.setCentralWidget(self.centralwidget)
        
        # 菜單欄
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        
        # 狀態欄
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # 添加動作到菜單
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        
        self.retranslateUi(MainWindow)
        
        # 設置默認標籤頁
        self.tabWidget.setCurrentIndex(0)
        
        QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        """設置UI文本"""
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BlackPiyan - 21點模擬分析", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"退出", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"關於", None))
        self.parametersGroup.setTitle(QCoreApplication.translate("MainWindow", u"參數設置", None))
        self.gameSettingsGroup.setTitle(QCoreApplication.translate("MainWindow", u"遊戲設置", None))
        self.decksLabel.setText(QCoreApplication.translate("MainWindow", u"牌副數量:", None))
        self.reshuffleLabel.setText(QCoreApplication.translate("MainWindow", u"洗牌閾值 (剩餘牌比例):", None))
        self.simulationSettingsGroup.setTitle(QCoreApplication.translate("MainWindow", u"模擬設置", None))
        self.gamesLabel.setText(QCoreApplication.translate("MainWindow", u"每個策略的模擬局數:", None))
        self.strategiesLabel.setText(QCoreApplication.translate("MainWindow", u"要測試的策略值 (逗號分隔):", None))
        self.strategiesLineEdit.setText(QCoreApplication.translate("MainWindow", u"16, 17, 18", None))
        self.simTimeLabel.setText(QCoreApplication.translate("MainWindow", u"模擬速度控制（目標完成時間）:", None))
        self.realtimeUpdateLabel.setText(QCoreApplication.translate("MainWindow", u"實時更新設置:", None))
        self.realtimeUpdateCheck.setText(QCoreApplication.translate("MainWindow", u"啟用實時更新", None))
        self.autoAdjustCheck.setText(QCoreApplication.translate("MainWindow", u"自動調整頻率", None))
        self.updateIntervalLabel.setText(QCoreApplication.translate("MainWindow", u"更新間隔:", None))
        self.controlsGroup.setTitle(QCoreApplication.translate("MainWindow", u"控制", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"執行模擬", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"停止", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"重置參數", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"就緒", None))
        self.logGroup.setTitle(QCoreApplication.translate("MainWindow", u"日誌", None))
        self.resultsLabel.setText(QCoreApplication.translate("MainWindow", u"模擬結果", None))
        self.distributionLabel.setText(QCoreApplication.translate("MainWindow", u"點數分佈", None))
        self.strategyDistLabel.setText(QCoreApplication.translate("MainWindow", u"策略:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.chartsTab), QCoreApplication.translate("MainWindow", u"分佈圖", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tableTab), QCoreApplication.translate("MainWindow", u"詳細數據", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comparisonTab), QCoreApplication.translate("MainWindow", u"策略比較", None))
        self.comparisonTabLabel.setText(QCoreApplication.translate("MainWindow", u"策略比較", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"文件", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"幫助", None)) 