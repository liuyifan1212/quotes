from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
	return render(request, 'first_app/index.html')

def register(request):
	result = User.objects.regis_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request,error)
		return redirect('/main')
	request.session['user_id'] = result.id
	return redirect('/quotes')

def login(request):
    result = User.objects.login_validator(request.POST)
    if not result:
        messages.error(request, "Wrong username or password")
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        return redirect('/quotes')

def quotes(request):
	try:
		context = {
		'user': User.objects.get(id=request.session['user_id']),
		'unlike_quotes':Quote.objects.exclude(liked_by=request.session['user_id']),
		'favorite':User.objects.get(id=request.session['user_id']).favorite.all()
        }
        	return render(request,'first_app/result.html',context)
	except KeyError:
		return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/main')


def addquotes(request):
	errors = []
	if len(request.POST['quotedby'])<3:
		errors.append('Quoted by must be at least 3 characters!')
	if len(request.POST['quotes'])<10:
		errors.append('Messages must be at least 3 characters!')
	for error in errors:
		messages.error(request,error)
		return redirect('/quotes')
	else:
		Quote.objects.create(content=request.POST["quotes"],author=request.POST["quotedby"],uploader=User.objects.get(id=request.session['user_id']))
        return redirect('/quotes')

def addlists(request):
	Quote.objects.get(id=request.POST['quote_id']).liked_by.add(User.objects.get(id=request.session['user_id']))
	return redirect('/quotes')

def relists(request):
	User.objects.get(id = request.session['user_id']).favorite.remove(Quote.objects.get(id=request.POST['quote_id']))
	return redirect('/quotes')

def showuser(request,user_id):
	users = User.objects.get(id=user_id)
	texts = users.uploaded_quotes.all()
	context = {
		'users':users,
		'texts':texts,
		'len':len(texts)
	}
	return render(request,'first_app/user.html',context)
















