import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404

from .models import ShortURL
from .utils import generateURL


@csrf_exempt
def shorten_url(request):
    """
    This API handles URL shortening.
    It accepts a POST request with a JSON body containing a long URL
    and returns a short code + full short URL.
    """

    # Check if request method is POST
    if request.method == "POST":
        try:
            # Parse JSON data sent from frontend
            data = json.loads(request.body)
            original_url = data.get("url")
        except Exception:
            # If JSON is invalid or cannot be parsed
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # If request does not contain a URL
        if not original_url:
            return JsonResponse({"error": "URL is required"}, status=400)

        # Check if this URL already exists in the database
        existing = ShortURL.objects.filter(original_url=original_url).first()

        # If URL already exists, return the same short URL
        if existing:
            short_url = request.build_absolute_uri(f"/{existing.short_code}")
            return JsonResponse({
                "short_code": existing.short_code,
                "short_url": short_url
            })

        # If URL does not exist, generate a new short code
        short_code = generateURL()

        # Save new URL mapping in database
        ShortURL.objects.create(
            original_url=original_url,
            short_code=short_code
        )

        # Build the full shortened URL 
        short_url = request.build_absolute_uri(f"/{short_code}")

        # Return the shortened URL to the user
        return JsonResponse({
            "short_code": short_code,
            "short_url": short_url
        })

    # If request method is not POST, inform the user
    return JsonResponse(
        {"message": "Use POST method to shorten a URL"},
        status=405
    )


def redirect_url(request, short_code):
    """
    This view handles redirection.
    When a user opens a short URL, this function:
    1. Finds the original URL from the database
    2. Redirects the user to that original URL
    """

    # Check if a URL with this short_code exists in database
    short_url = get_object_or_404(ShortURL, short_code=short_code)

    # Redirect the user to the original long URL
    return redirect(short_url.original_url)
