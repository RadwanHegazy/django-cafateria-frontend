from django.views import View
from globals.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from globals.request_manager import Action
from frontend.settings import MAIN_URL

class profile_view (View) : 
    
    @login_required
    def get(self,request,**kwargs):
        user = kwargs['user']
        context = {}

        # get all user orders
        orders = Action(
            url=MAIN_URL + "/order/get/",
            headers=kwargs['headers']
        )
        orders.get()
        context['orders'] = orders.json_data()

        if user['has_cafateria'] : 
            return render(request,'cafateria-profile.html',context)

        # get all products
        pd_action = Action(
            url=MAIN_URL + "/product/get/"
        )
        pd_action.get()
        context['products'] = pd_action.json_data()

        # get all cafaterias
        cafaterias = Action(
            url=MAIN_URL + "/product/get/cafateria/"
        )

        cafaterias.get()
        context['cafaterias'] = cafaterias.json_data()

        return render(request,'profile.html',context)
    

    @login_required
    def post(self, request, **kwargs) : 
        if kwargs['user']['has_cafateria'] :
            # post as a cafateria
            self.scan_qr_code(request,**kwargs)
        else:
            # post as a normal user
            self.post_as_user(request,**kwargs)


        return redirect('profile')

    @staticmethod
    def post_as_user (request,**kwargs):
        action = Action(
            url=MAIN_URL + "/order/create/",
            headers=kwargs['headers'],
            data={
                'cafateria' : request.POST.get('cafateria',None),
                'product' : request.POST.get('product',None),
            }
        )

        action.post()
        messages.success(request,'جاري تحضير طلبك')
        

    @staticmethod
    def scan_qr_code (request,**kwargs) :
        qr_code = request.POST.get('qr_id',None)
        action = Action(
            url = MAIN_URL + f"/order/scan/{qr_code}/",
            headers=kwargs['headers']
        )

        action.get()

        action.json_data()
        data = action.json_data()

        if action.is_valid() :
            messages.success(request,f"الاوردر الخاص ب : {data['user']}  و الطلب : {data['order']} و السعر سيكون : {data['price']}")
        else:
            messages.error(request,'الكود غير صحيح')
