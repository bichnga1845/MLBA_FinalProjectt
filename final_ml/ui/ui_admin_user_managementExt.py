from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddUserDialogExt import AddUserDialogExt
from final_ml.ui.EditUserDialogExt import EditUserDialogExt
from final_ml.ui.ui_admin_user_management import Ui_MainWindow_UserManagement


class ui_admin_user_managementExt(Ui_MainWindow_UserManagement):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        self.display_users()

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
        msg.setText(f"Do you want to delete user ID: {user_id}?")
        msg.setWindowTitle("Delete confirmation")
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
            msg.setText("Cannot delete user")
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
