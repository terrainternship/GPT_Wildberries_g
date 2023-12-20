import datetime as dt
from pathlib import Path

file1 = open('info_oferta.md', 'r', encoding='utf-8')
file2 = open('info_instruction.md', 'r', encoding='utf-8')
file3 = open('info_personal_data.md', 'r', encoding='utf-8')
file4 = open('info_privacy_policy.md', 'r', encoding='utf-8')
file5 = open('info_agreement.md', 'r', encoding='utf-8')
file6 = open('info_faq.md', 'r', encoding='utf-8')
file7= open('info_payments.md', 'r', encoding='utf-8')
file8 = open('info_contacts.md', 'r', encoding='utf-8')

# Читаем содержимое файлов
file1_content = file1.read()
file2_content = file2.read()
file3_content = file3.read()
file4_content = file4.read()
file5_content = file5.read()
file6_content = file6.read()
file7_content = file7.read()
file8_content = file8.read()
# Закрываем файлы
file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()
file7.close()
file8.close()
# Создаем новый файл для объединенного содержимого
output_file = open('output.md', 'w', encoding='utf-8')

# Записываем содержимое файлов в объединенный файл
output_file.write(file1_content + '\n')
output_file.write(file2_content + '\n')
output_file.write(file3_content + '\n')
output_file.write(file4_content + '\n')
output_file.write(file5_content + '\n')
output_file.write(file6_content + '\n')
output_file.write(file7_content + '\n')
output_file.write(file8_content + '\n')


# Закрываем новый файл
output_file.close()

# Подтверждаем успешное выполнение скрипта
print("Файлы успешно объединены в output.md!")
# Определение пути к загруженному файлу
THIS_PATH = Path(__file__).parent
OUT_DIR = 'outpu'
OUT_FILE = OUT_DIR + '/knowledge_base_new.md'

def process_file(md_file: Path) -> list[str]:
    """
    Построить базу знаний для файла md_file.
    Каждый заголовок будет заменен на полный набор заголовков до самого верхнего.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    out_lines = []
    stack = []  # заголовки от текущего уровня до самого верхнего
    headers_printed = False  # был ли уже выведен начальный заголовок чанка

    for line in text.split('\n'):
        if line.startswith('#'):  # обрабатываем только строки с заголовками
            headers_printed = False
            # уровень заголовка = количество символов '#' в начале строки
            level = len(line) - len(line.lstrip('#'))

            # оставляем только заголовки выше текущего
            while stack and level <= stack[-1][0]:
                stack.pop()

            # текст заголовка - то, что после начальных символов '#'
            title = line[level:].strip()
            stack.append((level, title))

            # сохраняем заголовок в результирующих строках
            hashes = '#' * level
            out_lines.append(f'{hashes} {title}')

        else:  # случай строки-не-заголовка
            # выводим начальный заголовок чанка (если он не был выведен ранее)
            if not headers_printed:
                # выводим цепочку заголовков (без '#')
                for _, title in stack:
                    out_lines.append(title)

                # выводим разделитель между начальной секцией и остальным текстом
                out_lines.append('')
                headers_printed = True

            out_lines.append(line)

    return out_lines

# Создание директории output, если она не существует
if not Path(OUT_DIR).exists():
    Path(OUT_DIR).mkdir()

# Обработка файла и сохранение результата
output_lines = process_file('output.md')  #пишем наименование файла для редактирования

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

