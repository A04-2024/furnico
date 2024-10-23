from django.shortcuts import render

def show_rating(request):
    context = {
        'rating': 5
    }

    return render(request, "rating.html", context)
