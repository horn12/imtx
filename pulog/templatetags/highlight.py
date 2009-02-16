from django import template
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

#pre = re.compile(r'<pre( lang=\w*).*>.*</pre>')
p_pre = re.compile(r'<pre (lang=\w+).*?>(?P<code>[\w\W]+?)</pre>')
#pre = re.compile(r'<pre( lang=\w*?).*?>.*?</pre>')
p_lang = re.compile(r'lang=[\'"]?(?P<lang>\w+)[\'"]?')

def code2html(code, lang):
    lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True)
    formatter = HtmlFormatter(encoding='utf-8')
    #            full = True,
    #            linenos=False,
    #            noclasses="True")
    result = highlight(code, lexer, formatter)
    return result

@register.filter
def do_highlight(value):
    m = p_pre.search(value)
    print 'is m here', m
    if m:
        pre_block = m.group()
        lm = p_lang.search(pre_block)
        if lm:
            lang = lm.group('lang')
            return p_pre.sub(code2html(m.group('code'), lang), value)
    return value
