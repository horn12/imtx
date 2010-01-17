# coding: utf-8
from django.http import HttpResponse

class MaintainMiddleware(object):
    def process_request(self, request):
        if not request.path == '/admin/' and not request.user.is_authenticated():
            return HttpResponse('''<head><title>IMTX正在转移中...</title></head>
            <body>
            <h1 style="color:blue">IMTX当前正在转移中</h1>
            <h2>一切都不会改变，稍候即会恢复。</h2>
            <p align="right">TualatriX</p>
            <p align="right">Jan 17, 2010</p>
            </body>''')
