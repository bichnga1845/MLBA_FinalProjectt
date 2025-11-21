from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import GOLDEN_CITRUS, apply_global_styles, create_glass_card


class Ui_MainWindow_DataManagement(object):
    def setupUi(self, MainWindow_DataManagement: QMainWindow) -> None:
        MainWindow_DataManagement.setObjectName("MainWindow_DataManagement")
        MainWindow_DataManagement.resize(1400, 820)
        apply_global_styles(
            MainWindow_DataManagement,
            extra_styles="""
            QLabel[data-role="label"] { font-weight:600; color:#0C2B1B; }
        """,
        )

        self.centralwidget = QWidget(parent=MainWindow_DataManagement)
        self.vlRoot = QVBoxLayout(self.centralwidget)
        self.vlRoot.setContentsMargins(42, 32, 42, 32)
        self.vlRoot.setSpacing(20)

        heroCard = create_glass_card(self.centralwidget, padding=32)
        heroLayout = QVBoxLayout(heroCard)
        heroLayout.setSpacing(16)

        titleRow = QHBoxLayout()
        self.lblHeader = QLabel(parent=heroCard)
        self.lblHeader.setObjectName("Headline")
        titleRow.addWidget(self.lblHeader, stretch=1)
        badge = QLabel(parent=heroCard)
        badge.setText("🍋 Dữ liệu trái cây chuẩn thương hiệu")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background-color:{GOLDEN_CITRUS}; padding:6px 18px; border-radius:999px; font-weight:600;"
        )
        titleRow.addWidget(badge, 0, Qt.AlignmentFlag.AlignRight)
        heroLayout.addLayout(titleRow)

        self.layoutToolbar = QHBoxLayout()
        self.layoutToolbar.setSpacing(10)

        self.txtSearchData = QLineEdit(parent=heroCard)
        self.txtSearchData.setObjectName("txtSearchData")
        self.txtSearchData.setMinimumHeight(46)
        self.layoutToolbar.addWidget(self.txtSearchData, stretch=2)

        self.comboLabelFilter = QComboBox(parent=heroCard)
        self.comboLabelFilter.setObjectName("comboLabelFilter")
        self.layoutToolbar.addWidget(self.comboLabelFilter)

        self.comboModelFilter = QComboBox(parent=heroCard)
        self.comboModelFilter.setObjectName("comboModelFilter")
        self.layoutToolbar.addWidget(self.comboModelFilter)

        self.txtUserFilter = QLineEdit(parent=heroCard)
        self.txtUserFilter.setObjectName("txtUserFilter")
        self.layoutToolbar.addWidget(self.txtUserFilter)

        self.dateFrom = QDateEdit(parent=heroCard)
        self.dateFrom.setObjectName("dateFrom")
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setDate(QDate.currentDate().addMonths(-1))
        self.layoutToolbar.addWidget(self.dateFrom)

        self.dateTo = QDateEdit(parent=heroCard)
        self.dateTo.setObjectName("dateTo")
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setDate(QDate.currentDate())
        self.layoutToolbar.addWidget(self.dateTo)

        self.btnRefreshData = QPushButton(parent=heroCard)
        self.btnRefreshData.setObjectName("btnRefreshData")
        self.btnRefreshData.setMinimumHeight(46)
        self.layoutToolbar.addWidget(self.btnRefreshData)
        heroLayout.addLayout(self.layoutToolbar)

        contentCard = create_glass_card(self.centralwidget, padding=24)
        self.layoutMain = QHBoxLayout(contentCard)
        self.layoutMain.setSpacing(18)

        tableWrapper = QVBoxLayout()
        tableWrapper.setSpacing(12)
        tableTitle = QLabel(parent=contentCard)
        tableTitle.setText("Bảng dữ liệu dự đoán mới nhất")
        tableTitle.setStyleSheet("font-weight:600; font-size:16px;")
        tableWrapper.addWidget(tableTitle)

        self.tblData = QTableWidget(parent=contentCard)
        self.tblData.setObjectName("tblData")
        self.tblData.setColumnCount(9)
        self.tblData.setRowCount(0)
        self.tblData.setAlternatingRowColors(True)
        self.tblData.horizontalHeader().setStretchLastSection(True)
        self.tblData.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tblData.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        for idx in range(9):
            self.tblData.setHorizontalHeaderItem(idx, QTableWidgetItem(""))
        tableWrapper.addWidget(self.tblData)
        self.layoutMain.addLayout(tableWrapper, stretch=3)

        sidebarCard = create_glass_card(contentCard, padding=20)
        sidebarLayout = QVBoxLayout(sidebarCard)
        sidebarLayout.setSpacing(12)
        self.tabRight = QTabWidget(parent=sidebarCard)
        self.tabRight.setObjectName("tabRight")
        self.tabRight.setTabPosition(QTabWidget.TabPosition.North)

        # Preview tab
        self.tabPreview = QWidget()
        self.vlPrev = QVBoxLayout(self.tabPreview)
        self.labelPreview = QLabel(parent=self.tabPreview)
        self.labelPreview.setObjectName("labelPreview")
        self.labelPreview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelPreview.setMinimumSize(320, 320)
        self.labelPreview.setStyleSheet("border-radius:18px; background:rgba(255,255,255,0.6);")
        self.labelPreview.setScaledContents(True)
        self.vlPrev.addWidget(self.labelPreview)
        self.tabRight.addTab(self.tabPreview, "Preview")

        # Details tab
        self.tabDetails = QWidget()
        detailsLayout = QFormLayout(self.tabDetails)
        detailsLayout.setHorizontalSpacing(12)
        detailsLayout.setVerticalSpacing(10)

        self.lblDId = QLabel(parent=self.tabDetails)
        self.lblDId.setObjectName("lblDId")
        self.lblDId.setProperty("data-role", "label")
        self.txtDId = QLineEdit(parent=self.tabDetails)
        self.txtDId.setObjectName("txtDId")
        self.txtDId.setReadOnly(True)
        detailsLayout.addRow(self.lblDId, self.txtDId)

        self.lblDImage = QLabel(parent=self.tabDetails)
        self.lblDImage.setObjectName("lblDImage")
        self.lblDImage.setProperty("data-role", "label")
        self.txtDImage = QLineEdit(parent=self.tabDetails)
        self.txtDImage.setObjectName("txtDImage")
        self.txtDImage.setReadOnly(True)
        detailsLayout.addRow(self.lblDImage, self.txtDImage)

        self.lblDResult = QLabel(parent=self.tabDetails)
        self.lblDResult.setProperty("data-role", "label")
        self.lblDResult.setObjectName("lblDResult")
        self.txtDResult = QLineEdit(parent=self.tabDetails)
        self.txtDResult.setObjectName("txtDResult")
        self.txtDResult.setReadOnly(True)
        detailsLayout.addRow(self.lblDResult, self.txtDResult)

        self.lblDConf = QLabel(parent=self.tabDetails)
        self.lblDConf.setProperty("data-role", "label")
        self.lblDConf.setObjectName("lblDConf")
        self.txtDConf = QLineEdit(parent=self.tabDetails)
        self.txtDConf.setObjectName("txtDConf")
        self.txtDConf.setReadOnly(True)
        detailsLayout.addRow(self.lblDConf, self.txtDConf)

        self.lblDUser = QLabel(parent=self.tabDetails)
        self.lblDUser.setProperty("data-role", "label")
        self.lblDUser.setObjectName("lblDUser")
        self.txtDUser = QLineEdit(parent=self.tabDetails)
        self.txtDUser.setObjectName("txtDUser")
        self.txtDUser.setReadOnly(True)
        detailsLayout.addRow(self.lblDUser, self.txtDUser)

        self.lblDModel = QLabel(parent=self.tabDetails)
        self.lblDModel.setProperty("data-role", "label")
        self.lblDModel.setObjectName("lblDModel")
        self.txtDModel = QLineEdit(parent=self.tabDetails)
        self.txtDModel.setObjectName("txtDModel")
        self.txtDModel.setReadOnly(True)
        detailsLayout.addRow(self.lblDModel, self.txtDModel)

        self.lblDTime = QLabel(parent=self.tabDetails)
        self.lblDTime.setProperty("data-role", "label")
        self.lblDTime.setObjectName("lblDTime")
        self.txtDTime = QLineEdit(parent=self.tabDetails)
        self.txtDTime.setObjectName("txtDTime")
        self.txtDTime.setReadOnly(True)
        detailsLayout.addRow(self.lblDTime, self.txtDTime)

        self.lblDNote = QLabel(parent=self.tabDetails)
        self.lblDNote.setProperty("data-role", "label")
        self.lblDNote.setObjectName("lblDNote")
        self.txtDNote = QTextEdit(parent=self.tabDetails)
        self.txtDNote.setObjectName("txtDNote")
        detailsLayout.addRow(self.lblDNote, self.txtDNote)

        self.tabRight.addTab(self.tabDetails, "Details")

        sidebarLayout.addWidget(self.tabRight)
        self.layoutMain.addWidget(sidebarCard, stretch=2)
        self.vlRoot.addWidget(contentCard)

        # Action buttons
        actionsCard = create_glass_card(self.centralwidget, padding=18)
        self.layoutActions = QHBoxLayout(actionsCard)
        self.layoutActions.setSpacing(12)

        self.btnAddImage = QPushButton(parent=actionsCard)
        self.btnAddImage.setObjectName("btnAddImage")
        self.layoutActions.addWidget(self.btnAddImage)

        self.btnRelabel = QPushButton(parent=actionsCard)
        self.btnRelabel.setObjectName("btnRelabel")
        self.layoutActions.addWidget(self.btnRelabel)

        self.btnDelete = QPushButton(parent=actionsCard)
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setProperty("secondary", True)
        self.layoutActions.addWidget(self.btnDelete)

        self.btnExport = QPushButton(parent=actionsCard)
        self.btnExport.setObjectName("btnExport")
        self.layoutActions.addWidget(self.btnExport)

        self.btnAddModel = QPushButton(parent=actionsCard)
        self.btnAddModel.setObjectName("btnAddModel")
        self.layoutActions.addWidget(self.btnAddModel)

        self.btnStatistics = QPushButton(parent=actionsCard)
        self.btnStatistics.setObjectName("btnStatistics")
        self.layoutActions.addWidget(self.btnStatistics)

        self.btnRefresh = QPushButton(parent=actionsCard)
        self.btnRefresh.setObjectName("btnRefresh")
        self.btnRefresh.setProperty("secondary", True)
        self.layoutActions.addWidget(self.btnRefresh)

        self.layoutActions.addStretch()

        self.btnBackToDashboard = QPushButton(parent=actionsCard)
        self.btnBackToDashboard.setObjectName("btnBackToDashboard")
        self.btnBackToDashboard.setProperty("secondary", True)
        self.layoutActions.addWidget(self.btnBackToDashboard)

        self.vlRoot.addWidget(actionsCard)

        MainWindow_DataManagement.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_DataManagement)
        MainWindow_DataManagement.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_DataManagement)
        self.tabRight.setCurrentIndex(1)

    def retranslateUi(self, MainWindow_DataManagement: QMainWindow) -> None:
        MainWindow_DataManagement.setWindowTitle("Kho dữ liệu trái cây cao cấp")
        header = self.centralwidget.findChild(QLabel, "Headline")
        if header:
            header.setText("Quản trị dữ liệu AI như trải nghiệm trang web sang trọng")

        self.txtSearchData.setPlaceholderText("Tìm kiếm theo ID dự đoán, loại trái cây hoặc nhãn chất lượng...")
        self.comboLabelFilter.clear()
        self.comboLabelFilter.addItems(["Nhãn: Tất cả", "Good", "Bad"])
        self.comboModelFilter.clear()
        self.comboModelFilter.addItems(["Model: Tất cả"])
        self.txtUserFilter.setPlaceholderText("Tên người dùng / email")
        self.btnRefreshData.setText("Lọc dữ liệu")

        headers = [
            "Prediction ID",
            "Ảnh",
            "Loại trái cây",
            "Độ tin cậy",
            "Người dùng",
            "Mô hình",
            "Thời gian",
            "Nhãn chất lượng",
            "Model ID",
        ]
        for idx, text in enumerate(headers):
            item = self.tblData.horizontalHeaderItem(idx)
            if item:
                item.setText(text)

        self.tabRight.setTabText(self.tabRight.indexOf(self.tabPreview), "Xem ảnh")
        self.tabRight.setTabText(self.tabRight.indexOf(self.tabDetails), "Chi tiết")

        self.lblDId.setText("ID:")
        self.lblDImage.setText("Ảnh:")
        self.lblDResult.setText("Kết quả:")
        self.lblDConf.setText("Confidence:")
        self.lblDUser.setText("Người dùng:")
        self.lblDModel.setText("Mô hình:")
        self.lblDTime.setText("Thời gian:")
        self.lblDNote.setText("Ghi chú:")

        self.btnAddImage.setText("Tải ảnh mới")
        self.btnRelabel.setText("Sửa nhãn")
        self.btnDelete.setText("Xoá")
        self.btnExport.setText("Xuất CSV")
        self.btnAddModel.setText("Mở quản lý mô hình")
        self.btnStatistics.setText("Thống kê")
        self.btnRefresh.setText("Làm mới")
        self.btnBackToDashboard.setText("🏠 Quay về Dashboard")
