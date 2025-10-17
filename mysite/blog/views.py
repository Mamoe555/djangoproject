from django.shortcuts import render, redirect
from .models import Post, Category
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    posts = Post.objects.all().order_by('-created_at')
    
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {'page_obj': page_obj, 'categories': categories, 'query': query})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'blog/post_form.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you could save the message to the database or send an email
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache this view for 5 minutes
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Pagination (if you have it)
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories': categories,
    })
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Compose email
            subject = f"New Contact Message from {name}"
            full_message = f"Message from {name} ({email}):\n\n{message}"

            # Send email
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Your email receives the message
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # redirect to the contact page
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})

from django.shortcuts import render

def contact_success(request):
    return render(request, 'blog/contact_success.html')



