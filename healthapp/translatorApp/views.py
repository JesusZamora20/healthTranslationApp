from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import os
import openai 
from dotenv import load_dotenv

load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("API Key not found")

def translate_text(text, target_language):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_language}:"},
            {"role": "user", "content": text},
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

def index(request):
    return render(request, 'translator/index.html')

def translate(request):
    if request.method == 'POST':
        original_text = request.POST.get('text')
        target_language = request.POST.get('language')
        translated_text = translate_text(original_text, target_language)
        return JsonResponse({'translated_text': translated_text})
    return JsonResponse({'error': 'Invalid request'}, status=400)