# coding: utf-8
from django.http import HttpResponse

class MaintainMiddleware(object):
    def process_request(self, request):
        if not request.path == '/admin/' and not request.user.is_authenticated():
            return HttpResponse('''<head><title>IMTX正在维护中...</title></head>
            <body>
            <h1 style="color:blue">IMTX当前正在维护中</h1>
            <h2>清理代码、修正bug，重构网站结构。</h2>
            <p align="right">TualatriX</p>
            <p align="right">March 16, 2009</p>
            </body>''')
