"""
Test Admin Dashboard Screen
Run: py -m final_ml.test.test_admin_dashboard
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
    
    from final_ml.ui.ui_admin_dashboardExt import ui_admin_dashboardExt
    
    window = QMainWindow()
    ui = ui_admin_dashboardExt(current_user)
    ui.setupUi(window)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
