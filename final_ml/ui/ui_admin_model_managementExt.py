from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddModelDialogExt import AddModelDialogExt
from final_ml.ui.EditModelDialogExt import EditModelDialogExt
from final_ml.ui.ui_admin_model_management import Ui_MainWindow_ModelManagement


class ui_admin_model_managementExt(Ui_MainWindow_ModelManagement):
    def __init__(self,current_user):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user=current_user
        #{'user_id': 1, 'full_name': 'Tran Thi Bich Nga', 'email': 'bichnga@hianlab.vn', 'role': 'admin'}

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.load_models()

    def setupSignalAndSlot(self):
        self.btnAddModel.clicked.connect(self.add_model)
        self.btnEditModel.clicked.connect(self.edit_model)
        self.btnSearchModel.clicked.connect(self.search_model)
        self.btnDeleteModel.clicked.connect(self.delete_model)
        self.btnRefreshModels.clicked.connect(self.load_models)

    def load_models(self):
        self.mc.connect()
        sql = "SELECT model_id, model_name, accuracy, file_path, created_at FROM models"
        models = self.mc.fetchall(sql,None)
        #print(models)
        self.tblModels.setRowCount(0)

        for model in models:
            row = self.tblModels.rowCount()
            self.tblModels.insertRow(row)
            for col, data in enumerate(model):
                self.tblModels.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

        self.txtSearchModel.clear()

    def add_model(self):
        dialog = AddModelDialogExt(self.current_user)
        if dialog.exec():
            self.load_models()

    def edit_model(self):
        row = self.tblModels.currentRow()
        if row == -1:
            return
        # Lấy model_id
        id_item = self.tblModels.item(row, 0)  # (row, column)
        if not id_item:
            return
        model_id = id_item.text()

        # Mở popup chỉnh sửa
        dialog = EditModelDialogExt(self.current_user,model_id)
        if dialog.exec():  # Nếu nhấn Lưu (accept)
            self.load_models()

    def search_model(self):
        try:
            self.mc.connect()
            # Lấy từ khóa tìm kiếm
            query = self.txtSearchModel.text().strip().lower()

            self.tblModels.setRowCount(0)

            sql = "SELECT model_id, model_name, accuracy, file_path, created_at FROM models " \
                  "WHERE LOWER(model_name) LIKE %s"
            val = (f"%{query}%",)

            models = self.mc.fetchall(sql, val)

            # Hiển thị kết quả
            for model in models:
                row = self.tblModels.rowCount()
                self.tblModels.insertRow(row)

                self.tblModels.setItem(row, 0, QtWidgets.QTableWidgetItem(str(model[0])))
                self.tblModels.setItem(row, 1, QtWidgets.QTableWidgetItem(model[1]))
                self.tblModels.setItem(row, 2, QtWidgets.QTableWidgetItem(str(model[2])))
                self.tblModels.setItem(row, 3, QtWidgets.QTableWidgetItem(model[3]))
                self.tblModels.setItem(row, 4, QtWidgets.QTableWidgetItem(model[4].strftime("%Y-%m-%d %H:%M:%S")))

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi khi tìm kiếm: {e}")

    def delete_model(self):
        row = self.tblModels.currentRow()
        if row == -1:
            return
        # Lấy model_id
        id_item = self.tblModels.item(row, 0)  # (row, column)
        if not id_item:
            return
        model_id = id_item.text()

        msg = QMessageBox(self.MainWindow)
        msg.setText(f"Bạn có muốn xóa model: {model_id}?")
        msg.setWindowTitle("Xác thực xóa")
        msg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msg.setStandardButtons(buttons)
        result = msg.exec()
        if result == QMessageBox.StandardButton.No:
            return
        # Xóa trong database
        sql = "DELETE FROM models WHERE model_id = %s"
        result = self.mc.insert_one(sql, (model_id,))
        if result > 0:
            self.load_models()
        else:
            # use msg for warning
            msg = QMessageBox()
            msg.setText("Không thể xóa mô hình")
            msg.setWindowTitle("Lỗi")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()