from django.template import Node
from django.template import Library, Variable

register = Library()

class WrapperObject(Node):
    def __init__(self, object, target):
        self.obj = Variable(object)
        print type(self.obj)

    def render(self, context):
        return ''

def do_wrapper_object(parser, token):
    args = token.contents.split()
    return WrapperObject(args[1], args[3])

register.tag('wrapper', do_wrapper_object)

