import sys
import os
import random
from collections import defaultdict
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QTextEdit, QWidget
)
from PySide6.QtGui import QIcon, QColor, QFont, QPixmap, QFontMetricsF
from PySide6.QtCore import Qt

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
# Кастомный QLabel для масштабирования выходного текста в зависимости от размера окошка 💋
class AutoScaleLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 14))
        self.setMinimumSize(1, 20)
        self.setTextFormat(Qt.PlainText)

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
        text_width = metrics.horizontalAdvance(self.text())

        if text_width == 0 or available_width == 0:
            return

        scale = available_width / text_width
        new_size = font.pointSizeF() * scale

        # Ограничиваем размер шрифта, мы же не хотим, чтобы наш шрифт был слишком большим 🧃
        max_font_size = 13  # Максимальный размер 💘
        min_font_size = 1   # Минимальный размер 🧸
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
        
        # Генерируем начальную карту эмодзи, чтобы всё было готово к работе, как мой маникюр 💅
        generate_emoji_map()

        self.setWindowTitle("Bimbo CRY 💕")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2e2e2e; color: white;")
        
        # Устанавливаем иконку окна, как мой аватар в соцсетях 🌟
        if getattr(sys, 'frozen', False):
            # Если приложение запущено как .exe
            icon_path = f"{sys._MEIPASS}/ico.ico"
        else:
            # Если приложение запущено как скрипт
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ico.ico")  # Путь к иконке
        
        self.setWindowIcon(QIcon(icon_path))
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Подсказка для ввода текста, чтобы ты знала, что делать, детка 😘
        input_label = QLabel("CRY Here 😭:")
        input_label.setFont(QFont("Helvetica", 14))
        input_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(input_label)
        
        # Поле для ввода текста, как дневник моих секретов 📝
        self.input_text = QLineEdit()
        self.input_text.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.input_text.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(self.input_text)
        
        # Кнопка для копирования ввода, потому что я люблю делиться своими мыслями 📋
        copy_input_button = QPushButton("Copy Input Secret 💅")
        copy_input_button.clicked.connect(self.copy_input_text)
        copy_input_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        copy_input_button.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(copy_input_button)
        
        # Кнопка для шифрования текста, как мои секретные записочки 💖
        convert_button = QPushButton("CRY to Mood 💖")
        convert_button.clicked.connect(self.on_convert_click)
        convert_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        convert_button.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(convert_button)
        
        # Тут будут показываться эмодзи, как мои эмоции в чате 💞
        self.emoji_output_label = AutoScaleLabel("")
        self.emoji_output_label.setFont(QFont("Arial", 14))
        self.emoji_output_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.emoji_output_label)
        
        # Кнопка для копирования эмодзи, чтобы поделиться настроением с подругами 💕
        copy_emoji_button = QPushButton("Copy Your Mood 💞")
        copy_emoji_button.clicked.connect(self.copy_emoji_text)
        copy_emoji_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        copy_emoji_button.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(copy_emoji_button)
        
        # Тут будет ключ, как пароль от моего инстаграма 🔑
        self.count_output_label = AutoScaleLabel("")
        self.count_output_label.setFont(QFont("Arial", 14))
        self.count_output_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.count_output_label)
        
        # Кнопка для копирования ключа, чтобы не забыть свои секреты 🤫
        copy_count_button = QPushButton("Copy Mood Key 🔑")
        copy_count_button.clicked.connect(self.copy_count_text)
        copy_count_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        copy_count_button.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(copy_count_button)
        
        # Кнопка для копирования всего сразу, как мой макияж — всё и сразу 😏
        copy_all_button = QPushButton("Copy Combined Secrets 😢")
        copy_all_button.clicked.connect(self.copy_all_text)
        copy_all_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        copy_all_button.setFont(QFont("Helvetica", 12))
        main_layout.addWidget(copy_all_button)
        
        # Seed functionality — это типа фиксатор настроения, чтобы всё было стабильно, как мой педикюр 🌱
        seed_layout = QHBoxLayout()
        seed_label = QLabel("Seed:")
        seed_label.setFont(QFont("Helvetica", 12))
        seed_layout.addWidget(seed_label)
        
        self.seed_input = QLineEdit()
        self.seed_input.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.seed_input.setFont(QFont("Helvetica", 12))
        seed_layout.addWidget(self.seed_input)
        
        # Кнопка для установки seed, как мой выбор помады — всегда фиксированный 🌸
        seed_button = QPushButton("Set Seed 🤤")
        seed_button.clicked.connect(self.set_seed)
        seed_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        seed_button.setFont(QFont("Helvetica", 12))
        seed_layout.addWidget(seed_button)
        
        main_layout.addLayout(seed_layout)
        
        # Дешифратор — это как раскрытие секретов, но только для своих 💔
        decrypt_frame = QFrame()
        decrypt_frame.setFrameStyle(QFrame.Box)
        decrypt_frame.setStyleSheet("background-color: #2e2e2e;")
        decrypt_layout = QVBoxLayout()
        
        decrypt_emoji_label = QLabel("Input Your Mood (With Space) 💕:")
        decrypt_emoji_label.setFont(QFont("Helvetica", 12))
        decrypt_emoji_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_emoji_label)
        
        self.decrypt_emoji_input = QLineEdit()
        self.decrypt_emoji_input.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.decrypt_emoji_input.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(self.decrypt_emoji_input)
        
        decrypt_key_label = QLabel("Input your Mood key 🔑:")
        decrypt_key_label.setFont(QFont("Helvetica", 12))
        decrypt_key_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_key_label)
        
        self.decrypt_key_input = QLineEdit()
        self.decrypt_key_input.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.decrypt_key_input.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(self.decrypt_key_input)
        
        # Кнопка для дешифровки, как чтение чужого дневника 💔
        decrypt_button = QPushButton("Mood to CRY 💔")
        decrypt_button.clicked.connect(self.on_decrypt_click)
        decrypt_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        decrypt_button.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(decrypt_button)
        
        # Тут будет расшифрованный текст, как мои признания ❤️
        self.decrypted_message_label = AutoScaleLabel("")
        self.decrypted_message_label.setFont(QFont("Arial", 14))
        self.decrypted_message_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(self.decrypted_message_label)
        
        # Кнопка для копирования расшифрованного текста, чтобы поделиться секретами 🌟
        copy_decrypted_button = QPushButton("Copy Decrypted Secret ✨")
        copy_decrypted_button.clicked.connect(self.copy_decrypted_text)
        copy_decrypted_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        copy_decrypted_button.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(copy_decrypted_button)
        
        # Новое поле для ввода данных в формате "эмодзи - ключ" 🎀
        decrypt_combined_label = AutoScaleLabel("Input Data (Mood - Mood Key):")
        decrypt_combined_label.setFont(QFont("Helvetica", 12))
        decrypt_combined_label.setAlignment(Qt.AlignCenter)
        decrypt_layout.addWidget(decrypt_combined_label)
        
        self.decrypt_combined_input = QLineEdit()
        self.decrypt_combined_input.setStyleSheet("background-color: #4e4e4e; color: white;")
        self.decrypt_combined_input.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(self.decrypt_combined_input)
        
        decrypt_combined_button = QPushButton("🤫 Reveal Combined Secrets 💕")
        decrypt_combined_button.clicked.connect(self.on_decrypt_combined_click)
        decrypt_combined_button.setStyleSheet("background-color: #ff8fa2; color: black;")
        decrypt_combined_button.setFont(QFont("Helvetica", 12))
        decrypt_layout.addWidget(decrypt_combined_button)
        
        decrypt_frame.setLayout(decrypt_layout)
        main_layout.addWidget(decrypt_frame)
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(resource_path("Group2.png"))
        if not pixmap.isNull():
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Image not found!")
        main_layout.addWidget(image_label)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
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