import markdown
from pathlib import Path
import base64
import pytest


def test_extension():
    md = markdown.Markdown(extensions=['markdown_inline_mermaid'])
    text = f"""
It works like this:

```mermaid
sequenceDiagram
    A->>A: Loop
```"""
    svg_start = base64.b64encode(b'<svg').decode('ascii')[:-3]

    converted_text = md.convert(text)

    assert 'Error' not in converted_text
    assert converted_text.startswith(f'<p>It works like this:</p>\n<p><img src="data:image/svg+xml;base64,{svg_start}')
