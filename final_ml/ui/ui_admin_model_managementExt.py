from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QSize

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddModelDialogExt import AddModelDialogExt
from final_ml.ui.EditModelDialogExt import EditModelDialogExt
from final_ml.ui.ui_admin_model_management import Ui_MainWindow_ModelManagement
import qtawesome as qta


class ui_admin_model_managementExt(Ui_MainWindow_ModelManagement):
    def __init__(self,current_user):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user=current_user
        #{'user_id': 17, 'full_name': 'sang', 'email': 'sang', 'role': 'admin', 'password': '123'}

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium admin design
        self.apply_premium_style()
        self.add_premium_icons()
        
        self.setupSignalAndSlot()
        self.load_models()
    
    def apply_premium_style(self):
        """Apply premium model management stylesheet"""
        self.MainWindow.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
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
            }
            
            QTableWidget::item {
                padding: 12px 10px;
                border-bottom: 1px solid #F0F4F2;
            }
            
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #2D7A4E;
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to buttons"""
        try:
            if hasattr(self, 'btnAddModel'):
                icon = qta.icon('fa5s.plus-circle', color='white', scale_factor=1.2)
                self.btnAddModel.setIcon(icon)
                self.btnAddModel.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnEditModel'):
                icon = qta.icon('fa5s.edit', color='white', scale_factor=1.2)
                self.btnEditModel.setIcon(icon)
                self.btnEditModel.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnDeleteModel'):
                icon = qta.icon('fa5s.trash-alt', color='white', scale_factor=1.2)
                self.btnDeleteModel.setIcon(icon)
                self.btnDeleteModel.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnSearchModel'):
                icon = qta.icon('fa5s.search', color='white', scale_factor=1.2)
                self.btnSearchModel.setIcon(icon)
                self.btnSearchModel.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnRefreshModels'):
                icon = qta.icon('fa5s.sync-alt', color='white', scale_factor=1.2)
                self.btnRefreshModels.setIcon(icon)
                self.btnRefreshModels.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

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