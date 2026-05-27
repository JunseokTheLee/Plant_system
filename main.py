#vibe coded template test.




import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QFrame, QGridLayout,
    QSplitter, QListWidget, QListWidgetItem, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPalette, QFont

# ── Colour palette ──────────────────────────────────────────────────────────
TEAL       = "#1D9E75"
TEAL_LIGHT = "#E1F5EE"
AMBER_LIGHT= "#FAEEDA"
RED_LIGHT  = "#FCEBEB"
BG         = "#F8F8F6"
SURFACE    = "#FFFFFF"
BORDER     = "#E8E6E0"
TEXT       = "#1A1A18"
TEXT_MUT   = "#6B6966"
TEXT_FAINT = "#9E9C96"

PLANTS = [
    {
        "name": "Monstera deliciosa",
        "species": "Araceae family",
        "status": "Healthy",
        "schedule": "Water every 7–10 days. Bright indirect light. Mist leaves weekly.",
        "diseases": "Root rot, leaf spot, spider mites, yellowing from overwatering.",
        "last_scan": "April 20, 2026 — No issues detected",
        "color": TEAL_LIGHT,
        "pill": ("Healthy", "#EAF3DE", "#3B6D11"),
    },
    {
        "name": "Ficus lyrata",
        "species": "Moraceae family",
        "status": "Needs water",
        "schedule": "Water every 5–7 days. Full sun to bright indirect light.",
        "diseases": "Leaf drop, root rot, spider mites, bacterial leaf spot.",
        "last_scan": "April 18, 2026 — Slight wilting noted",
        "color": AMBER_LIGHT,
        "pill": ("Needs water", "#FAEEDA", "#633806"),
    },
    {
        "name": "Dracaena marginata",
        "species": "Asparagaceae family",
        "status": "Root rot risk",
        "schedule": "Water sparingly every 10–14 days. Indirect light.",
        "diseases": "Root rot, fluoride toxicity, spider mites, soft rot.",
        "last_scan": "April 21, 2026 — Soggy soil detected",
        "color": RED_LIGHT,
        "pill": ("Root rot risk", "#FCEBEB", "#791F1F"),
    },
    {
        "name": "Pothos aureus",
        "species": "Araceae family",
        "status": "Healthy",
        "schedule": "Water every 7 days. Tolerates low light well.",
        "diseases": "Root rot, bacterial wilt, Rhizoctonia blight.",
        "last_scan": "April 19, 2026 — No issues detected",
        "color": TEAL_LIGHT,
        "pill": ("Healthy", "#EAF3DE", "#3B6D11"),
    },
    {
        "name": "Aloe vera",
        "species": "Asphodelaceae family",
        "status": "Overwatered",
        "schedule": "Water every 2–3 weeks. Full sun. Very well-draining soil.",
        "diseases": "Root rot, aloe rust, soft rot, basal stem rot.",
        "last_scan": "April 17, 2026 — Overwatering signs",
        "color": AMBER_LIGHT,
        "pill": ("Overwatered", "#FAEEDA", "#633806"),
    },
    {
        "name": "Peace lily",
        "species": "Spathiphyllum sp.",
        "status": "Healthy",
        "schedule": "Water every 7 days. Low to medium indirect light.",
        "diseases": "Root rot, leaf blight, Cylindrocladium, mealybugs.",
        "last_scan": "April 20, 2026 — No issues detected",
        "color": TEAL_LIGHT,
        "pill": ("Healthy", "#EAF3DE", "#3B6D11"),
    },
]


def styled(widget, css):
    widget.setStyleSheet(css)
    return widget


# ── Sidebar ──────────────────────────────────────────────────────────────────
class Sidebar(QFrame):
    NAV = [
        ("Plant catalog",   "🌿", True),
        ("Scan image",      "📷", False),
        ("My scans",        "📋", False),
        ("Add / edit plants","➕", False),
        ("Manage users",    "👤", False),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet(f"background:{SURFACE}; border-right:1px solid {BORDER};")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 8, 0, 0)
        root.setSpacing(0)

        # Section header
        def section(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(f"color:{TEXT_FAINT}; font-size:10px; padding:10px 14px 4px;")
            return lbl

        root.addWidget(section("NAVIGATION"))

        for label, icon, active in self.NAV[:3]:
            root.addWidget(self._nav_item(label, icon, active))

        root.addWidget(section("ADMIN"))
        for label, icon, active in self.NAV[3:]:
            root.addWidget(self._nav_item(label, icon, active))

        root.addStretch()

        # User row
        user_row = QFrame()
        user_row.setStyleSheet(f"border-top:1px solid {BORDER};")
        ur = QHBoxLayout(user_row)
        ur.setContentsMargins(12, 10, 12, 12)
        avatar = QLabel("AD")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"background:{TEAL_LIGHT}; color:{TEAL}; border-radius:14px;"
            "font-size:11px; font-weight:600;"
        )
        name_col = QVBoxLayout()
        name_col.setSpacing(1)
        name_lbl = QLabel("Admin User")
        name_lbl.setStyleSheet(f"color:{TEXT}; font-size:12px; font-weight:600;")
        role_lbl = QLabel("Administrator")
        role_lbl.setStyleSheet(f"color:{TEXT_FAINT}; font-size:10px;")
        name_col.addWidget(name_lbl)
        name_col.addWidget(role_lbl)
        ur.addWidget(avatar)
        ur.addLayout(name_col)
        root.addWidget(user_row)

    def _nav_item(self, label, icon, active):
        btn = QPushButton(f"  {icon}  {label}")
        btn.setFlat(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if active:
            btn.setStyleSheet(
                f"text-align:left; padding:8px 14px; font-size:13px; font-weight:600;"
                f"color:{TEXT}; background:{BG}; border-left:2.5px solid {TEAL};"
                "border-radius:0;"
            )
        else:
            btn.setStyleSheet(
                f"text-align:left; padding:8px 14px; font-size:13px;"
                f"color:{TEXT_MUT}; border-left:2.5px solid transparent;"
                "border-radius:0;"
            )
        return btn


# ── Plant card ───────────────────────────────────────────────────────────────
class PlantCard(QFrame):
    def __init__(self, plant, on_select, parent=None):
        super().__init__(parent)
        self.plant = plant
        self.on_select = on_select
        self.selected = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(172, 140)
        self._build()
        self._apply_style()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Image area
        img = QLabel("🌱")
        img.setFixedHeight(72)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setStyleSheet(f"background:{self.plant['color']}; font-size:28px;")
        root.addWidget(img)

        # Body
        body = QWidget()
        body.setStyleSheet(f"background:{SURFACE};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(10, 8, 10, 8)
        bl.setSpacing(2)

        name = QLabel(self.plant["name"])
        name.setStyleSheet(f"color:{TEXT}; font-size:12px; font-weight:600;")
        name.setWordWrap(True)

        species = QLabel(self.plant["species"])
        species.setStyleSheet(f"color:{TEXT_FAINT}; font-size:10px;")

        pill_text, pill_bg, pill_fg = self.plant["pill"]
        pill = QLabel(pill_text)
        pill.setStyleSheet(
            f"background:{pill_bg}; color:{pill_fg}; border-radius:8px;"
            "font-size:10px; font-weight:600; padding:2px 7px;"
        )
        pill.setFixedHeight(18)

        bl.addWidget(name)
        bl.addWidget(species)
        bl.addWidget(pill)
        root.addWidget(body)

    def _apply_style(self):
        border = f"2px solid {TEAL}" if self.selected else f"1px solid {BORDER}"
        self.setStyleSheet(
            f"QFrame {{ border:{border}; border-radius:10px; background:{SURFACE}; }}"
        )

    def set_selected(self, val):
        self.selected = val
        self._apply_style()

    def mousePressEvent(self, _):
        self.on_select(self.plant)


# ── Detail panel ─────────────────────────────────────────────────────────────
class DetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        self.setStyleSheet(f"background:{SURFACE}; border-left:1px solid {BORDER};")

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(16, 16, 16, 16)
        self.root.setSpacing(12)

        # Image box
        self.img_box = QLabel("🌿")
        self.img_box.setFixedHeight(90)
        self.img_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_box.setStyleSheet(
            f"background:{TEAL_LIGHT}; border-radius:8px; font-size:36px;"
        )

        # Name / species
        self.name_lbl = QLabel("")
        self.name_lbl.setStyleSheet(f"color:{TEXT}; font-size:14px; font-weight:600;")
        self.name_lbl.setWordWrap(True)
        self.species_lbl = QLabel("")
        self.species_lbl.setStyleSheet(f"color:{TEXT_FAINT}; font-size:11px;")

        def divider():
            d = QFrame()
            d.setFrameShape(QFrame.Shape.HLine)
            d.setStyleSheet(f"color:{BORDER};")
            return d

        def info_block(label_text):
            lbl = QLabel(label_text.upper())
            lbl.setStyleSheet(f"color:{TEXT_FAINT}; font-size:10px; font-weight:600;")
            val = QLabel("")
            val.setWordWrap(True)
            val.setStyleSheet(f"color:{TEXT}; font-size:12px;")
            val.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            return lbl, val

        self.sched_lbl, self.sched_val   = info_block("Care schedule")
        self.dis_lbl,   self.dis_val     = info_block("Known diseases")
        self.scan_lbl,  self.scan_val    = info_block("Last scan")

        self.scan_btn = QPushButton("Scan this plant")
        self.scan_btn.setStyleSheet(
            f"background:{TEAL}; color:#fff; border:none; border-radius:8px;"
            "font-size:12px; font-weight:600; padding:8px;"
        )
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        for w in [
            self.img_box, self.name_lbl, self.species_lbl, divider(),
            self.sched_lbl, self.sched_val, divider(),
            self.dis_lbl, self.dis_val, divider(),
            self.scan_lbl, self.scan_val,
        ]:
            self.root.addWidget(w)

        self.root.addStretch()
        self.root.addWidget(self.scan_btn)

    def load(self, plant):
        self.img_box.setStyleSheet(
            f"background:{plant['color']}; border-radius:8px; font-size:36px;"
        )
        self.name_lbl.setText(plant["name"])
        self.species_lbl.setText(plant["species"])
        self.sched_val.setText(plant["schedule"])
        self.dis_val.setText(plant["diseases"])
        self.scan_val.setText(plant["last_scan"])


# ── Catalog grid ─────────────────────────────────────────────────────────────
class CatalogGrid(QWidget):
    def __init__(self, on_select, parent=None):
        super().__init__(parent)
        self.on_select = on_select
        self.cards = []
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"background:{BG};")

        inner = QWidget()
        inner.setStyleSheet(f"background:{BG};")
        self.grid = QGridLayout(inner)
        self.grid.setContentsMargins(16, 16, 16, 16)
        self.grid.setSpacing(12)

        for i, plant in enumerate(PLANTS):
            card = PlantCard(plant, self._card_selected)
            self.cards.append(card)
            self.grid.addWidget(card, i // 3, i % 3)

        scroll.setWidget(inner)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        self._card_selected(PLANTS[0])

    def _card_selected(self, plant):
        for card in self.cards:
            card.set_selected(card.plant is plant)
        self.on_select(plant)


# ── Top bar ───────────────────────────────────────────────────────────────────
class TopBar(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.setStyleSheet(
            f"background:{SURFACE}; border-bottom:1px solid {BORDER};"
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color:{TEXT}; font-size:14px; font-weight:600;")

        search = QLineEdit()
        search.setPlaceholderText("Search plants...")
        search.setFixedWidth(180)
        search.setStyleSheet(
            f"background:{BG}; border:1px solid {BORDER}; border-radius:7px;"
            f"padding:4px 10px; font-size:12px; color:{TEXT};"
        )

        add_btn = QPushButton("+ Add plant")
        add_btn.setStyleSheet(
            f"background:{TEAL}; color:#fff; border:none; border-radius:7px;"
            "font-size:12px; font-weight:600; padding:6px 14px;"
        )
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(title_lbl)
        layout.addStretch()
        layout.addWidget(search)
        layout.addWidget(add_btn)


# ── Main window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plant Manager")
        self.resize(1000, 620)
        self.setStyleSheet(f"background:{BG};")

        central = QWidget()
        self.setCentralWidget(central)
        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Sidebar
        sidebar = Sidebar()

        # Right side: topbar + content + detail
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        topbar = TopBar("Plant catalog")
        right_layout.addWidget(topbar)

        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(0)

        self.detail = DetailPanel()
        catalog = CatalogGrid(self.detail.load)

        content_row.addWidget(catalog)
        content_row.addWidget(self.detail)
        right_layout.addLayout(content_row)

        outer.addWidget(sidebar)
        outer.addWidget(right)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()