from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
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
        Dialog.resize(560, 420)
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
        cardLayout.addWidget(header)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        self.lineEditName = QLineEdit(parent=card)
        form.addRow(self._label(card, "lblName"), self.lineEditName)

        self.lineEditEmail = QLineEdit(parent=card)
        form.addRow(self._label(card, "lblEmail"), self.lineEditEmail)

        self.lineEditPassword = QLineEdit(parent=card)
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow(self._label(card, "lblPassword"), self.lineEditPassword)

        self.comboRole = QComboBox(parent=card)
        form.addRow(self._label(card, "lblRole"), self.comboRole)

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
        Dialog.setWindowTitle("Tinh chỉnh thông tin người dùng")
        texts = {
            "Headline": "Cập nhật hồ sơ thành viên",
            "lblName": "Tên hiển thị",
            "lblEmail": "Email công việc",
            "lblPassword": "Đặt lại mật khẩu",
            "lblRole": "Vai trò",
        }
        for name, text in texts.items():
            lbl = Dialog.findChild(QLabel, name)
            if lbl:
                lbl.setText(text)
        self.comboRole.clear()
        self.comboRole.addItems(["User", "Admin"])
        self.btnSave.setText("Lưu thay đổi")
        self.btnCancel.setText("Đóng")
