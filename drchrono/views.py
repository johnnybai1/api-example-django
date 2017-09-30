from django.shortcuts import render, redirect
from django.contrib.auth import logout as _
from apiutils import *
# Create your views here.

def logout(request):
    """
    Generic logout function. Returns user to login page
    """
    del request.session['id']
    del request.session['access']
    del request.session['refresh']
    _(request)
    return redirect('index')