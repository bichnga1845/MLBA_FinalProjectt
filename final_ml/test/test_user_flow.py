"""
File test để chạy thử toàn bộ flow User: Login -> Upload -> Result -> History
Chạy từ thư mục gốc dự án: py -m final_ml.test.test_user_flow
"""
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt


class UserFlowTestLauncher(QWidget):
    """Menu launcher để test các màn hình user"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" User Flow Test Launcher")
        self.resize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(" Chọn màn hình để test")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2b6a4b;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Các nút test
        btn_login = QPushButton(" Test Login & Signup")
        btn_login.clicked.connect(self.launch_login)
        layout.addWidget(btn_login)
        
        btn_upload = QPushButton(" Test Upload Image")
        btn_upload.clicked.connect(self.launch_upload)
        layout.addWidget(btn_upload)
        
        btn_result = QPushButton(" Test Result Screen")
        btn_result.clicked.connect(self.launch_result)
        layout.addWidget(btn_result)
        
        btn_history = QPushButton(" Test History & Settings")
        btn_history.clicked.connect(self.launch_history)
        layout.addWidget(btn_history)
        
        # Style
        button_style = """
            QPushButton {
                padding: 12px;
                font-size: 12pt;
                background: #cfe8d6;
                border-radius: 6px;
                text-align: left;
            }
            QPushButton:hover {
                background: #b2d4c0;
            }
        """
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setStyleSheet(button_style)
        
        self.setLayout(layout)
    
    def launch_login(self):
        """Mở màn hình Login"""
        from final_ml.ui.ui_login_signupExt import ui_login_signupExt
        self.login_window = QMainWindow()
        self.login_ui = ui_login_signupExt()
        self.login_ui.setupUi(self.login_window)
        self.login_window.show()
    
    def launch_upload(self):
        """Mở màn hình Upload Image"""
        from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt
        
        # Giả lập user đã đăng nhập
        mock_user = {
            'user_id': 1,
            'username': 'testuser',
            'full_name': 'Nguyễn Văn Test',
            'email': 'test@example.com',
            'role': 'user'
        }
        
        self.upload_window = QMainWindow()
        self.upload_ui = ui_upload_imageExt(current_user=mock_user)
        self.upload_ui.setupUi(self.upload_window)
        self.upload_window.show()
    
    def launch_result(self):
        """Mở màn hình Result"""
        from final_ml.ui.ui_resultExt import ui_resultExt
        import os
        
        # Giả lập user và kết quả
        mock_user = {
            'user_id': 1,
            'username': 'testuser',
            'full_name': 'Nguyễn Văn Test',
            'email': 'test@example.com',
            'role': 'user'
        }
        
        image_path = os.path.join(os.getcwd(), "final_ml", "uploads", "test_image.jpg")
        
        mock_prediction = {
            'fruit_type': 'Apple',
            'quality': 'Good',
            'confidence': 95.67,
            'model_name': 'MobileNetV2',
            'model_id': 1,
            'product_id': 'BATCH-2024-001'
        }
        
        self.result_window = QMainWindow()
        self.result_ui = ui_resultExt(
            current_user=mock_user,
            image_path=image_path,
            prediction_result=mock_prediction
        )
        self.result_ui.setupUi(self.result_window)
        self.result_window.show()
    
    def launch_history(self):
        """Mở màn hình History & Settings"""
        from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt
        
        # Giả lập user
        mock_user = {
            'user_id': 1,
            'username': 'testuser',
            'full_name': 'Nguyễn Văn Test',
            'email': 'test@example.com',
            'role': 'user'
        }
        
        self.history_window = QMainWindow()
        self.history_ui = ui_history_settingsExt(current_user=mock_user)
        self.history_ui.setupUi(self.history_window)
        self.history_window.show()


if __name__ == "__main__":
    app = QApplication([])
    
    # Tạo và hiển thị launcher
    launcher = UserFlowTestLauncher()
    launcher.show()
    
    # Chạy ứng dụng
    app.exec()
