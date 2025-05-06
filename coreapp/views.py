import os
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from djangowebapp import settings
from .models import User, Article, Image
from .forms import UserForm, ArticleForm, ImageForm, ImageProcessForm
from PIL import Image as PILImage
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from io import BytesIO


# User CRUD

def user_list(request):
    return render(request, 'core/user_list.html', {'users': User.objects.all()})

def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'core/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'core/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'core/user_confirm_delete.html', {'user': user})

def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'core/user_details.html', {'user': user})

# Article CRUD + Search

def article_list(request):
    return render(request, 'core/article_list.html', {'articles': Article.objects.select_related('author').all()})

def article_create(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('article_list')
    return render(request, 'core/article_form.html', {'form': form})

def article_update(request, pk):
    art = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, instance=art)
    if form.is_valid():
        form.save()
        return redirect('article_list')
    return render(request, 'core/article_form.html', {'form': form})

def article_delete(request, pk):
    art = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        art.delete()
        return redirect('article_list')
    return render(request, 'core/article_confirm_delete.html', {'article': art})

def article_details(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'core/article_details.html', {'article': article})

from django.db.models import Q

def article_search(request):
    q = request.GET.get('query', '').strip()
    articles = Article.objects.select_related('author').filter(Q(body__icontains=q)) if q else Article.objects.none()
    return render(request, 'core/article_search.html', {'results': articles, 'query': q})

# Image CRUD + Processing
'''
def image_list(request):
    message = None

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = "Image uploaded successfully."
            form = ImageForm()
    else:
        form = ImageForm()

    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    image_files = []
    if os.path.exists(upload_dir):
        image_files = [
            os.path.join(settings.MEDIA_URL, 'uploads', f)
            for f in os.listdir(upload_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
        ]
    return render(request, 'core/image_list.html', {
        'form': form,
        'images': image_files,
        'message': message
    })
'''

def image_list(request):
    image_url = None
    message = None
    uploaded_file_name = None

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return HttpResponseBadRequest("No file uploaded.")

        save_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(save_dir, exist_ok=True)

        file_path = os.path.join(save_dir, uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        image_url = os.path.join(settings.MEDIA_URL, 'uploads', uploaded_file.name)
        message = f"Uploaded: {uploaded_file.name}"
        uploaded_file_name = uploaded_file.name

    return render(request, 'core/image_list.html', {
        'image': uploaded_file_name,
        'message': message,
        'image_url': image_url
    })
'''
def image_grayscale(request):
    file_name = request.GET.get('fileName')
    if not file_name:
        return HttpResponse("Missing fileName", status=400)

    image_obj = get_object_or_404(Image, file__icontains=file_name)
    pil_img = PILImage.open(image_obj.file.path).convert('L')

    buffer = BytesIO()
    pil_img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')
'''
def image_grayscale(request):
    file_name = request.GET.get('fileName')
    if not file_name:
        return HttpResponseBadRequest("Missing fileName")

    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

    if not os.path.exists(file_path):
        raise Http404("Image not found")

    try:
        pil_img = PILImage.open(file_path).convert('L')  
        buffer = BytesIO()
        pil_img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
    except Exception as e:
        return HttpResponse(f"Error processing image: {e}", status=500)


def image_resize(request):
    file_name = request.GET.get('fileName')
    if not file_name:
        return HttpResponseBadRequest("Missing fileName")

    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

    if not os.path.exists(file_path):
        raise Http404("Image not found")
    
    width = int(request.GET.get('width', 512))
    height = int(request.GET.get('height', 512))
    try:
        pil_img = PILImage.open(file_path).resize((width, height))

        buffer = BytesIO()
        pil_img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
    except Exception as e:
        return HttpResponse(f"Error processing image: {e}", status=500)


def image_crop(request):
    file_name = request.GET.get('fileName')
    if not file_name:
        return HttpResponseBadRequest("Missing fileName")

    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

    if not os.path.exists(file_path):
        raise Http404("Image not found")

    x = int(request.GET.get('x', 100))
    y = int(request.GET.get('y', 100))
    width = int(request.GET.get('width', 300))
    height = int(request.GET.get('height', 300))

    try:
        pil_img = PILImage.open(file_path).crop((x, y, x + width, y + height))

        buffer = BytesIO()
        pil_img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
    except Exception as e:
        return HttpResponse(f"Error processing image: {e}", status=500)

def image_multi_modification(request):
    message = None
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            message = "File wasn't uploaded."
            return render(request, 'core/image_multi.html', {'message': message})

        try:
            width = int(request.POST.get('width', 512))
            height = int(request.POST.get('height', 512))
            x = int(request.POST.get('x', 100))
            y = int(request.POST.get('y', 100))
            crop_width = int(request.POST.get('cropWidth', 300))
            crop_height = int(request.POST.get('cropHeight', 300))

            image = PILImage.open(file)

            resized = image.resize((width, height))
            cropped = resized.crop((x, y, x + crop_width, y + crop_height))
            grayscale = cropped.convert('L')

            buffer = BytesIO()
            grayscale.save(buffer, format='PNG')
            buffer.seek(0)

            return HttpResponse(buffer, content_type='image/png')

        except Exception as e:
            message = f"Error: {str(e)}"

    return render(request, 'core/image_multi.html', {'message': message})

def image_process(request, pk):
    img = get_object_or_404(Image, pk=pk)
    form = ImageProcessForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        img.composite(cd['width'], cd['height'], cd['left'], cd['top'], cd['right'], cd['bottom'])
        return redirect('image_list')
    return render(request, 'core/image_process.html', {'form': form, 'image': img})

def image_delete(request):
    file_name = request.GET.get('fileName')
    if not file_name:
        return HttpResponseBadRequest("Missing fileName.")

    base_name = os.path.basename(file_name)
    media_path = os.path.join(settings.MEDIA_UPLOADS, os.path.basename(file_name))

    Image.objects.filter(file__icontains=base_name).delete()

    if os.path.exists(media_path):
        os.remove(media_path)
        message = "Image deleted successfully."
    else:
        message = "Image not found."

    #return HttpResponseRedirect(reverse('image_list') + f"?message={message}")
    return render(request, 'core/image_list.html', {'message': message})

def image_details(request):
    file_name = request.GET.get('fileName')
    image_obj = get_object_or_404(Image, file__icontains=file_name)
    return render(request, 'core/image_details.html', {'image': image_obj})