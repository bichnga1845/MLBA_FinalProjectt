from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from final_ml.connector.ml_connector import FinalConnector


class ui_admin_dashboardExt(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("🍃 Fruit ML - Admin Dashboard")
        MainWindow.resize(800, 600)

        self.central_widget = QWidget(MainWindow)
        layout = QVBoxLayout(self.central_widget)

        lbl_title = QLabel(f"👩‍💻 Xin chào, {self.current_user['full_name']} (Admin)")
        lbl_title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2b6a4b;")
        layout.addWidget(lbl_title)

        lbl_intro = QLabel("Trang quản trị hệ thống Fruit ML.\n"
                           "Bạn có thể quản lý mô hình, dữ liệu, người dùng và xem thống kê.")
        lbl_intro.setStyleSheet("font-size: 12pt; color: #333;")
        layout.addWidget(lbl_intro)

        # Các nút điều hướng
        self.btn_models = QPushButton("📊 Quản lý mô hình")
        self.btn_datasets = QPushButton("🗂️ Quản lý bộ dữ liệu")
        self.btn_users = QPushButton("👥 Quản lý người dùng")
        self.btn_stats = QPushButton("📈 Xem thống kê")
        self.btn_logout = QPushButton("🚪 Đăng xuất")

        for btn in [self.btn_models, self.btn_datasets, self.btn_users, self.btn_stats, self.btn_logout]:
            btn.setStyleSheet("padding: 8px; font-size: 12pt; background: #cfe8d6; border-radius: 6px;")
            layout.addWidget(btn)

        # Gán sự kiện
        self.btn_logout.clicked.connect(self.logout)
        self.btn_stats.clicked.connect(self.show_statistics)

        MainWindow.setCentralWidget(self.central_widget)

    def logout(self):
        QMessageBox.information(None, "Đăng xuất", "Bạn đã đăng xuất khỏi hệ thống.")
        from final_ml.ui.ui_login_signupExt import ui_login_signupExt
        from PyQt6.QtWidgets import QMainWindow
        self.login_window = QMainWindow()
        self.ui_login = ui_login_signupExt()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()
        self.parentWidget().close()

    def show_statistics(self):
        try:
            self.mc.connect()
            sql = "SELECT COUNT(*) FROM Users WHERE role='user';"
            total_users = self.mc.fetchone(sql, ())[0]

            sql2 = "SELECT COUNT(*) FROM Uploads;"
            total_uploads = self.mc.fetchone(sql2, ())[0] if self.mc.fetchone(sql2, ()) else 0

            msg = f"Tổng số người dùng: {total_users}\nTổng số lượt upload: {total_uploads}"
            QMessageBox.information(None, "📈 Thống kê hệ thống", msg)
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi truy xuất thống kê: {e}")
