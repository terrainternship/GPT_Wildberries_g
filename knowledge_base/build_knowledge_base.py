"""
Собирает базу знаний из файлов *.md в папке input
и помещает её в файл output/knowledge_base.md
"""
import datetime as dt
from pathlib import Path


THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / 'input'
OUT_FILE = THIS_PATH / 'output/knowledge_base.md'


def process_file(md_file: Path) -> list[str]:
    """
    Построить базу знаний для файла md_file.
    Кажный заголовок будет заменен на полный набор заголовков до самого верхнего.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    out_lines = []

    stack = []  # заголовки от текущего уровня до самого верхнего

    headers_printed = False  # был ли уже выведена начальная секция чанка

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

        else:  # случай строки-не-заголовка

            # выводим начальную секцию будущего чанка (если она не была выведен ранее)
            if not headers_printed:
                if stack:
                    # выводим заголовок в формате маркдауна
                    hashes = '#' * stack[-1][0]
                    out_lines.append(
                        f'{hashes} {stack[-1][1]}'
                    )

                # выводим цепочку заголовков (без '#')
                for _, title in stack:
                    out_lines.append(title)

                # выводим разделитель между начальной секцией и остальным текстом
                out_lines.append('')
                
                headers_printed = True

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
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(out_text)


def main():
    md_files = list(INPUT_PATH.glob('**/*.md'))
    md_file_names = [f.relative_to(INPUT_PATH) for f in md_files]
    
    build_knowledge(md_files, md_file_names)


if __name__ == "__main__":
    main()
