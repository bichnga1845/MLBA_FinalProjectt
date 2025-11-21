from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from final_ml.ui.design_system import apply_global_styles, create_glass_card


class Ui_Dialog(object):
    def setupUi(self, Dialog: QDialog) -> None:
        Dialog.setObjectName("Dialog")
        Dialog.resize(580, 420)
        apply_global_styles(Dialog)

        layout = QVBoxLayout(Dialog)
        layout.setContentsMargins(32, 28, 32, 28)

        card = create_glass_card(Dialog, padding=32)
        layout.addWidget(card)
        cardLayout = QVBoxLayout(card)
        cardLayout.setSpacing(22)

        header = QLabel(parent=card)
        header.setObjectName("Headline")
        cardLayout.addWidget(header)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        self.lineEditName = QLineEdit(parent=card)
        form.addRow(self._label(card, "lblName"), self.lineEditName)

        self.lineEditAccuracy = QLineEdit(parent=card)
        form.addRow(self._label(card, "lblAccuracy"), self.lineEditAccuracy)

        self.lineEditPath = QLineEdit(parent=card)
        form.addRow(self._label(card, "lblPath"), self.lineEditPath)

        self.lineEditCreatedAt = QLineEdit(parent=card)
        self.lineEditCreatedAt.setReadOnly(True)
        form.addRow(self._label(card, "lblCreatedAt"), self.lineEditCreatedAt)

        cardLayout.addLayout(form)

        actions = QHBoxLayout()
        actions.addStretch()
        self.btnCancel = QPushButton(parent=card)
        self.btnCancel.setProperty("secondary", True)
        actions.addWidget(self.btnCancel)
        self.btnSave = QPushButton(parent=card)
        actions.addWidget(self.btnSave)
        cardLayout.addLayout(actions)

        self.retranslateUi(Dialog)

    def _label(self, parent, name: str) -> QLabel:
        lbl = QLabel(parent=parent)
        lbl.setObjectName(name)
        return lbl

    def retranslateUi(self, Dialog: QDialog) -> None:
        Dialog.setWindowTitle("Điều chỉnh thông tin mô hình")
        texts = {
            "Headline": "Cập nhật mô hình đang phục vụ",
            "lblName": "Tên mô hình",
            "lblAccuracy": "Độ chính xác (%)",
            "lblPath": "Đường dẫn file",
            "lblCreatedAt": "Ngày khởi tạo",
        }
        for name, text in texts.items():
            lbl = Dialog.findChild(QLabel, name)
            if lbl:
                lbl.setText(text)
        self.btnSave.setText("Lưu thay đổi")
        self.btnCancel.setText("Huỷ")
