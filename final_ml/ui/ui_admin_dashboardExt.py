from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_dashboard import Ui_MainWindow_AdminDashboard
from final_ml.ui.ui_admin_data_managementExt import ui_admin_data_managementExt
from final_ml.ui.ui_admin_model_managementExt import ui_admin_model_managementExt
from final_ml.ui.ui_admin_user_managementExt import ui_admin_user_managementExt
from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt
import qtawesome as qta


class ui_admin_dashboardExt(Ui_MainWindow_AdminDashboard):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium admin design
        self.apply_premium_admin_style()
        self.add_premium_icons()
        
        self.setupSignalAndSlot()
    
    def apply_premium_admin_style(self):
        """Apply ultra premium admin dashboard stylesheet"""
        self.MainWindow.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            /* Dashboard Title */
            QLabel {
                color: #1A3A2E;
            }
            
            /* Premium Buttons with Gradients */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px 24px;
                font-size: 15px;
                font-weight: 600;
                min-height: 48px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E5A35, stop:1 #246A3F);
            }
            
            /* Stats Cards */
            QFrame {
                background: white;
                border: 2px solid #E8F5E9;
                border-radius: 14px;
                padding: 20px;
            }
            
            QFrame:hover {
                border-color: #4A9D6E;
            }
            
            /* Labels in Cards */
            QLabel#statValue {
                font-size: 36px;
                font-weight: 700;
                color: #2D7A4E;
            }
            
            QLabel#statLabel {
                font-size: 13px;
                color: #5A7A6A;
                font-weight: 600;
                text-transform: uppercase;
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to admin buttons"""
        try:
            # User Management button
            if hasattr(self, 'btnGoUserMgmt'):
                icon = qta.icon('fa5s.users', color='white', scale_factor=1.2)
                self.btnGoUserMgmt.setIcon(icon)
                self.btnGoUserMgmt.setIconSize(QSize(20, 20))
            
            # Data Management button
            if hasattr(self, 'btnGoDataMgmt'):
                icon = qta.icon('fa5s.database', color='white', scale_factor=1.2)
                self.btnGoDataMgmt.setIcon(icon)
                self.btnGoDataMgmt.setIconSize(QSize(20, 20))
            
            # Model Management button
            if hasattr(self, 'btnGoModelMgmt'):
                icon = qta.icon('fa5s.brain', color='white', scale_factor=1.2)
                self.btnGoModelMgmt.setIcon(icon)
                self.btnGoModelMgmt.setIconSize(QSize(20, 20))
            
            # History button
            if hasattr(self, 'btnGoHistory'):
                icon = qta.icon('fa5s.history', color='white', scale_factor=1.2)
                self.btnGoHistory.setIcon(icon)
                self.btnGoHistory.setIconSize(QSize(20, 20))
            
            # Statistics button
            if hasattr(self, 'btnGoStatistics'):
                icon = qta.icon('fa5s.chart-bar', color='white', scale_factor=1.2)
                self.btnGoStatistics.setIcon(icon)
                self.btnGoStatistics.setIconSize(QSize(20, 20))
            
            # Logout button
            if hasattr(self, 'btnLogout'):
                icon = qta.icon('fa5s.sign-out-alt', color='white', scale_factor=1.2)
                self.btnLogout.setIcon(icon)
                self.btnLogout.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

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
        self.ui = ui_admin_data_managementExt(self.current_user)
        self.ui.setupUi(self.window)
        self.MainWindow.close()
        self.window.show()

    def go_model_mgmt(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_admin_model_managementExt(self.current_user)
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