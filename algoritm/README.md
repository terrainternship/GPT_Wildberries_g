# Информация по алгоритму для нейро-консультанта тех.поддержки клиентов по внутренним документам, инструкциям и правилам ООО «Вайлдберриз»
---
Ссылки на колабы:

https://colab.research.google.com/drive/1PUvJK0OktG5UxGCKd_SF27FPAGdGYy9R?usp=sharing - Колаб с функциями чтения и записи ячеек документа Google Таблицы. Проставлена ссылка на таблицу в которой должны появляться тестоваые вопросы и ответы GPT. Проверил работу, записав один тестовый вопрос "Тестовый вопрос" во 2-ю строку колонки "Вопрос" и один тестовый ответ "Тестовый ответ" в колонку "Тестовый ответ GPT" той же строки.
Добавлены функции : read_range_from_spreadsheet(sheet_url, sheet_name, column_name, start_row, end_row) - чтение строк диапазона start_row, end_row;
write_range_to_spreadsheet(sheet_url, sheet_name, column_name, start_row, end_row, values) - запись строк диапазона start_row, end_row зачениями values - список []

Колаб с моделью вопросов и ответов с возможностью отработки по файлу :
https://colab.research.google.com/drive/1Tboe273zmDWuIiX_noFTsh2h9gf5mHs_?usp=sharing

Колаб с реализацией памяти в диалоговом режиме :
https://colab.research.google.com/drive/1MvboBEutgO21cHG9iNqMk8kI4fBoe9-7?usp=sharing

Колаб для сравнения ответа GPT и эталонного ответа с выставлением оценки по файлу вопросов-ответов :
https://colab.research.google.com/drive/1_x9kuqvr6AE8JNl1ASVWlpJfqSuvd1V5?usp=sharing

