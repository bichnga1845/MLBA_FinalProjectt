from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import (
    GOLDEN_CITRUS,
    PRIMARY_GREEN,
    apply_global_styles,
    create_glass_card,
    create_gradient_panel,
)


class Ui_MainWindow_LoginSignUp(object):
    def setupUi(self, MainWindow_LoginSignUp: QMainWindow) -> None:
        MainWindow_LoginSignUp.setObjectName("MainWindow_LoginSignUp")
        MainWindow_LoginSignUp.resize(1180, 720)
        apply_global_styles(MainWindow_LoginSignUp)

        self.centralwidget = QWidget(parent=MainWindow_LoginSignUp)
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(48, 32, 48, 32)
        self.mainLayout.setSpacing(32)

        # Gradient hero similar to provided mockup
        self.heroPanel = create_gradient_panel(self.centralwidget)
        self.heroPanel.setMinimumWidth(380)
        heroLayout = QVBoxLayout(self.heroPanel)
        heroLayout.setSpacing(18)

        self.logoLabel = QLabel(parent=self.heroPanel)
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setFixedSize(96, 96)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logoLabel.setStyleSheet(
            "border-radius:48px; background:rgba(255,255,255,0.2); font-size:28px; font-weight:700;"
        )
        heroLayout.addWidget(self.logoLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        self.lblWelcome = QLabel(parent=self.heroPanel)
        self.lblWelcome.setObjectName("lblWelcome")
        self.lblWelcome.setStyleSheet("font-size:32px; font-weight:700; color:white;")
        heroLayout.addWidget(self.lblWelcome)

        self.lblSubtitle = QLabel(parent=self.heroPanel)
        self.lblSubtitle.setObjectName("lblSubtitle")
        self.lblSubtitle.setWordWrap(True)
        self.lblSubtitle.setStyleSheet("color: rgba(255,255,255,0.85); font-size:15px; line-height:1.4;")
        heroLayout.addWidget(self.lblSubtitle)

        self.heroDescription = QLabel(parent=self.heroPanel)
        self.heroDescription.setObjectName("heroDescription")
        self.heroDescription.setWordWrap(True)
        self.heroDescription.setStyleSheet("color: rgba(255,255,255,0.7); font-size:13px;")
        heroLayout.addWidget(self.heroDescription)

        heroLayout.addStretch()

        self.heroCTA = QPushButton(parent=self.heroPanel)
        self.heroCTA.setObjectName("heroCTA")
        self.heroCTA.setProperty("secondary", True)
        self.heroCTA.setStyleSheet(
            "QPushButton { background:rgba(255,255,255,0.2); color:white; border:1px solid rgba(255,255,255,0.5); }"
        )
        heroLayout.addWidget(self.heroCTA, alignment=Qt.AlignmentFlag.AlignLeft)

        self.heroFooter = QLabel(parent=self.heroPanel)
        self.heroFooter.setObjectName("heroFooter")
        self.heroFooter.setStyleSheet("color: rgba(255,255,255,0.6); font-size:12px;")
        heroLayout.addWidget(self.heroFooter)

        self.mainLayout.addWidget(self.heroPanel, stretch=1)

        # White form card
        self.loginCard = create_glass_card(parent=self.centralwidget, padding=36)
        self.loginCard.setMinimumWidth(460)
        cardLayout = QVBoxLayout(self.loginCard)
        cardLayout.setSpacing(18)

        headerLayout = QVBoxLayout()
        title = QLabel(parent=self.loginCard)
        title.setObjectName("Headline")
        headerLayout.addWidget(title)

        self.lblAuthStatus = QLabel(parent=self.loginCard)
        self.lblAuthStatus.setObjectName("lblAuthStatus")
        self.lblAuthStatus.setStyleSheet("color: rgba(12,43,27,0.65); font-size:13px;")
        headerLayout.addWidget(self.lblAuthStatus)
        cardLayout.addLayout(headerLayout)

        self.tabAuth = QTabWidget(parent=self.loginCard)
        self.tabAuth.setObjectName("tabAuth")
        self.tabAuth.setDocumentMode(True)

        self.tabLogin = QWidget()
        self.gridLogin = QGridLayout(self.tabLogin)
        self.gridLogin.setSpacing(12)

        self.lblUsernameLogin = QLabel(parent=self.tabLogin)
        self.gridLogin.addWidget(self.lblUsernameLogin, 0, 0)
        self.lineEditLoginUsername = QLineEdit(parent=self.tabLogin)
        self.lineEditLoginUsername.setProperty("pill", "true")
        self.gridLogin.addWidget(self.lineEditLoginUsername, 1, 0, 1, 2)

        self.lblPasswordLogin = QLabel(parent=self.tabLogin)
        self.gridLogin.addWidget(self.lblPasswordLogin, 2, 0)
        self.lineEditLoginPassword = QLineEdit(parent=self.tabLogin)
        self.lineEditLoginPassword.setProperty("pill", "true")
        self.lineEditLoginPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridLogin.addWidget(self.lineEditLoginPassword, 3, 0, 1, 2)

        self.lblRoleLogin = QLabel(parent=self.tabLogin)
        self.gridLogin.addWidget(self.lblRoleLogin, 4, 0)
        self.comboRoleLogin = QComboBox(parent=self.tabLogin)
        self.comboRoleLogin.setProperty("pill", "true")
        self.gridLogin.addWidget(self.comboRoleLogin, 5, 0, 1, 2)

        self.chkRemember = QCheckBox(parent=self.tabLogin)
        self.gridLogin.addWidget(self.chkRemember, 6, 0)

        rememberRow = QHBoxLayout()
        rememberRow.addStretch()
        self.btnForgotPassword = QPushButton(parent=self.tabLogin)
        self.btnForgotPassword.setProperty("secondary", True)
        rememberRow.addWidget(self.btnForgotPassword, 0, Qt.AlignmentFlag.AlignRight)
        self.gridLogin.addLayout(rememberRow, 6, 1)

        self.btnLogin = QPushButton(parent=self.tabLogin)
        self.btnLogin.setMinimumHeight(48)
        self.gridLogin.addWidget(self.btnLogin, 7, 0, 1, 2)

        self.tabAuth.addTab(self.tabLogin, "")

        self.tabSignup = QWidget()
        self.gridSignup = QGridLayout(self.tabSignup)
        self.gridSignup.setSpacing(12)

        self.lblUsernameSignup = QLabel(parent=self.tabSignup)
        self.gridSignup.addWidget(self.lblUsernameSignup, 0, 0)
        self.lineEditSignupUsername = QLineEdit(parent=self.tabSignup)
        self.lineEditSignupUsername.setProperty("pill", "true")
        self.gridSignup.addWidget(self.lineEditSignupUsername, 1, 0, 1, 2)

        self.lblEmailSignup = QLabel(parent=self.tabSignup)
        self.gridSignup.addWidget(self.lblEmailSignup, 2, 0)
        self.lineEditSignupEmail = QLineEdit(parent=self.tabSignup)
        self.lineEditSignupEmail.setProperty("pill", "true")
        self.gridSignup.addWidget(self.lineEditSignupEmail, 3, 0, 1, 2)

        self.lblPasswordSignup = QLabel(parent=self.tabSignup)
        self.gridSignup.addWidget(self.lblPasswordSignup, 4, 0)
        self.lineEditSignupPassword = QLineEdit(parent=self.tabSignup)
        self.lineEditSignupPassword.setProperty("pill", "true")
        self.lineEditSignupPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridSignup.addWidget(self.lineEditSignupPassword, 5, 0, 1, 2)

        self.lblConfirmPassword = QLabel(parent=self.tabSignup)
        self.gridSignup.addWidget(self.lblConfirmPassword, 6, 0)
        self.lineEditSignupCFPassword = QLineEdit(parent=self.tabSignup)
        self.lineEditSignupCFPassword.setProperty("pill", "true")
        self.lineEditSignupCFPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.gridSignup.addWidget(self.lineEditSignupCFPassword, 7, 0, 1, 2)

        self.lblRoleSignup = QLabel(parent=self.tabSignup)
        self.gridSignup.addWidget(self.lblRoleSignup, 8, 0)
        self.comboRoleSignup = QComboBox(parent=self.tabSignup)
        self.comboRoleSignup.setProperty("pill", "true")
        self.gridSignup.addWidget(self.comboRoleSignup, 9, 0, 1, 2)

        self.btnSignup = QPushButton(parent=self.tabSignup)
        self.btnSignup.setMinimumHeight(48)
        self.gridSignup.addWidget(self.btnSignup, 10, 0, 1, 2)

        self.tabAuth.addTab(self.tabSignup, "")
        cardLayout.addWidget(self.tabAuth)

        badgeRow = QHBoxLayout()
        badge = QLabel(parent=self.loginCard)
        badge.setText("Chào mừng đến với Fruit ML!")
        badge.setStyleSheet(
            f"background-color:{GOLDEN_CITRUS}; color:{PRIMARY_GREEN}; padding:6px 16px; border-radius:999px; font-weight:600;"
        )
        badgeRow.addWidget(badge)
        badgeRow.addStretch()
        cardLayout.addLayout(badgeRow)

        self.mainLayout.addWidget(self.loginCard, stretch=1)

        MainWindow_LoginSignUp.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_LoginSignUp)
        self.statusbar.setObjectName("statusbar")
        MainWindow_LoginSignUp.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_LoginSignUp)
        self.tabAuth.setCurrentIndex(0)

    def retranslateUi(self, MainWindow_LoginSignUp: QMainWindow) -> None:
        MainWindow_LoginSignUp.setWindowTitle("dYUZ Fruit ML ")
        self.logoLabel.setText("FML")
        self.lblWelcome.setText("Welcome back!")
        self.lblSubtitle.setText(
            "Stay connected with your orchards and monitor fruit batches from anywhere."
        )
        self.heroDescription.setText("Log in to sync AI predictions, shipment history, and premium dashboards.")
        self.heroCTA.setText("Khám phá bảng điều khiển")
        self.heroFooter.setText("© 2025 Fruit ML - All rights reserved.")

        self.loginCard.findChild(QLabel, "Headline").setText("Login experience")
        self.lblAuthStatus.setText("Đăng nhập hoặc đăng ký để tiếp tục.")

        self.lblUsernameLogin.setText("Email / Username")
        self.lblPasswordLogin.setText("Mật khẩu")
        self.lblRoleLogin.setText("Vai trò")
        self.comboRoleLogin.clear()
        self.comboRoleLogin.addItems(["User", "Admin"])
        self.chkRemember.setText("Ghi nhớ tôi")
        self.btnForgotPassword.setText("Quên mật khẩu?")
        self.btnLogin.setText("Sign in")

        self.lblUsernameSignup.setText("Họ tên / Thương hiệu")
        self.lblEmailSignup.setText("Email liên hệ")
        self.lblPasswordSignup.setText("Mật khẩu")
        self.lblConfirmPassword.setText("Xác nhận mật khẩu")
        self.lblRoleSignup.setText("Chọn vai trò")
        self.comboRoleSignup.clear()
        self.comboRoleSignup.addItems(["User", "Admin"])
        self.btnSignup.setText("Tạo tài khoản mới")

        self.tabAuth.setTabText(self.tabAuth.indexOf(self.tabLogin), "Đăng nhập")
        self.tabAuth.setTabText(self.tabAuth.indexOf(self.tabSignup), "Đăng ký")
