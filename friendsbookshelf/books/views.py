from django.shortcuts import render

def books_wishlist(request):
    return render(request, 'books_wishlist.html')

def books_liked(request):
    return render(request, 'books_liked.html')
