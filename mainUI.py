import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFrame,
    QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea,
    QFileDialog, QInputDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect

from model.infer import predict
import db


def load_pixmap(image_path):
    """Loads a QPixmap from a local file path or a Supabase Storage URL."""
    if not image_path:
        return QPixmap()
    if image_path.startswith("http://") or image_path.startswith("https://"):
        try:
            resp = requests.get(image_path, timeout=10)
            resp.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(resp.content)
            return pixmap
        except Exception:
            return QPixmap()
    return QPixmap(image_path)


CARD_W, CARD_H = 265, 165
CARD_COLUMNS = 3


class PlantCard(QFrame):
    def __init__(self, plant, on_select):
        super().__init__()

        self.plant = plant
        self.on_select = on_select
        self.active = False

        self.setFixedSize(CARD_W, CARD_H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def set_active(self, active):
        if self.active == active:
            return
        self.active = active
        self._apply_style()
        self.update()

    def _apply_style(self):
        if self.active:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 6px solid #1D9E75;
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_select(self.plant)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        margin = 12
        image_height = 70
        image_rect = QRect(margin, margin, w - margin * 2, image_height)

        image_path = self.plant.get("image_path")
        if image_path:
            pixmap = load_pixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    image_rect.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter.drawPixmap(image_rect, pixmap)
        else:
             
             placeholder = QFont("Arial", 20)
             painter.setFont(placeholder)
             painter.setPen(QPen(QColor("#9e9e9e")))
             painter.drawText(image_rect, Qt.AlignmentFlag.AlignCenter, "placeholder")

        name_font = QFont("Arial", 14)
        painter.setFont(name_font)
        painter.setPen(QPen(QColor("#111111")))
        name = QFontMetrics(name_font).elidedText(
            self.plant["name"], Qt.TextElideMode.ElideRight, w - 2 * margin
        )
        painter.drawText(margin, margin + image_height + 22, name)

        painter.setFont(QFont("Arial", 10))
        painter.setPen(QPen(QColor("#6b6966")))
        painter.drawText(margin, margin + image_height + 40, f"Last status: {self.plant['status']}")


class DetailPanel(QFrame):
    def __init__(self, on_scan):
        super().__init__()

        self.on_scan = on_scan
        self.plant = None

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

        self.title = QLabel("")
        self.title.setFont(QFont("Arial", 24))
        self.title.setStyleSheet("border: none;")

        self.status = QLabel("")
        self.status.setFont(QFont("Arial", 20))
        self.status.setStyleSheet("border: none;")

        self.desc = QLabel("")
        self.desc.setFont(QFont("Arial", 14))
        self.desc.setStyleSheet("border: none;")
        self.desc.setWordWrap(True)

        text_layout.addWidget(self.title)
        text_layout.addWidget(self.status)
        text_layout.addSpacing(12)
        text_layout.addWidget(self.desc)
        text_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_box = QLabel()
        self.image_box.setFixedSize(165, 165)
        self.image_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_box.setFont(QFont("Arial", 90))
        self.image_box.setScaledContents(True)

        self.filename = QLabel("")
        self.filename.setFont(QFont("Arial", 12))
        self.filename.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filename.setStyleSheet("border: none;")

        self.scan_btn = QPushButton("Scan")
        self.scan_btn.setFixedSize(90, 33)
        self.scan_btn.setFont(QFont("Arial", 16))
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                border: none;
                border-radius: 3px;
            }
        """)
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.clicked.connect(self._scan_clicked)

        right_layout.addWidget(self.image_box)
        right_layout.addWidget(self.filename)
        right_layout.addWidget(self.scan_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(text_layout)
        main_layout.addStretch()
        main_layout.addLayout(right_layout)

        self.load(None)

    def _scan_clicked(self):
        if self.plant is not None:
            self.on_scan(self.plant)

    def load(self, plant):
        self.plant = plant

        if plant is None:
            self.title.setText("No plant selected")
            self.status.setText("")
            self.desc.setText("Add a plant or pick one from the catalog above.")
            self._set_image(None)
            self.filename.setText("")
            self.scan_btn.setEnabled(False)
            return

        self.scan_btn.setEnabled(True)
        self.title.setText(plant["name"])
        self.status.setText(f"Last Status: {plant['status']}")
        self.desc.setText(plant.get("description", ""))
        self._set_image(plant.get("image_path"))
        self.filename.setText(plant.get("image_path") or "No image set")

    def _set_image(self, image_path):
        pixmap = load_pixmap(image_path) if image_path else None
        if pixmap and not pixmap.isNull():
            self.image_box.setPixmap(pixmap)
            self.image_box.setText("")
            self.image_box.setStyleSheet("""
                QLabel {
                    background-color: #dedede;
                    border: 2px solid black;
                }
            """)
        else:
            self.image_box.setPixmap(QPixmap())
            self.image_box.setText("+")
            self.image_box.setStyleSheet("""
                QLabel {
                    background-color: #dedede;
                    color: #9e9e9e;
                    border: 2px solid black;
                }
            """)


class PlantApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plant UI")
        self.resize(1280, 832)
        self.setStyleSheet("background-color: white;")

        self.plants = self._load_plants()
        self.cards = []

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────
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
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.add_plant)

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
        admin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        admin_btn.clicked.connect(self.show_admin_placeholder)

        logout_btn = QPushButton("Log Out")
        logout_btn.setFixedSize(240, 49)
        logout_btn.setFont(QFont("Arial", 15))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9d9;
                border: none;
            }
        """)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self.close)

        sidebar_layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # ── Content ──────────────────────────────────────────────────────
        content = QFrame()
        content.setStyleSheet("background-color: white; border: none;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(48, 40, 18, 0)
        content_layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background-color: white; border: none;")

        grid_holder = QWidget()
        grid_holder.setStyleSheet("background-color: white;")
        self.grid = QGridLayout(grid_holder)
        self.grid.setHorizontalSpacing(55)
        self.grid.setVerticalSpacing(30)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(grid_holder)
        content_layout.addWidget(scroll, stretch=1)

        self.detail_panel = DetailPanel(on_scan=self.scan_plant)
        content_layout.addWidget(self.detail_panel)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self._rebuild_grid()
        self.select_plant(self.plants[0])

    def _load_plants(self):
        sample = [
            {
                "name": "Sample Plant",
                "status": "Healthy",
                "description": "Click Scan to preview a leaf photo, or use Add/Edit Plant to add your own.",
                "image_path": "plant.jpeg",
            },
            {
                "name": "Sample Plant 2",
                "status": "Healthy",
                "description": "Click Scan to preview a leaf photo, or use Add/Edit Plant to add your own.",
                "image_path": "plant.jpeg",
            },
        ]

        try:
            rows = db.fetch_plants()
        except Exception as e:
            print(f"[db] Could not reach Supabase, running with local-only data: {e}")
            return sample

        if rows:
            return rows

        # First run against an empty database: seed it with the sample plants.
        seeded = []
        for plant in sample:
            try:
                seeded.append(db.insert_plant(**plant))
            except Exception as e:
                print(f"[db] Could not seed sample plant: {e}")
                seeded.append(plant)
        return seeded

    def _rebuild_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self.cards = []
        for i, plant in enumerate(self.plants):
            card = PlantCard(plant, self.select_plant)
            self.cards.append(card)
            self.grid.addWidget(card, i // CARD_COLUMNS, i % CARD_COLUMNS)

    def select_plant(self, plant):
        for card in self.cards:
            card.set_active(card.plant is plant)
        self.detail_panel.load(plant)

    def add_plant(self):
        name, ok = QInputDialog.getText(self, "Add Plant", "Plant name:")
        if not ok or not name.strip():
            return

        local_image_path, _ = QFileDialog.getOpenFileName(
            self, "Choose a photo for this plant", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        image_url = local_image_path or None
        if local_image_path:
            try:
                image_url = db.upload_image(local_image_path)
            except Exception as e:
                print(f"[db] Image upload failed, keeping local path: {e}")
                image_url = local_image_path

        plant = {
            "name": name.strip(),
            "status": "Unknown",
            "description": "No scan performed yet.",
            "image_path": image_url,
        }

        try:
            plant = db.insert_plant(**plant)
        except Exception as e:
            print(f"[db] Could not save plant to Supabase, keeping it local-only: {e}")

        self.plants.append(plant)
        self._rebuild_grid()
        self.select_plant(plant)

    def scan_plant(self, plant):
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Choose a leaf photo to scan", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not image_path:
            return

        try:
            label, confidence = predict(image_path)
        except Exception as e:
            QMessageBox.warning(self, "Scan failed", f"Could not run detection:\n{e}")
            return

        crop, condition = label.split("___", 1)
        condition = condition.replace("_", " ")

        image_url = image_path
        try:
            image_url = db.upload_image(image_path)
        except Exception as e:
            print(f"[db] Image upload failed, keeping local path: {e}")

        plant["image_path"] = image_url
        plant["status"] = condition
        plant["description"] = f"Detected on {crop.replace('_', ' ')}: {condition} ({confidence:.0%} confidence)"

        if plant.get("id"):
            try:
                db.update_plant(
                    plant["id"],
                    image_path=plant["image_path"],
                    status=plant["status"],
                    description=plant["description"],
                )
            except Exception as e:
                print(f"[db] Could not save scan result to Supabase: {e}")

        self._rebuild_grid()
        self.select_plant(plant)

    def show_admin_placeholder(self):
        QMessageBox.information(self, "Admin", "Admin tools aren't implemented yet.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantApp()
    window.show()
    sys.exit(app.exec())
