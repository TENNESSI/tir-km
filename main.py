import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                             QWidget, QFileDialog, QPushButton, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
# import os
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'C:\\\\Users\\Константин\\AppData\\Local\\Programs\\Python\\Python312' \
#                                             + '\\Lib\\site-packages\\PyQt5\\Qt5\\plugins'


class TargetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Электронная мишень")
        self.setGeometry(100, 100, 800, 700)

        self.background_image = None
        self.hits = []
        self.hit_radius = 5
        self.image_offset = QPoint(0, 0)  # Смещение изображения относительно виджета
        self.image_scale = 1.0  # Масштаб изображения

        # Виджеты
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.mousePressEvent = self.add_hit

        # Кнопки
        self.load_btn = QPushButton("Загрузить мишень")
        self.load_btn.clicked.connect(self.load_image)

        self.clear_btn = QPushButton("Очистить мишень")
        self.clear_btn.clicked.connect(self.clear_hits)

        self.save_btn = QPushButton("Сохранить результат")
        self.save_btn.clicked.connect(self.save_result)

        # Разметка
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.save_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_image(self):
        """Загружает изображение и вычисляет параметры отображения"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.bmp)"
        )
        if file_path:
            self.background_image = QPixmap(file_path)
            self.hits = []
            self.update_display()

    def add_hit(self, event):
        """Добавляет попадание с учетом смещения изображения"""
        if self.background_image:
            # Получаем реальные координаты внутри изображения
            x = event.pos().x() - self.image_offset.x()
            y = event.pos().y() - self.image_offset.y()

            # Проверяем, что клик был по изображению (а не по пустым полям)
            if 0 <= x < self.background_image.width() * self.image_scale and \
                    0 <= y < self.background_image.height() * self.image_scale:
                # Масштабируем координаты к оригинальному размеру
                original_x = int(x / self.image_scale)
                original_y = int(y / self.image_scale)
                self.hits.append(QPoint(original_x, original_y))
                self.update_display()

    def update_display(self):
        """Обновляет отображение с учетом центрирования"""
        if self.background_image:
            # Масштабируем изображение с сохранением пропорций
            scaled_pixmap = self.background_image.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            # Вычисляем смещение для центрирования
            self.image_offset = QPoint(
                (self.image_label.width() - scaled_pixmap.width()) // 2,
                (self.image_label.height() - scaled_pixmap.height()) // 2
            )

            # Масштаб для пересчета координат
            self.image_scale = scaled_pixmap.width() / self.background_image.width()

            # Рисуем попадания
            painter = QPainter(scaled_pixmap)
            painter.setPen(QPen(QColor(255, 0, 0), 3))

            for hit in self.hits:
                scaled_x = int(hit.x() * self.image_scale)
                scaled_y = int(hit.y() * self.image_scale)
                painter.drawEllipse(QPoint(scaled_x, scaled_y), self.hit_radius, self.hit_radius)

            painter.end()
            self.image_label.setPixmap(scaled_pixmap)

    def clear_hits(self):
        self.hits = []
        self.update_display()

    def save_result(self):
        if self.background_image and self.hits:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить результат",
                "мишень_с_попаданиями.png",
                "PNG (*.png)"
            )
            if file_path:
                result_pixmap = self.background_image.copy()
                painter = QPainter(result_pixmap)
                painter.setPen(QPen(QColor(255, 0, 0), 3))

                for hit in self.hits:
                    painter.drawEllipse(hit, self.hit_radius, self.hit_radius)

                painter.end()
                result_pixmap.save(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TargetApp()
    window.show()
    sys.exit(app.exec_())