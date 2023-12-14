# Используем базовый образ Python
FROM python:3.9

# Установка зависимостей
RUN pip install python-dotenv
RUN pip install python-telegram-bot



# Создание директории приложения внутри контейнера
WORKDIR /app

# Копирование исходного кода в контейнер
COPY . /app

# Установка переменных окружения (можно заменить значения на реальные во время запуска контейнера)
# ENV TOKEN=your_telegram_token

# Запуск приложения
CMD ["python", "src/bot.py"]
