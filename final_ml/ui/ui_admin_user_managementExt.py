from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_admin_user_management import Ui_MainWindow_UserManagement


class ui_admin_user_managementExt(Ui_MainWindow_UserManagement):
    def __init__(self):
        super().__init__()
        self.mc = FinalConnector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        pass