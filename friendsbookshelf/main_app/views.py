from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from main_app.models import Post, Comment
from users.models import FriendList
from users.forms import UserLoginForm
from users.forms import UserRegisterForm
from main_app.forms import UserPostForm


def home_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserPostForm(user=request.user, data=request.POST)

            if form.is_valid():
                post = form.cleaned_data['post']
                book = form.cleaned_data['book_choice']

                if not book:
                    book = None
                    
                Post.objects.create(description=post, user=request.user, book=book)
        else:
            form = UserPostForm(request.user)

        friend_list = FriendList.objects.select_related(
            'friend').filter(user=request.user, accept=True).values_list('friend', flat=True)
        posts = Post.objects.select_related('book', 'user').prefetch_related(
            'comments', 'comments__user').filter(Q(user=request.user) | Q(user__in=friend_list)).order_by('-created_date')
        return render(request, 'newsfeed.html', {'posts': posts, 'form': form})
    else:
        return render(request, 'home.html')


@csrf_exempt
def post_comment(request):
    if request.is_ajax():
        text = request.POST.get('text')
        comment = Comment.objects.create(text=text, user=request.user)
        post = Post.objects.get(id=request.POST.get('post_id'))
        post.comments.add(comment)
        return JsonResponse({'text': text, 'user_id': request.user.id, 'full_name': request.user.first_name + ' ' + request.user.last_name})