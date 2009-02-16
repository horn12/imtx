from django import template
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

pre = re.compile(r'<pre( lang=\w*).*>.*</pre>')
    [17:38:16] re.sub('<pre lang=\w*.*>[\w\W]*</pre>','xxxx',s)
        [17:38:20] 先用这个吧
            [17:38:54] \s\S 也行
#pre = re.compile(r'<pre( lang=\w*?).*?>.*?</pre>')
lang = re.compile(r'lang=[\'"]?(?P<lang>\w+)[\'"]?')

def code2html(code, lang):
    lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True)
    formatter = HtmlFormatter(encoding='utf-8')
    #            full = True,
    #            linenos=False,
    #            noclasses="True")
    result = highlight(code, lexer, formatter)
    return result

@register.filter
def highlight(value):
    m = pre.search(value)
    if m:
        pre_block = m.group()
        lm = lang.search(pre_block)
        if lm:
            lang = lm.group('lang')

        return pre.sub(code2html(pre_block, lang), value)
    return value
