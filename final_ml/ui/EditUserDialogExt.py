from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.EditUserDialog import Ui_Dialog
import qtawesome as qta


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
        
        # Apply premium dialog style
        self.apply_premium_style()
        self.add_premium_icons()
        
        self.setupSignalAndSlot()
    
    def apply_premium_style(self):
        """Apply premium dialog stylesheet"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton#btnCancel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #6C757D, stop:1 #8B95A0);
            }
            
            QPushButton#btnCancel:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5A6268, stop:1 #6C757D);
            }
            
            QLineEdit, QComboBox {
                border: 2px solid #E0E7E4;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-height: 18px;
            }
            
            QLineEdit:hover, QComboBox:hover {
                border-color: #4A9D6E;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border-color: #2D7A4E;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E0E7E4;
                border-radius: 8px;
                selection-background-color: #E8F5E9;
                selection-color: #2D7A4E;
                color: #2D7A4E;
                padding: 4px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-radius: 4px;
                color: #2D7A4E;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F5E9;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 13px;
                font-weight: 500;
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to buttons"""
        try:
            if hasattr(self, 'btnSave'):
                icon = qta.icon('fa5s.save', color='white', scale_factor=1.1)
                self.btnSave.setIcon(icon)
                self.btnSave.setIconSize(QSize(16, 16))
            
            if hasattr(self, 'btnCancel'):
                icon = qta.icon('fa5s.times-circle', color='white', scale_factor=1.1)
                self.btnCancel.setIcon(icon)
                self.btnCancel.setIconSize(QSize(16, 16))
        except Exception as e:
            print(f"Could not add icons: {e}")

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
