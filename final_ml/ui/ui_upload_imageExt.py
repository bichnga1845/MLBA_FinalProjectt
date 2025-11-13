import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize
from final_ml.connector.ml_connector import FinalConnector
from datetime import datetime
import qtawesome as qta


class ui_upload_imageExt(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()
        
    def setupUi(self, MainWindow):
        # Apply premium stylesheet
        self.apply_premium_style(MainWindow)
        MainWindow.setWindowTitle("🍎 Fruit ML - Upload & Classify")
        MainWindow.resize(1000, 700)

        self.central_widget = QWidget(MainWindow)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Header with premium styling
        lbl_title = QLabel(f"👋 Xin chào, {self.current_user['full_name']}")
        lbl_title.setObjectName("pageTitle")
        layout.addWidget(lbl_title)

        lbl_intro = QLabel("📤 Tải ảnh trái cây lên để hệ thống AI phân tích và phân loại chất lượng")
        lbl_intro.setObjectName("pageSubtitle")
        lbl_intro.setWordWrap(True)
        layout.addWidget(lbl_intro)

        # Upload button with icon
        self.btn_upload = QPushButton("  Tải ảnh lên")
        self.btn_upload.setObjectName("btnPrimary")
        self.btn_upload.setMinimumHeight(55)
        try:
            upload_icon = qta.icon('fa5s.cloud-upload-alt', color='white', scale_factor=1.3)
            self.btn_upload.setIcon(upload_icon)
            self.btn_upload.setIconSize(QSize(22, 22))
        except:
            pass
        layout.addWidget(self.btn_upload)

        # History button with icon
        self.btn_history = QPushButton("  Xem lịch sử dự đoán")
        self.btn_history.setObjectName("btnSecondary")
        self.btn_history.setMinimumHeight(50)
        try:
            history_icon = qta.icon('fa5s.history', color='#2D7A4E', scale_factor=1.2)
            self.btn_history.setIcon(history_icon)
            self.btn_history.setIconSize(QSize(20, 20))
        except:
            pass
        layout.addWidget(self.btn_history)

        # Table with premium styling
        self.tbl_history = QTableWidget()
        self.tbl_history.setObjectName("premiumTable")
        self.tbl_history.setColumnCount(5)
        self.tbl_history.setHorizontalHeaderLabels(["🖼️ Ảnh", "🍎 Loại quả", "⭐ Chất lượng", "📊 Độ tin cậy", "🕐 Thời gian"])
        layout.addWidget(self.tbl_history)

        # Logout button with icon
        self.btn_logout = QPushButton("  Đăng xuất")
        self.btn_logout.setObjectName("btnDanger")
        self.btn_logout.setMinimumHeight(45)
        try:
            logout_icon = qta.icon('fa5s.sign-out-alt', color='white', scale_factor=1.2)
            self.btn_logout.setIcon(logout_icon)
            self.btn_logout.setIconSize(QSize(18, 18))
        except:
            pass
        layout.addWidget(self.btn_logout)

        # Gán sự kiện
        self.btn_upload.clicked.connect(self.upload_image)
        self.btn_history.clicked.connect(self.load_history)
        self.btn_logout.clicked.connect(self.logout)

        MainWindow.setCentralWidget(self.central_widget)

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Chọn ảnh trái cây", "", "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return

        try:
            self.mc.connect()
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1]
            sql = """INSERT INTO Uploads (user_id, image_url, image_extension, upload_date)
                     VALUES (%s, %s, %s, %s)"""
            self.mc.insert_one(sql, (self.current_user['user_id'], file_path, ext, datetime.now()))

            QMessageBox.information(None, "Thành công", f"Ảnh {filename} đã được tải lên thành công!")
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi tải ảnh: {e}")

    def load_history(self):
        try:
            self.mc.connect()
            sql = """SELECT image_url, fruit_type, quality_label, confidence, predicted_at
                     FROM Predictions p
                     JOIN Uploads u ON p.upload_id = u.upload_id
                     WHERE u.user_id = %s"""
            data = self.mc.fetchall(sql, (self.current_user['user_id'],))
            self.tbl_history.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tbl_history.insertRow(row_num)
                for col_num, col_value in enumerate(row_data):
                    self.tbl_history.setItem(row_num, col_num, QTableWidgetItem(str(col_value)))
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi tải lịch sử: {e}")

    def logout(self):
        QMessageBox.information(None, "Đăng xuất", "Bạn đã đăng xuất khỏi hệ thống.")
        from final_ml.ui.ui_login_signupExt import ui_login_signupExt
        from PyQt6.QtWidgets import QMainWindow
        self.login_window = QMainWindow()
        self.ui_login = ui_login_signupExt()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()
        self.parentWidget().close()
    
    def apply_premium_style(self, widget):
        """Apply ultra premium stylesheet"""
        widget.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            /* Page Title */
            QLabel#pageTitle {
                font-size: 28px;
                font-weight: 700;
                color: #2D7A4E;
                letter-spacing: -0.5px;
            }
            
            QLabel#pageSubtitle {
                font-size: 15px;
                color: #5A7A6A;
                font-weight: 500;
            }
            
            /* Premium Primary Button */
            QPushButton#btnPrimary {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 28px;
                font-size: 16px;
                font-weight: 600;
            }
            
            QPushButton#btnPrimary:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton#btnPrimary:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E5A35, stop:1 #246A3F);
            }
            
            /* Secondary Button */
            QPushButton#btnSecondary {
                background: white;
                color: #2D7A4E;
                border: 2px solid #2D7A4E;
                border-radius: 12px;
                padding: 14px 26px;
                font-size: 15px;
                font-weight: 600;
            }
            
            QPushButton#btnSecondary:hover {
                background: #E8F5E9;
                border-color: #4A9D6E;
            }
            
            /* Danger Button */
            QPushButton#btnDanger {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #E53935, stop:1 #EF5350);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 600;
            }
            
            QPushButton#btnDanger:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #C62828, stop:1 #E53935);
            }
            
            /* Premium Table */
            QTableWidget#premiumTable {
                background-color: white;
                border: none;
                border-radius: 14px;
                gridline-color: #F0F4F2;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.2);
                padding: 16px 14px;
                font-weight: 600;
                font-size: 14px;
            }
            
            QTableWidget::item {
                padding: 14px 12px;
                border-bottom: 1px solid #F0F4F2;
                font-size: 13px;
            }
            
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #2D7A4E;
            }
            
            QTableWidget::item:hover {
                background-color: rgba(45, 122, 78, 0.05);
            }
            
            /* Scrollbar */
            QScrollBar:vertical {
                background-color: #F8FAF9;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #246A3F;
            }
        """)
