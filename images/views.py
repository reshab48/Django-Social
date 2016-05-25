from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageCreateForm, ImageEditForm
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from django.utils.text import slugify
from django.conf import settings
import redis

#connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@login_required
def image_create(request):
	if request.method == 'POST':
		form = ImageCreateForm(request.POST, request.FILES)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.user = request.user
			new_image.slug = slugify(request.user)
			new_image.save()
			create_action(request.user, 'bookmarked image', new_image)
			messages.success(request, 'Image added successfully!')
			return redirect(new_image.get_absolute_url())

	else:
		form = ImageCreateForm()

	return render(request, 'images/image/create.html', {'section' : 'images', 'form' : form})

def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	# increment total image views by 1
	total_views = r.incr('image:{}:views' .format(image.id))
	# increment image ranking by 1
	r.zincrby('image_ranking', image.id, 1)
	return render(request, 'images/image/detail.html', {'section' : 'images', 'image' : image, 'total_views' : total_views})

@login_required
def image_list(request):
	user = request.user
	images = Image.objects.all()
	if images:
		images = Image.objects.all()
		paginator = Paginator(images, 3)
		page = request.GET.get('page')
	else:
		images = Image.objects.all()
		paginator = Paginator(images, 3)
		page = request.GET.get('page') 
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse("")
		images = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'images/image/list_ajax.html', {'section' : 'images', 'images' : images})
	return render(request, 'images/image/list.html', {'section' : 'images', 'images' : images})

@ajax_required
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_like.add(request.user)
				create_action(request.user, 'likes', image)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status' : 'ok'})
		except:
			pass
	return JsonResponse({'status' : 'ko'})

@login_required
def image_ranking(request):
	image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
	image_ranking_ids = [int(id) for id in image_ranking]
	most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
	most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
	return render(request, 'images/image/ranking.html', { 'section' : 'images', 'most_viewed' : most_viewed })

@login_required
def image_edit(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	if request.method == 'POST':
		form = ImageEditForm(instance=get_object_or_404(Image, id=id, slug=slug), data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Image updated successfully!')
		else:
			messages.error(request, 'Error while updating image!')
	else:
		form = ImageEditForm(instance=get_object_or_404(Image, id=id, slug=slug))
	return render(request, 'images/image/edit.html', {'section' : 'images', 'image' : image, 'form' : form})