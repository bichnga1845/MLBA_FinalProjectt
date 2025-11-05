from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_history_settings import Ui_MainWindow_HistorySettings


class ui_history_settingsExt(Ui_MainWindow_HistorySettings):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        pass