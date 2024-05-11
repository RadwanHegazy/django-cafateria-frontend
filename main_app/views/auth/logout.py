from django.views import View
from globals.request_manager import Action
from django.shortcuts import redirect

class logout_view (View) : 
    
    def get(self,request,**kwargs):
        res = redirect('login')
        res.delete_cookie('user')
        return res
    