from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_dashboard import Ui_MainWindow_AdminDashboard


class ui_admin_dashboardExt(Ui_MainWindow_AdminDashboard):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        pass

    def logout(self):
        QMessageBox.information(None, "Đăng xuất", "Bạn đã đăng xuất khỏi hệ thống.")
        from final_ml.ui.ui_login_signupExt import ui_login_signupExt
        from PyQt6.QtWidgets import QMainWindow
        self.login_window = QMainWindow()
        self.ui_login = ui_login_signupExt()
        self.ui_login.setupUi(self.login_window)
        self.login_window.show()

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
