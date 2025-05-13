import sys
import os
import random
from collections import defaultdict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QTextEdit, QWidget, QSizePolicy
)
from PySide6.QtGui import QIcon, QColor, QFont, QPixmap, QFontMetricsF, QCursor, QDesktopServices
from PySide6.QtCore import Qt, QUrl


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Функция для загрузки QSS-стиля из файла 💕
def load_stylesheet():
    qss_path = resource_path("style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


class AutoScaleLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 14))
        self.setMinimumSize(1, 1)  # Убираем фиксированную высоту
        self.setTextFormat(Qt.PlainText)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.setWordWrap(False)  # Отключаем перенос, чтобы работало масштабирование
        self.setMinimumSize(1, 30)  # Минимальная высота = 30px

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_size()

    def setText(self, text):
        super().setText(text)
        self._update_font_size()

    def _update_font_size(self):
        if not self.text():
            return

        font = self.font()
        metrics = QFontMetricsF(font)

        available_width = self.width() - 10
        available_height = self.height() - 4  # Учитываем высоту

        text_width = metrics.horizontalAdvance(self.text())
        text_height = metrics.height()

        if text_width == 0 or text_height == 0 or available_width == 0 or available_height == 0:
            return

        scale_w = available_width / text_width
        scale_h = available_height / text_height
        scale = min(scale_w, scale_h)

        new_size = font.pointSizeF() * scale

        max_font_size = 13
        min_font_size = 6

        new_size = max(min_font_size, min(max_font_size, new_size))

        font.setPointSize(int(new_size))
        self.setFont(font)


# Ооооой, тут будет моя карта эмодзи, детка! 💋
emoji_map = {}


# Функция для создания карты эмодзи. Можно даже задать seed, чтобы всё было фиксированно, как моя диета 🍑
def generate_emoji_map(seed=1):
    global emoji_map
    random.seed(seed)
    emoji_map.clear()
    # Ой, вот мой любимый список девчачьих эмодзи! Тут всё самое важное для настроения 🫶
    emoji_pool = [
        "💋", "👠", "💄", "🎀", "💅", "💗", "🩷", "👛", "🧸", "⛓️",
        "🐷", "🍼", "💍", "🔥", "💎", "👑", "🩸", "💔", "🫶", "😼",
        "😈", "🫦", "💘", "👅", "🍑", "🍒", "🍓", "🪷", "🥵", "🍾",
        "📱", "💌", "🧁", "🍭", "🍬", "🍹", "🥂", "🤤", "🤍", "🫶",
        "🩱", "👢", "👡", "✨", "💖", "💓", "💞", "💃🏼", "😵‍💫", "💦",
        "🫧", "🔞", "💃", "👩‍🦳", "🖤", "😏", "🍷", "🧃", "😻", "🧴",
    ]
    # А вот и буквы, которые мы будем шифровать, как секретики в дневнике 📓
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    emoji_map.clear()  # Очищаем старый мап, потому что я люблю всё обновлять 💅
    emoji_usage = defaultdict(int)

    # Проверяем, можно ли использовать этот эмодзи на этой позиции, чтобы не было повторов, как у меня с бывшими 😏
    def can_use_emoji(emoji, position, letter_map):
        for other_letter, emojis in letter_map.items():
            if position < len(emojis) and emojis[position] == emoji:
                return False
        return True

    # Делим эмодзи по буквам, как конфетки между подружками 🍬
    for letter in letters:
        emoji_map[letter] = []
        while len(emoji_map[letter]) < 100:  # Каждой букве по 100 эмодзи, чтобы хватило на все настроения 💕
            emoji = random.choice(emoji_pool)
            position = len(emoji_map[letter])
            # Проверяем, что эмодзи ещё не использован слишком много раз, как мой любимый блеск для губ 💋
            if emoji_usage[emoji] < 100 and can_use_emoji(emoji, position, emoji_map):
                emoji_map[letter].append(emoji)
                emoji_usage[emoji] += 1


# Превращаем текст в эмодзи, как магию настроения 🪄
def text_to_emoji(text):
    emoji_result = []
    count_result = []
    for letter in text.upper():
        if letter.isalpha() and letter in emoji_map:
            emoji_list = emoji_map[letter]
            selected_emoji = random.choice(emoji_list)
            emoji_result.append(selected_emoji)
            count_result.append(emoji_list.index(selected_emoji) + 1)
    return emoji_result, count_result


# Расшифровываем эмодзи обратно в текст, как секретное послание от подруги 💌
def decrypt_message(numerical_key, emoji_input):
    reverse_emoji_map = {v: k for k, values in emoji_map.items() for v in values}
    decrypted_message = []
    for num, emoji in zip(numerical_key, emoji_input):
        letter = reverse_emoji_map.get(emoji, '')
        for letter_in_map, emojis in emoji_map.items():
            if emojis[num - 1] == emoji:
                decrypted_message.append(letter_in_map)
                break
    result = ''.join(decrypted_message)
    # Замены на пробел
    result = result.replace("ПРБЕЛ", " ")
    result = result.replace("SPCE", " ")
    return result


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        with open(resource_path("style.qss"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # Генерируем начальную карту эмодзи, чтобы всё было готово к работе, как мой маникюр 💅
        generate_emoji_map()

        self.setWindowTitle("Bimbo CRY 💕")
        self.setGeometry(100, 100, 600, 400)

        # Загружаем стиль из файла 💕
        self.setStyleSheet(load_stylesheet())

        # Устанавливаем иконку окна, как мой аватар в соцсетях 🌟
        if getattr(sys, 'frozen', False):
            icon_path = f"{sys._MEIPASS}/ico.ico"
        else:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ico.ico")
        self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Подсказка для ввода текста, чтобы ты знала, что делать, детка 😘
        input_label = QLabel("CRY Here 😭:")
        input_label.setObjectName("input_label")
        input_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(input_label)

        # Поле для ввода текста, как дневник моих секретов 📝
        self.input_text = QLineEdit()
        self.input_text.setObjectName("input_text")
        main_layout.addWidget(self.input_text)

        # Кнопка для копирования ввода, потому что я люблю делиться своими мыслями 📋
        copy_input_button = QPushButton("Copy Input Secret 💅")
        copy_input_button.setObjectName("copy_input_button")
        copy_input_button.setCursor(Qt.PointingHandCursor)
        copy_input_button.clicked.connect(self.copy_input_text)
        main_layout.addWidget(copy_input_button)

        # Кнопка для шифрования текста, как мои секретные записочки 💖
        convert_button = QPushButton("CRY to Mood 💖")
        convert_button.setObjectName("convert_button")
        convert_button.setCursor(Qt.PointingHandCursor)
        convert_button.clicked.connect(self.on_convert_click)
        main_layout.addWidget(convert_button)

        # Тут будут показываться эмодзи, как мои эмоции в чате 💞
        self.emoji_output_label = AutoScaleLabel("")
        self.emoji_output_label.setObjectName("emoji_output_label")
        self.emoji_output_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.emoji_output_label)

        # Кнопка для копирования эмодзи, чтобы поделиться настроением с подругами 💕
        copy_emoji_button = QPushButton("Copy Your Mood 💞")
        copy_emoji_button.setObjectName("copy_emoji_button")
        copy_emoji_button.setCursor(Qt.PointingHandCursor)
        copy_emoji_button.clicked.connect(self.copy_emoji_text)
        main_layout.addWidget(copy_emoji_button)

        # Тут будет ключ, как пароль от моего инстаграма 🔑
        self.count_output_label = AutoScaleLabel("")
        self.count_output_label.setObjectName("count_output_label")
        self.count_output_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.count_output_label)

        # Кнопка для копирования ключа, чтобы не забыть свои секреты 🤫
        copy_count_button = QPushButton("Copy Mood Key 🔑")
        copy_count_button.setObjectName("copy_count_button")
        copy_count_button.setCursor(Qt.PointingHandCursor)
        copy_count_button.clicked.connect(self.copy_count_text)
        main_layout.addWidget(copy_count_button)

        # Кнопка для копирования всего сразу, как мой макияж — всё и сразу 😏
        copy_all_button = QPushButton("Copy Combined Secrets 😢")
        copy_all_button.setObjectName("copy_all_button")
        copy_all_button.setCursor(Qt.PointingHandCursor)
        copy_all_button.clicked.connect(self.copy_all_text)
        main_layout.addWidget(copy_all_button)

        # Seed functionality — это типа фиксатор настроения, чтобы всё было стабильно, как мой педикюр 🌱
        seed_layout = QHBoxLayout()
        seed_label = QLabel("Seed:")
        seed_label.setObjectName("seed_label")
        seed_layout.addWidget(seed_label)
        self.seed_input = QLineEdit()
        self.seed_input.setObjectName("seed_input")
        seed_layout.addWidget(self.seed_input)
        # Кнопка для установки seed, как мой выбор помады — всегда фиксированный 🌸
        seed_button = QPushButton("Set Seed 🤤")
        seed_button.setObjectName("seed_button")
        seed_button.setCursor(Qt.PointingHandCursor)
        seed_button.clicked.connect(self.set_seed)
        seed_layout.addWidget(seed_button)
        main_layout.addLayout(seed_layout)

        # Дешифратор — это как раскрытие секретов, но только для своих 💔
        decrypt_frame = QFrame()
        decrypt_frame.setObjectName("decrypt_frame")
        decrypt_layout = QVBoxLayout()

        decrypt_emoji_label = QLabel("Input Your Mood (With Space) 💕:")
        decrypt_emoji_label.setObjectName("decrypt_emoji_label")
        decrypt_emoji_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_emoji_label)

        self.decrypt_emoji_input = QLineEdit()
        self.decrypt_emoji_input.setObjectName("decrypt_emoji_input")
        decrypt_layout.addWidget(self.decrypt_emoji_input)

        decrypt_key_label = QLabel("Input your Mood key 🔑:")
        decrypt_key_label.setObjectName("decrypt_key_label")
        decrypt_key_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_key_label)

        self.decrypt_key_input = QLineEdit()
        self.decrypt_key_input.setObjectName("decrypt_key_input")
        decrypt_layout.addWidget(self.decrypt_key_input)

        # Кнопка для дешифровки, как чтение чужого дневника 💔
        decrypt_button = QPushButton("Mood to CRY 💔")
        decrypt_button.setObjectName("decrypt_button")
        decrypt_button.setCursor(Qt.PointingHandCursor)
        decrypt_button.clicked.connect(self.on_decrypt_click)
        decrypt_layout.addWidget(decrypt_button)

        # Тут будет расшифрованный текст, как мои признания ❤️
        self.decrypted_message_label = AutoScaleLabel("")
        self.decrypted_message_label.setObjectName("decrypted_message_label")
        self.decrypted_message_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(self.decrypted_message_label)

        # Кнопка для копирования расшифрованного текста, чтобы поделиться секретами 🌟
        copy_decrypted_button = QPushButton("Copy Decrypted Secret ✨")
        copy_decrypted_button.setObjectName("copy_decrypted_button")
        copy_decrypted_button.setCursor(Qt.PointingHandCursor)
        copy_decrypted_button.clicked.connect(self.copy_decrypted_text)
        decrypt_layout.addWidget(copy_decrypted_button)

        # Новое поле для ввода данных в формате "эмодзи - ключ" 🎀
        decrypt_combined_label = AutoScaleLabel("Input Data (Mood - Mood Key):")
        decrypt_combined_label.setObjectName("decrypt_combined_label")
        decrypt_combined_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_combined_label)

        self.decrypt_combined_input = QLineEdit()
        self.decrypt_combined_input.setObjectName("decrypt_combined_input")
        decrypt_layout.addWidget(self.decrypt_combined_input)

        decrypt_combined_button = QPushButton("🤫 Reveal Combined Secrets 💕")
        decrypt_combined_button.setObjectName("decrypt_combined_button")
        decrypt_combined_button.setCursor(Qt.PointingHandCursor)
        decrypt_combined_button.clicked.connect(self.on_decrypt_combined_click)
        decrypt_layout.addWidget(decrypt_combined_button)

        clear_combined_button = QPushButton("🧼 Clear Combined Secrets")
        clear_combined_button.setObjectName("clear_combined_button")
        clear_combined_button.setCursor(Qt.PointingHandCursor)
        clear_combined_button.clicked.connect(self.clear_combined_input)
        decrypt_layout.addWidget(clear_combined_button)

        decrypt_frame.setLayout(decrypt_layout)
        main_layout.addWidget(decrypt_frame)

        class ClickableLabel(QLabel):
            def __init__(self, url, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.url = url
                self.setCursor(QCursor(Qt.PointingHandCursor))

            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                    QDesktopServices.openUrl(QUrl(self.url))

        #Контейнер для двух картинок на одной строке 💕💕
        images_container = QWidget()
        images_hbox = QHBoxLayout()
        images_hbox.setContentsMargins(0, 0, 0, 0)
        images_hbox.setSpacing(0)

        left_image_label = ClickableLabel("https://github.com/R3DCyclops", self)
        left_image_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        left_pixmap = QPixmap(resource_path("Group3.png"))
        if not left_pixmap.isNull():
            left_pixmap = left_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            left_image_label.setPixmap(left_pixmap)
        else:
            left_image_label.setText("Left image not found!")

        right_image_label = ClickableLabel("https://github.com/R3DCyclops/Bimbo_CRY", self)
        right_image_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        right_pixmap = QPixmap(resource_path("Group2.png"))
        if not right_pixmap.isNull():
            right_pixmap = right_pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            right_image_label.setPixmap(right_pixmap)
        else:
            right_image_label.setText("Right image not found!")

        #Собираем всё вместе: stretch + Group3 + отступ + Group2, как ночёвка у лучших подружек💖
        images_hbox.addStretch()
        images_hbox.addWidget(left_image_label)
        images_hbox.addSpacing(12)
        images_hbox.addWidget(right_image_label)
        images_container.setLayout(images_hbox)
        main_layout.addWidget(images_container)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def clear_combined_input(self):
        self.decrypt_combined_input.clear()

    # Шифруем текст, как мои мысли в чате с подругами 💖
    def on_convert_click(self):
        text = self.input_text.text()
        emoji_result, count_result = text_to_emoji(text)
        self.emoji_output_label.setText(" ".join(emoji_result))
        self.count_output_label.setText(" ".join(map(str, count_result)))

    # Копируем ввод, чтобы не забыть, что я написала 📋
    def copy_input_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.input_text.text())

    # Копируем эмодзи, как мои эмоции в сторис 💕
    def copy_emoji_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.emoji_output_label.text())

    # Копируем ключ, как пароль от моего вайфаю 🔑
    def copy_count_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.count_output_label.text())

    # Копируем всё сразу, как мой образ — полностью готовый 😏
    def copy_all_text(self):
        emoji_result = self.emoji_output_label.text()
        count_result = self.count_output_label.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(f"{emoji_result} - {count_result}")

    # Дешифруем текст, как раскрываем секреты 💔
    def on_decrypt_click(self):
        try:
            numerical_key = list(map(int, self.decrypt_key_input.text().split()))
            emoji_input = self.decrypt_emoji_input.text().split()
            decrypted_message = decrypt_message(numerical_key, emoji_input)
            self.decrypted_message_label.setText(decrypted_message)
        except ValueError:
            self.decrypted_message_label.setText("Invalid input!")

    # Копируем расшифрованный текст, чтобы поделиться секретами 🌟
    def copy_decrypted_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.decrypted_message_label.text())

    # Устанавливаем seed, как мой выбор платья — всегда фиксированный 🌸
    def set_seed(self):
        try:
            seed = int(self.seed_input.text())
            generate_emoji_map(seed)
            self.emoji_output_label.setText("Emoji map updated with new seed!")
        except ValueError:
            self.emoji_output_label.setText("Invalid seed! Please enter a number.")

    # Дешифруем данные из поля "эмодзи - ключ" 🎀
    def on_decrypt_combined_click(self):
        try:
            combined_input = self.decrypt_combined_input.text()
            emoji_part, key_part = combined_input.split(" - ")
            emoji_input = emoji_part.split()
            numerical_key = list(map(int, key_part.split()))
            decrypted_message = decrypt_message(numerical_key, emoji_input)
            self.decrypted_message_label.setText(decrypted_message)
        except Exception:
            self.decrypted_message_label.setText("Invalid format! Use 'emoji - key'.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
