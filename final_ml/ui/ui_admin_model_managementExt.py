from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_model_management import Ui_MainWindow_ModelManagement


class ui_admin_model_managementExt(Ui_MainWindow_ModelManagement):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        pass