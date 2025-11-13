"""
Test Admin User Management Screen
Run: py -m final_ml.test.test_admin_user_management
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

def main():
    app = QApplication(sys.argv)
    
    from final_ml.ui.ui_admin_user_managementExt import ui_admin_user_managementExt
    
    window = QMainWindow()
    ui = ui_admin_user_managementExt()
    ui.setupUi(window)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
