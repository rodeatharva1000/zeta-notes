from django.shortcuts import render, redirect
from .forms import AddContentForm, AddSubjectForm, ChooseSubjectForm
from django.contrib import messages
from .models import Content
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Content
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Content
from django.http import HttpResponseForbidden


def home_view(request):
    user_content = Content.objects.filter(uploaded_by=request.user)
    return render(request, 'materials/home.html', {'contents' : user_content})

@login_required
def add_subject_view(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'subject added !')
            return redirect('home')
        else:
            messages.error(request, 'There was a problem adding the subject. Please check the form.')

    else:
        form = AddSubjectForm()

    return render(request, 'materials/add_subject.html', {'form' : form})

@login_required
def add_content_view(request):
    if request.method == 'POST':
        form = AddContentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            messages.success(request, 'content added !')
            return redirect('home')
        else:
            messages.error(request, 'There was a problem adding the content. Please check the form.')
    else:
        form = AddContentForm()

    return render(request, 'materials/add_content.html', {'form' : form})

@login_required
def show_content(request, id):
    content = Content.objects.filter(subject__id=id)
    return render(request, 'materials/show_content.html', {'content' : content})

@login_required
def choose_subject(request):
    if request.method == 'POST':
        form = ChooseSubjectForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            return redirect('show', subject.id)
    else:
        form = ChooseSubjectForm()

    return render(request, 'materials/choose_subject.html', {'form': form})

def detail_view(request, pk):
    material = get_object_or_404(Content, pk=pk)
    context = {
        'file_url': material.file.url
    }
    print(material.file.url)
    return render(request, 'materials/detail.html', context)

import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.http import JsonResponse
import json
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            # Load user input from the request
            data = json.loads(request.body)
            user_input = data.get('message', '')

            # Send to Gemini API
            gemini_api_key = settings.GEMINI_API_KEY  # Store your API key securely
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"

            payload = {
                "contents": [{
                    "parts": [{"text": user_input}]
                }]
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post(gemini_url, headers=headers, json=payload)

            # Check if the response is valid
            response.raise_for_status()  # This will raise an exception for non-2xx responses

            # Parse the response
            try:
                reply = response.json()['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError):
                reply = "Sorry, something went wrong with the response."
            except Exception as e:
                reply = f"Error parsing the response: {str(e)}"

        except requests.exceptions.RequestException as e:
            reply = f"Error sending request: {str(e)}"
        except json.JSONDecodeError:
            reply = "Invalid JSON in the request."
        except Exception as e:
            reply = f"Unexpected error: {str(e)}"

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "GET method not allowed"}, status=405)


@login_required
def edit_view(request, id):
    obj = Content.objects.get(id=id)
    if obj.uploaded_by != request.user:
        return HttpResponseForbidden('You cant delete this !')

    if request.method == 'POST':
        form = AddContentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddContentForm(instance=obj)

    return render(request, 'materials/add_content.html', {'form' : form})

@login_required
def delete_view(request, id):
    obj = Content.objects.get(id=id)

    if obj.uploaded_by != request.user:
        return HttpResponseForbidden('You cant delete this !')
    obj.delete()
    return redirect('home')