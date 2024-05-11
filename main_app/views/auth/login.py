from django.views import View
from globals.request_manager import Action
from django.shortcuts import render, redirect
from frontend.settings import MAIN_URL
from django.contrib import messages

class login_view (View) : 
    
    def get(self,request,**kwargs):
        return render(request,'login.html')
    
    def post(self,request,**kwargs) : 

        data = {
            'email' : request.POST.get('email',None),
            'password' : request.POST.get('password',None),            
        }

        action = Action(
            url = MAIN_URL + '/user/auth/login/',
            data=data,
        )

        action.post()
        respones = action.json_data()
        if action.is_valid() : 
            user_token = respones['token']
            res = redirect('profile')
            res.set_cookie('user',user_token)
            return res
        

        msg = respones['message'][0]
        messages.error(request,msg)
        return redirect('login')