"""
Mermaid extensions for Markdown.
Renders the output inline, eliminating the need to configure an output
directory.

Supports output types of SVG and PNG. The output will be taken from the
filename specified in the tag. Example:

```mermaid
graph TD
A[Client] --> B[Load Balancer]
```

Requires the mermaid cli (https://github.com/mermaid-js/mermaid-cli)

Inspired by cesaremorel/markdown-inline-graphviz (http://github.com/cesaremorel/markdown-inline-graphviz)
"""

import re
import tempfile
import subprocess
import base64
from pathlib import Path

from markdown import Extension
from markdown.preprocessors import Preprocessor

# Global vars
BLOCK_RE = re.compile(
    r"^```mermaid\s*\n(?P<content>.*?)```\s*$", re.MULTILINE | re.DOTALL
)

puppeteer_config_content = """{
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
}
"""


class InlineMermaidExtension(Extension):
    def extendMarkdown(self, md):
        """Add InlineMermaidPreprocessor to the Markdown instance."""
        md.registerExtension(self)
        md.preprocessors.register(InlineMermaidPreprocessor(md), "mermaid_block", 27)


class InlineMermaidPreprocessor(Preprocessor):
    def run(self, lines):
        """Match and generate mermaid code blocks."""

        text = "\n".join(lines)
        while 1:
            m = BLOCK_RE.search(text)
            if m:
                content = m.group("content")

                with tempfile.TemporaryDirectory() as tmp:
                    tmp_dir = Path(tmp)
                    tmp_svg_path = tmp_dir / "out.svg"

                    puppeteer_config = tmp_dir / "puppeteer-config.json"
                    with puppeteer_config.open("w") as f:
                        f.write(puppeteer_config_content)

                    args = ["mmdc", "-p", str(puppeteer_config), "-o", str(tmp_svg_path)]

                    try:
                        res = subprocess.run(
                            args,
                            input=content,
                            capture_output=True,
                            text=True,
                        )

                        if not tmp_svg_path.is_file():
                            return (
                                "<pre>Error : Image not created</pre>"
                                "<pre>Args : " + str(args) + "</pre>"
                                "<pre>stdout : " + res.stdout + "</pre>"
                                "<pre>stderr : " + res.stderr + "</pre>"
                                "<pre>graph code : " + content + "</pre>"
                            ).split("\n")

                        with tmp_svg_path.open("rb") as f:
                            encoded_image_content = base64.b64encode(f.read()).decode(
                                "utf-8"
                            )
                            img = f'<img src="data:image/svg+xml;base64,{encoded_image_content}">'

                            text = "{}\n{}\n{}".format(
                                text[: m.start()],
                                self.md.htmlStash.store(img),
                                text[m.end() :],
                            )

                    except Exception as e:
                        return (
                            "<pre>Error : " + str(e) + "</pre>"
                            "<pre>Args : " + str(args) + "</pre>"
                            "<pre>" + content + "</pre>"
                        ).split("\n")

            else:
                break
        return text.split("\n")


def makeExtension(**kwargs):
    return InlineMermaidExtension(**kwargs)
