import sys
from time import time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QProgressBar,
                             QPushButton, QLineEdit, QFileDialog, QMessageBox, QApplication)
from system_files.file_system import FilesSystem
from system_files.luhn_algorithm import luhn_algorithm
from system_files.make_plot import make_plot
from system_files.recovery_card import recover_card_number
import multiprocessing as mp
import matplotlib.pyplot as plt


DEFAULT_FILE_SETTINGS = 'files/settings.json'


class RecoveryCardGUI(QMainWindow):
    def __init__(self) -> None:
        """Initialization of the application window.
        """
        super().__init__()
        self.are_settings_loaded = False
        self.setWindowTitle('Restore Card Number')
        self.setGeometry(100, 100, 500, 350)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 300, 450, 25)
        self.pbar.setMaximum(100)
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
        self.plot_label = QLabel(
            'Building a histogram:', self.central_widget)
        self.plot_label.setGeometry(50, 200, 110, 30)
        self.plot_button = QPushButton(
            'Build', self.central_widget)
        self.plot_button.setGeometry(200, 200, 100, 30)
        self.plot_button.clicked.connect(
            self.make_plot)
        self.check_label = QLabel(
            'Checking card:', self.central_widget)
        self.check_label.setGeometry(50, 250, 110, 30)
        self.check_button = QPushButton(
            'Check', self.central_widget)
        self.check_button.setGeometry(200, 250, 100, 30)
        self.check_button.clicked.connect(
            self.check_luhn)

    def init_settings(self) -> None:
        """Settings initialization.
        """
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, 'Open Settings File', '', 'Settings Files (*.json)')
            self._restore_system = FilesSystem(file_name)
            QMessageBox.information(
                self, 'Settings', f'Settings file successfully loaded from file {file_name}')
        except Exception as err:
            self._restore_system = FilesSystem(DEFAULT_FILE_SETTINGS)
            QMessageBox.information(
                self, 'Settings', f'Settings file was not loaded from file {file_name}.'
                f'The default path was applied.\nPath: {DEFAULT_FILE_SETTINGS}')
        finally:
            self.are_settings_loaded = True

    def check_luhn(self) -> None:
        """Сhecking the card number for validity.
        """
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            card_number = self._restore_system.settings['card_number']
            if card_number == 0:
                QMessageBox.information(
                    self, 'Сhecking the correctness of the card', 'The card number is incorrect.')
            else:
                mark = luhn_algorithm(str(card_number))
                self._restore_system.settings['result'] = f'{card_number} is {mark}'
                self._restore_system.save_settings()
                QMessageBox.information(
                    self, 'Сhecking the correctness of the card', 'The card number is correct.')
        except Exception as err:
            QMessageBox.information(
                self, 'Cheking the correctness of the card', f'Something went wrong.\n{err.__str__}')
            pass

    def restore_card_number(self) -> None:
        """Selects the BIN cards for this hash.
        """
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            self.pbar.setValue(0)

            def update_progress(progress: int) -> None:
                self.pbar.setValue(progress)
            if not self.number_cores_input.text():
                start = time()
                cores = mp.cpu_count()
                card_number = recover_card_number(
                    self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin, update_progress)
                end = time()
            else:
                start = time()
                cores = int(self.number_cores_input.text())
                card_number = recover_card_number(
                    self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin, update_progress, cores)
                end = time()
            self.pbar.setValue(0)
            self._restore_system.settings['card_number'] = card_number
            self._restore_system.save_settings()
            self._restore_system.save_stat(end - start, cores)
        except Exception as err:
            QMessageBox.information(
                self, 'Restore Card Number', f'Something went wrong.\n{err.__str__}')

    def make_plot(self) -> None:
        """Creates a histogram using matplotlib.
        """
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            stats = self._restore_system.load_stat()
            self._restore_system.save_plot_image(make_plot(stats))
        except Exception as err:
            QMessageBox.information(
                self, 'Build image', f'Something went wrong.\n{err.__str__}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RecoveryCardGUI()
    win.show()
    sys.exit(app.exec_())
