"""
Mermaid extensions for Markdown.
Renders the output inline, eliminating the need to configure an output
directory.

Supports outputs types of SVG and PNG. The output will be taken from the
filename specified in the tag. Example:

```mermaid
graph TD
A[Client] --> B[Load Balancer]
```

Requires the mermaid cli (https://github.com/mermaid-js/mermaid-cli)

Inspired by cesaremorel/markdown-inline-graphviz (http://github.com/cesaremorel/markdown-inline-graphviz)
"""

import re
import markdown
import tempfile
import os.path
import subprocess
import base64


# Global vars
BLOCK_RE = re.compile(
    r'^```mermaid\s*\n(?P<content>.*?)```\s*$',
    re.MULTILINE | re.DOTALL)

puppeteerConfigContent = """{
  "args": ["--no-sandbox"]
}
"""

class InlineMermaidExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add InlineMermaidPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('mermaid_block',
                             InlineMermaidPreprocessor(md),
                             ">normalize_whitespace")


class InlineMermaidPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        super(InlineMermaidPreprocessor, self).__init__(md)

    def run(self, lines):
        """ Match and generate mermaid code blocks."""

        text = "\n".join(lines)
        while 1:
            m = BLOCK_RE.search(text)
            if m:
                content = m.group('content')

                with tempfile.TemporaryDirectory() as tmp:
                    path = os.path.join(tmp, 'out.svg')

                    puppeteerConfig = os.path.join(tmp, 'puppeteer-config.json')
                    with open(puppeteerConfig, 'w') as f:
                        f.write(puppeteerConfigContent)

                    args = ['mmdc', '-p', puppeteerConfig, '-o', path]

                    try:
                        proc = subprocess.Popen(
                            args,
                            stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)

                        stdout, stderr = proc.communicate(input=content.encode('utf-8'))

                        if not os.path.isfile(path):
                            return (
                                '<pre>Error : Image not created</pre>'
                                '<pre>Args : ' + str(args) + '</pre>'
                                '<pre>stdout : ' + stdout.decode('utf-8') + '</pre>'
                                '<pre>stderr : ' + stderr.decode('utf-8') + '</pre>'
                                '<pre>graph code : ' + content + '</pre>').split('\n')

                        with open(path, 'rb') as f:
                            encodedImageContent = base64.b64encode(f.read()).decode('utf-8')
                            img = '<img src=\'data:image/svg+xml;base64,%s\'>' % encodedImageContent

                            text = '%s\n%s\n%s' % (
                                text[:m.start()], self.md.htmlStash.store(img), text[m.end():])

                    except Exception as e:
                            return (
                                '<pre>Error : ' + str(e) + '</pre>'
                                '<pre>Args : ' + str(args) + '</pre>'
                                '<pre>' + content + '</pre>').split('\n')

            else:
                break
        return text.split("\n")


def makeExtension(*args, **kwargs):
    return InlineMermaidExtension(*args, **kwargs)
