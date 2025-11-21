import json
import os
from pathlib import Path
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QMessageBox,
    QMainWindow,
    QGraphicsOpacityEffect,
    QLabel,
)
from PyQt6.QtCore import QSize, Qt
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_login_signup import Ui_MainWindow_LoginSignUp
from final_ml.ui.ui_admin_dashboardExt import ui_admin_dashboardExt
from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt
import qtawesome as qta


#GHI NHỚ ĐĂNG NHẬP

def save_credentials(email, password):
    """Lưu thông tin đăng nhập vào file JSON"""
    with open("credentials.json", "w", encoding="utf-8") as f:
        json.dump({"email": email, "password": password}, f)

def load_credentials():
    """Đọc thông tin đăng nhập nếu có"""
    if os.path.exists("credentials.json"):
        with open("credentials.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def clear_credentials():
    """Xóa thông tin đăng nhập"""
    if os.path.exists("credentials.json"):
        os.remove("credentials.json")

class ui_login_signupExt(Ui_MainWindow_LoginSignUp):
    def __init__(self, brand_logo_path: str | None = None, hero_background_path: str | None = None):
        super().__init__()
        self.mc = FinalConnector()
        self.MainWindow = None
        base_dir = Path(__file__).resolve().parent.parent
        default_logo = base_dir / "uploads" / "logo.jpg"
        default_bg = base_dir / "uploads" / "hero_bg.jpg"
        self.brand_logo_path = (
            brand_logo_path
            or os.getenv("FRUIT_APP_LOGO")
            or (str(default_logo) if default_logo.exists() else None)
        )
        self.hero_background_path = (
            hero_background_path
            or os.getenv("FRUIT_APP_HERO_BG")
            or (str(default_bg) if default_bg.exists() else str(default_logo) if default_logo.exists() else None)
        )
        self._hero_overlay_pixmap = None
        self._hero_resize_hooked = False

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.apply_premium_styles()
        self.add_premium_icons()
        self.configure_hero_copy()
        self.hide_role_inputs()
        self.set_brand_logo(self.brand_logo_path)
        self.set_hero_background(self.hero_background_path)
        self.setupSignalAndSlot()
        self.load_saved_credentials()
    
    def apply_premium_styles(self):
        extra = """
            QTabWidget::pane { border: none; background: transparent; }
            QTabBar::tab {
                background: transparent;
                color: #9AA8A0;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                margin-right: 6px;
            }
            QTabBar::tab:selected { color: #0A8754; border-bottom: 3px solid #0A8754; }
            QTabBar::tab:hover { color: #0BBE6E; }
            QLabel#lblAuthStatus { letter-spacing: 0.5px; }
        """
        base = self.MainWindow.styleSheet() or ''
        self.MainWindow.setStyleSheet(base + '\n' + extra)

    def configure_hero_copy(self):
        if hasattr(self, 'lblWelcome'):
            self.lblWelcome.setText('Welcome back!')
        if hasattr(self, 'lblSubtitle'):
            self.lblSubtitle.setText('hihihi')
        if hasattr(self, 'heroDescription'):
            self.heroDescription.setText('Sign in to sync prediction data and shipment history.')
        if hasattr(self, 'heroCTA'):
            self.heroCTA.setText('Explore dashboard')

    def hide_role_inputs(self):
        """Hide role selection on login; role is determined automatically from the account."""
        for widget_name in ("lblRoleLogin", "comboRoleLogin"):
            widget = getattr(self, widget_name, None)
            if widget:
                widget.hide()

    def set_brand_logo(self, image_path: str | None):
        if not hasattr(self, 'logoLabel'):
            return
        final_path = image_path
        if not final_path:
            candidate = os.path.join(os.path.dirname(__file__), '../final_ml/upload/logo.jpg')
            if os.path.exists(candidate):
                final_path = candidate
        if not final_path or not os.path.exists(final_path):
            return
        pix = QPixmap(final_path)
        if pix.isNull():
            return
        scaled = pix.scaled(
            self.logoLabel.width(),
            self.logoLabel.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.logoLabel.setPixmap(scaled)
        self.logoLabel.setStyleSheet('border-radius:48px;')
        self.logoLabel.setText('')

    def set_hero_background(self, image_path: str | None):
        if not hasattr(self, 'heroPanel'):
            return
        if not image_path:
            if hasattr(self, 'heroOverlay'):
                self.heroOverlay.hide()
            return
        normalized = Path(image_path)
        if not normalized.exists():
            return
        pix = QPixmap(str(normalized))
        if pix.isNull():
            return
        self._hero_overlay_pixmap = pix
        if not hasattr(self, 'heroOverlay'):
            self.heroOverlay = QLabel(parent=self.heroPanel)
            self.heroOverlay.setObjectName("heroOverlay")
            self.heroOverlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            self.heroOverlay.setScaledContents(True)
            opacity = QGraphicsOpacityEffect(self.heroOverlay)
            opacity.setOpacity(0.25)
            self.heroOverlay.setGraphicsEffect(opacity)
        self.heroOverlay.show()
        self.heroOverlay.lower()
        self._update_hero_overlay_geometry()
        if not self._hero_resize_hooked:
            original_resize = self.heroPanel.resizeEvent

            def _resized(event):
                self._update_hero_overlay_geometry()
                if original_resize:
                    original_resize(event)

            self.heroPanel.resizeEvent = _resized
            self._hero_resize_hooked = True

    def _update_hero_overlay_geometry(self):
        if not hasattr(self, 'heroOverlay') or self._hero_overlay_pixmap is None:
            return
        panel_rect = self.heroPanel.rect()
        if panel_rect.width() <= 0 or panel_rect.height() <= 0:
            return
        self.heroOverlay.setGeometry(0, 0, panel_rect.width(), panel_rect.height())
        scaled = self._hero_overlay_pixmap.scaled(
            self.heroOverlay.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.heroOverlay.setPixmap(scaled)


    def add_premium_icons(self):
        """Add FontAwesome icons to buttons and inputs"""
        try:
            # Login button with icon
            login_icon = qta.icon('fa5s.sign-in-alt', color='white', scale_factor=1.2)
            self.btnLogin.setIcon(login_icon)
            self.btnLogin.setIconSize(QSize(18, 18))
            self.btnLogin.setText("  Đăng nhập")
            
            # Signup button with icon
            signup_icon = qta.icon('fa5s.user-plus', color='white', scale_factor=1.2)
            self.btnSignup.setIcon(signup_icon)
            self.btnSignup.setIconSize(QSize(18, 18))
            self.btnSignup.setText("  Tạo tài khoản")
            
            # Forgot password with icon
            forgot_icon = qta.icon('fa5s.key', color='white', scale_factor=1.0)
            self.btnForgotPassword.setIcon(forgot_icon)
            self.btnForgotPassword.setIconSize(QSize(14, 14))
            
        except Exception as e:
            print(f"Could not add icons: {e}")

    def setupSignalAndSlot(self):
        self.btnLogin.clicked.connect(self.process_login)
        self.btnSignup.clicked.connect(self.process_signup)
        self.btnForgotPassword.clicked.connect(self.process_forgot_password)


    def load_saved_credentials(self):
        creds = load_credentials()
        if creds:
            self.lineEditLoginUsername.setText(creds["email"])
            self.lineEditLoginPassword.setText(creds["password"])
            self.chkRemember.setChecked(True)


    def process_login(self):
        email = self.lineEditLoginUsername.text().strip()
        pwd = self.lineEditLoginPassword.text().strip()

        if not email or not pwd:
            QMessageBox.warning(None, "Thiếu thông tin", "Vui lòng nhập đầy đủ email và mật khẩu.")
            return

        try:
            self.mc.connect()
            sql = "SELECT * FROM Users WHERE email=%s AND password=%s"
            user = self.mc.fetchone(sql, (email, pwd))

            if user is None:
                QMessageBox.critical(None, "Đăng nhập thất bại", "Email hoặc mật khẩu không đúng.")
                return

            if self.chkRemember.isChecked():
                save_credentials(email, pwd)
            else:
                clear_credentials()

            #Cập nhật last login
            sql_last_login = """
                UPDATE Users
                SET last_login = NOW()
                WHERE user_id = %s
            """
            val=(user[0],)
            self.mc.insert_one(sql_last_login, val)

            current_user = {
                "user_id": user[0],
                "full_name": user[1],
                "email": user[2],
                "role": user[4],
                "password":user[3]
            }

            role = (user[4] or "").lower()
            if role == "admin":
                self.open_admin_dashboard(current_user)
            else:
                self.open_user_upload(current_user)

        except Exception as e:
            QMessageBox.critical(None, "Lỗi hệ thống", f"Lỗi khi đăng nhập: {e}")


    # ĐĂNG KÝ

    def process_signup(self):
        name = self.lineEditSignupUsername.text().strip()
        email = self.lineEditSignupEmail.text().strip()
        pwd = self.lineEditSignupPassword.text().strip()
        cf_pwd = self.lineEditSignupCFPassword.text().strip()
        role = self.comboRoleSignup.currentText().lower()

        if not all([name, email, pwd, cf_pwd]):
            QMessageBox.warning(None, "Thiếu thông tin", "Vui lòng điền đầy đủ các trường.")
            return

        if pwd != cf_pwd:
            QMessageBox.warning(None, "Mật khẩu không khớp", "Vui lòng nhập lại mật khẩu trùng khớp.")
            return

        try:
            self.mc.connect()
            # Kiểm tra tồn tại
            sql_check = "SELECT * FROM Users WHERE email=%s"
            existed = self.mc.fetchone(sql_check, (email,))
            if existed:
                QMessageBox.warning(None, "Đã tồn tại", "Email này đã được sử dụng.")
                return

            # Thêm người dùng mới
            sql_insert = """INSERT INTO Users (full_name, email, password, role, created_at, last_login)
                            VALUES (%s, %s, %s, %s, NOW(), NOW())"""
            self.mc.insert_one(sql_insert, (name, email, pwd, role))
            QMessageBox.information(None, "Thành công", "Đăng ký tài khoản thành công!")

            # Tự động lưu vào bảng Admins / NormalUsers
            sql_get = "SELECT user_id FROM Users WHERE email=%s"
            new_user = self.mc.fetchone(sql_get, (email,))
            if role == "admin":
                self.mc.insert_one("INSERT INTO Admins (admin_id, admin_level) VALUES (%s, 'super_admin')", (new_user[0],))
            else:
                self.mc.insert_one("INSERT INTO NormalUsers (normal_user_id, organization) VALUES (%s, 'N/A')", (new_user[0],))

        except Exception as e:
            QMessageBox.critical(None, "Lỗi đăng ký", f"Lỗi khi tạo tài khoản: {e}")


    # QUÊN MẬT KHẨU

    def process_forgot_password(self):
        email = self.lineEditLoginUsername.text().strip()
        if not email:
            QMessageBox.warning(None, "Thiếu thông tin", "Vui lòng nhập email để khôi phục mật khẩu.")
            return
        try:
            self.mc.connect()
            sql = "SELECT password FROM Users WHERE email=%s"
            user = self.mc.fetchone(sql, (email,))
            if user:
                QMessageBox.information(None, "Khôi phục mật khẩu",
                                        f"Mật khẩu của bạn là: {user[0]}\n(Hãy đổi mật khẩu sau khi đăng nhập.)")
            else:
                QMessageBox.warning(None, "Không tồn tại", "Không tìm thấy tài khoản với email này.")
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi khôi phục mật khẩu: {e}")


    def open_admin_dashboard(self, current_user):
        from PyQt6.QtWidgets import QMainWindow
        self.admin_window = QMainWindow()
        self.ui_admin = ui_admin_dashboardExt(current_user)
        self.ui_admin.setupUi(self.admin_window)
        self.MainWindow.close()
        self.admin_window.show()

    def open_user_upload(self, current_user):
        from PyQt6.QtWidgets import QMainWindow
        self.user_window = QMainWindow()
        self.ui_user = ui_upload_imageExt(current_user)
        self.ui_user.setupUi(self.user_window)
        self.MainWindow.close()
        self.user_window.show()
