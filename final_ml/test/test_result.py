"""
File test để chạy thử màn hình Result (Kết quả dự đoán)
Chạy từ thư mục gốc dự án: py -m final_ml.test.test_result
"""
from PyQt6.QtWidgets import QApplication, QMainWindow
import os

# Import màn hình result
from final_ml.ui.ui_resultExt import ui_resultExt

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

# ✅ Giả lập đường dẫn ảnh (thay đổi đường dẫn này theo ảnh thực tế của bạn)
# Nếu không có ảnh, có thể để đường dẫn trống hoặc ảnh bất kỳ
image_path = os.path.join(os.getcwd(), "final_ml", "uploads", "test_image.jpg")
# Hoặc dùng ảnh demo:
# image_path = "d:/MLBA_FinalProjectt/file_test_image_may_be_used/test_apple.jpg"

# ✅ Giả lập kết quả dự đoán
mock_prediction = {
    'fruit_type': 'Apple',
    'quality': 'Good',
    'confidence': 95.67,
    'model_name': 'MobileNetV2',
    'model_id': 1,
    'product_id': 'BATCH-2024-001'
}

# ✅ Tạo cửa sổ chính
main_window = QMainWindow()

# ✅ Khởi tạo giao diện result với dữ liệu giả lập
result_ui = ui_resultExt(
    current_user=mock_user,
    image_path=image_path,
    prediction_result=mock_prediction
)

# ✅ Thiết lập UI trên cửa sổ chính
result_ui.setupUi(main_window)

# ✅ Hiển thị cửa sổ
main_window.show()

# ✅ Chạy ứng dụng
app.exec()
