"""Starter Windows desktop app — PySide6 + SQLite.

Form (name, phone, notes) -> saves into a local SQLite database,
shows all saved records in a table, delete the selected one.
Run from source:  python main.py
Build the .exe:    pyinstaller app.spec
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import db

APP_STYLE = """
QMainWindow { background: #F4F7FA; }
QLabel { font-size: 13px; color: #1A4D7A; }
QLineEdit, QTextEdit {
    background: white; border: 1px solid #D5DDE5; border-radius: 6px;
    padding: 8px 10px; font-size: 14px; color: #1F2937;
}
QLineEdit:focus, QTextEdit:focus { border: 1px solid #06A7D7; }
QPushButton {
    background: #1A4D7A; color: white; border: none; border-radius: 6px;
    padding: 10px 18px; font-size: 14px; font-weight: 600;
}
QPushButton:hover { background: #06A7D7; }
QPushButton#danger { background: #DC2626; }
QPushButton#danger:hover { background: #B91C1C; }
QPushButton:disabled { background: #9CA3AF; }
QTableWidget { background: white; border: 1px solid #D5DDE5; border-radius: 6px;
    font-size: 13px; gridline-color: #E5E7EB; }
QHeaderView::section { background: #EAF6FC; color: #1A4D7A; font-weight: 600;
    padding: 8px; border: none; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = db.init_db()
        self.setWindowTitle("Customer Records")
        self.resize(760, 560)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Add Customer")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #102A43;")
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name *")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes")
        self.notes_input.setMaximumHeight(70)
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Phone"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.notes_input)

        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save)
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.clicked.connect(self.on_delete)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.delete_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        layout.addWidget(QLabel("Saved Records"))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Phone", "Notes", "Added On"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.setCentralWidget(root)
        self.refresh_table()

    def refresh_table(self):
        rows = db.list_records(self.conn)
        self.table.setRowCount(len(rows))
        for r, (record_id, name, phone, notes, created) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(name))
            self.table.setItem(r, 1, QTableWidgetItem(phone or ""))
            self.table.setItem(r, 2, QTableWidgetItem(notes or ""))
            self.table.setItem(r, 3, QTableWidgetItem(created))
            # Keep the id on the first cell so Delete knows which row it is.
            self.table.item(r, 0).setData(Qt.UserRole, record_id)
        self.delete_btn.setEnabled(len(rows) > 0)

    def on_save(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing name", "Please enter a name.")
            self.name_input.setFocus()
            return
        db.add_record(
            self.conn, name, self.phone_input.text(), self.notes_input.toPlainText()
        )
        self.name_input.clear()
        self.phone_input.clear()
        self.notes_input.clear()
        self.refresh_table()
        self.status.setText(f"Saved: {name}")

    def on_delete(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.information(
                self, "Nothing selected", "Please select a record first."
            )
            return
        row = selected[0].row()
        record_id = self.table.item(row, 0).data(Qt.UserRole)
        name = self.table.item(row, 0).text()
        answer = QMessageBox.question(
            self,
            "Delete record?",
            f'Delete "{name}"? This can\'t be undone.',
        )
        if answer == QMessageBox.Yes:
            db.delete_record(self.conn, record_id)
            self.refresh_table()
            self.status.setText(f"Deleted: {name}")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
