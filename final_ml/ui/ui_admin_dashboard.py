# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import apply_global_styles


class Ui_MainWindow_AdminDashboard(object):
    def setupUi(self, MainWindow_AdminDashboard: QMainWindow) -> None:
        MainWindow_AdminDashboard.setObjectName("MainWindow_AdminDashboard")
        MainWindow_AdminDashboard.resize(1200, 800)
        apply_global_styles(
            MainWindow_AdminDashboard,
            extra_styles="""
            QPushButton[role="navCard"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8FAF9);
                color: #0C2B1B;
                border: 2px solid rgba(10, 135, 84, 0.2);
                border-radius: 18px;
                text-align: left;
                padding: 28px;
                font-size: 17px;
                font-weight: 600;
                min-height: 140px;
            }
            QPushButton[role="navCard"]:hover {
                border-color: #2D7A4E;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E8F5E9, stop:1 #F1F8F3);
            }
            QPushButton#btnLogout {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFF5F5, stop:1 #FFE8E8);
                border-color: rgba(196, 74, 74, 0.3);
                color: #C44A4A;
            }
            QPushButton#btnLogout:hover {
                border-color: #C44A4A;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFE8E8, stop:1 #FFD5D5);
            }
        """,
        )

        self.centralwidget = QWidget(parent=MainWindow_AdminDashboard)
        self.centralwidget.setObjectName("centralwidget")
        self.vlRoot = QVBoxLayout(self.centralwidget)
        self.vlRoot.setContentsMargins(50, 40, 50, 40)
        self.vlRoot.setSpacing(30)

        # Header
        headerLayout = QVBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 0)
        headerLayout.setSpacing(8)

        self.lblHeader = QLabel(parent=self.centralwidget)
        self.lblHeader.setObjectName("Headline")
        self.lblHeader.setStyleSheet("font-size:32px; font-weight:700; color:#0C2B1B;")
        headerLayout.addWidget(self.lblHeader)

        self.lblSubtitle = QLabel(parent=self.centralwidget)
        self.lblSubtitle.setObjectName("Subtitle")
        self.lblSubtitle.setWordWrap(True)
        self.lblSubtitle.setStyleSheet("font-size:15px; color:rgba(12,43,27,0.7);")
        headerLayout.addWidget(self.lblSubtitle)

        self.vlRoot.addLayout(headerLayout)

        # Navigation Grid
        self.gridNav = QGridLayout()
        self.gridNav.setHorizontalSpacing(24)
        self.gridNav.setVerticalSpacing(24)
        self.gridNav.setContentsMargins(0, 0, 0, 0)

        nav_items = [
            ("btnGoUserMgmt", "Quản lý người dùng"),
            ("btnGoDataMgmt", "Quản lý dữ liệu"),
            ("btnGoModelMgmt", "Quản lý mô hình"),
            ("btnGoStatistics", "Thống kê"),
            ("btnGoHistory", "Lịch sử"),
            ("btnLogout", "Đăng xuất"),
        ]

        for idx, (obj_name, title) in enumerate(nav_items):
            button = QPushButton(parent=self.centralwidget)
            button.setObjectName(obj_name)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setCheckable(False)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Set button text (QPushButton supports basic HTML)
            button.setText(title)
            button.setProperty("role", "navCard")
            
            self.gridNav.addWidget(button, idx // 2, idx % 2)
            setattr(self, obj_name, button)

        self.vlRoot.addLayout(self.gridNav)

        MainWindow_AdminDashboard.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_AdminDashboard)
        MainWindow_AdminDashboard.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_AdminDashboard)

    def retranslateUi(self, MainWindow_AdminDashboard: QMainWindow) -> None:
        MainWindow_AdminDashboard.setWindowTitle("Bảng điều khiển Admin - Fruit ML")
        self.lblHeader.setText("Khu điều khiển trung tâm")
        self.lblSubtitle.setText("Theo dõi dữ liệu, quản lý người dùng và mô hình chỉ với vài thao tác.")

