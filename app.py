import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel

from forms.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.setupUi(self)
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'ff84e7f3-328d-4f10-b875-a97c40735b9e'
        ll_spn = 'll=37.530887,55.703118&spn=0.002,0.002'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.map_canvas.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
