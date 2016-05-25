from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile, Contact
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from actions.utils import create_action
from actions.models import Action
from geopy.geocoders import Nominatim

@login_required
def dashboard(request):
	actions = Action.objects.exclude(user=request.user)
	following_ids = request.user.following.values_list('id', flat=True)
	if following_ids:
		actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
	actions = actions[:10]
	return render(request, 'account/dashboard.html', {'section' : 'dashboard', 'actions' : actions})

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			create_action(new_user, 'has created an account')
			messages.success(request, 'You have been successfully registered!')
			return redirect('login')
		else:
			messages.error(request, 'Error while registering User!')
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form' : user_form})

@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Updated successfully!')
			return redirect('dashboard')
		else:
			messages.error(request, 'Error wile placing order!')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 'account/edit.html', {'section' : 'images', 'user_form' : user_form, 'profile_form' : profile_form})

@login_required
def user_list(request):
	users = User.objects.filter(is_active=True)
	return render(request, 'account/user/list.html', {'section' : 'people', 'users' : users})

@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	return render(request, 'account/user/detail.html', {'section' : 'people', 'user' : user})

@login_required
@require_POST
@ajax_required
def user_follow(request):
	user_id = request.POST.get('id')
	action = request.POST.get('action')
	if user_id and action:
		try:
			user = User.objects.get(id=user_id)
			if action == 'follow':
				Contact.objects.get_or_create(user_from=request.user, user_to=user)
				create_action(request.user, 'is following', user)
			else:
				Contact.objects.filter(user_from=request.user, user_to=user).delete()
			return JsonResponse({'status' : 'ok'})
		except User.DoesNotExist:
			return JsonResponse({'status' : 'ko'})
	return JsonResponse({'status' : 'ko'})

@login_required
@require_POST
@ajax_required
def add_location(request):
	user = request.POST.get('user')
	action = request.POST.get('action')
	lattitude = request.POST.get('lattitude')
	longitude = request.POST.get('longitude')
	string = ""
	string += lattitude
	string += ", " + longitude
	if user and action:
		if lattitude and longitude:
			try:
				profile = Profile.objects.get(id=user)
				geolocator = Nominatim()
				spot = geolocator.reverse(string)
				if action == 'Get Location':
					profile.location = spot
					profile.save()
				else:
					profile.location = spot
					profile.save()
					return JsonResponse({'status' : 'ko'})
				return JsonResponse({'status' : 'ok'})
			except:
				pass
		else:
			messages.error(request, 'Your brouser might not have navigation support! Please upgrade..')
	return JsonResponse({'status' : 'ko'})