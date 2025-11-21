from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import apply_global_styles, create_glass_card


class Ui_MainWindow_ModelManagement(object):
    def setupUi(self, MainWindow_ModelManagement: QMainWindow) -> None:
        MainWindow_ModelManagement.setObjectName("MainWindow_ModelManagement")
        MainWindow_ModelManagement.resize(1100, 720)
        apply_global_styles(
            MainWindow_ModelManagement,
            extra_styles="""
            QPushButton[role="ghost"] {
                background: transparent;
                border: 1px dashed rgba(10, 135, 84, 0.45);
                color: #0A8754;
            }
        """,
        )

        self.centralwidget = QWidget(parent=MainWindow_ModelManagement)
        self.centralwidget.setObjectName("centralwidget")
        self.vlRoot = QVBoxLayout(self.centralwidget)
        self.vlRoot.setContentsMargins(48, 36, 48, 36)
        self.vlRoot.setSpacing(24)

        headerCard = create_glass_card(self.centralwidget, padding=32)
        headerLayout = QVBoxLayout(headerCard)
        headerLayout.setSpacing(8)

        title = QLabel(parent=headerCard)
        title.setObjectName("Headline")
        headerLayout.addWidget(title)

        subtitle = QLabel(parent=headerCard)
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)
        headerLayout.addWidget(subtitle)

        self.toolbar = QHBoxLayout()
        self.toolbar.setSpacing(12)

        self.txtSearchModel = QLineEdit(parent=headerCard)
        self.txtSearchModel.setObjectName("txtSearchModel")
        self.txtSearchModel.setMinimumHeight(46)
        self.toolbar.addWidget(self.txtSearchModel, stretch=2)

        self.btnSearchModel = QPushButton(parent=headerCard)
        self.btnSearchModel.setObjectName("btnSearchModel")
        self.btnSearchModel.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnSearchModel)

        self.btnRefreshModels = QPushButton(parent=headerCard)
        self.btnRefreshModels.setObjectName("btnRefreshModels")
        self.btnRefreshModels.setProperty("secondary", True)
        self.btnRefreshModels.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnRefreshModels)

        self.btnAddModel = QPushButton(parent=headerCard)
        self.btnAddModel.setObjectName("btnAddModel")
        self.btnAddModel.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnAddModel)

        self.btnEditModel = QPushButton(parent=headerCard)
        self.btnEditModel.setObjectName("btnEditModel")
        self.btnEditModel.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnEditModel)

        self.btnDeleteModel = QPushButton(parent=headerCard)
        self.btnDeleteModel.setObjectName("btnDeleteModel")
        self.btnDeleteModel.setProperty("secondary", True)
        self.btnDeleteModel.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnDeleteModel)

        self.toolbar.addStretch()

        self.btnBackToDashboard = QPushButton(parent=headerCard)
        self.btnBackToDashboard.setObjectName("btnBackToDashboard")
        self.btnBackToDashboard.setProperty("secondary", True)
        self.btnBackToDashboard.setMinimumHeight(46)
        self.toolbar.addWidget(self.btnBackToDashboard)

        headerLayout.addLayout(self.toolbar)
        self.vlRoot.addWidget(headerCard)

        tableCard = create_glass_card(self.centralwidget, padding=18)
        tableLayout = QVBoxLayout(tableCard)
        tableLayout.setContentsMargins(16, 16, 16, 16)
        tableLayout.setSpacing(12)

        tableHeader = QLabel(parent=tableCard)
        tableHeader.setText("Danh sách mô hình đang hoạt động")
        tableHeader.setStyleSheet("font-weight:600; font-size:16px;")
        tableLayout.addWidget(tableHeader)

        self.tblModels = QTableWidget(parent=tableCard)
        self.tblModels.setObjectName("tblModels")
        self.tblModels.setColumnCount(5)
        self.tblModels.setRowCount(0)
        self.tblModels.setAlternatingRowColors(True)
        self.tblModels.horizontalHeader().setStretchLastSection(True)
        self.tblModels.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tblModels.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        headers = ["", "", "", "", ""]
        for idx, text in enumerate(headers):
            item = QTableWidgetItem(text)
            self.tblModels.setHorizontalHeaderItem(idx, item)
        tableLayout.addWidget(self.tblModels)

        badgeRow = QHBoxLayout()
        badgeRow.addStretch()
        badge = QLabel(parent=tableCard)
        badge.setText("🍏 Hiệu chuẩn tự động mỗi 24h")
        badge.setStyleSheet("color:#0A8754; font-weight:600;")
        badgeRow.addWidget(badge)
        tableLayout.addLayout(badgeRow)

        self.vlRoot.addWidget(tableCard)

        MainWindow_ModelManagement.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_ModelManagement)
        self.statusbar.setObjectName("statusbar")
        MainWindow_ModelManagement.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_ModelManagement)

    def retranslateUi(self, MainWindow_ModelManagement: QMainWindow) -> None:
        MainWindow_ModelManagement.setWindowTitle("Trung tâm mô hình AI nông sản")
        title = self.centralwidget.findChild(QLabel, "Headline")
        if title:
            title.setText("Tối ưu mô hình phân loại trái cây")
        subtitle = self.centralwidget.findChild(QLabel, "Subtitle")
        if subtitle:
            subtitle.setText("Chọn, chỉnh sửa và triển khai mô hình AI")

        self.txtSearchModel.setPlaceholderText("Tìm kiếm mô hình, ví dụ: EfficientNet")
        self.btnSearchModel.setText("Tìm kiếm")
        self.btnRefreshModels.setText("Tải lại")
        self.btnAddModel.setText("Thêm mô hình")
        self.btnEditModel.setText("Chỉnh sửa")
        self.btnDeleteModel.setText("Xoá")
        self.btnBackToDashboard.setText("🏠 Quay về Dashboard")

        headers = [
            "ID",
            "Tên mô hình",
            "Độ chính xác",
            "Đường dẫn",
            "Ngày tạo",
        ]
        for idx, text in enumerate(headers):
            item = self.tblModels.horizontalHeaderItem(idx)
            if item:
                item.setText(text)
