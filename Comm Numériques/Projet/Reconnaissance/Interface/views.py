from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr

def index(request):
    return render(request, 'index.html')

def ecoute(request):
    recognizer = sr.Recognizer()
    couleurMapping = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF'
    }

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
            texte = recognizer.recognize_google(audio, language='fr-FR').lower()
            
            for couleur, couleurHexa in couleurMapping.items():
                if couleur in texte:
                    return JsonResponse({'couleur': couleurHexa, 'nom': couleur})

        return JsonResponse({'error': 'Aucune couleur reconnue'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
