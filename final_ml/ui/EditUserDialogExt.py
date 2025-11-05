from PyQt6.QtWidgets import QMessageBox, QDialog

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.EditUserDialog import Ui_Dialog


class EditUserDialogExt(QDialog, Ui_Dialog):
    def __init__(self,user_id):
        super().__init__()
        self.mc = FinalConnector()
        self.user_id = user_id
        self.setupUi(self)
        self.load_user_data()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.save_user)
        self.btnCancel.clicked.connect(self.reject)

    def load_user_data(self):
        try:
            self.mc.connect()
            sql = "SELECT full_name, email, password, role FROM users WHERE user_id = %s"
            user = self.mc.fetchone(sql, (self.user_id,))
            if user:
                self.lineEditName.setText(user[0])
                self.lineEditEmail.setText(user[1])
                self.lineEditPassword.setText(user[2])
                self.comboRole.setCurrentText(user[3].capitalize())
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Không tải được thông tin: {e}")

    def save_user(self):
        name = self.lineEditName.text().strip()
        email = self.lineEditEmail.text().strip()
        password = self.lineEditPassword.text().strip()
        role = self.comboRole.currentText()

        if not name or not email or not password:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            self.mc.connect()

            # Lấy role hiện tại trong database
            sql_get_role = "SELECT role FROM users WHERE user_id = %s"
            current_role = self.mc.fetchone(sql_get_role, (self.user_id,))
            old_role = current_role[0] if current_role else None

            # Cập nhật user
            sql = """UPDATE users
                     SET full_name=%s, email=%s, password=%s, role=%s
                     WHERE user_id=%s"""
            val = (name, email, password, role, self.user_id)
            result = self.mc.insert_one(sql, val)

            # Nếu role thay đổi thì cập nhật bảng phụ tương ứng
            if old_role != role:
                if role.lower() == "admin":
                    # Xóa khỏi bảng NormalUsers nếu có
                    self.mc.insert_one("DELETE FROM NormalUsers WHERE normal_user_id=%s", (self.user_id,))
                    # Thêm vào bảng Admins
                    self.mc.insert_one(
                        "INSERT INTO Admins (admin_id, admin_level) VALUES (%s, 'super_admin')",
                        (self.user_id,)
                    )
                else:  # role == "user"
                    # Xóa khỏi bảng Admins nếu có
                    self.mc.insert_one("DELETE FROM Admins WHERE admin_id=%s", (self.user_id,))
                    # Thêm vào bảng NormalUsers
                    self.mc.insert_one(
                        "INSERT INTO NormalUsers (normal_user_id, organization) VALUES (%s, 'N/A')",
                        (self.user_id,)
                    )

            if result > 0:
                QMessageBox.information(self, "Thành công", "Cập nhật thông tin thành công!")
                self.accept()
            else:
                QMessageBox.warning(self, "Không thay đổi", "Không có thay đổi nào được lưu.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu: {e}")
