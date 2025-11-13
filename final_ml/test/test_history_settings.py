"""
File test để chạy thử màn hình History & Settings
Chạy từ thư mục gốc dự án: py -m final_ml.test.test_history_settings
"""
from PyQt6.QtWidgets import QApplication, QMainWindow

# Import màn hình history settings
from final_ml.ui.ui_history_settingsExt import ui_history_settingsExt

# Tạo ứng dụng PyQt6
app = QApplication([])

# ✅ Giả lập thông tin user đã đăng nhập
mock_user = {
    'user_id': 1,
    'username': 'testuser',
    'full_name': 'Nguyễn Văn Test',
    'email': 'test@example.com',
    'role': 'user'
}

# ✅ Tạo cửa sổ chính
main_window = QMainWindow()

# ✅ Khởi tạo giao diện history & settings với thông tin user
history_ui = ui_history_settingsExt(current_user=mock_user)

# ✅ Thiết lập UI trên cửa sổ chính
history_ui.setupUi(main_window)

# ✅ Hiển thị cửa sổ
main_window.show()

# ✅ Chạy ứng dụng
app.exec()
