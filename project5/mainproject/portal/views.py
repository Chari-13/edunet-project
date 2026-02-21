import json
import os
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required


from google import genai
from .models import Alert


# ================= BASIC PAGES ================= #
def home(request):
    alerts = Alert.objects.filter(status='active')

    alert_data = []
    for alert in alerts:
        alert_data.append({
            "disaster_type": alert.disaster_type,
            "severity": alert.severity,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "description": alert.description,
        })

    context = {
        "alerts": alerts,
        "alert_data": json.dumps(alert_data),
    }

    return render(request, "home.html", context)


import json
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    alerts = Alert.objects.filter(status='active')

    alert_data = []
    for alert in alerts:
        alert_data.append({
            "disaster_type": alert.disaster_type,
            "severity": alert.severity,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "description": alert.description,
        })

    context = {
        "alerts": alerts,
        "alert_data": json.dumps(alert_data),
    }

    return render(request, "dashboard.html", context)





def alerts(request):
    import requests

    try:
        # Karnataka center coordinates (you can change)
        lat = 12.9716
        lon = 77.5946

        api_key = settings.OPENWEATHER_API_KEY

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )

        response = requests.get(weather_url, timeout=5)
        weather = response.json()

        if weather.get("cod") == 200:
            temp = weather["main"]["temp"]
            condition = weather["weather"][0]["description"].lower()

            # 🔥 HEATWAVE CONDITION
            if temp >= 40:
                Alert.objects.get_or_create(
                    disaster_type="Heatwave Alert",
                    location="Karnataka",
                    severity="High",
                    description="Extreme heat detected. Avoid outdoor exposure, stay hydrated, and remain indoors during peak hours.",
                    latitude=12.9716,
                    longitude=77.5946,
                    status="active"
                )

            # 🌧 HEAVY RAIN CONDITION
            if "rain" in condition:
                Alert.objects.get_or_create(
                    disaster_type="Heavy Rain Alert",
                    location="Karnataka",
                    severity="Medium",
                    description="Heavy rainfall detected. Risk of flooding in low-lying areas. Move to safer elevated areas.",
                    latitude=12.9716,
                    longitude=77.5946,
                    status="active"
                )

            # 🌪 CYCLONE CONDITION
            if "storm" in condition or "cyclone" in condition:
                Alert.objects.get_or_create(
                    disaster_type="Storm Alert",
                    location="Karnataka",
                    severity="High",
                    description="Severe storm conditions detected. Stay indoors and avoid travel.",
                    latitude=12.9716,
                    longitude=77.5946,
                    status="active"
                )

    except Exception:
        pass  # prevent crash if weather API fails

    alerts = Alert.objects.filter(status='active')

    return render(request, "alerts.html", {
        "alerts": alerts
    })




def safety(request):
    return render(request, "safety.html")


def contact(request):
    return render(request, "contact.html")


def disaster_ai(request):
    return render(request, "disaster_ai.html", {
        "alerts": Alert.objects.all()
    })


# ================= LOCATION + WEATHER ================= #

def get_location_weather(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if not lat or not lon:
        return JsonResponse({"error": "Location not provided"}, status=400)

    try:
        # -------- Reverse Geocoding -------- #
        geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {"User-Agent": "DisasterAlertApp"}
        geo_response = requests.get(geo_url, headers=headers, timeout=5)
        geo_data = geo_response.json()

        address = geo_data.get("address", {})
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("state")
            or "Unknown"
        )
        country = address.get("country", "Unknown")

        # -------- Weather API -------- #
        api_key = "28bed61908410cd0fe990299b2cd50cd"  # <-- Hardcoded API key

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()

        if weather_data.get("cod") != 200:
            raise Exception(weather_data.get("message", "Failed to fetch weather"))

        temperature = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]

        return JsonResponse({
            "city": city,
            "country": country,
            "temperature": temperature,
            "condition": condition
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# ================= GEMINI AI CHAT ================= #

def ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({
                "success": False,
                "error": "Message is required"
            }, status=400)

        api_key = settings.GEMINI_API_KEY

        if not api_key:
            return JsonResponse({
                "success": False,
                "error": "API key not configured in server"
            }, status=500)

        client = genai.Client(api_key=api_key)

        alerts = Alert.objects.all()

        if alerts.exists():
            alerts_context = "Current Disaster Alerts:\n"
            for alert in alerts:
                alerts_context += (
                    f"- {alert.disaster_type} in {alert.location}\n"
                    f"  Severity: {alert.severity}\n"
                    f"  Status: {alert.status}\n"
                    f"  Description: {alert.description}\n"
                    f"  Time: {alert.date_time}\n\n"
                )
        else:
            alerts_context = "No active disaster alerts."

        prompt = f"""
You are a Disaster Management AI assistant.

{alerts_context}

User Question:
{user_message}

Provide a clear, accurate, and safety-focused response.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = response.text if response and response.text else "No response generated."

        return JsonResponse({
            "success": True,
            "response": reply
        })

    except Exception as e:
        error_msg = str(e)

        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            return JsonResponse({
                "success": False,
                "error": "AI service temporarily unavailable due to quota limits. Please try again later."
            }, status=429)

        return JsonResponse({
            "success": False,
            "error": error_msg
        }, status=500)


# ================= AUTHENTICATION ================= #

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")
