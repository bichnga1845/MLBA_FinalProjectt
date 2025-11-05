import json
import os
from PyQt6.QtWidgets import QMessageBox
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_login_signup import Ui_MainWindow_LoginSignUp
from final_ml.ui.ui_admin_dashboardExt import ui_admin_dashboardExt
from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt
from PyQt6.QtWidgets import QMainWindow


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
        self.setupSignalAndSlot()
        self.load_saved_credentials()

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
