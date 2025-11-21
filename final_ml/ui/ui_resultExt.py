import random
from pathlib import Path

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_result import Ui_MainWindow_Result
from datetime import datetime
import qtawesome as qta


class ui_resultExt(Ui_MainWindow_Result):
    def __init__(self, current_user, image_path, up_img, prediction_result=None):
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
        self.upload_image_id = up_img
        self.prediction_result = prediction_result or self._mock_prediction_from_filename()
        self.mc = FinalConnector()
        # Preload the three supported models for selection in the result screen
        self.available_models = [
            {"id": "EfficientNetB0_Type_Quality", "name": "EfficientNetB0 Type & Quality"},
            {"id": "MobileNetV2_Quality", "name": "MobileNetV2 Quality"},
            {"id": "MobileNetV2_Type", "name": "MobileNetV2 Type"},
        ]

    def _mock_prediction_from_filename(self):
        """Generate a fake prediction based on image filename."""
        stem = Path(self.image_path).stem.lower() if self.image_path else ""
        fruit_map = {
            "banana": "Banana",
            "apple": "Apple",
            "orange": "Orange",
            "mango": "Mango",
            "grape": "Grape",
            "watermelon": "Watermelon",
            "guava": "Guava",
            "pear": "Pear",
            "lime": "Lime",
        }
        fruit = "Fruit"
        for key, value in fruit_map.items():
            if key in stem:
                fruit = value
                break

        if "good" in stem:
            quality = "Good"
        elif "bad" in stem:
            quality = "Bad"
        else:
            quality = random.choice(["Good", "Bad"])

        confidence = round(random.uniform(85, 95), 2)

        return {
            "fruit_type": fruit,
            "quality": quality,
            "confidence": confidence,
            "model_name": "...",
            "product_id": "",
        }

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium stylesheet
        self.apply_premium_style()
        self.add_premium_icons()
        
        MainWindow.setWindowTitle("🍃 Fruit ML - Classification Result")
        MainWindow.resize(900, 700)
        
        self.display_placeholder_results()
        self.populate_model_choices()
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
        """Thiết lập sự kiện cho các nút"""
        if hasattr(self, 'btnBackDashboard'):
            self.btnBackDashboard.clicked.connect(self.back_to_dashboard)
        if hasattr(self, 'btnTryAgain'):
            self.btnTryAgain.clicked.connect(self.try_again)
        if hasattr(self, 'btnSaveHistory'):
            self.btnSaveHistory.clicked.connect(self.save_to_history)
        if hasattr(self, 'btnLoadModel'):
            self.btnLoadModel.clicked.connect(self.load_selected_model)

    # def populate_model_choices(self):
    #     """Fill the combo box with available models."""
    #     if not hasattr(self, 'comboBoxModels'):
    #         return
    #     self.comboBoxModels.clear()
    #     for model in self.available_models:
    #         self.comboBoxModels.addItem(model["name"], model)

    #     # Try to align selection with current prediction result
    #     current_model_name = self.prediction_result.get("model_name")
    #     if current_model_name:
    #         idx = self.comboBoxModels.findText(current_model_name)
    #         if idx != -1:
    #             self.comboBoxModels.setCurrentIndex(idx)
    #             return
    #     self.comboBoxModels.setCurrentIndex(0)
    def populate_model_choices(self):
        if not hasattr(self, 'comboBoxModels'):
            return
        """Lấy danh sách model từ database và thêm vào comboBoxModels"""
        self.comboBoxModels.clear()
        has_remote_models = False

        try:
            conn = self.mc.connect()
            if conn:
                sql = "SELECT model_id, model_name FROM models ORDER BY created_at DESC"
                rows = self.mc.fetchall(sql, None) or []
                for model_id, model_name in rows:
                    metadata = {'source': 'db', 'model_id': model_id}
                    self.comboBoxModels.addItem(model_name, userData=metadata)
                has_remote_models = bool(rows)
        except Exception as e:
            QMessageBox.warning(
                self.MainWindow,
                "Kết nối cơ sở dữ liệu",
                f"Không thể tải danh sách model từ CSDL:\n{e}\n\n"
                "Danh sách model demo cục bộ sẽ được sử dụng."
            )
        finally:
            try:
                self.mc.disConnect()
            except Exception:
                pass
        """Fill the combo box with available models."""
        if not has_remote_models:
            for model in self.available_models:
                self.comboBoxModels.addItem(model["name"], model)

            # Try to align selection with current prediction result
            current_model_name = self.prediction_result.get("model_name")
            if current_model_name:
                idx = self.comboBoxModels.findText(current_model_name)
                if idx != -1:
                    self.comboBoxModels.setCurrentIndex(idx)
                    return
            self.comboBoxModels.setCurrentIndex(0)

    def _set_result_image(self):
        """Load and show the uploaded image if available."""
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.labelResultImage.setPixmap(pixmap)
        else:
            self.labelResultImage.setText("Không thể tải ảnh")

    def display_placeholder_results(self):
        """Show placeholders until a model is loaded."""
        self._set_result_image()
        self.lblResult.setText("...")
        self.lblConfidence.setText("...")
        self.lblModelUsed.setText("...")

    def display_result(self):
        """Hiển thị kết quả dự đoán"""
        self._set_result_image()

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
        if hasattr(self, "lblProductId"):
            self.lblProductId.setText(product_id)

    # def load_selected_model(self):
    #     """Update the displayed model name based on the selected combo box item."""
    #     if not hasattr(self, "comboBoxModels"):
    #         return

    #     model_data = self.comboBoxModels.currentData()
    #     model_name = model_data["name"] if model_data else self.comboBoxModels.currentText()
    #     self.prediction_result["model_name"] = model_name

    #     # After selecting a model, show the full prediction details
    #     self.display_result()
    #     QMessageBox.information(self.MainWindow, "Đã tải mô hình", f"Đang sử dụng mô hình: {model_name}")
    def load_selected_model(self):
        """Update the displayed model name based on the selected combo box item."""
        if not hasattr(self, "comboBoxModels"):
            return

        model_data = self.comboBoxModels.currentData()
        # Nếu là model từ database → dùng currentText() để lấy tên
        if model_data and model_data.get("source") == "db":
            model_name = self.comboBoxModels.currentText()
        else:
            model_name = model_data["name"] if model_data else self.comboBoxModels.currentText()

        self.prediction_result["model_name"] = model_name

        # After selecting a model, show the full prediction details
        self.display_result()
        QMessageBox.information(self.MainWindow, "Đã tải mô hình", f"Đang sử dụng mô hình: {model_name}")

    # def save_to_history(self):
    #     """Lưu kết quả dự đoán vào database"""
    #     try:
    #         self.mc.connect()
            
    #         # Lưu thông tin upload
    #         import os
    #         filename = os.path.basename(self.image_path)
    #         ext = os.path.splitext(filename)[1]
            
    #         sql_upload = """INSERT INTO Uploads (user_id, image_url, image_extension, upload_date)
    #                        VALUES (%s, %s, %s, %s)"""
    #         upload_id = self.mc.insert_one(sql_upload, 
    #             (self.current_user['user_id'], self.image_path, ext, datetime.now()))
            
    #         # Lưu kết quả dự đoán
    #         sql_prediction = """INSERT INTO Predictions 
    #                            (upload_id, model_id, fruit_type, quality_label, confidence, predicted_at)
    #                            VALUES (%s, %s, %s, %s, %s, %s)"""
            
    #         # Lấy model_id (giả sử có trong prediction_result hoặc lấy từ tên model)
    #         model_id = self.prediction_result.get('model_id', 1)  # default 1
            
    #         self.mc.insert_one(sql_prediction, 
    #             (upload_id, model_id, 
    #              self.prediction_result.get('fruit_type', ''),
    #              self.prediction_result.get('quality', ''),
    #              self.prediction_result.get('confidence', 0.0),
    #              datetime.now()))
            
    #         QMessageBox.information(self.MainWindow, "Thành công", 
    #                                "Kết quả đã được lưu vào lịch sử!")
    #         self.btnSaveHistory.setEnabled(False)
            
    #     except Exception as e:
    #         QMessageBox.critical(self.MainWindow, "Lỗi", 
    #                            f"Lỗi khi lưu vào lịch sử: {e}")
    def save_to_history(self):
        """Lưu kết quả dự đoán vào database"""
        try:
            self.mc.connect()

            # Lấy model_name hiện tại
            model_name = self.prediction_result.get('model_name')

            # Query model_id từ bảng models
            sql_model = "SELECT model_id FROM models WHERE model_name=%s"
            result = self.mc.fetchone(sql_model, (model_name,))
            if result:
                model_id = result[0]
            else:
                QMessageBox.warning(self.MainWindow, "Lỗi", f"Không tìm thấy model_id cho {model_name}")
                return

            # Lưu kết quả dự đoán
            sql_prediction = """INSERT INTO predictions 
                                        (upload_id, model_id, fruit_type, quality_label, confidence, predicted_at)
                                        VALUES (%s, %s, %s, %s, %s, %s)"""

            self.mc.insert_one(sql_prediction,
                               (self.upload_image_id, model_id,
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
