from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QComboBox,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from final_ml.ui.design_system import GOLDEN_CITRUS, apply_global_styles, create_glass_card


class Ui_MainWindow_Result(object):
    def setupUi(self, MainWindow_Result: QMainWindow) -> None:
        MainWindow_Result.setObjectName("MainWindow_Result")
        MainWindow_Result.resize(1200, 760)
        apply_global_styles(MainWindow_Result)

        self.centralwidget = QWidget(parent=MainWindow_Result)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(48, 36, 48, 36)
        self.verticalLayout.setSpacing(24)

        heroCard = create_glass_card(self.centralwidget, padding=32)
        heroLayout = QVBoxLayout(heroCard)
        heroLayout.setSpacing(16)

        titleRow = QHBoxLayout()
        titleRow.setSpacing(12)
        title = QLabel(parent=heroCard)
        title.setObjectName("Headline")
        titleRow.addWidget(title, stretch=1)

        badge = QLabel(parent=heroCard)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background-color:{GOLDEN_CITRUS}; padding:6px 16px; border-radius:999px; font-weight:600;"
        )
        badge.setText("Fruit ML Lab")
        titleRow.addWidget(badge, 0, Qt.AlignmentFlag.AlignRight)
        heroLayout.addLayout(titleRow)

        contentRow = QHBoxLayout()
        contentRow.setSpacing(20)

        imageCard = create_glass_card(heroCard, padding=12)
        imageLayout = QVBoxLayout(imageCard)
        self.labelResultImage = QLabel(parent=imageCard)
        self.labelResultImage.setObjectName("labelResultImage")
        self.labelResultImage.setMinimumSize(420, 420)
        self.labelResultImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelResultImage.setScaledContents(True)
        self.labelResultImage.setStyleSheet("border-radius:18px; background:rgba(255,255,255,0.6);")
        imageLayout.addWidget(self.labelResultImage)
        contentRow.addWidget(imageCard, stretch=3)

        infoCard = create_glass_card(heroCard, padding=28)
        infoLayout = QVBoxLayout(infoCard)
        infoLayout.setSpacing(16)

        comboRow = QHBoxLayout()
        comboRow.setSpacing(10)
        self.comboBoxModels = QComboBox(parent=infoCard)
        self.comboBoxModels.setObjectName("comboBoxModels")
        self.comboBoxModels.setMinimumHeight(42)
        comboRow.addWidget(self.comboBoxModels, stretch=2)
        self.btnLoadModel = QPushButton(parent=infoCard)
        self.btnLoadModel.setObjectName("btnLoadModel")
        self.btnLoadModel.setMinimumHeight(42)
        comboRow.addWidget(self.btnLoadModel)
        infoLayout.addLayout(comboRow)

        self.gridResultInfo = QGridLayout()
        self.gridResultInfo.setHorizontalSpacing(18)
        self.gridResultInfo.setVerticalSpacing(12)

        self.lblResultTitle = QLabel(parent=infoCard)
        self.lblResultTitle.setObjectName("lblResultTitle")
        self.gridResultInfo.addWidget(self.lblResultTitle, 0, 0)

        self.lblResult = QLabel(parent=infoCard)
        self.lblResult.setObjectName("lblResult")
        self.lblResult.setStyleSheet("font-size:28px; font-weight:600;")
        self.gridResultInfo.addWidget(self.lblResult, 0, 1)

        self.lblConfidenceTitle = QLabel(parent=infoCard)
        self.lblConfidenceTitle.setObjectName("lblConfidenceTitle")
        self.gridResultInfo.addWidget(self.lblConfidenceTitle, 1, 0)

        self.lblConfidence = QLabel(parent=infoCard)
        self.lblConfidence.setObjectName("lblConfidence")
        self.lblConfidence.setStyleSheet("font-size:22px; font-weight:600; color:#0A8754;")
        self.gridResultInfo.addWidget(self.lblConfidence, 1, 1)

        self.lblModelUsedTitle = QLabel(parent=infoCard)
        self.lblModelUsedTitle.setObjectName("lblModelUsedTitle")
        self.gridResultInfo.addWidget(self.lblModelUsedTitle, 2, 0)

        self.lblModelUsed = QLabel(parent=infoCard)
        self.lblModelUsed.setObjectName("lblModelUsed")
        self.gridResultInfo.addWidget(self.lblModelUsed, 2, 1)

        infoLayout.addLayout(self.gridResultInfo)
        contentRow.addWidget(infoCard, stretch=2)
        heroLayout.addLayout(contentRow)

        self.layoutButtons = QHBoxLayout()
        self.layoutButtons.setSpacing(12)
        self.btnBackDashboard = QPushButton(parent=heroCard)
        self.btnBackDashboard.setObjectName("btnBackDashboard")
        self.btnBackDashboard.setProperty("secondary", True)
        self.layoutButtons.addWidget(self.btnBackDashboard)
        self.btnPredict = QPushButton(parent=heroCard)
        self.btnPredict.setObjectName("btnPredict")
        self.layoutButtons.addWidget(self.btnPredict)
        self.btnSaveHistory = QPushButton(parent=heroCard)
        self.btnSaveHistory.setObjectName("btnSaveHistory")
        self.layoutButtons.addWidget(self.btnSaveHistory)
        heroLayout.addLayout(self.layoutButtons)

        self.verticalLayout.addWidget(heroCard)

        MainWindow_Result.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(parent=MainWindow_Result)
        MainWindow_Result.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_Result)

    def retranslateUi(self, MainWindow_Result: QMainWindow) -> None:
        MainWindow_Result.setWindowTitle("Studio phân loại trái cây - Kết quả AI")
        title = self.centralwidget.findChild(QLabel, "Headline")
        if title:
            title.setText("Kết quả phân tích: Trái cây của bạn")

        self.labelResultImage.setText("Chưa có ảnh")
        self.btnLoadModel.setText("Tải mô hình")
        self.lblResultTitle.setText("Loại trái cây")
        self.lblConfidenceTitle.setText("Độ tin cậy")
        self.lblModelUsedTitle.setText("Mô hình sử dụng")

        self.lblResult.setText("—")
        self.lblConfidence.setText("—")
        self.lblModelUsed.setText("—")

        self.btnBackDashboard.setText("Quay lại trang chủ")
        self.btnPredict.setText("Chạy dự đoán khác")
        self.btnSaveHistory.setText("Lưu vào lịch sử")
