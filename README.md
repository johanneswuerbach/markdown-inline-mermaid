Markdown Inline Mermaid
========================

A Python Markdown extension that replaces inline Mermaid definitions with
inline SVGs or PNGs!

Why render the graphs inline? No configuration! Works with any
Python-Markdown-based static site generator, such as
[MkDocs](http://www.mkdocs.org/), [Pelican](http://blog.getpelican.com/), and
[Nikola](https://getnikola.com/) out of the box without configuring an output
directory.

# Installation

    $ pip install markdown-inline-mermaid

# Usage

Activate the `markdown_inline_mermaid` extension. For example, with Mkdocs, you add a
stanza to mkdocs.yml:

```
markdown_extensions:
    - markdown_inline_mermaid
```

Afterwards you can use it in your Markdown doc:

~~~
```mermaid
graph TD
A[Client] --> B[Load Balancer]
```
~~~

# Credits

Heavily inspired by [github.com/cesaremorel/markdown-inline-graphviz](https://github.com/cesaremorel/markdown-inline-graphviz),
which provides this functionality for graphviz.


# License

[MIT License](http://www.opensource.org/licenses/mit-license.php)
