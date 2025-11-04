from PyQt6.QtWidgets import QApplication, QMainWindow
from final_ml.ui.ui_login_signupExt import ui_login_signupExt

app = QApplication([])

# ✅ Tạo cửa sổ chính
main_window = QMainWindow()

# ✅ Khởi tạo đối tượng giao diện
login_ui = ui_login_signupExt()

# ✅ Thiết lập UI trên cửa sổ chính
login_ui.setupUi(main_window)

# ✅ Hiển thị cửa sổ
main_window.show()

# ✅ Chạy ứng dụng
app.exec()
