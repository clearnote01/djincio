from django import template
from threading import Thread
import re
import asyncio
import aiohttp
register = template.Library()
result = {}
result['x'] = 'null'
def async_wrapper(func):
    def inner(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asycnio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return inner
class AsyncAwaitNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = 'foo'
        return ''
@register.tag(name= 'async')
def do_format_node(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    format_string, var_name = [None, None]
    return AsyncAwaitNode(format_string[1:-1], var_name)
@register.filter(name='await')
def await_async(promise):
    print('filter is called')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(promise)
    return result

