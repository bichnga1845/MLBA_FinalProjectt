import json
import os
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QSize
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
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()
        self.MainWindow = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.apply_premium_styles()
        self.add_premium_icons()
        self.setupSignalAndSlot()
        self.load_saved_credentials()
    
    def apply_premium_styles(self):
        """Apply ultra premium stylesheet with gradients and effects"""
        self.MainWindow.setStyleSheet("""
            /* Main Window Background */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            /* Title Styles */
            QLabel#lblWelcome {
                font-size: 32px;
                font-weight: 700;
                color: #2D7A4E;
                letter-spacing: -0.5px;
                background: transparent;
            }
            
            QLabel#lblSubtitle {
                font-size: 13px;
                color: #5A7A6A;
                background: transparent;
                margin-top: 4px;
            }
            
            /* Field Labels */
            QLabel {
                color: #1A3A2E;
                font-weight: 600;
                font-size: 12px;
                background: transparent;
            }
            
            /* Tab Widget */
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: transparent;
                color: #8B9D94;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 14px;
                margin-right: 4px;
            }
            
            QTabBar::tab:selected {
                color: #2D7A4E;
                border-bottom: 3px solid #2D7A4E;
            }
            
            QTabBar::tab:hover {
                color: #4A9D6E;
                background-color: rgba(45, 122, 78, 0.05);
                border-radius: 8px 8px 0 0;
            }
            
            /* Input Fields with Premium Style */
            QLineEdit {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 11px 14px;
                background-color: #FFFFFF;
                font-size: 13px;
                color: #1A3A2E;
                min-height: 34px;
            }
            
            QLineEdit:hover {
                border-color: #4A9D6E;
                background-color: rgba(45, 122, 78, 0.02);
            }
            
            QLineEdit:focus {
                border-color: #2D7A4E;
                background-color: #FAFFFE;
            }
            
            /* ComboBox Premium Style */
            QComboBox {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 9px 12px;
                background-color: #FFFFFF;
                color: #2D7A4E;
                min-height: 34px;
                font-size: 13px;
            }
            
            QComboBox:hover {
                border-color: #4A9D6E;
            }
            
            QComboBox:focus {
                border-color: #2D7A4E;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 36px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                selection-background-color: #E8F5E9;
                selection-color: #2D7A4E;
                color: #2D7A4E;
                padding: 4px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 10px;
                border-radius: 6px;
                color: #2D7A4E;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F5E9;
            }
            
            /* Premium Gradient Buttons */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-height: 38px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E5A35, stop:1 #246A3F);
            }
            
            /* Checkbox Premium Style */
            QCheckBox {
                color: #2D7A4E;
                spacing: 8px;
                font-size: 12px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #E0E7E4;
                border-radius: 5px;
                background-color: white;
            }
            
            QCheckBox::indicator:hover {
                border-color: #4A9D6E;
            }
            
            QCheckBox::indicator:checked {
                background-color: #2D7A4E;
                border-color: #2D7A4E;
            }
            
            /* Card Style */
            QFrame#loginCard {
                background-color: rgba(255, 255, 255, 0.98);
                border: 1px solid rgba(224, 231, 228, 0.5);
                border-radius: 16px;
            }
        """)
    
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
            forgot_icon = qta.icon('fa5s.key', color='#2D7A4E', scale_factor=1.0)
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
        role = self.comboRoleLogin.currentText().lower()

        if not email or not pwd:
            QMessageBox.warning(None, "Thiếu thông tin", "Vui lòng nhập đầy đủ email và mật khẩu.")
            return

        try:
            self.mc.connect()
            sql = "SELECT * FROM Users WHERE email=%s AND password=%s AND role=%s"
            user = self.mc.fetchone(sql, (email, pwd, role))

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
                "role": user[4]
            }

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
