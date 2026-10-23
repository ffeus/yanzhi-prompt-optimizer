#!/usr/bin/env python3
"""构建两个明确列出内容的分享包，不扫描用户配置或浏览器数据。"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'yanzhi-prompt-optimizer'
OUT = ROOT / 'dist'


def build():
    OUT.mkdir(exist_ok=True)
    skill_files = [SKILL / 'SKILL.md', SKILL / 'agents/openai.yaml', SKILL / 'references/cases.md']
    public_files = [ROOT / name for name in [
        'index.html', 'README.md', 'LICENSE', 'CONTRIBUTING.md', '.gitignore',
        'docs/TESTING.md', 'docs/workspace.jpg', 'tests/core.test.cjs',
        'examples/style-output.json', 'examples/style-prompt.md', 'scripts/package.py',
    ]] + skill_files
    for path in public_files:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Expected regular release file: {path.relative_to(ROOT)}')
    with ZipFile(OUT / 'yanzhi-prompt-optimizer-skill.zip', 'w', ZIP_DEFLATED) as archive:
        for path in skill_files:
            archive.write(path, 'yanzhi-prompt-optimizer/' + path.relative_to(SKILL).as_posix())
        archive.write(ROOT / 'LICENSE', 'yanzhi-prompt-optimizer/LICENSE')
    with ZipFile(OUT / 'yanzhi-project.zip', 'w', ZIP_DEFLATED) as archive:
        for path in public_files:
            archive.write(path, 'yanzhi-prompt-optimizer/' + path.relative_to(ROOT).as_posix())
    print('Built dist/yanzhi-prompt-optimizer-skill.zip and dist/yanzhi-project.zip')


if __name__ == '__main__':
    build()
