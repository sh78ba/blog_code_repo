from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.db import IntegrityError
from .models import User
from core.email import normalize_email
from core.bloom import email_bloom
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    raw_email = data.get("email")
    password = data.get("password")

    if not raw_email or not password:
        return JsonResponse({"error": "Missing fields"}, status=400)

    # Normalize
    email = normalize_email(raw_email)

    # Bloom filter check
    if email not in email_bloom:
        # definitely new → skip DB read
        try:
            user = User.objects.create(email=email, password=password)

            #  Add to Bloom
            email_bloom.add(email)

            return JsonResponse({"message": "Signup successful"})

        except IntegrityError:
            # race condition fallback
            pass

    # Maybe exists → check DB
    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "message": "If this email is valid, you'll receive a link"
        })

    # Try insert anyway (race-safe)
    try:
        user = User.objects.create(email=email, password=password)
        email_bloom.add(email)

        return JsonResponse({"message": "Signup successful"})

    except IntegrityError:
        return JsonResponse({
            "message": "If this email is valid, you'll receive a link"
        })