from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import apply_global_styles, create_glass_card


class Ui_MainWindow_HistorySettings(object):
    def setupUi(self, MainWindow_HistorySettings: QMainWindow) -> None:
        MainWindow_HistorySettings.setObjectName("MainWindow_HistorySettings")
        MainWindow_HistorySettings.resize(1100, 720)
        apply_global_styles(MainWindow_HistorySettings)

        self.centralwidget = QWidget(parent=MainWindow_HistorySettings)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(48, 36, 48, 36)
        self.verticalLayout.setSpacing(24)

        hero = create_glass_card(self.centralwidget, padding=32)
        heroLayout = QVBoxLayout(hero)
        heroLayout.setSpacing(8)

        headline = QLabel(parent=hero)
        headline.setObjectName("Headline")
        heroLayout.addWidget(headline)

        sub = QLabel(parent=hero)
        sub.setObjectName("Subtitle")
        sub.setWordWrap(True)
        heroLayout.addWidget(sub)

        self.tabMain = QTabWidget(parent=hero)
        self.tabMain.setObjectName("tabMain")

        # History tab
        self.tabHistory = QWidget()
        self.vlHistory = QVBoxLayout(self.tabHistory)
        self.vlHistory.setSpacing(16)

        filterCard = create_glass_card(self.tabHistory, padding=20)
        filterLayout = QVBoxLayout(filterCard)
        filterLayout.setSpacing(12)

        self.layoutFilters = QHBoxLayout()
        self.layoutFilters.setSpacing(10)

        self.txtSearchHistory = QLineEdit(parent=filterCard)
        self.txtSearchHistory.setObjectName("txtSearchHistory")
        self.txtSearchHistory.setMinimumHeight(44)
        self.layoutFilters.addWidget(self.txtSearchHistory, stretch=2)

        self.comboLabelHistory = QComboBox(parent=filterCard)
        self.comboLabelHistory.setObjectName("comboLabelHistory")
        self.comboLabelHistory.setMinimumWidth(150)
        self.layoutFilters.addWidget(self.comboLabelHistory)

        self.dateFrom = QDateEdit(parent=filterCard)
        self.dateFrom.setObjectName("dateFrom")
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setDate(QDate.currentDate().addMonths(-1))
        self.layoutFilters.addWidget(self.dateFrom)

        self.dateTo = QDateEdit(parent=filterCard)
        self.dateTo.setObjectName("dateTo")
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setDate(QDate.currentDate())
        self.layoutFilters.addWidget(self.dateTo)

        self.btnReloadHistory = QPushButton(parent=filterCard)
        self.btnReloadHistory.setObjectName("btnReloadHistory")
        self.btnReloadHistory.setMinimumHeight(44)
        self.layoutFilters.addWidget(self.btnReloadHistory)

        self.btnDeleteHistory = QPushButton(parent=filterCard)
        self.btnDeleteHistory.setObjectName("btnDeleteHistory")
        self.btnDeleteHistory.setProperty("secondary", True)
        self.btnDeleteHistory.setMinimumHeight(44)
        self.layoutFilters.addWidget(self.btnDeleteHistory)

        filterLayout.addLayout(self.layoutFilters)
        self.vlHistory.addWidget(filterCard)

        tableCard = create_glass_card(self.tabHistory, padding=20)
        tableLayout = QVBoxLayout(tableCard)
        self.tblHistory = QTableWidget(parent=tableCard)
        self.tblHistory.setObjectName("tblHistory")
        self.tblHistory.setColumnCount(6)
        self.tblHistory.setRowCount(0)
        self.tblHistory.setAlternatingRowColors(True)
        self.tblHistory.horizontalHeader().setStretchLastSection(True)
        self.tblHistory.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        for idx in range(6):
            self.tblHistory.setHorizontalHeaderItem(idx, QTableWidgetItem(""))
        tableLayout.addWidget(self.tblHistory)

        self.vlHistory.addWidget(tableCard)
        self.tabMain.addTab(self.tabHistory, "")

        # Settings tab
        self.tabSettings = QWidget()
        tabSettingsLayout = QVBoxLayout(self.tabSettings)
        tabSettingsLayout.setSpacing(16)

        profileCard = create_glass_card(self.tabSettings, padding=28)
        self.gridSettings = QGridLayout(profileCard)
        self.gridSettings.setHorizontalSpacing(18)
        self.gridSettings.setVerticalSpacing(14)

        self.lblUsername = QLabel(parent=profileCard)
        self.gridSettings.addWidget(self.lblUsername, 0, 0)
        self.txtUsername = QLineEdit(parent=profileCard)
        self.gridSettings.addWidget(self.txtUsername, 0, 1)

        self.lblEmail = QLabel(parent=profileCard)
        self.gridSettings.addWidget(self.lblEmail, 1, 0)
        self.txtEmail = QLineEdit(parent=profileCard)
        self.gridSettings.addWidget(self.txtEmail, 1, 1)

        self.lblOldPassword = QLabel(parent=profileCard)
        self.gridSettings.addWidget(self.lblOldPassword, 2, 0)
        self.txtOldPassword = QLineEdit(parent=profileCard)
        self.txtOldPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridSettings.addWidget(self.txtOldPassword, 2, 1)

        self.lblNewPassword = QLabel(parent=profileCard)
        self.gridSettings.addWidget(self.lblNewPassword, 3, 0)
        self.txtNewPassword = QLineEdit(parent=profileCard)
        self.txtNewPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridSettings.addWidget(self.txtNewPassword, 3, 1)

        self.lblConfirmNewPassword = QLabel(parent=profileCard)
        self.gridSettings.addWidget(self.lblConfirmNewPassword, 4, 0)
        self.txtConfirmNewPassword = QLineEdit(parent=profileCard)
        self.txtConfirmNewPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridSettings.addWidget(self.txtConfirmNewPassword, 4, 1)

        actionRow = QHBoxLayout()
        actionRow.addStretch()
        
        self.btnBackToDashboard = QPushButton(parent=profileCard)
        self.btnBackToDashboard.setObjectName("btnBackToDashboard")
        self.btnBackToDashboard.setProperty("secondary", True)
        actionRow.addWidget(self.btnBackToDashboard)
        
        self.btnUpdateProfile = QPushButton(parent=profileCard)
        self.btnUpdateProfile.setObjectName("btnUpdateProfile")
        actionRow.addWidget(self.btnUpdateProfile)

        self.btnLogout = QPushButton(parent=profileCard)
        self.btnLogout.setObjectName("btnLogout")
        self.btnLogout.setProperty("secondary", True)
        actionRow.addWidget(self.btnLogout)
        self.gridSettings.addLayout(actionRow, 5, 0, 1, 2)

        tabSettingsLayout.addWidget(profileCard)
        self.tabMain.addTab(self.tabSettings, "")

        heroLayout.addWidget(self.tabMain)
        self.verticalLayout.addWidget(hero)

        MainWindow_HistorySettings.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_HistorySettings)
        MainWindow_HistorySettings.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_HistorySettings)

    def retranslateUi(self, MainWindow_HistorySettings: QMainWindow) -> None:
        MainWindow_HistorySettings.setWindowTitle("Trải nghiệm khách hàng - Lịch sử & cài đặt")
        headline = self.centralwidget.findChild(QLabel, "Headline")
        if headline:
            headline.setText("Theo dõi lịch sử dự đoán & chăm sóc tài khoản")
        subtitle = self.centralwidget.findChild(QLabel, "Subtitle")
        if subtitle:
            subtitle.setText("Chào mừng bạn đến với bảng điều khiển cá nhân của bạn, nơi bạn có thể xem lịch sử dự đoán trái cây và quản lý cài đặt tài khoản của mình.")

        self.txtSearchHistory.setPlaceholderText("Tìm kiếm theo loại trái cây, chất lượng hoặc ID phiên.")
        self.comboLabelHistory.clear()
        self.comboLabelHistory.addItems(["Tất cả nhãn", "Good", "Bad"])
        self.btnReloadHistory.setText("Tải dữ liệu")
        self.btnDeleteHistory.setText("Xoá bản ghi")

        headers = [
            "ID dự đoán",
            "Hình ảnh",
            "Kết quả",
            "Độ tin cậy",
            "Thời gian",
            "Mô hình",
        ]
        for idx, text in enumerate(headers):
            item = self.tblHistory.horizontalHeaderItem(idx)
            if item:
                item.setText(text)

        self.tabMain.setTabText(self.tabMain.indexOf(self.tabHistory), "Lịch sử")
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabSettings), "Cài đặt")

        self.lblUsername.setText("Tên hiển thị")
        self.lblEmail.setText("Email")
        self.lblOldPassword.setText("Mật khẩu hiện tại")
        self.lblNewPassword.setText("Mật khẩu mới")
        self.lblConfirmNewPassword.setText("Xác nhận mật khẩu mới")
        self.btnBackToDashboard.setText("🏠 Quay về Dashboard")
        self.btnUpdateProfile.setText("Cập nhật hồ sơ")
        self.btnLogout.setText("Đăng xuất")
