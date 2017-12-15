from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET','POST'])
def login(request):
    if request.method=='GET':
        return render(request,'account/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or password is None:
            return render(request, 'account/login.html', {
                'errorMessage': 'Username and password cannot be empty.'
            })
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return render(request, 'account/login.html', {
                'errorMessage': 'Wrong username or password.'
            })
        auth.login(request, user)
        return HttpResponseRedirect(redirect_to='/disk/file/list/')