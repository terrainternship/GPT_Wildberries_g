"""
Собирает базу знаний из файлов *.md в папке input
и помещает её в файл output/knowledge_base.md
"""
import datetime as dt
from pathlib import Path


THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / 'input'
OUT_FILE = THIS_PATH / 'output/knowledge_base.md'


def build_knowledge(md_file: Path) -> list[str]:
    """
    Построить базу знаний для файла md_file.
    Кажный заголовок будет заменен на полный набор заголовков до самого верхнего.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    out_lines = []

    stack = []  # заголовки от текущего уровня до самого верхнего

    headers_printed = False  # был ли уже выведен заголовок

    for line in text.split('\n'):
        if line.startswith('#'):  # обрабатываем только строки с заголовками
            headers_printed = False
            
            # уровень заголовка = количество символов '#' в начале строки
            level = len(line) - len(line.lstrip('#'))

            # оставляем только заголовки выше текущего
            while stack and level <= stack[-1][0]:
                stack.pop()

            stack.append((level, line))

        else:  # случай строки-не-заголовка

            # выводим цепочку заголовков, если ещё не выводили
            if not headers_printed:
                for _, header in stack:
                    out_lines.append(header)
                headers_printed = True

            out_lines.append(line)

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
        out_lines += build_knowledge(md_file)

    out_text = '\n'.join(out_lines) + '\n'
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(out_text)


if __name__ == "__main__":
    main()
