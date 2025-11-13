"""
File test để chạy thử màn hình Upload Image của user
Chạy từ thư mục gốc dự án: py -m final_ml.test.test_upload_image
"""
from PyQt6.QtWidgets import QApplication, QMainWindow

# Import màn hình upload image
from final_ml.ui.ui_upload_imageExt import ui_upload_imageExt

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

# ✅ Khởi tạo giao diện upload image với thông tin user
upload_ui = ui_upload_imageExt(current_user=mock_user)

# ✅ Thiết lập UI trên cửa sổ chính
upload_ui.setupUi(main_window)

# ✅ Hiển thị cửa sổ
main_window.show()

# ✅ Chạy ứng dụng
app.exec()
