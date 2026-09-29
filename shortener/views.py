from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
import secrets
import string


def home(request):

    urls = URL.objects.all().order_by('-created_at')

    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        # Check if URL is empty
        if not original_url:
            return render(
                request,
                'shortener/home.html',
                {'error': 'Please enter a URL.'}
            )

        # Generate a unique 6-character short code
        characters = string.ascii_letters + string.digits

        while True:
            short_code = ''.join(
                secrets.choice(characters) for _ in range(6)
            )

            if not URL.objects.filter(short_code=short_code).exists():
                break

        # Save URL and short code to database
        url = URL.objects.create(
            original_url=original_url,
            short_code=short_code
        )

        # Create complete short URL
        short_url = request.build_absolute_uri(
            '/' + short_code + '/'
        )

        print("Original URL:", original_url)
        print("Short Code:", short_code)

        return render(
            request,
            'shortener/home.html',
            {'short_url': short_url,
             'clicks': url.clicks
            }
        )

    return render(request, 'shortener/home.html',{'urls':urls})


def redirect_url(request, short_code):

    url = get_object_or_404(URL, short_code=short_code)

    # Increase click count
    url.clicks += 1
    url.save()

    return redirect(url.original_url)