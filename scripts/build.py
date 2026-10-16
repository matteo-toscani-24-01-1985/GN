"""Create a single-file distribution in the repository root."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
html=(root/'src'/'template.html').read_text(encoding='utf-8')
script=(root/'src'/'app.js').read_text(encoding='utf-8').replace('/*__MATH__*/',(root/'src'/'math.js').read_text(encoding='utf-8'))
script+='\n'+(root/'src'/'page.js').read_text(encoding='utf-8')
(root/'index.html').write_text(html.replace("'USE_SCRIPTS_HERE'",script),encoding='utf-8')
print('Created',root/'index.html')
