from PyQt6.QtWidgets import QMessageBox
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_dashboard import Ui_MainWindow_AdminDashboard
from final_ml.ui.ui_admin_data_managementExt import ui_admin_data_managementExt
from final_ml.ui.ui_admin_model_managementExt import ui_admin_model_managementExt
from final_ml.ui.ui_admin_user_managementExt import ui_admin_user_managementExt
from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt


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
        self.btnGoUserMgmt.clicked.connect(self.go_user_mgmt)
        self.btnGoDataMgmt.clicked.connect(self.go_data_mgmt)
        self.btnGoModelMgmt.clicked.connect(self.go_model_mgmt)
        self.btnGoHistory.clicked.connect(self.go_history_and_setting)
        self.btnGoStatistics.clicked.connect(self.show_statistics)
        self.btnLogout.clicked.connect(self.process_log_out)

    def go_user_mgmt(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_admin_user_managementExt()
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def go_data_mgmt(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_admin_data_managementExt()
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def go_model_mgmt(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_admin_model_managementExt()
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def go_history_and_setting(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_history_settingsExt()
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def show_statistics(self):
        try:
            self.mc.connect()
            sql = "SELECT COUNT(*) FROM Users WHERE role='user';"
            total_users = self.mc.fetchone(sql, ())[0]

            sql2 = "SELECT COUNT(*) FROM Uploads;"
            total_uploads = self.mc.fetchone(sql2, ())[0] #if self.mc.fetchone(sql2, ()) else 0

            msg = f"Tổng số người dùng (user): {total_users}\nTổng số lượt upload: {total_uploads}"
            QMessageBox.information(None, "Thống kê hệ thống", msg)
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi khi truy xuất thống kê: {e}")

    def process_log_out(self):
        confirmation = QMessageBox.question(None,
                                            "Đăng xuất",
                                            "Bạn có chắc muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmation == QMessageBox.StandardButton.Yes:
            self.current_user=None

            from final_ml.ui.ui_login_signupExt import ui_login_signupExt
            from PyQt6.QtWidgets import QMainWindow
            self.window = QMainWindow()
            self.ui = ui_login_signupExt()
            self.ui.setupUi(self.window)
            self.MainWindow.close()
            self.window.show()