from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QWidget,
)


PRIMARY_GREEN: Final = "#0A8754"
SECONDARY_GREEN: Final = "#63C382"
DEEP_FOREST: Final = "#0C2B1B"
GOLDEN_CITRUS: Final = "#F5C453"
LIGHT_SAGE: Final = "#EFF8F1"
PALE_MINT: Final = "#F8FFFB"
EMERALD_DARK: Final = "#03502F"
EMERALD_MID: Final = "#0E6B3C"
EMERALD_SOFT: Final = "#2AA15B"

FONT_STACK: Final = '"Poppins", "Segoe UI", "Helvetica Neue", Arial, sans-serif'

GLOBAL_STYLE: Final = f"""
* {{
    font-family: {FONT_STACK};
    color: {DEEP_FOREST};
}}

QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {PALE_MINT},
        stop:0.5 {LIGHT_SAGE},
        stop:1 #E4F4EA);
}}

QFrame#GlassCard {{
    background: rgba(255, 255, 255, 230);
    border-radius: 22px;
    border: 1px solid rgba(10, 135, 84, 0.08);
    padding: 32px;
}}

QLabel#Headline {{
    font-size: 34px;
    font-weight: 600;
    letter-spacing: -0.5px;
}}

QLabel#Subtitle {{
    font-size: 15px;
    color: rgba(12, 43, 27, 0.7);
}}

QPushButton {{
    border-radius: 16px;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 600;
    background-color: {PRIMARY_GREEN};
    color: white;
    border: none;
}}

QPushButton[secondary="true"] {{
    background-color: white;
    color: {PRIMARY_GREEN};
    border: 1px solid rgba(10, 135, 84, 0.35);
}}

QPushButton:hover {{
    background-color: {SECONDARY_GREEN};
}}

QLineEdit,
QComboBox,
QDateEdit,
QSpinBox,
QDoubleSpinBox,
QTextEdit,
QPlainTextEdit {{
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid rgba(10, 135, 84, 0.25);
    background: rgba(255, 255, 255, 0.9);
    selection-background-color: {PRIMARY_GREEN};
    selection-color: white;
    font-size: 14px;
    color: {PRIMARY_GREEN};
}}

QLineEdit::placeholder,
QPlainTextEdit::placeholder {{
    color: rgba(10, 135, 84, 0.55);
}}

QLineEdit[pill="true"],
QComboBox[pill="true"] {{
    border-radius: 999px;
    padding: 13px 22px;
    font-size: 15px;
    border: 1.8px solid rgba(255, 255, 255, 0.4);
    background: rgba(255, 255, 255, 0.92);
    color: {PRIMARY_GREEN};
}}

QLineEdit[pill="true"]::placeholder {{
    color: rgba(10, 135, 84, 0.6);
}}

QComboBox QAbstractItemView {{
    background-color: white;
    border: 2px solid #E0E7E4;
    border-radius: 10px;
    selection-background-color: #E8F5E9;
    selection-color: {PRIMARY_GREEN};
    color: {PRIMARY_GREEN};
    padding: 4px;
}}

QComboBox QAbstractItemView::item {{
    padding: 10px;
    border-radius: 6px;
    color: {PRIMARY_GREEN};
}}

QTableView {{
    background: transparent;
    border: none;
    alternate-background-color: rgba(255,255,255,0.6);
    gridline-color: rgba(10, 135, 84, 0.25);
    font-size: 13px;
}}

QHeaderView::section {{
    background: rgba(10, 135, 84, 0.08);
    border: none;
    padding: 12px;
    font-weight: 600;
}}

QScrollBar:vertical {{
    background: #F8FAF9;
    width: 14px;
    margin: 0px;
    border-radius: 7px;
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #2D7A4E, stop:1 #4A9D6E);
    border-radius: 7px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 #246A3F, stop:1 #2D7A4E);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
    height: 0px;
}}

QScrollBar:horizontal {{
    background: #F8FAF9;
    height: 14px;
    margin: 0px;
    border-radius: 7px;
}}

QScrollBar::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #2D7A4E, stop:1 #4A9D6E);
    border-radius: 7px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        stop:0 #246A3F, stop:1 #2D7A4E);
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    border: none;
    background: none;
    width: 0px;
}}
"""


def apply_global_styles(widget: QWidget, extra_styles: str | None = None) -> None:
    """Apply the shared stylesheet to any window/container."""
    combined = GLOBAL_STYLE
    if extra_styles:
        combined += "\n" + extra_styles
    widget.setStyleSheet(combined)


def create_glass_card(parent: QWidget | None = None, padding: int = 32) -> QFrame:
    """
    Create a rounded translucent card with soft drop shadow, similar to a modern web tile.
    """
    frame = QFrame(parent)
    frame.setObjectName("GlassCard")
    effect = QGraphicsDropShadowEffect(blurRadius=40, xOffset=0, yOffset=20)
    effect.setColor(QColor(10, 135, 84, 45))
    frame.setGraphicsEffect(effect)
    frame.setStyleSheet(f"QFrame#GlassCard {{ padding: {padding}px; }}")
    return frame


@dataclass(frozen=True)
class AccentBadge:
    text: str
    background: str = GOLDEN_CITRUS
    foreground: str = DEEP_FOREST

    def stylesheet(self) -> str:
        return (
            "background-color: "
            f"{self.background}; color: {self.foreground}; "
            "border-radius: 20px; padding: 6px 18px; "
            "font-weight: 600;"
        )


def create_gradient_panel(
    parent: QWidget | None = None,
    *,
    start_color: str = EMERALD_MID,
    end_color: str = EMERALD_DARK,
    radius: int = 32,
) -> QFrame:
    """
    Create a hero-like gradient panel reminiscent of the provided layout.
    """
    panel = QFrame(parent)
    panel.setObjectName("HeroPanel")
    effect = QGraphicsDropShadowEffect(blurRadius=50, xOffset=0, yOffset=15)
    effect.setColor(QColor(5, 64, 36, 80))
    panel.setGraphicsEffect(effect)
    panel.setStyleSheet(
        f"""
        QFrame#HeroPanel {{
            border-radius: {radius}px;
            padding: 36px;
            background: qradialgradient(
                cx:0.2, cy:0.2, radius:1,
                fx:0.3, fy:0.2,
                stop:0 {EMERALD_SOFT},
                stop:0.4 {start_color},
                stop:1 {end_color}
            );
            color: white;
        }}
        """
    )
    return panel
