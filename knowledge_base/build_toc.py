"""
Создает полное оглавление всех файлов *.md в папке input.
Записывает его в файл output/tocs.md
"""
import datetime as dt
from pathlib import Path


THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / 'input'
OUT_FILE = THIS_PATH / 'output/tocs.md'  # table of contents = оглавления


def extract_headers(md_file: Path, *, fname_str=None):
    """
    Извлекает заголовки из файла md_file и возвращает их в виде списка строк.
    Параметры:
        md_file: путь к файлу
        fname_str: если задан, то добавляет в результат имя файла как первый уровень
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    out_lines = []

    if fname_str:
        # добавляем имя файла как первый уровень
        out_lines.append(
            f'- {fname_str}'
        )
        extra_level = 1
    else:
        extra_level = 0

    for line in text.split('\n'):
        if line.startswith('#'):  # обрабатываем только строки с заголовками
            
            # уровень заголовка = количество символов '#' в начале строки
            level = len(line) - len(line.lstrip('#'))

            # текст заголовка - то, что после начальных символов '#'
            title = line[level:].strip()

            # отступы для вложенных заголовков
            indent = '  ' * (level - 1 + extra_level)
            
            out_lines.append(
                f'{indent}- {title}'
            )
    
    return out_lines    


def main():
    now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    out_lines = [
        f'[comment]: # (Этот файл создан {Path(__file__).name}, {now})'
    ]

    for md_file in INPUT_PATH.glob('**/*.md'):
        fname_str = md_file.relative_to(INPUT_PATH)
        out_lines.append(
            f'\n'
            f'[comment]: # ({fname_str})\n'
        )
        # out_lines += extract_headers(md_file, fname_str=fname_str)  # включить в список имя файла
        out_lines += extract_headers(md_file)

    out_text = '\n'.join(out_lines) + '\n'
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(out_text)


if __name__ == '__main__':
    main()
