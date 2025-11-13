from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_result import Ui_MainWindow_Result
from datetime import datetime
import qtawesome as qta


class ui_resultExt(Ui_MainWindow_Result):
    def __init__(self, current_user, image_path, prediction_result):
        """
        Khởi tạo màn hình kết quả
        
        Args:
            current_user: thông tin user hiện tại
            image_path: đường dẫn ảnh đã upload
            prediction_result: dict chứa kết quả dự đoán {
                'fruit_type': str,
                'quality': str,
                'confidence': float,
                'model_name': str,
                'product_id': str (optional)
            }
        """
        super().__init__()
        self.current_user = current_user
        self.image_path = image_path
        self.prediction_result = prediction_result
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium stylesheet
        self.apply_premium_style()
        self.add_premium_icons()
        
        MainWindow.setWindowTitle("🍃 Fruit ML - Classification Result")
        MainWindow.resize(900, 700)
        
        self.display_result()
        self.setupSignalAndSlot()
    
    def apply_premium_style(self):
        """Apply premium result screen stylesheet"""
        self.MainWindow.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 42px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton#btnTryAgain {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #6C757D, stop:1 #8B95A0);
            }
            
            QPushButton#btnTryAgain:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5A6268, stop:1 #6C757D);
            }
            
            QLabel {
                background-color: transparent;
                font-size: 14px;
                color: #2C3E50;
            }
            
            QLabel#labelResultTitle {
                font-size: 24px;
                font-weight: bold;
                color: #2D7A4E;
            }
            
            QLabel#labelFruitType, QLabel#labelQuality, 
            QLabel#labelConfidence, QLabel#labelModel {
                font-size: 16px;
                font-weight: 600;
                color: #1E5A32;
            }
            
            QLabel#labelResultImage {
                background-color: white;
                border: 3px solid #E0E7E4;
                border-radius: 16px;
                padding: 10px;
            }
            
            QGroupBox {
                background-color: white;
                border: 2px solid #E0E7E4;
                border-radius: 12px;
                padding: 16px;
                margin-top: 12px;
                font-weight: 600;
                font-size: 14px;
                color: #2D7A4E;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 4px 12px;
                background-color: white;
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to buttons"""
        try:
            if hasattr(self, 'btnSaveHistory'):
                icon = qta.icon('fa5s.save', color='white', scale_factor=1.2)
                self.btnSaveHistory.setIcon(icon)
                self.btnSaveHistory.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnTryAgain'):
                icon = qta.icon('fa5s.redo', color='white', scale_factor=1.2)
                self.btnTryAgain.setIcon(icon)
                self.btnTryAgain.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnBackDashboard'):
                icon = qta.icon('fa5s.home', color='white', scale_factor=1.2)
                self.btnBackDashboard.setIcon(icon)
                self.btnBackDashboard.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

    def setupSignalAndSlot(self):
        """Thiết lập các sự kiện cho các nút"""
        self.btnBackDashboard.clicked.connect(self.back_to_dashboard)
        self.btnTryAgain.clicked.connect(self.try_again)
        self.btnSaveHistory.clicked.connect(self.save_to_history)

    def display_result(self):
        """Hiển thị kết quả dự đoán"""
        # Hiển thị ảnh
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.labelResultImage.setPixmap(pixmap)
        else:
            self.labelResultImage.setText("Không thể tải ảnh")

        # Hiển thị thông tin kết quả
        fruit_type = self.prediction_result.get('fruit_type', 'N/A')
        quality = self.prediction_result.get('quality', 'N/A')
        self.lblResult.setText(f"{fruit_type} - {quality}")
        self.lblResult.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2b6a4b;")
        
        confidence = self.prediction_result.get('confidence', 0)
        self.lblConfidence.setText(f"{confidence:.2f}%")
        
        model_name = self.prediction_result.get('model_name', 'N/A')
        self.lblModelUsed.setText(model_name)
        
        product_id = self.prediction_result.get('product_id', 'N/A')
        self.lblProductId.setText(product_id)

    def save_to_history(self):
        """Lưu kết quả dự đoán vào database"""
        try:
            self.mc.connect()
            
            # Lưu thông tin upload
            import os
            filename = os.path.basename(self.image_path)
            ext = os.path.splitext(filename)[1]
            
            sql_upload = """INSERT INTO Uploads (user_id, image_url, image_extension, upload_date)
                           VALUES (%s, %s, %s, %s)"""
            upload_id = self.mc.insert_one(sql_upload, 
                (self.current_user['user_id'], self.image_path, ext, datetime.now()))
            
            # Lưu kết quả dự đoán
            sql_prediction = """INSERT INTO Predictions 
                               (upload_id, model_id, fruit_type, quality_label, confidence, predicted_at)
                               VALUES (%s, %s, %s, %s, %s, %s)"""
            
            # Lấy model_id (giả sử có trong prediction_result hoặc lấy từ tên model)
            model_id = self.prediction_result.get('model_id', 1)  # default 1
            
            self.mc.insert_one(sql_prediction, 
                (upload_id, model_id, 
                 self.prediction_result.get('fruit_type', ''),
                 self.prediction_result.get('quality', ''),
                 self.prediction_result.get('confidence', 0.0),
                 datetime.now()))
            
            QMessageBox.information(self.MainWindow, "Thành công", 
                                   "Kết quả đã được lưu vào lịch sử!")
            self.btnSaveHistory.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", 
                               f"Lỗi khi lưu vào lịch sử: {e}")

    def back_to_dashboard(self):
        """Quay về màn hình upload/dashboard"""
        from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt
        from PyQt6.QtWidgets import QMainWindow
        
        self.upload_window = QMainWindow()
        self.ui_upload = ui_upload_imageExt(self.current_user)
        self.ui_upload.setupUi(self.upload_window)
        self.upload_window.show()
        self.MainWindow.close()

    def try_again(self):
        """Thử lại - quay về màn hình upload"""
        self.back_to_dashboard()
