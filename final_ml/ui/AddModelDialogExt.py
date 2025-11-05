from datetime import datetime

from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.AddModelDialog import Ui_Dialog


class AddModelDialogExt(QDialog, Ui_Dialog):
    def __init__(self,current_user):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.save_model)
        self.btnCancel.clicked.connect(self.reject)
        self.lineEditPath.mousePressEvent = self.choose_file

    def choose_file(self, event):
        # Chọn file
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file mô hình", "", "All Files (*)")
        if file_path:
            self.lineEditPath.setText(file_path)

    def save_model(self):
        name = self.lineEditName.text().strip()
        accuracy_text = self.lineEditAccuracy.text().strip()
        path = self.lineEditPath.text().strip()

        if not name or not path:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền tên và đường dẫn.")
            return

        # Chuyển độ chính xác sang float
        try:
            accuracy = float(accuracy_text) if accuracy_text else None
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Độ chính xác phải là số.")
            return

        created_at = datetime.now()
        created_by = self.current_user['user_id']  # ID admin hiện tại

        try:
            self.mc.connect()
            sql = """
                        INSERT INTO models (model_name, accuracy, file_path, created_at, created_by)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            val = (name, accuracy, path, created_at, created_by)
            result = self.mc.insert_one(sql, val)
            if result > 0:
                QMessageBox.information(self, "Thành công", "Thêm mô hình thành công!")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể thêm mô hình.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Lỗi: {e}")