from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from wykop.accounts.forms import RegistrationForm
from wykop.accounts.models import User

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

def staff_required():
    return user_passes_test(lambda u: u.is_staff)

class BanedView(View):
    @method_decorator(staff_required())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self,request,*args, **kwargs):
        print(request.POST)
        print(kwargs)
        user_pk = kwargs['user_pk']
        u = User.objects.get(pk=user_pk)
        if request.POST.get('set')=='1':
            u.banned = True
        else:
            u.banned = False
        u.save()
        return redirect(request.META.get('HTTP_REFERER'))
    