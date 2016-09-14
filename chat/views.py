from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound

from .models import Dialog, Message

def chat(request):
	if not request.user.is_authenticated():
		return redirect('/login/')

	dialogs = Dialog.objects.filter(participants=request.user).order_by('-last_message')

	try:
		pk = request.GET['pk']
		partner = User.objects.get(pk=pk)

		try:
			dialog = dialogs.get(participants=partner)
			messages = dialog.messages.order_by('date')
		except ObjectDoesNotExist:
			messages = []

		return render(request, 'chat/dialog.html', {'messages': messages, 'partner': partner})
	except:
		for dialog in dialogs:
			dialog.partner = dialog.participants.exclude(pk=request.user.pk)[0]
			dialog.message = dialog.messages.order_by('-date')[0]

		return render(request, 'chat/chat.html', {'dialogs': dialogs})

def dialogs(request):
	if request.is_ajax():
		dialogs = Dialog.objects.filter(participants=request.user).order_by('-last_message')
		for dialog in dialogs:
			dialog.partner = dialog.participants.exclude(pk=request.user.pk)[0]
			dialog.message = dialog.messages.order_by('-date')[0]

		return render(request, 'chat/dialogs.html', {'dialogs': dialogs})
	
	return HttpResponseNotFound('<h1>Page not found</h1>')

def search(request):
	if request.method == 'POST':
		if request.is_ajax():
			search_text = request.POST.get('search_text')
			users = User.objects.exclude(pk=request.user.pk).filter(username__icontains=search_text)
			return render(request, 'chat/search.html', {'users': users})

	return HttpResponse('Request must be POST.')

def send_message(request):
	if request.method == "POST":
		if request.is_ajax():
			msg = request.POST.get('msg_text')
			partner = User.objects.get(pk=request.GET['pk'])
			dialogs = Dialog.objects.filter(participants=request.user)
			
			try:
				dialog = dialogs.get(participants=partner)
			except ObjectDoesNotExist:
				dialog = Dialog.objects.create()
				dialog.participants.add(request.user, partner)

			message = Message(dialog=dialog, text=msg, sender=request.user)
			message.save()

			data = {'msg': msg, 'date': message.date, 'sender': request.user.username}
			return JsonResponse(data)
	
	return HttpResponse('Request must be POST.')

def messages(request):
	if not request.is_ajax():
		return HttpResponseNotFound('<h1>Page not found</h1>')

	try:
		pk = request.GET['pk']
		partner = User.objects.get(pk=pk)

		try:
			dialogs = Dialog.objects.filter(participants=request.user)
			dialog = dialogs.get(participants=partner)
			messages = dialog.messages.order_by('date')
		except:
			messages = []

		return render(request, 'chat/messages.html', {'messages': messages})
	except:
		return HttpResponseNotFound('<h1>Page not found</h1>')

def login(request):
	if request.user.is_authenticated():
		return redirect('/chat/')

	login_error = 0

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				return redirect('/chat/')
			else:
				return HttpResponse("Account is not active at the moment.")
		else:
			login_error = 1

	return render(request, 'chat/login.html', {'login_error': login_error})

def register(request):
	if request.user.is_authenticated():
		return redirect('/chat/')

	if request.POST:
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = request.POST['username']
			password = request.POST['password2']
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return redirect('/chat/')
	else:
		form = UserCreationForm()

	return render(request, 'chat/register.html', {'form': form})
