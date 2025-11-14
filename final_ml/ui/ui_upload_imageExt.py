import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize
from final_ml.connector.ml_connector import FinalConnector
from datetime import datetime
import qtawesome as qta

from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt
from final_ml.ui.ui_resultExt import ui_resultExt


class ui_upload_imageExt(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()
        
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
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

        # Predict button with icon
        self.btn_predict = QPushButton("  Dự đoán")
        self.btn_predict.setObjectName("btnPredict")
        self.btn_predict.setMinimumHeight(55)
        try:
            predict_icon = qta.icon('fa5s.robot', color='white', scale_factor=1.3)
            self.btn_predict.setIcon(predict_icon)
            self.btn_predict.setIconSize(QSize(22, 22))
        except:
            pass
        layout.addWidget(self.btn_predict)

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
        self.tbl_upload = QTableWidget()
        self.tbl_upload.setObjectName("premiumTable")
        self.tbl_upload.setColumnCount(3)
        self.tbl_upload.setHorizontalHeaderLabels(["🖼️ Ảnh", "Đuôi ảnh", "🕐 Ngày upload"])
        layout.addWidget(self.tbl_upload)

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

        self.load_all_upload_image()
        # Gán sự kiện
        self.btn_upload.clicked.connect(self.upload_image)
        self.btn_history.clicked.connect(self.open_history)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_predict.clicked.connect(self.open_predict)
        self.tbl_upload.itemSelectionChanged.connect(self.choose_img_to_predict)

        MainWindow.setCentralWidget(self.central_widget)

    def load_all_upload_image(self):
        #print(self.current_user)
        try:
            self.mc.connect()
            sql = """SELECT u.image_url, u.image_extension, u.upload_date
                     FROM Uploads u
                     WHERE u.user_id = %s
                     ORDER BY u.upload_date DESC"""
            data = self.mc.fetchall(sql, (self.current_user['user_id'],))
            #print(data)
            self.tbl_upload.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tbl_upload.insertRow(row_num)
                for col_num, col_value in enumerate(row_data):
                    self.tbl_upload.setItem(row_num, col_num, QTableWidgetItem(str(col_value)))
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi tải lịch sử: {e}")

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Chọn ảnh trái cây", "", "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return

        try:
            self.mc.connect()
            file_name = os.path.basename(file_path)
            dest_dir = "../uploads"
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, file_name)
            dest_path = dest_path.replace("\\", "/")
            if not os.path.exists(dest_path):
                with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())

            sql = """INSERT INTO uploads (user_id, image_url, image_extension, upload_date)
                                 VALUES (%s, %s, %s, %s)"""
            ext = os.path.splitext(file_name)[1]
            uid = self.current_user['user_id']
            self.mc.insert_one(sql, (uid, dest_path, ext, datetime.now()))

            #Lưu đường dẫn hình vừa upload để dự đoán
            self.image_path=dest_path

            QMessageBox.information(None, "Thành công", f"Ảnh {file_name} đã được tải lên thành công!")
            self.load_all_upload_image()

        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi tải ảnh: {e}")

    def choose_img_to_predict(self):
        try:
            row = self.tbl_upload.currentRow()
            if row == -1:
                return

            # Cột chứa đường dẫn ảnh
            image_item = self.tbl_upload.item(row, 0)

            if not image_item:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Không lấy được đường dẫn ảnh từ bảng!")
                return

            image_path = image_item.text()

            if not os.path.exists(image_path):
                QMessageBox.warning(self.MainWindow, "Lỗi", f"Ảnh không tồn tại:\n{image_path}")
                return

            # Lưu lại để dùng cho Predict
            self.image_path = image_path

            QMessageBox.information(
                self.MainWindow,
                "Thành công",
                f"Đã chọn ảnh để dự đoán:\n{os.path.basename(image_path)}"
            )

        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Lỗi chọn ảnh", str(e))

    def open_predict(self):
        if not hasattr(self, "image_path"):
            QMessageBox.warning(self, "Thông báo", "Vui lòng upload ảnh trước!")
            return
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_resultExt(self.current_user,self.image_path)
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def open_history(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_history_settingsExt(self.current_user)
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def logout(self):
        """Đăng xuất khỏi hệ thống và quay lại màn hình đăng nhập"""
        from PyQt6.QtWidgets import QMainWindow
        from final_ml.ui.ui_login_signupExt import ui_login_signupExt

        # Hộp thoại xác nhận
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        # Nếu người dùng chọn "No" → hủy đăng xuất
        if reply == QMessageBox.StandardButton.No:
            return

        # Nếu chọn Yes thì tiếp tục
        QMessageBox.information(self.MainWindow, "Đăng xuất", "Bạn đã đăng xuất khỏi hệ thống.")

        self.window = QMainWindow()
        self.ui = ui_login_signupExt()
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

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
            
            /* Predict Button */
            QPushButton#btnPredict {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1565C0, stop:1 #1E88E5);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 28px;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.3px;
                box-shadow: 0px 4px 10px rgba(21, 101, 192, 0.3);
            }
            
            QPushButton#btnPredict:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0D47A1, stop:1 #1565C0);
                box-shadow: 0px 6px 14px rgba(21, 101, 192, 0.45);
            }
            
            QPushButton#btnPredict:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0B3C91, stop:1 #0D47A1);
                box-shadow: inset 0px 3px 8px rgba(0, 0, 0, 0.2);
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