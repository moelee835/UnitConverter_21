"""GUI boundary (PRD A5, G1~G5) — PyQt6 only here."""

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import ParseError, parse_input
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import create_default_registry


class UnitConverterWindow(QMainWindow):
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        super().__init__()
        self._registry = registry or create_default_registry()
        self.setWindowTitle("Unit Converter")
        self._build_ui()
        self.convert_button.clicked.connect(self._on_convert)

    def _build_ui(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        unit_options = self._registry.names()

        self.from_unit = QComboBox()
        self.from_unit.addItems(unit_options)
        self.to_unit = QComboBox()
        self.to_unit.addItems(unit_options)
        self.value_input = QLineEdit()
        self.convert_button = QPushButton("Convert")
        self.result_label = QLabel()
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)

        layout.addWidget(QLabel("From unit"))
        layout.addWidget(self.from_unit)
        layout.addWidget(QLabel("To unit"))
        layout.addWidget(self.to_unit)
        layout.addWidget(QLabel("Value"))
        layout.addWidget(self.value_input)
        layout.addWidget(self.convert_button)
        layout.addWidget(QLabel("Result"))
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel("Error"))
        layout.addWidget(self.error_label)

        self.setCentralWidget(central)

    def _on_convert(self) -> None:
        raw = (
            f"{self.from_unit.currentText()}:"
            f"{self.value_input.text().strip()}:"
            f"{self.to_unit.currentText()}"
        )
        self.apply_input(raw)

    def apply_input(self, raw: str) -> None:
        self.error_label.clear()
        self.result_label.clear()
        try:
            parsed = parse_input(raw)
            lines = convert_parsed(parsed, self._registry)
            self.result_label.setText("\n".join(lines))
        except ParseError as err:
            self.error_label.setText(err.message)
        except ValueError as err:
            self.error_label.setText(str(err))

    def get_result_text(self) -> str:
        return self.result_label.text()


def main() -> None:
    app = QApplication.instance() or QApplication([])
    registry = create_default_registry()
    window = UnitConverterWindow(registry=registry)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
