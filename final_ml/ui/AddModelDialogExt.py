from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog
from PyQt6.QtCore import QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddModelDialog import Ui_Dialog
import qtawesome as qta


class AddModelDialogExt(QDialog, Ui_Dialog):
    def __init__(self,current_user):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user
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
            
            QLineEdit, QComboBox, QTextEdit {
                border: 2px solid #E0E7E4;
                border-radius: 8px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-height: 18px;
            }
            
            QLineEdit:hover, QComboBox:hover, QTextEdit:hover {
                border-color: #4A9D6E;
            }
            
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
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
        self.btnSave.clicked.connect(self.save_model)
        self.btnCancel.clicked.connect(self.reject)
        self.lineEditPath.mousePressEvent = self.choose_file

    def choose_file(self, event):
        # Chọn file
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file mô hình", "", "All Files (*)")
        if file_path:
            self.lineEditPath.setText(file_path)

    def save_model(self):
        name = self.lineEditName.text().strip()
        accuracy_text = self.lineEditAccuracy.text().strip()
        path = self.lineEditPath.text().strip()

        if not name or not path:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền tên và đường dẫn.")
            return

        # Chuyển độ chính xác sang float
        try:
            accuracy = float(accuracy_text) if accuracy_text else None
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Độ chính xác phải là số.")
            return

        created_at = datetime.now()
        created_by = self.current_user['user_id']  # ID admin hiện tại

        try:
            self.mc.connect()
            sql = """
                        INSERT INTO models (model_name, accuracy, file_path, created_at, created_by)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            val = (name, accuracy, path, created_at, created_by)
            result = self.mc.insert_one(sql, val)
            if result > 0:
                QMessageBox.information(self, "Thành công", "Thêm mô hình thành công!")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể thêm mô hình.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Lỗi: {e}")