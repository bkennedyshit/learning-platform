---
title: "Pyqt Minimal Apps"
subject: "_examples"
catalog: advanced
audience_tier: higher-education
chapter: "8.4"
type: examples
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [22.4 - PyQt6 & PySide6 - Signals, Slots & Event Loops](22.4---PyQt6-&-PySide6---Signals,-Slots-&-Event-Loops) | Part of [Subject_Plan](Subject_Plan)*

# 8.4 Examples — PyQt/PySide6 Minimal Apps

> Annotated minimal applications demonstrating core Qt patterns. Each example is self-contained and runnable.

---

## 1. Hello Window (Absolute Minimum)

```python
"""The simplest possible PySide6 application: a window with a label."""
import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

# Step 1: Create QApplication (MUST be first — initializes Qt internals)
# sys.argv allows Qt to parse command-line flags like -style or -platform
app = QApplication(sys.argv)

# Step 2: Create a widget. QLabel is the simplest visible widget.
# Without a parent, it becomes a top-level window.
label = QLabel("Hello, PySide6!")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
label.setFixedSize(300, 100)

# Step 3: Show the widget (posts a QShowEvent to the event queue)
label.show()

# Step 4: Enter the event loop. Blocks until app.quit() or last window closes.
# sys.exit() ensures the process returns the correct exit code.
sys.exit(app.exec())
```

**What this demonstrates:**
- `QApplication` must exist before any widget.
- A widget without a parent is a top-level window.
- `show()` makes it visible; `exec()` starts event processing.

---

## 2. Signals & Slots Demo (Custom Signals)

```python
"""Demonstrates custom signals, built-in signals, and slot connections."""
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QSpinBox,
)
from PySide6.QtCore import Signal, Slot, QObject


class TemperatureConverter(QWidget):
    """Widget that converts Celsius to Fahrenheit using signals."""

    # Custom signal: emitted when conversion is performed
    # Signal(float, float) means it carries two float values
    conversion_done = Signal(float, float)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature Converter")
        layout = QVBoxLayout(self)

        # Input row
        input_row = QHBoxLayout()
        self.celsius_input = QSpinBox()
        self.celsius_input.setRange(-273, 1000)
        self.celsius_input.setSuffix(" °C")
        input_row.addWidget(QLabel("Celsius:"))
        input_row.addWidget(self.celsius_input)
        layout.addLayout(input_row)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        layout.addWidget(self.convert_btn)

        # Result label
        self.result_label = QLabel("Result: —")
        layout.addWidget(self.result_label)

        # History label (demonstrates signal chaining)
        self.history_label = QLabel("Last conversion: none")
        layout.addWidget(self.history_label)

        # ─── Signal Connections ───────────────────────────────────
        # Built-in signal → custom slot
        self.convert_btn.clicked.connect(self.perform_conversion)

        # Custom signal → multiple slots (one signal, many receivers)
        self.conversion_done.connect(self.display_result)
        self.conversion_done.connect(self.update_history)

        # Built-in signal with value → lambda slot
        # QSpinBox.valueChanged emits the new int value
        self.celsius_input.valueChanged.connect(
            lambda val: self.result_label.setText("Result: —")  # Reset on change
        )

    @Slot()
    def perform_conversion(self):
        """Slot: triggered by button click."""
        celsius = self.celsius_input.value()
        fahrenheit = celsius * 9 / 5 + 32
        # Emit our custom signal with both values
        self.conversion_done.emit(celsius, fahrenheit)

    @Slot(float, float)
    def display_result(self, celsius, fahrenheit):
        """Slot: displays the conversion result."""
        self.result_label.setText(f"Result: {celsius}°C = {fahrenheit:.1f}°F")

    @Slot(float, float)
    def update_history(self, celsius, fahrenheit):
        """Slot: updates history (demonstrates multiple slots per signal)."""
        self.history_label.setText(f"Last conversion: {celsius}°C → {fahrenheit:.1f}°F")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TemperatureConverter()
    widget.show()
    sys.exit(app.exec())
```

---

## 3. QThread Worker (Background Processing)

```python
"""Demonstrates the correct QThread worker pattern with progress and cancellation."""
import sys
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QProgressBar, QLabel, QTextEdit,
)
from PySide6.QtCore import QObject, QThread, Signal, Slot


class PrimeWorker(QObject):
    """Finds prime numbers in a range. Runs in a separate thread."""

    # Signals for communicating results back to the main thread
    progress = Signal(int)          # Percentage complete
    prime_found = Signal(int)       # Each prime number found
    finished = Signal(int)          # Total primes found
    error = Signal(str)             # Error message

    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self._cancelled = False

    @Slot()
    def find_primes(self):
        """Main work method. Runs in worker thread."""
        count = 0
        try:
            for num in range(2, self.limit + 1):
                # Check cancellation (flag set from main thread)
                if self._cancelled:
                    self.finished.emit(count)
                    return

                # Check if prime
                if self._is_prime(num):
                    count += 1
                    self.prime_found.emit(num)

                # Emit progress every 100 numbers
                if num % 100 == 0:
                    percent = int((num / self.limit) * 100)
                    self.progress.emit(percent)

            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    @Slot()
    def cancel(self):
        """Thread-safe cancellation via flag."""
        self._cancelled = True


class MainWindow(QWidget):
    """Main window with start/cancel buttons and progress display."""

    cancel_requested = Signal()  # Signal to tell worker to stop

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prime Finder (QThread Demo)")
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout(self)

        self.status = QLabel("Ready. Will find primes up to 10,000.")
        self.progress_bar = QProgressBar()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)

        self.start_btn = QPushButton("Start")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)

        layout.addWidget(self.status)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.cancel_btn)

        self.start_btn.clicked.connect(self.start_work)
        self.cancel_btn.clicked.connect(self.cancel_work)

        self.thread = None

    def start_work(self):
        """Set up worker thread and start processing."""
        # Create fresh thread and worker for each run
        self.thread = QThread()
        self.worker = PrimeWorker(limit=10000)

        # Move worker to thread (changes thread affinity)
        self.worker.moveToThread(self.thread)

        # Wire up signals
        self.thread.started.connect(self.worker.find_primes)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.prime_found.connect(self.on_prime_found)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.cancel_requested.connect(self.worker.cancel)

        # Cleanup chain
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # UI state
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.log.clear()
        self.status.setText("Finding primes...")

        self.thread.start()

    def cancel_work(self):
        self.cancel_requested.emit()
        self.status.setText("Cancelling...")

    @Slot(int)
    def on_prime_found(self, prime):
        # Only log every 50th prime to avoid flooding the text edit
        if prime < 100 or prime % 50 == 1:
            self.log.append(f"Found prime: {prime}")

    @Slot(int)
    def on_finished(self, total):
        self.status.setText(f"Done! Found {total} primes.")
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(100)

    @Slot(str)
    def on_error(self, msg):
        self.status.setText(f"Error: {msg}")
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

---

## 4. Custom QPainter Widget (Animated Ring)

```python
"""Custom widget with QPainter rendering and QTimer animation."""
import sys
import math
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QTimer, QRectF


class AnimatedRing(QWidget):
    """A spinning ring with animated segments."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPainter Animation")
        self.setFixedSize(300, 300)

        self._angle = 0  # Current rotation angle

        # QTimer: emits timeout() signal at regular intervals
        # Connected to our rotation update method
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._advance_angle)
        self.timer.start(16)  # ~60 FPS (1000ms / 60 ≈ 16ms)

    def _advance_angle(self):
        """Slot: advance rotation and request repaint."""
        self._angle = (self._angle + 3) % 360
        self.update()  # Schedule repaint (coalesced — efficient)

    def paintEvent(self, event):
        """Paint the animated ring."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Center the coordinate system
        painter.translate(self.width() / 2, self.height() / 2)

        # Draw multiple arc segments with varying opacity
        radius = 100
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)

        for i in range(12):
            # Each segment is offset by 30 degrees
            segment_angle = i * 30 + self._angle
            # Opacity fades for trailing segments (creates motion blur effect)
            opacity = 1.0 - (i / 12.0) * 0.8

            color = QColor(66, 135, 245)
            color.setAlphaF(opacity)

            pen = QPen(color, 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            # drawArc uses 1/16th degree units
            start = int(segment_angle * 16)
            span = int(20 * 16)  # Each segment spans 20 degrees
            painter.drawArc(rect, start, span)

        # Draw center text
        painter.setPen(QPen(QColor(200, 200, 200)))
        painter.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        painter.drawText(QRectF(-50, -15, 100, 30), Qt.AlignmentFlag.AlignCenter, f"{self._angle}°")

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AnimatedRing()
    widget.show()
    sys.exit(app.exec())
```

---

## 5. Model/View/Delegate (Editable Table)

```python
"""Model/View pattern with custom model, editable cells, and styled delegate."""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView,
    QStyledItemDelegate, QLineEdit, QHeaderView,
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QPainter, QBrush


class ContactModel(QAbstractTableModel):
    """Custom table model storing contact data."""

    COLUMNS = ["Name", "Email", "Phone", "Department"]

    def __init__(self):
        super().__init__()
        self._data = [
            ["Alice Johnson", "alice@example.com", "555-0101", "Engineering"],
            ["Bob Smith", "bob@example.com", "555-0102", "Design"],
            ["Charlie Brown", "charlie@example.com", "555-0103", "Marketing"],
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.COLUMNS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self._data[index.row()][index.column()]
        if role == Qt.ItemDataRole.BackgroundRole:
            # Alternate row colors for readability
            if index.row() % 2 == 0:
                return QColor(45, 45, 50)
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """Called when user edits a cell."""
        if role == Qt.ItemDataRole.EditRole and index.isValid():
            self._data[index.row()][index.column()] = value
            # Emit dataChanged to notify the view that this cell needs repaint
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        """Make cells editable."""
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.COLUMNS[section]
            return str(section + 1)
        return None

    def add_contact(self, name, email, phone, dept):
        """Insert a new row and notify the view."""
        row = self.rowCount()
        # beginInsertRows/endInsertRows notify the view about structural changes
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.append([name, email, phone, dept])
        self.endInsertRows()


class DepartmentDelegate(QStyledItemDelegate):
    """Custom delegate that color-codes the Department column."""

    DEPT_COLORS = {
        "Engineering": QColor(76, 175, 80, 80),
        "Design": QColor(156, 39, 176, 80),
        "Marketing": QColor(255, 152, 0, 80),
    }

    def paint(self, painter, option, index):
        # Only customize the Department column (index 3)
        if index.column() == 3:
            dept = index.data()
            color = self.DEPT_COLORS.get(dept, QColor(100, 100, 100, 50))

            painter.save()
            painter.fillRect(option.rect, QBrush(color))
            painter.setPen(QColor(220, 220, 220))
            painter.drawText(
                option.rect.adjusted(8, 0, 0, 0),
                Qt.AlignmentFlag.AlignVCenter,
                dept or "",
            )
            painter.restore()
        else:
            super().paint(painter, option, index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Manager (Model/View)")
        self.setMinimumSize(700, 400)

        # Create model
        self.model = ContactModel()

        # Create view and connect to model
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setItemDelegate(DepartmentDelegate())

        # Configure view appearance
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(False)  # We handle this in the model

        self.setCentralWidget(self.table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

---

*See also: [22.4 - PyQt6 & PySide6 - Signals, Slots & Event Loops](22.4---PyQt6-&-PySide6---Signals,-Slots-&-Event-Loops) for the full architectural deep-dive.*

---

## Related Notes
- [8.1_react_nextjs_starter](8.1_react_nextjs_starter) - Same _examples folder
- [8.2_angular_starter](8.2_angular_starter) - Same _examples folder
- [8.5_flutter_dart_patterns](8.5_flutter_dart_patterns) - Same _examples folder
- [8.3_vite_config_recipes](8.3_vite_config_recipes) - Same _examples folder
