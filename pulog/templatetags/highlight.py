from django import template
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

p_pre = re.compile(r'<pre (?=lang=[\'"]?\w+[\'"]?).*?>(?P<code>[\w\W]+?)</pre>')
p_lang = re.compile(r'lang=[\'"]?(?P<lang>\w+)[\'"]?')

def code2html(code, lang):
    lexer = get_lexer_by_name(lang, encoding = 'utf-8', stripall = True)
    formatter = HtmlFormatter(encoding = 'utf-8')
    return highlight(code, lexer, formatter)

@register.filter
def do_highlight(value):
    s_list = p_pre.split(value)
    f_list = p_pre.findall(value)
    if f_list:
        for code_block in p_pre.finditer(value):
            lang = p_lang.search(code_block.group()).group('lang')
            code = code_block.group('code')
            index = s_list.index(code)

            s_list[index] = code2html(code, lang)

    return ''.join(s_list)
