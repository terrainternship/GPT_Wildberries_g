"""
Собирает базу знаний из файлов *.md в папке input
и помещает её в файл output/knowledge.md
"""
import datetime as dt
from dataclasses import dataclass
from pathlib import Path


THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / 'input'
OUT_KNOWLEDGE_FILE = THIS_PATH / 'output/knowledge.md'
OUT_TOC_FILE = THIS_PATH / 'output/toc.md'


@dataclass
class Header:
    level: int
    title: str
    is_printed: bool = False


def header_block(headers) -> list[str]:
    """
    Возвращает список строк, которые будем выводить сразу после любого заголовка.
    """
    out_lines = []

    for header in headers:
        if header.is_printed:
            continue

        # выводим строку-заголовок в формате маркдауна
        out_lines.append(
            f'{"#" * header.level} {header.title}'
        )
        header.is_printed = True

    # выводим цепочку заголовков (без '#')
    for header in headers:
        out_lines.append(header.title)

    # выводим разделитель между этой секцией и остальным текстом
    out_lines.append('')

    return out_lines


def process_file(md_file: Path) -> list[str]:
    """
    Построить базу знаний для файла md_file.
    После каждого заголовка будет создан список заголовков до самого верхнего.
    В виде текста, который пойдет в чанк.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    out_lines = []

    headers = []  # стек заголовков от текущего уровня до самого верхнего
    for line in text.split('\n'):
        if line.startswith('#'):  # обрабатываем строки с заголовками

            # уровень заголовка = количество символов '#' в начале строки
            level = len(line) - len(line.lstrip('#'))

            # оставляем только заголовки выше текущего
            while headers and level <= headers[-1].level:
                headers.pop()

            # текст заголовка - то, что после начальных символов '#'
            title = line[level:].strip()

            h = Header(level, title)
            headers.append(h)

        else:  # случай строки-не-заголовка
            if headers and not headers[-1].is_printed:
                out_lines += header_block(headers)
            out_lines.append(line)

    return out_lines


def build_knowledge(md_files, md_file_names):
    """
    Построить базу знаний из файлов md_files.
    """
    if len(md_files) != len(md_file_names):
        raise ValueError('Количество файлов и их имен должно совпадать')

    now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    out_lines = [
        f'[comment]: # (Этот файл создан {Path(__file__).name}, {now})'
    ]

    for i, md_file in enumerate(md_files):
        out_lines.append(
            f'\n'
            f'[comment]: # ({md_file_names[i]})\n'
        )
        out_lines += process_file(md_file)

    out_text = '\n'.join(out_lines) + '\n'
    with open(OUT_KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        f.write(out_text)


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


def build_toc(md_files, md_file_names):
    """
    Построить оглавление из файлов md_files. Полезно для исследования базы знаний.
    """
    if len(md_files) != len(md_file_names):
        raise ValueError('Количество файлов и их имен должно совпадать')

    now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    out_lines = [
        f'[comment]: # (Этот файл создан {Path(__file__).name}, {now})\n'
    ]

    for i, md_file in enumerate(md_files):
        out_lines += extract_headers(md_file, fname_str=md_file_names[i])

    out_text = '\n'.join(out_lines) + '\n'
    with open(OUT_TOC_FILE, 'w', encoding='utf-8') as f:
        f.write(out_text)


def main():
    # собрать результат из всех файлов *.md в папке INPUT_PATH
    # md_files = list(INPUT_PATH.glob('**/*.md'))
    # md_file_names = [f.relative_to(INPUT_PATH) for f in md_files]

    # хотим получить такой порядок в итоговом файле:
    md_file_names = [
        'info_oferta.md',
        'info_instruction.md',
        'info_personal_data.md',
        'info_privacy_policy.md',
        'info_agreement.md',
        'info_faq.md',
        'info_payments.md',
        'info_contacts.md',
    ]
    md_files = [INPUT_PATH / f for f in md_file_names]

    build_knowledge(md_files, md_file_names)
    build_toc(md_files, md_file_names)


if __name__ == "__main__":
    main()
