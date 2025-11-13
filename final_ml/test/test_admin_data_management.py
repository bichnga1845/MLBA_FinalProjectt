"""
Test Admin Data Management Screen
Run: py -m final_ml.test.test_admin_data_management
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

def main():
    app = QApplication(sys.argv)
    
    # Mock current user as admin
    current_user = {
        'user_id': 1,
        'full_name': 'Admin User',
        'email': 'admin@fruitml.com',
        'role': 'admin'
    }
    
    from final_ml.ui.ui_admin_data_managementExt import ui_admin_data_managementExt
    
    window = QMainWindow()
    ui = ui_admin_data_managementExt(current_user)
    ui.setupUi(window)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
