"""
Complete UI Test Launcher
Launch all screens for testing the redesigned UI
Run: py -m final_ml.test.test_all_screens
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFrame, QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AllScreensLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fruit ML - Complete UI Test Launcher")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Header
        title = QLabel("🍎 Fruit ML - UI Test Launcher")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2D7A4E; padding: 20px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Kiểm tra toàn bộ giao diện đã được redesign với minimalist green theme")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #5A7A6A; padding-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # User Screens Section
        user_section = self.create_section("👤 USER SCREENS", [
            ("🔐 Login / Sign Up", self.launch_login),
            ("📤 Upload Image", self.launch_upload),
            ("📊 Result Display", self.launch_result),
            ("📜 History & Settings", self.launch_history),
        ])
        layout.addWidget(user_section)
        
        # Admin Screens Section
        admin_section = self.create_section("👨‍💼 ADMIN SCREENS", [
            ("📈 Admin Dashboard", self.launch_admin_dashboard),
            ("👥 User Management", self.launch_user_management),
            ("🗂️ Data Management", self.launch_data_management),
            ("🤖 Model Management", self.launch_model_management),
        ])
        layout.addWidget(admin_section)
        
        # Footer
        footer = QLabel("Tất cả màn hình đã áp dụng design system mới")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #8B9D94; font-size: 10px; padding-top: 20px;")
        layout.addWidget(footer)
        
        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            QFrame.section {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #E0E7E4;
            }
            QLabel.sectionTitle {
                font-size: 14px;
                font-weight: 600;
                color: #2D7A4E;
                padding-bottom: 10px;
            }
            QPushButton {
                background-color: #2D7A4E;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: 600;
                text-align: left;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #246A3F;
            }
            QPushButton:pressed {
                background-color: #1E5A35;
            }
        """)
    
    def create_section(self, title, buttons_data):
        """Create a section with title and buttons"""
        section = QFrame()
        section.setObjectName("section")
        section.setProperty("class", "section")
        
        layout = QVBoxLayout(section)
        layout.setSpacing(12)
        
        # Section title
        title_label = QLabel(title)
        title_label.setProperty("class", "sectionTitle")
        layout.addWidget(title_label)
        
        # Buttons grid
        grid = QGridLayout()
        grid.setSpacing(12)
        
        for i, (btn_text, btn_action) in enumerate(buttons_data):
            btn = QPushButton(btn_text)
            btn.clicked.connect(btn_action)
            row = i // 2
            col = i % 2
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        
        return section
    
    def launch_login(self):
        self.launch_screen("login")
    
    def launch_upload(self):
        self.launch_screen("upload")
    
    def launch_result(self):
        self.launch_screen("result")
    
    def launch_history(self):
        self.launch_screen("history")
    
    def launch_admin_dashboard(self):
        self.launch_screen("admin_dashboard")
    
    def launch_user_management(self):
        self.launch_screen("user_management")
    
    def launch_data_management(self):
        self.launch_screen("data_management")
    
    def launch_model_management(self):
        self.launch_screen("model_management")
    
    def launch_screen(self, screen_name):
        """Launch a specific screen"""
        try:
            from PyQt6.QtWidgets import QMainWindow
            
            window = QMainWindow()
            
            if screen_name == "login":
                from final_ml.ui.ui_login_signupExt import ui_login_signupExt
                ui = ui_login_signupExt()
                
            elif screen_name == "upload":
                from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt
                mock_user = {'user_id': 1, 'full_name': 'Test User', 'role': 'user'}
                ui = ui_upload_imageExt(mock_user)
                
            elif screen_name == "result":
                from final_ml.ui.ui_resultExt import ui_resultExt
                mock_user = {'user_id': 1, 'full_name': 'Test User'}
                mock_result = {
                    'image_path': '',
                    'fruit_type': 'Apple',
                    'quality': 'Good',
                    'confidence': 95.5
                }
                ui = ui_resultExt(mock_user, mock_result)
                
            elif screen_name == "history":
                from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt
                mock_user = {'user_id': 1, 'full_name': 'Test User', 'email': 'test@fruit.com'}
                ui = ui_history_settingsExt(mock_user)
                
            elif screen_name == "admin_dashboard":
                from final_ml.ui.ui_admin_dashboardExt import ui_admin_dashboardExt
                mock_admin = {'user_id': 1, 'full_name': 'Admin', 'role': 'admin'}
                ui = ui_admin_dashboardExt(mock_admin)
                
            elif screen_name == "user_management":
                from final_ml.ui.ui_admin_user_managementExt import ui_admin_user_managementExt
                ui = ui_admin_user_managementExt()
                
            elif screen_name == "data_management":
                from final_ml.ui.ui_admin_data_managementExt import ui_admin_data_managementExt
                mock_admin = {'user_id': 1, 'full_name': 'Admin', 'role': 'admin'}
                ui = ui_admin_data_managementExt(mock_admin)
                
            elif screen_name == "model_management":
                from final_ml.ui.ui_admin_model_managementExt import ui_admin_model_managementExt
                mock_admin = {'user_id': 1, 'full_name': 'Admin', 'role': 'admin'}
                ui = ui_admin_model_managementExt(mock_admin)
            
            ui.setupUi(window)
            window.show()
            
            # Store window reference to prevent garbage collection
            if not hasattr(self, 'windows'):
                self.windows = []
            self.windows.append(window)
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Lỗi", f"Không thể mở màn hình {screen_name}:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    launcher = AllScreensLauncher()
    launcher.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
