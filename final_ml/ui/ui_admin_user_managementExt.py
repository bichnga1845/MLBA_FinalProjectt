from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QSize

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddUserDialogExt import AddUserDialogExt
from final_ml.ui.EditUserDialogExt import EditUserDialogExt
from final_ml.ui.ui_admin_user_management import Ui_MainWindow_UserManagement
import qtawesome as qta


class ui_admin_user_managementExt(Ui_MainWindow_UserManagement):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium admin design
        self.apply_premium_style()
        self.add_premium_icons()
        
        self.setupSignalAndSlot()
        self.display_users()
    
    def apply_premium_style(self):
        """Apply premium admin stylesheet"""
        self.MainWindow.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            /* Premium Buttons */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-height: 42px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1E5A35, stop:1 #246A3F);
            }
            
            /* Input Fields */
            QLineEdit {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 10px 14px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            
            QLineEdit:hover {
                border-color: #4A9D6E;
            }
            
            QLineEdit:focus {
                border-color: #2D7A4E;
                background-color: rgba(45, 122, 78, 0.02);
            }
            
            /* ComboBox */
            QComboBox {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 10px 14px;
                background-color: white;
                min-height: 20px;
                font-size: 14px;
            }
            
            QComboBox:hover {
                border-color: #4A9D6E;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 36px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 10px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E0E7E4;
                border-radius: 8px;
                selection-background-color: #E8F5E9;
                selection-color: #2D7A4E;
                color: #2D7A4E;
                padding: 4px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-radius: 4px;
                color: #2D7A4E;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F5E9;
            }
            
            /* Premium Table */
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #F0F4F2;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.2);
                padding: 14px 12px;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
            }
            
            QTableWidget::item {
                padding: 12px 10px;
                border-bottom: 1px solid #F0F4F2;
            }
            
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #2D7A4E;
            }
            
            QTableWidget::item:hover {
                background-color: rgba(45, 122, 78, 0.05);
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to buttons"""
        try:
            if hasattr(self, 'btnAddUser'):
                icon = qta.icon('fa5s.user-plus', color='white', scale_factor=1.2)
                self.btnAddUser.setIcon(icon)
                self.btnAddUser.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnEditUser'):
                icon = qta.icon('fa5s.edit', color='white', scale_factor=1.2)
                self.btnEditUser.setIcon(icon)
                self.btnEditUser.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnDeleteUser'):
                icon = qta.icon('fa5s.trash-alt', color='white', scale_factor=1.2)
                self.btnDeleteUser.setIcon(icon)
                self.btnDeleteUser.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnSearchUser'):
                icon = qta.icon('fa5s.search', color='white', scale_factor=1.2)
                self.btnSearchUser.setIcon(icon)
                self.btnSearchUser.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnRefreshUser'):
                icon = qta.icon('fa5s.sync-alt', color='white', scale_factor=1.2)
                self.btnRefreshUser.setIcon(icon)
                self.btnRefreshUser.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

    def setupSignalAndSlot(self):
        self.btnAddUser.clicked.connect(self.add_user)
        self.btnEditUser.clicked.connect(self.edit_user)
        self.btnDeleteUser.clicked.connect(self.delete_user)
        self.btnSearchUser.clicked.connect(self.search_user)
        self.comboRoleFilter.currentIndexChanged.connect(self.display_users)
        self.btnRefreshUser.clicked.connect(self.refresh_all_users)

    def display_users(self):
        try:
            self.mc.connect()
            # Xóa dữ liệu cũ
            self.tableWidgetUsers.setRowCount(0)

            # Lấy giá trị filter từ QComboBox
            role_filter = self.comboRoleFilter.currentText()

            #load users from database
            if role_filter == "Admin":
                sql = "SELECT * FROM users WHERE role='admin'"
            elif role_filter == "User":
                sql = "SELECT * FROM users WHERE role='user'"
            else:
                sql = "SELECT * FROM users"

            users = self.mc.fetchall(sql, None)
            for user in users:
                #get last row
                row=self.tableWidgetUsers.rowCount()
                #insert new row at the end of the table
                self.tableWidgetUsers.insertRow(row)
                #assign value for each column
                column_id=QTableWidgetItem(str(user[0]))
                column_name=QTableWidgetItem(user[1])
                column_email=QTableWidgetItem(user[2])
                column_role=QTableWidgetItem(user[4])
                formatted_time = user[5].strftime("%Y-%m-%d %H:%M:%S")
                column_created=QTableWidgetItem(formatted_time)
                column_password=QTableWidgetItem(user[3])
                formatted_time = user[6].strftime("%Y-%m-%d %H:%M:%S")
                column_last_login = QTableWidgetItem(formatted_time)

                #push column(s) into row
                self.tableWidgetUsers.setItem(row, 0, column_id)
                self.tableWidgetUsers.setItem(row, 1, column_name)
                self.tableWidgetUsers.setItem(row, 2, column_email)
                self.tableWidgetUsers.setItem(row, 3, column_role)
                self.tableWidgetUsers.setItem(row, 4, column_created)
                self.tableWidgetUsers.setItem(row, 5, column_password)
                self.tableWidgetUsers.setItem(row, 6, column_last_login)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi khi tải dữ liệu: {e}")

    def refresh_all_users(self):
        try:
            self.mc.connect()
            # Xóa dữ liệu cũ
            self.tableWidgetUsers.setRowCount(0)

            sql = "SELECT * FROM users"

            users = self.mc.fetchall(sql, None)
            for user in users:
                #get last row
                row=self.tableWidgetUsers.rowCount()
                #insert new row at the end of the table
                self.tableWidgetUsers.insertRow(row)
                #assign value for each column
                column_id=QTableWidgetItem(str(user[0]))
                column_name=QTableWidgetItem(user[1])
                column_email=QTableWidgetItem(user[2])
                column_role=QTableWidgetItem(user[4])
                formatted_time = user[5].strftime("%Y-%m-%d %H:%M:%S")
                column_created=QTableWidgetItem(formatted_time)
                column_password=QTableWidgetItem(user[3])
                formatted_time = user[6].strftime("%Y-%m-%d %H:%M:%S")
                column_last_login = QTableWidgetItem(formatted_time)

                #push column(s) into row
                self.tableWidgetUsers.setItem(row, 0, column_id)
                self.tableWidgetUsers.setItem(row, 1, column_name)
                self.tableWidgetUsers.setItem(row, 2, column_email)
                self.tableWidgetUsers.setItem(row, 3, column_role)
                self.tableWidgetUsers.setItem(row, 4, column_created)
                self.tableWidgetUsers.setItem(row, 5, column_password)
                self.tableWidgetUsers.setItem(row, 6, column_last_login)

            self.lineEditSearchUser.setText("")
            self.comboRoleFilter.setCurrentText("Tất cả")

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi khi tải dữ liệu: {e}")

    def add_user(self):
        dialog = AddUserDialogExt()
        if dialog.exec():
            self.refresh_all_users()

    def edit_user(self):
        row = self.tableWidgetUsers.currentRow()
        if row == -1:
            return
        # Lấy user_id
        id_item = self.tableWidgetUsers.item(row, 0)  # (row, column)
        if not id_item:
            return
        user_id = id_item.text()

        # Mở popup chỉnh sửa
        dialog = EditUserDialogExt(user_id)
        if dialog.exec():  # Nếu nhấn Lưu (accept)
            self.refresh_all_users()

    def search_user(self):
        try:
            self.mc.connect()
            # Lấy từ khóa tìm kiếm
            query = self.lineEditSearchUser.text().strip().lower()
            role_filter = self.comboRoleFilter.currentText()

            self.tableWidgetUsers.setRowCount(0)

            sql = "SELECT * FROM users WHERE (LOWER(full_name) LIKE %s OR LOWER(email) LIKE %s)"
            val = (f"%{query}%", f"%{query}%")

            # Thêm điều kiện lọc role
            if role_filter == "Admin":
                sql += " AND role = 'admin'"
            elif role_filter == "User":
                sql += " AND role = 'user'"

            users = self.mc.fetchall(sql, val)

            # Hiển thị kết quả
            for user in users:
                row = self.tableWidgetUsers.rowCount()
                self.tableWidgetUsers.insertRow(row)

                self.tableWidgetUsers.setItem(row, 0, QTableWidgetItem(str(user[0])))
                self.tableWidgetUsers.setItem(row, 1, QTableWidgetItem(user[1]))
                self.tableWidgetUsers.setItem(row, 2, QTableWidgetItem(user[2]))
                self.tableWidgetUsers.setItem(row, 3, QTableWidgetItem(user[4]))
                self.tableWidgetUsers.setItem(row, 4, QTableWidgetItem(user[5].strftime("%Y-%m-%d %H:%M:%S")))
                self.tableWidgetUsers.setItem(row, 5, QTableWidgetItem(user[3]))
                self.tableWidgetUsers.setItem(row, 6, QTableWidgetItem(user[6].strftime("%Y-%m-%d %H:%M:%S")))

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi khi tìm kiếm: {e}")

    def delete_user(self):
        row = self.tableWidgetUsers.currentRow()
        if row == -1:
            return
        # Lấy user_id
        id_item = self.tableWidgetUsers.item(row, 0)  # (row, column)
        if not id_item:
            return
        user_id = id_item.text()

        msg = QMessageBox(self.MainWindow)
        msg.setText(f"Bạn có muốn xóa người dùng với ID {user_id}?")
        msg.setWindowTitle("Xác thực xóa")
        msg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msg.setStandardButtons(buttons)
        result = msg.exec()
        if result == QMessageBox.StandardButton.No:
            return
        # Sau khi xác nhận, xóa user trong database
        sql = "DELETE FROM Users WHERE user_id = %s"
        result=self.mc.insert_one(sql, (user_id,))
        if result > 0:
            # reload list of user
            self.display_users()
        else:
            # use msg for warning
            msg = QMessageBox()
            msg.setText("Không thể xóa người dùng")
            msg.setWindowTitle("Lỗi")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
