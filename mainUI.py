import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFrame,
    QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRect


class PlantCard(QFrame):
    def __init__(self, active=False, image_path=None):
        super().__init__()

        self.active = active
        self.image_path = image_path

        self.setFixedSize(265, 165)

        if active:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 10px solid #24e62d;
                    border-radius: 18px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 2px solid #b5b5b5;
                    border-radius: 15px;
                }
            """)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        if self.active:
            margin = 10
            image_height = 60

            image_rect = QRect(margin, margin, w - margin * 2, image_height)

            if self.image_path:
                pixmap = QPixmap(self.image_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(
                        image_rect.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    painter.drawPixmap(image_rect, pixmap)

            painter.setPen(QPen(QColor("#111111")))
            painter.setFont(QFont("Arial", 15))
            painter.drawText(20, 105, "Plant Name Plant Name")

            painter.setFont(QFont("Arial", 11))
            painter.drawText(20, 132, "Last Status:")

        else:
            painter.setPen(QPen(QColor("#b5b5b5"), 2))
            painter.drawLine(0, 95, w, 95)


class DetailPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(280)

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #b5b5b5;
                border-radius: 28px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 20)
        main_layout.setSpacing(30)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)

        title = QLabel("Plant Name Plant Name")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("border: none;")

        status = QLabel("Last Status: Healthy")
        status.setFont(QFont("Arial", 23))
        status.setStyleSheet("border: none;")

        desc = QLabel("Additional Description")
        desc.setFont(QFont("Arial", 14))
        desc.setStyleSheet("border: none;")

        text_layout.addWidget(title)
        text_layout.addWidget(status)
        text_layout.addSpacing(12)
        text_layout.addWidget(desc)
        text_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_box = QLabel()
        image_box.setFixedSize(165, 165)
        image_box.setStyleSheet("""
            QLabel {
                background-color: #dedede;
                border: 2px solid black;
                border-radius: 0px;
            }
        """)
        image_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_box.setFont(QFont("Arial", 90))
        image_box.setText("+")
        image_box.setStyleSheet("""
            QLabel {
                background-color: #dedede;
                color: #9e9e9e;
                border: 2px solid black;
            }
        """)

        filename = QLabel("asdf.jpg")
        filename.setFont(QFont("Arial", 13))
        filename.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filename.setStyleSheet("border: none;")

        scan_btn = QPushButton("Scan")
        scan_btn.setFixedSize(90, 33)
        scan_btn.setFont(QFont("Arial", 21))
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                border: none;
                border-radius: 3px;
            }
        """)

        right_layout.addWidget(image_box)
        right_layout.addWidget(filename)
        right_layout.addWidget(scan_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(text_layout)
        main_layout.addStretch()
        main_layout.addLayout(right_layout)


class PlantApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plant UI")
        self.setFixedSize(1280, 832)
        self.setStyleSheet("background-color: white;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(290)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 2px solid #b5b5b5;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 82, 20, 43)
        sidebar_layout.setSpacing(0)

        add_btn = QPushButton("Add/Edit Plant")
        add_btn.setFixedSize(240, 51)
        add_btn.setFont(QFont("Arial", 15))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                border: none;
            }
        """)

        sidebar_layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addStretch()

        admin_btn = QPushButton("Admin")
        admin_btn.setFixedSize(254, 52)
        admin_btn.setFont(QFont("Arial", 15))
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #b5b5b5;
                border-radius: 25px;
            }
        """)

        logout_btn = QPushButton("Log Out")
        logout_btn.setFixedSize(240, 49)
        logout_btn.setFont(QFont("Arial", 15))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                border: none;
            }
        """)

        sidebar_layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        content = QFrame()
        content.setStyleSheet("background-color: white; border: none;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(48, 78, 18, 0)
        content_layout.setSpacing(0)

        grid = QGridLayout()
        grid.setHorizontalSpacing(55)
        grid.setVerticalSpacing(47)

        plant_image = "plant.jpeg"

        positions = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        for i, pos in enumerate(positions):
            if i == 0:
                card = PlantCard(active=True, image_path=plant_image)
            else:
                card = PlantCard(active=False)

            grid.addWidget(card, pos[0], pos[1])

        content_layout.addLayout(grid)
        content_layout.addStretch()

        detail_panel = DetailPanel()
        content_layout.addWidget(detail_panel)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantApp()
    window.show()
    sys.exit(app.exec())