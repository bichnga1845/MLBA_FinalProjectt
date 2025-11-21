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
        Dialog.resize(560, 360)
        apply_global_styles(Dialog)

        layout = QVBoxLayout(Dialog)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        card = create_glass_card(Dialog, padding=32)
        layout.addWidget(card)

        cardLayout = QVBoxLayout(card)
        cardLayout.setSpacing(22)

        header = QLabel(parent=card)
        header.setObjectName("Headline")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        cardLayout.addWidget(header)

        sub = QLabel(parent=card)
        sub.setObjectName("Subtitle")
        sub.setWordWrap(True)
        cardLayout.addWidget(sub)

        formLayout = QFormLayout()
        formLayout.setHorizontalSpacing(18)
        formLayout.setVerticalSpacing(12)

        self.lineEditName = QLineEdit(parent=card)
        formLayout.addRow(self._create_form_label(card, "lblName"), self.lineEditName)

        self.lineEditAccuracy = QLineEdit(parent=card)
        formLayout.addRow(self._create_form_label(card, "lblAccuracy"), self.lineEditAccuracy)

        self.lineEditPath = QLineEdit(parent=card)
        formLayout.addRow(self._create_form_label(card, "lblPath"), self.lineEditPath)

        cardLayout.addLayout(formLayout)

        actions = QHBoxLayout()
        actions.addStretch()
        self.btnCancel = QPushButton(parent=card)
        self.btnCancel.setProperty("secondary", True)
        actions.addWidget(self.btnCancel)

        self.btnSave = QPushButton(parent=card)
        actions.addWidget(self.btnSave)
        cardLayout.addLayout(actions)

        self.retranslateUi(Dialog)

    def _create_form_label(self, parent, object_name: str) -> QLabel:
        lbl = QLabel(parent=parent)
        lbl.setObjectName(object_name)
        return lbl

    def retranslateUi(self, Dialog: QDialog) -> None:
        Dialog.setWindowTitle("Thêm mô hình AI mới")
        self.central_texts = {
            "Headline": "Thêm mô hình học máy",
            "Subtitle": "Chuẩn hóa kho mô hình bằng cách cập nhật thông tin trực tiếp tại đây.",
            "lblName": "Tên mô hình",
            "lblAccuracy": "Độ chính xác (%)",
            "lblPath": "Đường dẫn file",
        }
        for object_name, text in self.central_texts.items():
            lbl = Dialog.findChild(QLabel, object_name)
            if lbl:
                lbl.setText(text)
        self.btnSave.setText("Lưu mô hình")
        self.btnCancel.setText("Huỷ")
