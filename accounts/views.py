from django.shortcuts import render
from django.views.generic.base import TemplateView
from accounts.forms import createuserform
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'accounts/home.html'


def singuppage(request):
    form = createuserform

    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'accounts/signup.html',context)


def userlogin(request):
    if request.method == "POST":
        # first get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django;s Built in authentication function
        user = authenticate(username=username,password=password)

        # if we have the user
        if user:
            # check it the account is active
            if user.is_active:
                #Log the user in
                login(request,user)
                #send the user back in same page
                # In this case there is home page
                return HttpResponseRedirect(reverse('home'))
            else:
                #pass
                # if account is not active
                return HttpResponse('Your account is active')
        else:
            print('Someone tried to login and failed')
            print('They used username: {} and password: {}'.format(username,password))
    else:
        return render(request,'accounts/login.html')


#Logout function view
@login_required
def userlogout(request):
    #Log out user
    logout(request)
    #return home page
    return HttpResponseRedirect(reverse('home'))