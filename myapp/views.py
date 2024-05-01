from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Attendance
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from django.conf import settings
from deepface import DeepFace  # Import DeepFace for face recognition
from .models import UserProfile
import cv2
import json
from django.utils import timezone


# @csrf_exempt  # Allow AJAX POST requests
def process_attendance(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("andar")
        # data = request.json() if request.json else request.POST
        data = json.loads(request.body)
        image_data = data.get('image')
        print("hello")

        if image_data:
            # Remove the data URL prefix and decode the base64 image
            img_str = image_data.split(",")[1]
            img_bytes = base64.b64decode(img_str)

            # Save the image temporarily to process with DeepFace
            img_path = os.path.join(settings.MEDIA_ROOT, 'capturedimage.jpg')  # Temporary image storage
            with open(img_path, 'wb') as img_file:
                img_file.write(img_bytes)  # Write the image to a file

            # Match the captured image with profile pictures using DeepFace
            db_path = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')  # Path to profile pictures

            try:
                # Use DeepFace to find a matching face
                dfs = DeepFace.find(img_path=img_path, db_path=db_path, detector_backend='opencv', enforce_detection=False)

                # Check if a match was found
                if len(dfs) > 0:  # If a match is found
                    # Get the first match (assuming a single match is sufficient)
                    match = dfs[0]
                    print(f"this is dfs: {dfs} and this is dfs[0]: {dfs[0]}")
                    # Extract the matched user profile from the returned DeepFace match
                    matched_user_profile = None
                    if 'identity' in match:
                        print("hello")
                        # Extract the user profile based on the matched identity
                        # identity = os.path.basename(match['identity'])  # Get the base name of the matched file
                        identity = match['identity'][0]
                        print(identity)
                        x = identity.split("profile_pictures")[1]
                        identity = x[1:]
                        print(f"After deleting: {identity}")
                        matched_user_profile = UserProfile.objects.filter(profile_picture__endswith=identity).first()
                        print(f"matched_user_profile: {matched_user_profile}")

                    # If a matching user profile is found, mark attendance
                    if matched_user_profile:
                        print("kind")
                        # Create a new attendance record for the matched user profile
                        Attendance.objects.create(
                            user_profile=matched_user_profile,
                            date=timezone.now().date(),
                            time=timezone.now().time(),
                            status="Present"
                        )
                        return JsonResponse({'match': True, 'name': matched_user_profile.name, 'enrollment': matched_user_profile.user.username, 'department': matched_user_profile.department, 'semester': matched_user_profile.semester})  # Face recognized, attendance marked

                return JsonResponse({'match': False})  # No match found

            except Exception as e:
                print("DeepFace Error:", e)  # Handle DeepFace errors
                return JsonResponse({'match': False})  # No match found or error occurred
            
            finally:
                # Ensure the captured image is deleted after processing
                if os.path.exists(img_path):  # Check if the file exists
                    os.remove(img_path)  # Delete the temporary file

    return JsonResponse({'error': 'Invalid request'})  # If the request method is not POST

def mark_attendance(request):
    return render(request, 'mark_attendance.html')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required  # Ensure the user is logged in
def dashboard(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    context['user']=user
    # Get the UserProfile for the logged-in user
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile:
            context['user_profile']=user_profile
        try:
            attendance_records = Attendance.objects.filter(user_profile=user_profile)
            if attendance_records:
                context['attendance_records']=attendance_records
        except:
            pass
    except:
        pass

    # Retrieve all attendance records for this user
    
    return render(request, 'dashboard.html', context)

@login_required  # Ensure the user is logged in
def edit(request):
    if request.method == 'POST':
        name = request.POST.get('student-name')
        department = request.POST.get('department')
        semester = request.POST.get('semester')

        # Get the current user and create or update their profile
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user)
        user_profile.name = name
        user_profile.department = department
        user_profile.semester = semester
        if 'profile_picture' in request.FILES:
            # Check if a profile image already exists
            if user_profile.profile_picture:
                # Delete the existing profile image from storage
                default_storage.delete(user_profile.profile_picture.path)

            # Assign the new profile image
            # user_profile.profile_image = request.FILES['profile_image']

            # below code is for compression of profile image and then store
            profile_picture = request.FILES['profile_picture']

            # Open the uploaded image using PIL
            img = Image.open(profile_picture)
            # Convert image to RGB mode if it's in RGBA mode
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Create an in-memory stream to save the image data
            output_stream = BytesIO()

            # Save the image with reduced quality (adjust quality as needed, 0-100)
            img.save(output_stream, format='JPEG', quality=70)

            # Save the compressed image to the UserProfile object
            user_profile.profile_picture.save(
                profile_picture.name,
                content=ContentFile(output_stream.getvalue()),
                save=False
            )
        user_profile.save()
        return redirect('dashboard')
    return render(request, 'edit.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        curr_user = authenticate(request, username=username, password=password)
        if curr_user is not None:
            auth_login(request, curr_user)
            return redirect('dashboard')
        else:
            # Display an error message for invalid login.
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'A user with this username already exists.'})

        
        if password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'Both password should be same.'})
        else:
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                curr_user = User.objects.create_user(username, email, password)
                curr_user.save()
                login_user = authenticate(
                    request, username=username, password=password)
                auth_login(request, login_user)
                return redirect('dashboard')  # Redirect to your login page
            else:
                return render(request, 'signup.html', {'error_message': 'One user with this email already exists.'})
    return render(request, 'signup.html')


def log_out(request):
    logout(request)
    return redirect('login')