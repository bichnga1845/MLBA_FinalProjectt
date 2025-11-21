from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure
import qtawesome as qta

from final_ml.connector.ml_connector import FinalConnector


SQL_UPLOADS_BY_USER = """
    SELECT
        COALESCE(NULLIF(usr.full_name, ''), usr.email, CONCAT('User #', usr.user_id)) AS user_label,
        COUNT(up.upload_id) AS total_uploads
    FROM uploads up
    JOIN users usr ON up.user_id = usr.user_id
    GROUP BY usr.user_id, user_label
    ORDER BY total_uploads DESC
"""

SQL_FRUIT_TYPES = """
    SELECT
        COALESCE(NULLIF(p.fruit_type, ''), 'KhÃ¡c') AS fruit_type,
        COUNT(*) AS total_predictions
    FROM predictions p
    GROUP BY fruit_type
    ORDER BY total_predictions DESC
"""

SQL_QUALITY_LABELS = """
    SELECT
        COALESCE(NULLIF(p.quality_label, ''), 'Unknown') AS quality_label,
        COUNT(*) AS total_records
    FROM predictions p
    GROUP BY quality_label
    ORDER BY total_records DESC
"""


@dataclass(frozen=True)
class StatisticCard:
    key: str
    title: str
    description: str
    icon: str
    sql: str
    chart: str
    colors: Tuple[str, str] | None = None


class StatisticsWindow(QMainWindow):
    """Standalone statistics dashboard window."""

    CARDS: Tuple[StatisticCard, ...] = (
        StatisticCard(
            key="uploads",
            title="Bar chart: Lượt upload theo người dùng",
            description="Theo dõi người dùng hoạt động nhiều hay ít",
            icon="fa5s.user-friends",
            sql=SQL_UPLOADS_BY_USER,
            chart="bar",
            colors=("#2D7A4E", "#81C784"),
        ),
        StatisticCard(
            key="fruit_pie",
            title="Pie chart: Tỷ lệ dự đoán theo loại trái cây",
            description="Loại trái cây xuất hiện nhiều nhất",
            icon="fa5s.apple-alt",
            sql=SQL_FRUIT_TYPES,
            chart="pie",
            colors=("#FFB74D", "#4DB6AC")
        ),
        StatisticCard(
            key="quality",
            title="Bar chart: Chất lượng Good vs Bad",
            description="Số lượng nhãn chất lượng",
            icon="fa5s.balance-scale",
            sql=SQL_QUALITY_LABELS,
            chart="bar_quality",
            colors=("#2E7D32", "#E53935"),
        ),
    )
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Dashboard Thống kê - Fruit ML")
        self.resize(1400, 850)
        self.mc = FinalConnector()
        self.datasets: Dict[str, Dict[str, Sequence]] = {}
        self.active_key: str | None = None
        self.cards_group = QButtonGroup(self)
        self.cards_group.setExclusive(True)
        self.card_buttons: Dict[str, QPushButton] = {}

        self._setup_ui()
        self.load_all_statistics()

    # --- UI setup -------------------------------------------------
    def _setup_ui(self) -> None:
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(scroll_area)

        central = QWidget()
        scroll_area.setWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(32, 28, 32, 28)
        root_layout.setSpacing(20)

        header = QLabel("Kho dữ liệu thống kê")
        header.setStyleSheet("font-size:32px; font-weight:700; color:#154734; margin-bottom: 8px;")
        root_layout.addWidget(header)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color:#2D7A4E; font-size:13px;")
        self.status_label.setVisible(False)
        root_layout.addWidget(self.status_label)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)
        root_layout.addLayout(content_layout, stretch=1)

        # Left navigation cards
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_frame.setMaximumWidth(380)
        nav_frame.setStyleSheet(
            """
            QFrame#navFrame {
                background: white;
                border: 2px solid #E0E7E4;
                border-radius: 16px;
            }
            """
        )
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(16, 16, 16, 16)
        nav_layout.setSpacing(10)

        for idx, card in enumerate(self.CARDS, start=1):
            button = QPushButton()
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            use_rich_text = hasattr(button, "setTextFormat")
            button.setProperty("useRichText", use_rich_text)
            icon = qta.icon(card.icon, color="#0A8754")
            button.setIcon(icon)
            button.setIconSize(QSize(32, 32))
            button.setStyleSheet(
                """
                QPushButton {
                    text-align: left;
                    padding: 14px;
                    border-radius: 12px;
                    border: 2px solid rgba(10, 135, 84, 0.15);
                    background: rgba(10, 135, 84, 0.05);
                    font-size: 14px;
                    font-weight: 600;
                    color: #0C2B1B;
                    min-height: 45px;
                }
                QPushButton:hover {
                    background: rgba(10, 135, 84, 0.1);
                    border-color: rgba(10, 135, 84, 0.3);
                }
                QPushButton:checked {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 #2D7A4E, stop:1 #4A9D6E);
                    color: white;
                    border-color: transparent;
                }
                QPushButton:checked span {
                    color: rgba(255,255,255,0.8);
                }
                """
            )
            if use_rich_text:
                button.setTextFormat(Qt.TextFormat.RichText)
                desc_text = (
                    f"<span style='color:rgba(12,43,27,0.65); font-size:13px;'>{card.description}</span>"
                )
                button.setText(f"({idx}) {card.title}<br>{desc_text}")
            else:
                button.setText(f"({idx}) {card.title}\n{card.description}")
            button.clicked.connect(lambda _, key=card.key: self.render_view(key))
            self.cards_group.addButton(button)
            self.card_buttons[card.key] = button
            nav_layout.addWidget(button)

        nav_layout.addStretch()
        content_layout.addWidget(nav_frame)

        # Right detail area (table + chart)
        detail_layout = QVBoxLayout()
        detail_layout.setSpacing(18)
        content_layout.addLayout(detail_layout, stretch=3)

        # Table section
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(12)

        self.view_title = QLabel("")
        self.view_title.setStyleSheet("font-size:20px; font-weight:700; color:#2D7A4E;")
        table_layout.addWidget(self.view_title)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                color: #2D7A4E;
                font-size: 13px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(220)
        self.table.setMaximumHeight(260)
        table_layout.addWidget(self.table)

        self.btnRefresh = QPushButton("Làm mới dữ liệu")
        self.btnRefresh.setIcon(qta.icon("fa5s.sync-alt", color="white"))
        self.btnRefresh.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #2D7A4E, stop:1 #4A9D6E);
                border: none;
                color: white;
                padding: 10px 18px;
                border-radius: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #246A3F, stop:1 #2D7A4E);
            }
            """
        )
        self.btnRefresh.clicked.connect(self.load_all_statistics)
        table_layout.addWidget(self.btnRefresh, alignment=Qt.AlignmentFlag.AlignRight)

        detail_layout.addWidget(table_container)

        # Chart section
        chart_container = QFrame()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        chart_layout.setSpacing(10)

        self.chartCanvas = FigureCanvas(Figure(figsize=(8, 4)))
        self.chartCanvas.figure.patch.set_facecolor("#FFFFFF")
        self.chartCanvas.setMinimumHeight(320)
        self.toolbar = NavigationToolbar2QT(self.chartCanvas, self)

        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.chartCanvas, stretch=1)
        detail_layout.addWidget(chart_container, stretch=1)
    # --- Data loading & rendering --------------------------------
    def load_all_statistics(self) -> None:
        """Fetch every statistics dataset."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.status_label.setText("Đang tải dữ liệu thống kê...")
        try:
            conn = self.mc.connect()
            if conn is None:
                raise RuntimeError("Không thể kết nối cơ sở dữ liệu")

            datasets: Dict[str, Dict[str, Sequence]] = {}
            for card in self.CARDS:
                columns, rows = self._execute_query(conn, card.sql)
                datasets[card.key] = {"columns": columns, "rows": rows}
            self.datasets = datasets

            default_key = self.active_key or self.CARDS[0].key
            self._check_card(default_key)
            self.render_view(default_key)
            self.status_label.setVisible(False)
        except Exception as exc:
            self.status_label.setVisible(True)
            self.status_label.setText(f"Lỗi tải dữ liệu: {exc}")
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self._render_empty_chart("Không có dữ liệu để hiển thị")
        finally:
            QApplication.restoreOverrideCursor()
            try:
                self.mc.disConnect()
            except Exception:
                pass

    def _execute_query(self, conn, sql: str) -> Tuple[List[str], List[Tuple]]:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = list(cursor.column_names)
        cursor.close()
        return columns, rows

    def _check_card(self, key: str) -> None:
        for card_key, button in self.card_buttons.items():
            button.setChecked(card_key == key)

    def render_view(self, key: str) -> None:
        """Update table & chart for selected statistic."""
        card = next((c for c in self.CARDS if c.key == key), None)
        if card is None:
            return

        self.active_key = key
        dataset = self.datasets.get(key, {"columns": [], "rows": []})
        columns = dataset.get("columns", [])
        rows = dataset.get("rows", [])

        self.view_title.setText(card.title)
        self._populate_table(columns, rows)
        self._render_chart(card, rows)

    def _populate_table(self, columns: Sequence[str], rows: Sequence[Sequence]) -> None:
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(rows))
        for r, data_row in enumerate(rows):
            for c, value in enumerate(data_row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def _render_chart(self, card: StatisticCard, rows: Sequence[Sequence]) -> None:
        if not rows:
            self._render_empty_chart("KKhông có dữ liệu cho biểu đồ này")
            return

        labels = [str(row[0]) for row in rows]
        values = [float(row[1]) if len(row) > 1 else 0 for row in rows]

        self.chartCanvas.figure.clear()
        ax = self.chartCanvas.figure.add_subplot(111)
        ax.set_facecolor("#FFFFFF")

        if card.chart == "pie":
            ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                counterclock=False,
                textprops={'fontsize': 14, 'weight': 'bold'},
            )
            ax.axis("equal")
        elif card.chart == "bar_quality":
            colors = card.colors or ("#2D7A4E", "#FF7043")
            mapped_colors = [
                colors[0] if "good" in label.lower() else colors[1] for label in labels
            ]
            bars = ax.bar(labels, values, color=mapped_colors)
            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{value:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=14,
                    fontweight='bold',
                )
        else:  # default bar
            bars = ax.bar(labels, values, color="#2D7A4E")
            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{value:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=14,
                    fontweight='bold',
                )

        ax.set_ylabel("Số Lượng", fontsize=14, fontweight='bold')
        ax.set_xlabel("", fontsize=14)
        if len(labels) > 0:
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=13)
        ax.tick_params(axis='y', labelsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        try:
            self.chartCanvas.figure.tight_layout()
        except:
            pass
        self.chartCanvas.draw()

    def _render_empty_chart(self, message: str) -> None:
        self.chartCanvas.figure.clear()
        ax = self.chartCanvas.figure.add_subplot(111)
        ax.axis("off")
        ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color="#5C6F65")
        self.chartCanvas.figure.tight_layout()
        self.chartCanvas.draw()
