from django.urls import resolve, Resolver404
from  django.http import HttpResponseRedirect
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

class RedirectToDashboard:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        path = request.path 

        try:
            resolve(path)

        except Resolver404:
            return HttpResponseRedirect('/dashboard/')
        
        return await self.get_response(request) 