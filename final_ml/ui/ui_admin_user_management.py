from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QComboBox,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import create_glass_card, apply_global_styles


class Ui_MainWindow_UserManagement(object):
    def setupUi(self, MainWindow_UserManagement: QMainWindow) -> None:
        MainWindow_UserManagement.setObjectName("MainWindow_UserManagement")
        MainWindow_UserManagement.resize(1180, 720)
        apply_global_styles(MainWindow_UserManagement)

        self.centralwidget = QWidget(parent=MainWindow_UserManagement)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(48, 36, 48, 36)
        self.verticalLayout.setSpacing(24)

        heroCard = create_glass_card(self.centralwidget, padding=32)
        heroLayout = QVBoxLayout(heroCard)
        heroLayout.setSpacing(10)

        title = QLabel(parent=heroCard)
        title.setObjectName("Headline")
        heroLayout.addWidget(title)

        subtitle = QLabel(parent=heroCard)
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)
        heroLayout.addWidget(subtitle)

        self.layoutToolbar = QHBoxLayout()
        self.layoutToolbar.setSpacing(12)

        self.lineEditSearchUser = QLineEdit(parent=heroCard)
        self.lineEditSearchUser.setObjectName("lineEditSearchUser")
        self.lineEditSearchUser.setMinimumHeight(46)
        self.layoutToolbar.addWidget(self.lineEditSearchUser, stretch=3)

        self.comboRoleFilter = QComboBox(parent=heroCard)
        self.comboRoleFilter.setObjectName("comboRoleFilter")
        self.comboRoleFilter.setMinimumWidth(160)
        self.layoutToolbar.addWidget(self.comboRoleFilter, stretch=1)

        self.btnSearchUser = QPushButton(parent=heroCard)
        self.btnSearchUser.setObjectName("btnSearchUser")
        self.btnSearchUser.setMinimumHeight(46)
        self.layoutToolbar.addWidget(self.btnSearchUser)

        self.btnRefreshUser = QPushButton(parent=heroCard)
        self.btnRefreshUser.setObjectName("btnRefreshUser")
        self.btnRefreshUser.setProperty("secondary", True)
        self.btnRefreshUser.setMinimumHeight(46)
        self.layoutToolbar.addWidget(self.btnRefreshUser)

        heroLayout.addLayout(self.layoutToolbar)

        actionRow = QHBoxLayout()
        actionRow.setSpacing(12)
        actionRow.addStretch()

        self.btnAddUser = QPushButton(parent=heroCard)
        self.btnAddUser.setObjectName("btnAddUser")
        self.btnAddUser.setMinimumHeight(44)
        actionRow.addWidget(self.btnAddUser)

        self.btnEditUser = QPushButton(parent=heroCard)
        self.btnEditUser.setObjectName("btnEditUser")
        self.btnEditUser.setMinimumHeight(44)
        actionRow.addWidget(self.btnEditUser)

        self.btnDeleteUser = QPushButton(parent=heroCard)
        self.btnDeleteUser.setObjectName("btnDeleteUser")
        self.btnDeleteUser.setProperty("secondary", True)
        self.btnDeleteUser.setMinimumHeight(44)
        actionRow.addWidget(self.btnDeleteUser)

        actionRow.addStretch()

        self.btnBackToDashboard = QPushButton(parent=heroCard)
        self.btnBackToDashboard.setObjectName("btnBackToDashboard")
        self.btnBackToDashboard.setProperty("secondary", True)
        self.btnBackToDashboard.setMinimumHeight(44)
        actionRow.addWidget(self.btnBackToDashboard)

        heroLayout.addLayout(actionRow)
        self.verticalLayout.addWidget(heroCard)

        tableCard = create_glass_card(self.centralwidget, padding=24)
        tableLayout = QVBoxLayout(tableCard)
        tableLayout.setSpacing(12)

        tableHeader = QLabel(parent=tableCard)
        tableHeader.setText("Danh sách thành viên & đối tác")
        tableHeader.setStyleSheet("font-weight:600; font-size:16px;")
        tableLayout.addWidget(tableHeader)

        self.tableWidgetUsers = QTableWidget(parent=tableCard)
        self.tableWidgetUsers.setObjectName("tableWidgetUsers")
        self.tableWidgetUsers.setColumnCount(7)
        self.tableWidgetUsers.setRowCount(0)
        self.tableWidgetUsers.setAlternatingRowColors(True)
        self.tableWidgetUsers.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetUsers.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidgetUsers.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        headers = ["", "", "", "", "", "", ""]
        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            self.tableWidgetUsers.setHorizontalHeaderItem(i, item)
        tableLayout.addWidget(self.tableWidgetUsers)

        self.verticalLayout.addWidget(tableCard)

        MainWindow_UserManagement.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_UserManagement)
        MainWindow_UserManagement.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_UserManagement)

    def retranslateUi(self, MainWindow_UserManagement: QMainWindow) -> None:
        MainWindow_UserManagement.setWindowTitle("Quản trị thành viên - Orchard Intelligence")
        title = self.centralwidget.findChild(QLabel, "Headline")
        if title:
            title.setText("Điều phối thành viên & quyền truy cập")
        subtitle = self.centralwidget.findChild(QLabel, "Subtitle")
        if subtitle:
            subtitle.setText("Giao diện dạng website sang trọng giúp bạn kiểm soát tài khoản và phân quyền theo vai trò.")

        self.lineEditSearchUser.setPlaceholderText("Tìm theo họ tên, email hoặc ID người dùng...")
        self.comboRoleFilter.clear()
        self.comboRoleFilter.addItems(["Tất cả vai trò", "Admin", "User"])

        self.btnSearchUser.setText("Lọc dữ liệu")
        self.btnRefreshUser.setText("Làm mới")
        self.btnAddUser.setText("Thêm người dùng")
        self.btnEditUser.setText("Chỉnh sửa")
        self.btnDeleteUser.setText("Xoá")
        self.btnBackToDashboard.setText("🏠 Quay về Dashboard")

        headers = ["ID", "Tên hiển thị", "Email", "Vai trò", "Ngày tạo", "Mật khẩu", "Lần đăng nhập cuối"]
        for idx, text in enumerate(headers):
            item = self.tableWidgetUsers.horizontalHeaderItem(idx)
            if item:
                item.setText(text)
