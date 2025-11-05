from PyQt6.QtWidgets import QMessageBox, QDialog

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddUserDialog import Ui_Dialog


class AddUserDialogExt(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.save_user)
        self.btnCancel.clicked.connect(self.cancel)

    def save_user(self):
        name = self.lineEditName.text().strip()
        email = self.lineEditEmail.text().strip()
        password = self.lineEditPassword.text().strip()
        role = self.comboRole.currentText()

        if not name or not email or not password:
            QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            self.mc.connect()

            # Kiểm tra tồn tại
            sql_check = "SELECT * FROM Users WHERE email=%s"
            existed = self.mc.fetchone(sql_check, (email,))
            if existed:
                QMessageBox.warning(self.MainWindow, "Đã tồn tại", "Email này đã được sử dụng.")
                return

            sql = """INSERT INTO users (full_name, email, password, role, created_at, last_login)
                     VALUES (%s, %s, %s, %s, NOW(), NOW())"""
            val = (name, email, password, role)
            result = self.mc.insert_one(sql, val)

            # Tự động lưu vào bảng Admins / NormalUsers
            sql_get = "SELECT user_id FROM Users WHERE email=%s"
            new_user = self.mc.fetchone(sql_get, (email,))
            if role.lower() == "admin":
                self.mc.insert_one("INSERT INTO Admins (admin_id, admin_level) VALUES (%s, 'super_admin')",
                                   (new_user[0],))
            else:
                self.mc.insert_one("INSERT INTO NormalUsers (normal_user_id, organization) VALUES (%s, 'N/A')",
                                   (new_user[0],))

            if result > 0:
                QMessageBox.information(self.MainWindow, "Thành công", "Thêm người dùng thành công!")
                self.accept()
            else:
                QMessageBox.critical(self.MainWindow, "Lỗi", "Không thể thêm người dùng.")

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi: {e}")

    def cancel(self):
        self.close()