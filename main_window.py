import sys
from time import time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel,
                             QPushButton, QLineEdit, QFileDialog, QMessageBox, QApplication)
from system_files.card_recovery import *
from system_files.luhn_algorithm import luhn_algorithm


DEFAULT_FILE_SETTINGS = 'files/settings.json'


class RecoveryCardGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.are_settings_loaded = False
        self.setWindowTitle('Restore Card Number')
        self.setGeometry(100, 100, 500, 350)
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

    def check_luhn(self) -> None:
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            if not self.card_number:
                QMessageBox.information(
                    self, 'Сhecking the correctness of the card', 'The card number is incorrect.')
            else:
                mark = luhn_algorithm(self.card_number)
                self._restore_system.save_text(
                    self.card_number, self._restore_system.settings['card_number'])
                self._restore_system.save_text(
                    f'{self.card_number} is {mark}', self._restore_system.settings['result'])
                QMessageBox.information(
                    self, 'Сhecking the correctness of the card', 'The card number is correct.')
        except Exception as err:
            QMessageBox.information(
                self, 'Cheking the correctness of the card', f'Something went wrong.\n{err.__str__}')
            pass

    def restore_card_number(self) -> None:
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            if not self.number_cores_input.text():
                start = time()
                cores = mp.cpu_count()
                self.card_number = self._restore_system.recover_card_number(
                    self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin)
                end = time()
            else:
                start = time()
                cores = int(self.number_cores_input.text())
                self.card_number = self._restore_system.recover_card_number(
                    self._restore_system.hash, self._restore_system.last_symbols, self._restore_system.bin, cores)
                end = time()
            self._restore_system.save_stat(end-start, cores)
            QMessageBox.information(
                self, 'Restore Card Number', 'Successfull!')
        except Exception as err:
            QMessageBox.information(
                self, 'Restore Card Number', f'Something went wrong.\n{err.__str__}')

    def make_plot(self) -> None:
        if not self.are_settings_loaded:
            self.init_settings()
            return
        try:
            stats = self._restore_system.load_stat()
            x = stats.keys()
            y = stats.values()
            figure = plt.figure(figsize=(30, 5))
            plt.xlabel('Количество ядер')
            plt.ylabel('Время выполнения (сек)')
            plt.title('Гистограмма времени выполнения от количества ядер')
            plt.bar(x, y, color="orange", width=0.1)
            plt.show()
            self._restore_system.save_plot_image(figure)
        except Exception as err:
            QMessageBox.information(
                self, 'Build image', f'Something went wrong.\n{err.__str__}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RecoveryCardGUI()
    win.show()
    sys.exit(app.exec_())
