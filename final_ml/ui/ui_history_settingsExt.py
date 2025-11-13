from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDate, QSize
from final_ml.connector.ml_connector import FinalConnector
from final_ml.ui.ui_history_settings import Ui_MainWindow_HistorySettings
from datetime import datetime
import qtawesome as qta


class ui_history_settingsExt(Ui_MainWindow_HistorySettings):
    def __init__(self, current_user=None):
        """
        Khởi tạo màn hình History & Settings
        
        Args:
            current_user: dict thông tin user hiện tại (optional cho test)
        """
        super().__init__()
        self.mc = FinalConnector()
        self.current_user = current_user or {
            'user_id': 1,
            'username': 'demo_user',
            'email': 'demo@example.com',
            'full_name': 'Demo User'
        }

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        
        # Apply premium stylesheet
        self.apply_premium_style()
        self.add_premium_icons()
        
        MainWindow.setWindowTitle("🍃 Fruit ML - History & Settings")
        MainWindow.resize(1000, 700)
        
        self.setupSignalAndSlot()
        self.load_user_info()
        self.load_history()
    
    def apply_premium_style(self):
        """Apply premium history & settings stylesheet"""
        self.MainWindow.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #F8FAF9, stop:1 #E8F5E9);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-height: 42px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            
            QLineEdit, QDateEdit {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 10px 14px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            
            QLineEdit:hover, QDateEdit:hover {
                border-color: #4A9D6E;
            }
            
            QLineEdit:focus, QDateEdit:focus {
                border-color: #2D7A4E;
            }
            
            QComboBox {
                border: 2px solid #E0E7E4;
                border-radius: 10px;
                padding: 10px 14px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            
            QComboBox:hover {
                border-color: #4A9D6E;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #2D7A4E;
                margin-right: 8px;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #E0E7E4;
                border-radius: 8px;
                selection-background-color: #E8F5E9;
                selection-color: #2D7A4E;
                color: #2D7A4E;
                padding: 4px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-radius: 4px;
                color: #2D7A4E;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F5E9;
            }
            
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #F0F4F2;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                color: white;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.2);
                padding: 14px 12px;
                font-weight: 600;
                font-size: 13px;
            }
            
            QTableWidget::item {
                padding: 12px 10px;
                border-bottom: 1px solid #F0F4F2;
            }
            
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #2D7A4E;
            }
            
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            
            QTabBar::tab {
                background: transparent;
                color: #8B9D94;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 12px 28px;
                font-weight: 600;
                font-size: 15px;
                margin-right: 8px;
            }
            
            QTabBar::tab:selected {
                color: #2D7A4E;
                border-bottom: 3px solid #2D7A4E;
            }
            
            QTabBar::tab:hover {
                color: #4A9D6E;
                background-color: rgba(45, 122, 78, 0.05);
                border-radius: 8px 8px 0 0;
            }
        """)
    
    def add_premium_icons(self):
        """Add FontAwesome icons to buttons"""
        try:
            if hasattr(self, 'btnReloadHistory'):
                icon = qta.icon('fa5s.sync-alt', color='white', scale_factor=1.2)
                self.btnReloadHistory.setIcon(icon)
                self.btnReloadHistory.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnDeleteHistory'):
                icon = qta.icon('fa5s.trash-alt', color='white', scale_factor=1.2)
                self.btnDeleteHistory.setIcon(icon)
                self.btnDeleteHistory.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnUpdateProfile'):
                icon = qta.icon('fa5s.save', color='white', scale_factor=1.2)
                self.btnUpdateProfile.setIcon(icon)
                self.btnUpdateProfile.setIconSize(QSize(18, 18))
            
            if hasattr(self, 'btnLogout'):
                icon = qta.icon('fa5s.sign-out-alt', color='white', scale_factor=1.2)
                self.btnLogout.setIcon(icon)
                self.btnLogout.setIconSize(QSize(18, 18))
        except Exception as e:
            print(f"Could not add icons: {e}")

    def setupSignalAndSlot(self):
        """Thiết lập các sự kiện cho các nút và controls"""
        # Tab History
        self.btnReloadHistory.clicked.connect(self.load_history)
        self.btnDeleteHistory.clicked.connect(self.delete_selected_history)
        self.txtSearchHistory.textChanged.connect(self.filter_history)
        self.comboLabelHistory.currentIndexChanged.connect(self.filter_history)
        self.dateFrom.dateChanged.connect(self.filter_history)
        self.dateTo.dateChanged.connect(self.filter_history)
        
        # Tab Settings
        self.btnUpdateProfile.clicked.connect(self.update_profile)
        self.btnLogout.clicked.connect(self.logout)
        
        # Thiết lập ngày mặc định (30 ngày trước đến hôm nay)
        self.dateTo.setDate(QDate.currentDate())
        self.dateFrom.setDate(QDate.currentDate().addDays(-30))

    def load_user_info(self):
        """Tải thông tin user lên form Settings"""
        self.txtUsername.setText(self.current_user.get('username', ''))
        self.txtEmail.setText(self.current_user.get('email', ''))
        self.txtUsername.setReadOnly(True)  # Username không cho sửa

    def load_history(self):
        """Tải lịch sử dự đoán từ database"""
        try:
            self.mc.connect()
            
            # Query lấy lịch sử của user hiện tại
            sql = """
                SELECT 
                    u.image_url,
                    CONCAT(p.fruit_type, ' - ', p.quality_label) as result,
                    p.confidence,
                    p.predicted_at,
                    m.model_name
                FROM Predictions p
                JOIN Uploads u ON p.upload_id = u.upload_id
                LEFT JOIN Models m ON p.model_id = m.model_id
                WHERE u.user_id = %s
                ORDER BY p.predicted_at DESC
            """
            
            data = self.mc.fetchall(sql, (self.current_user['user_id'],))
            
            # Hiển thị dữ liệu lên bảng
            self.tblHistory.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tblHistory.insertRow(row_num)
                
                # Ảnh (chỉ hiển thị tên file)
                import os
                image_name = os.path.basename(row_data[0]) if row_data[0] else 'N/A'
                self.tblHistory.setItem(row_num, 0, QTableWidgetItem(image_name))
                
                # Kết quả
                self.tblHistory.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))
                
                # Confidence
                confidence_str = f"{float(row_data[2]):.2f}%" if row_data[2] else 'N/A'
                self.tblHistory.setItem(row_num, 2, QTableWidgetItem(confidence_str))
                
                # Thời gian
                time_str = row_data[3].strftime('%Y-%m-%d %H:%M:%S') if row_data[3] else 'N/A'
                self.tblHistory.setItem(row_num, 3, QTableWidgetItem(time_str))
                
                # Mô hình
                self.tblHistory.setItem(row_num, 4, QTableWidgetItem(str(row_data[4]) if row_data[4] else 'N/A'))
            
            # Tự động điều chỉnh độ rộng cột
            self.tblHistory.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Thông báo", 
                              f"Không thể tải lịch sử: {e}\n(Có thể chưa kết nối database)")

    def filter_history(self):
        """Lọc lịch sử theo tìm kiếm, label và ngày"""
        search_text = self.txtSearchHistory.text().lower()
        selected_label = self.comboLabelHistory.currentText()
        date_from = self.dateFrom.date().toPyDate()
        date_to = self.dateTo.date().toPyDate()
        
        # Duyệt qua từng row và ẩn/hiện theo điều kiện
        for row in range(self.tblHistory.rowCount()):
            show_row = True
            
            # Kiểm tra search text
            if search_text:
                row_text = ""
                for col in range(self.tblHistory.columnCount()):
                    item = self.tblHistory.item(row, col)
                    if item:
                        row_text += item.text().lower() + " "
                if search_text not in row_text:
                    show_row = False
            
            # Kiểm tra label filter
            if selected_label != "Tất cả":
                result_item = self.tblHistory.item(row, 1)
                if result_item and selected_label not in result_item.text():
                    show_row = False
            
            # Kiểm tra date range
            time_item = self.tblHistory.item(row, 3)
            if time_item:
                try:
                    time_str = time_item.text()
                    record_date = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').date()
                    if not (date_from <= record_date <= date_to):
                        show_row = False
                except:
                    pass
            
            # Ẩn hoặc hiện row
            self.tblHistory.setRowHidden(row, not show_row)

    def delete_selected_history(self):
        """Xóa các bản ghi được chọn"""
        selected_rows = set()
        for item in self.tblHistory.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.warning(self.MainWindow, "Cảnh báo", 
                              "Vui lòng chọn ít nhất một bản ghi để xóa!")
            return
        
        # Xác nhận xóa
        reply = QMessageBox.question(self.MainWindow, "Xác nhận xóa",
                                     f"Bạn có chắc muốn xóa {len(selected_rows)} bản ghi?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.mc.connect()
                
                # Xóa từng bản ghi (cần có prediction_id hoặc logic khác)
                # Tạm thời chỉ xóa khỏi UI
                for row in sorted(selected_rows, reverse=True):
                    self.tblHistory.removeRow(row)
                
                QMessageBox.information(self.MainWindow, "Thành công", 
                                      f"Đã xóa {len(selected_rows)} bản ghi!")
                
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Lỗi", 
                                   f"Lỗi khi xóa: {e}")

    def update_profile(self):
        """Cập nhật thông tin cá nhân và đổi mật khẩu"""
        new_email = self.txtEmail.text().strip()
        old_password = self.txtOldPassword.text()
        new_password = self.txtNewPassword.text()
        confirm_password = self.txtConfirmNewPassword.text()
        
        # Validate
        if not new_email:
            QMessageBox.warning(self.MainWindow, "Cảnh báo", "Email không được để trống!")
            return
        
        # Nếu muốn đổi mật khẩu
        if old_password or new_password or confirm_password:
            if not all([old_password, new_password, confirm_password]):
                QMessageBox.warning(self.MainWindow, "Cảnh báo", 
                                  "Vui lòng điền đầy đủ thông tin mật khẩu!")
                return
            
            if new_password != confirm_password:
                QMessageBox.warning(self.MainWindow, "Cảnh báo", 
                                  "Mật khẩu mới và xác nhận không khớp!")
                return
            
            if len(new_password) < 6:
                QMessageBox.warning(self.MainWindow, "Cảnh báo", 
                                  "Mật khẩu mới phải có ít nhất 6 ký tự!")
                return
        
        try:
            self.mc.connect()
            
            # Cập nhật email
            sql_update = "UPDATE Users SET email = %s WHERE user_id = %s"
            self.mc.execute_query(sql_update, (new_email, self.current_user['user_id']))
            
            # Cập nhật password nếu có
            if new_password:
                # TODO: Cần verify old_password trước
                sql_password = "UPDATE Users SET password = %s WHERE user_id = %s"
                # Nên hash password trước khi lưu
                self.mc.execute_query(sql_password, (new_password, self.current_user['user_id']))
            
            QMessageBox.information(self.MainWindow, "Thành công", 
                                  "Cập nhật thông tin thành công!")
            
            # Xóa các trường password
            self.txtOldPassword.clear()
            self.txtNewPassword.clear()
            self.txtConfirmNewPassword.clear()
            
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", 
                               f"Lỗi khi cập nhật: {e}")

    def logout(self):
        """Đăng xuất và quay về màn hình login"""
        reply = QMessageBox.question(self.MainWindow, "Xác nhận",
                                     "Bạn có chắc muốn đăng xuất?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Quay về màn hình login
            from final_ml.ui.ui_login_signupExt import ui_login_signupExt
            from PyQt6.QtWidgets import QMainWindow
            
            self.login_window = QMainWindow()
            self.login_ui = ui_login_signupExt()
            self.login_ui.setupUi(self.login_window)
            self.login_window.show()
            self.MainWindow.close()