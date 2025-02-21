from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class QuotePreprocessor(Preprocessor):
    QUOTE_RE = re.compile(r'\[quote=(.*?)\](.*?)\[/quote\]', re.DOTALL)

    def run(self, lines):
        text = "\n".join(lines)
        text = self.QUOTE_RE.sub(
            r'<div class="quote"><strong>\1 said:</strong><br>\2</div>', text
        )
        return text.split("\n")

class QuoteExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(QuotePreprocessor(md), 'quote', 175)

def makeExtension(**kwargs):  # Required for markdown to find the extension
    return QuoteExtension(**kwargs)
