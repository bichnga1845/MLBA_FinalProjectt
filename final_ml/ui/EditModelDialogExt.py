from datetime import datetime

from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog

from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.EditModelDialog import Ui_Dialog


class EditModelDialogExt(QDialog, Ui_Dialog):
    def __init__(self,current_user,model_id):
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user
        self.model_id = model_id

        self.setupUi(self)

        self.load_model_data()

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

    def load_model_data(self):
        self.mc.connect()
        sql = "SELECT model_name, accuracy, file_path, created_at FROM models WHERE model_id=%s"
        model = self.mc.fetchone(sql, (self.model_id,))
        if model:
            self.lineEditName.setText(model[0])
            self.lineEditAccuracy.setText(str(model[1]))
            self.lineEditPath.setText(model[2])
            self.lineEditCreatedAt.setText(str(model[3]))
            self.lineEditCreatedAt.setReadOnly(True)

    def save_model(self):
        name = self.lineEditName.text().strip()
        accuracy = self.lineEditAccuracy.text().strip()
        file_path = self.lineEditPath.text().strip()

        if not name or not accuracy or not file_path:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        try:
            accuracy = float(accuracy) if accuracy else None
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Độ chính xác phải là số.")
            return

        try:
            self.mc.connect()
            sql = """UPDATE models
                     SET model_name=%s, accuracy=%s, file_path=%s
                     WHERE model_id=%s"""
            val = (name, accuracy, file_path, self.model_id)
            result = self.mc.insert_one(sql, val)
            if result > 0:
                QMessageBox.information(self, "Thành công", "Cập nhật model thành công!")
                self.accept()
            else:
                QMessageBox.warning(self, "Không thay đổi", "Không có thay đổi nào được lưu.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu: {e}")
