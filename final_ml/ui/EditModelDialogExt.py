import os
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog
from PyQt6.QtCore import QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.EditModelDialog import Ui_Dialog
import qtawesome as qta


class EditModelDialogExt(QDialog, Ui_Dialog):
    def __init__(self,current_user,model_id):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user
        self.model_id = model_id

        self.setupUi(self)

        self.load_model_data()

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
            file_name = os.path.basename(file_path)
            dest_dir = "../../train_ml_result"
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, file_name)
            dest_path = dest_path.replace("\\", "/")
            if not os.path.exists(dest_path):
                with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())
            self.lineEditPath.setText(dest_path)

    def load_model_data(self):
        self.mc.connect()
        sql = "SELECT model_name, accuracy, file_path, created_at FROM models WHERE model_id=%s"
        model = self.mc.fetchone(sql, (self.model_id,))
        if model:
            self.lineEditName.setText(model[0])
            self.lineEditAccuracy.setText(str(model[1]))
            self.lineEditPath.setText(model[2])
            self.lineEditCreatedAt.setText(str(model[3]))
            self.lineEditCreatedAt.setReadOnly(True)

    def save_model(self):
        name = self.lineEditName.text().strip()
        accuracy = self.lineEditAccuracy.text().strip()
        file_path = self.lineEditPath.text().strip()

        if not name or not accuracy or not file_path:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            accuracy = float(accuracy) if accuracy else None
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Độ chính xác phải là số.")
            return

        try:
            self.mc.connect()
            sql = """UPDATE models
                     SET model_name=%s, accuracy=%s, file_path=%s
                     WHERE model_id=%s"""
            val = (name, accuracy, file_path, self.model_id)
            result = self.mc.insert_one(sql, val)
            if result > 0:
                QMessageBox.information(self, "Thành công", "Cập nhật model thành công!")
                self.accept()
            else:
                QMessageBox.warning(self, "Không thay đổi", "Không có thay đổi nào được lưu.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu: {e}")
