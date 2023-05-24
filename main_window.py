import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from system_files.card_restore import *
from system_files.luhn_algorithm import luhn_algorithm


DEFAULT_FILE_SETTINGS = 'files/settings.json'


class RestoreCardGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_UI()
        self.are_settings_loaded = False

    def init_UI(self) -> None:
        self.setWindowTitle('Restore Card Number')
        self.setGeometry(100, 100, 500, 300)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.settings_load_label = QLabel(
            'Settings file:', self.central_widget)
        self.settings_load_label.setGeometry(50, 50, 100, 30)
        self.settings_load_button = QPushButton(
            'Load', self.central_widget)
        self.settings_load_button.setGeometry(200, 50, 100, 30)
        self.settings_load_button.clicked.connect(
            self.init_settings)
        self.number_cores_label = QLabel(
            'Number of cores:', self.central_widget)
        self.number_cores_label.setGeometry(50, 100, 100, 30)
        self.number_cores_input = QLineEdit(self.central_widget)
        self.number_cores_input.setGeometry(160, 100, 200, 30)
        self.restore_label = QLabel(
            'Restore card number:', self.central_widget)
        self.restore_label.setGeometry(50, 150, 110, 30)
        self.restore_button = QPushButton(
            'Restore', self.central_widget)
        self.restore_button.setGeometry(200, 150, 100, 30)
        self.restore_button.clicked.connect(
            self.restore_card_number)

    def init_settings(self) -> None:
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, 'Open Settings File', '', 'Settings Files (*.json)')
            self._restore_system = RecoverySystem(file_name)
            QMessageBox.information(
                self, 'Settings', f'Settings file successfully loaded from file {file_name}')
        except Exception as err:
            self._restore_system = RecoverySystem(DEFAULT_FILE_SETTINGS)
            QMessageBox.information(
                self, 'Settings', f'Settings file was not loaded from file {file_name}.'
                f'The default path was applied.\nPath: {DEFAULT_FILE_SETTINGS}')
        finally:    
            self.are_settings_loaded = True

    def restore_card_number(self) -> None:
        if not self.are_settings_loaded:
            self.init_settings()
            return
        if not self.number_cores_input.text():
            card_number = self._restore_system.recover_card_number(
                self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin)
        else:
            card_number = self._restore_system.recover_card_number(
                self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin, int(self.number_cores_input.text()))
        if not card_number:
            QMessageBox.information(
                self, 'Restore Card Number', 'Failed to find card number.')
        else:
            mark = luhn_algorithm(card_number)
            self._restore_system.save_text(card_number, self._restore_system.settings['card_number'])
            self._restore_system.save_text(
                f'{card_number} is {mark}', self._restore_system.settings['result'])
            QMessageBox.information(
                self, 'Restore Card Number', 'Search completed successfully.')
    
               


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RestoreCardGUI()
    win.show()
    sys.exit(app.exec_())
