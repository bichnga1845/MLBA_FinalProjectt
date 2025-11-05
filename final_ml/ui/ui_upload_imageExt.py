import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from final_ml.connector.ml_connector import FinalConnector
from datetime import datetime


class ui_upload_imageExt(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("🍎 Fruit ML - Upload Image")
        MainWindow.resize(800, 600)

        self.central_widget = QWidget(MainWindow)
        layout = QVBoxLayout(self.central_widget)

        lbl_title = QLabel(f"🍃 Xin chào, {self.current_user['full_name']} (User)")
        lbl_title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2b6a4b;")
        layout.addWidget(lbl_title)

        lbl_intro = QLabel("Tải ảnh trái cây của bạn lên để hệ thống nhận dạng và phân loại chất lượng.")
        lbl_intro.setStyleSheet("font-size: 12pt; color: #333;")
        layout.addWidget(lbl_intro)

        self.btn_upload = QPushButton("📤 Tải ảnh lên")
        self.btn_upload.setStyleSheet("padding: 10px; font-size: 12pt; background: #cfe8d6; border-radius: 6px;")
        layout.addWidget(self.btn_upload)

        self.btn_history = QPushButton("🕓 Xem lịch sử dự đoán")
        self.btn_history.setStyleSheet("padding: 10px; font-size: 12pt; background: #cfe8d6; border-radius: 6px;")
        layout.addWidget(self.btn_history)

        self.tbl_history = QTableWidget()
        self.tbl_history.setColumnCount(5)
        self.tbl_history.setHorizontalHeaderLabels(["Ảnh", "Loại quả", "Chất lượng", "Độ tin cậy", "Thời gian"])
        layout.addWidget(self.tbl_history)

        self.btn_logout = QPushButton("🚪 Đăng xuất")
        self.btn_logout.setStyleSheet("padding: 8px; font-size: 12pt; background: #e8cfcf; border-radius: 6px;")
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
