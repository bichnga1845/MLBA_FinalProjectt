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

        sub = QLabel(parent=card)
        sub.setObjectName("Subtitle")
        sub.setWordWrap(True)
        cardLayout.addWidget(sub)

        form = QFormLayout()
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(12)

        self.lineEditName = QLineEdit(parent=card)
        self.lineEditName.setObjectName("lineEditName")
        form.addRow(self._label(card, "lblName"), self.lineEditName)

        self.lineEditEmail = QLineEdit(parent=card)
        self.lineEditEmail.setObjectName("lineEditEmail")
        form.addRow(self._label(card, "lblEmail"), self.lineEditEmail)

        self.lineEditPassword = QLineEdit(parent=card)
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        form.addRow(self._label(card, "lblPassword"), self.lineEditPassword)

        self.comboRole = QComboBox(parent=card)
        self.comboRole.setObjectName("comboRole")
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
        Dialog.setWindowTitle("Thêm người dùng cao cấp")
        texts = {
            "Headline": "Tạo tài khoản mới",
            "Subtitle": "Kết nối các chuyên gia nông sản với nền tảng AI của bạn.",
            "lblName": "Tên hiển thị",
            "lblEmail": "Email công việc",
            "lblPassword": "Mật khẩu",
            "lblRole": "Vai trò",
        }
        for name, text in texts.items():
            lbl = Dialog.findChild(QLabel, name)
            if lbl:
                lbl.setText(text)
        self.comboRole.clear()
        self.comboRole.addItems(["User", "Admin"])
        self.btnSave.setText("Mời tham gia")
        self.btnCancel.setText("Đóng")
