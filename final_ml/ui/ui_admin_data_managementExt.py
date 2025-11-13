from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from PyQt6.QtCore import QSize
import csv
import os
from datetime import datetime

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_data_management import Ui_MainWindow_DataManagement
from final_ml.ui.ui_admin_model_managementExt import ui_admin_model_managementExt
import qtawesome as qta


class ui_admin_data_managementExt(Ui_MainWindow_DataManagement):
    def __init__(self, current_user):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user
        self.data_list = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium admin design
        self.apply_premium_style()
        self.add_premium_icons()
        
        self.setupSignalAndSlot()
        self.load_all_data()
        self.load_model_filter()
    
    def apply_premium_style(self):
        """Apply premium data management stylesheet"""
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
            
            QLineEdit, QComboBox, QDateEdit {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 10px 14px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
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
        """Add FontAwesome icons"""
        try:
            if hasattr(self, 'btnAddImage'):
                icon = qta.icon('fa5s.image', color='white', scale_factor=1.2)
                self.btnAddImage.setIcon(icon)
                self.btnAddImage.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnRelabel'):
                icon = qta.icon('fa5s.tag', color='white', scale_factor=1.2)
                self.btnRelabel.setIcon(icon)
                self.btnRelabel.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnDelete'):
                icon = qta.icon('fa5s.trash-alt', color='white', scale_factor=1.2)
                self.btnDelete.setIcon(icon)
                self.btnDelete.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnExport'):
                icon = qta.icon('fa5s.file-export', color='white', scale_factor=1.2)
                self.btnExport.setIcon(icon)
                self.btnExport.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnRefreshData'):
                icon = qta.icon('fa5s.search', color='white', scale_factor=1.2)
                self.btnRefreshData.setIcon(icon)
                self.btnRefreshData.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnRefresh'):
                icon = qta.icon('fa5s.sync-alt', color='white', scale_factor=1.2)
                self.btnRefresh.setIcon(icon)
                self.btnRefresh.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

    def setupSignalAndSlot(self):
        self.btnRefreshData.clicked.connect(self.search_data)
        self.btnRefresh.clicked.connect(self.load_all_data)
        self.tblData.itemSelectionChanged.connect(self.show_details)
        self.btnAddImage.clicked.connect(self.upload_image)
        self.btnRelabel.clicked.connect(self.relabel_image)
        self.btnDelete.clicked.connect(self.delete_prediction)
        self.btnExport.clicked.connect(self.export_to_csv)
        self.btnAddModel.clicked.connect(self.open_model_management)
        #self.btnStatistics.clicked.connect(self.process_statistics)

    # ----------------- Load data -----------------
    def load_all_data(self):
        """Load full prediction data with joins"""
        try:
            self.mc.connect()
            sql = """
                SELECT p.prediction_id,
                       u.image_url,
                       p.fruit_type,
                       p.confidence,
                       usr.full_name AS user_name,
                       m.model_name,
                       p.predicted_at,
                       p.quality_label,
                       p.model_id,
                       u.upload_id
                FROM predictions p
                JOIN uploads u ON p.upload_id = u.upload_id
                JOIN users usr ON u.user_id = usr.user_id
                JOIN models m ON p.model_id = m.model_id
                ORDER BY p.predicted_at DESC
            """
            self.data_list = self.mc.fetchall(sql, None)
            self.populate_table(self.data_list)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi hệ thống", f"Lỗi khi tải dữ liệu: {e}")

    def load_model_filter(self):
        """Fill model combobox"""
        try:
            self.mc.connect()
            sql = "SELECT model_name FROM models"
            models = self.mc.fetchall(sql, None)
            #print(models)
            self.comboModelFilter.clear()
            self.comboModelFilter.addItem("Model: Tất cả")
            for m in models:
                self.comboModelFilter.addItem(m[0])
        except Exception:
            pass

    # ----------------- Populate table -----------------
    def populate_table(self, data):
        self.tblData.setRowCount(0)
        for row_data in data:
            row = self.tblData.rowCount()
            self.tblData.insertRow(row)
            for col, value in enumerate(row_data[:9]):  # 9 cột chính
                self.tblData.setItem(row, col, QTableWidgetItem(str(value)))

    # ----------------- Search / Filter -----------------
    def search_data(self):
        """Filter loaded data locally"""
        try:
            keyword = self.txtSearchData.text().strip().lower()
            label_filter = self.comboLabelFilter.currentText()
            model_filter = self.comboModelFilter.currentText()
            user_filter = self.txtUserFilter.text().strip().lower()
            date_from = self.dateFrom.date().toPyDate()
            date_to = self.dateTo.date().toPyDate()

            filtered = []
            #print(self.data_list)
            for row in self.data_list:
                match = True
                if keyword and keyword not in row[1].lower():
                    match = False
                if label_filter != "Tất cả" and row[7].lower() != label_filter.lower():
                    match = False
                if model_filter != "Model: Tất cả" and row[5] != model_filter:
                    match = False
                if user_filter and user_filter not in row[4].lower():
                    match = False
                if not (date_from <= row[6].date() <= date_to):
                    match = False
                if match:
                    filtered.append(row)
            self.populate_table(filtered)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi tìm kiếm", f"{e}")

    # ----------------- Show details -----------------
    def show_details(self):
        row = self.tblData.currentRow()
        if row == -1:
            return
        try:
            img_path = self.tblData.item(row, 1).text()
            if os.path.exists(img_path):
                pixmap = QtGui.QPixmap(img_path)
                self.labelPreview.setPixmap(pixmap)
            else:
                self.labelPreview.setText("Ảnh không tồn tại")

            self.txtDId.setText(self.tblData.item(row, 0).text())
            self.txtDImage.setText(img_path)
            self.txtDResult.setText(self.tblData.item(row, 2).text())
            self.txtDConf.setText(self.tblData.item(row, 3).text())
            self.txtDUser.setText(self.tblData.item(row, 4).text())
            self.txtDModel.setText(self.tblData.item(row, 5).text())
            self.txtDTime.setText(self.tblData.item(row, 6).text())
            self.txtDNote.setText(self.tblData.item(row, 7).text())
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Lỗi hiển thị chi tiết", str(e))

    # ----------------- Upload new image -----------------
    def upload_image(self):
        """Allow admin to add new upload entry manually"""
        file_path, _ = QFileDialog.getOpenFileName(self.MainWindow, "Chọn ảnh upload", "",
                                                   "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return
        try:
            file_name = os.path.basename(file_path)
            dest_dir = "../uploads"
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, file_name)
            if not os.path.exists(dest_path):
                with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())

            sql = """INSERT INTO uploads (user_id, image_url, image_extension, upload_date)
                     VALUES (%s, %s, %s, %s)"""
            ext = os.path.splitext(file_name)[1]
            uid = self.current_user['user_id']
            self.mc.insert_one(sql, (uid, dest_path, ext, datetime.now()))
            QMessageBox.information(self.MainWindow, "Thành công", "Upload ảnh thành công.")
            self.load_all_data()
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi upload ảnh", f"{e}")

    # ----------------- Relabel (change quality_label) -----------------
    def relabel_image(self):
        row = self.tblData.currentRow()
        if row == -1:
            return
        pred_id = self.tblData.item(row, 0).text()
        new_label, ok = QtWidgets.QInputDialog.getItem(self.MainWindow, "Sửa nhãn", "Chọn nhãn mới:",
                                                       ["good", "bad"], editable=False)
        if not ok:
            return
        try:
            sql = "UPDATE predictions SET quality_label=%s WHERE prediction_id=%s"
            self.mc.insert_one(sql, (new_label, pred_id))
            self.load_all_data()
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi sửa nhãn", str(e))

    # ----------------- Delete prediction -----------------
    def delete_prediction(self):
        row = self.tblData.currentRow()
        if row == -1:
            return
        pred_id = self.tblData.item(row, 0).text()
        msg = QMessageBox.question(self.MainWindow, "Xác nhận xóa",
                                   f"Bạn có chắc chắn muốn xóa dự đoán ID {pred_id} không?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.No:
            return
        try:
            sql = "DELETE FROM predictions WHERE prediction_id=%s"
            self.mc.insert_one(sql, (pred_id,))
            self.load_all_data()
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi xóa dữ liệu", str(e))

    # ----------------- Export to CSV -----------------
    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self.MainWindow, "Xuất CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return
        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                headers = [self.tblData.horizontalHeaderItem(i).text() for i in range(self.tblData.columnCount())]
                writer.writerow(headers)
                for row in range(self.tblData.rowCount()):
                    row_data = [self.tblData.item(row, col).text() if self.tblData.item(row, col) else "" for col in
                                range(self.tblData.columnCount())]
                    writer.writerow(row_data)
            QMessageBox.information(self.MainWindow, "Thành công", "Xuất dữ liệu thành công.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi xuất CSV", str(e))

    # ----------------- Open model management -----------------
    def open_model_management(self):
        from PyQt6.QtWidgets import QMainWindow
        self.window = QMainWindow()
        self.ui = ui_admin_model_managementExt(self.current_user)
        self.ui.setupUi(self.window)
        #self.MainWindow.close()
        self.window.show()