from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddUserDialog import Ui_Dialog
import qtawesome as qta


class AddUserDialogExt(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()
        self.setupUi(self)

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