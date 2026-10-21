"""Check lesson Markdown files for math-markup problems that break rendering.

Usage: python3 scripts/check_math.py [files...]   (defaults to all lessons)
Exits 1 if any problem is found.
"""
import glob
import re
import sys

CHECKS = [
    (re.compile(r'"\$|\$"'), 'math touching a quote mark (renders as raw text in some viewers)'),
    (re.compile(r'\\\$\$'), 'escaped dollar touching math (\\$$x$); write "an amount $X$" instead'),
    (re.compile(r'\\\{|\\\}'), 'use \\lbrace / \\rbrace instead of \\{ / \\}'),
]


def strip_blocks(text):
    """Blank out display math and code blocks, keeping line numbers aligned."""
    def blank(m):
        return re.sub(r'[^\n]', ' ', m.group(0))
    text = re.sub(r'```.*?```', blank, text, flags=re.S)
    return re.sub(r'\$\$.*?\$\$', blank, text, flags=re.S)


def check(path):
    text = open(path, encoding='utf-8').read()
    problems = []
    if text.count('$$') % 2:
        problems.append((0, 'odd number of $$ (unclosed display math)'))
    inline = strip_blocks(text)
    for n, line in enumerate(inline.split('\n'), 1):
        if line.replace('\\$', '').count('$') % 2:
            problems.append((n, 'odd number of inline $ (unclosed inline math)'))
    for n, line in enumerate(text.split('\n'), 1):
        if line.lstrip().startswith(('```', '    ')):
            continue
        for pattern, message in CHECKS:
            if pattern.search(line):
                problems.append((n, message))
    return problems


def main(paths):
    paths = paths or sorted(glob.glob('math/*.md') + glob.glob('options_theory/*.md'))
    bad = False
    for path in paths:
        for n, message in check(path):
            bad = True
            print(f'{path}:{n}: {message}')
    if not bad:
        print(f'OK: {len(paths)} file(s) checked')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
