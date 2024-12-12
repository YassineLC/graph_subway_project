from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import random  # Pour avoir un fallback si la reconnaissance vocale ne fonctionne pas

def index(request):
    return render(request, 'index.html')

def ecoute(request):
    recognizer = sr.Recognizer()

    # Dictionnaire des couleurs et leurs codes hexadécimaux
    couleur_mapping = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'jaune': '#FFFF00',
        'orange': '#FFA500',
        'violet': '#800080',
        'noir': '#000000',
        'blanc': '#FFFFFF'
    }

    try:
        # Utilisation du microphone pour capturer la voix
        with sr.Microphone() as source:
            # Ajuste le niveau de bruit ambiant
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Écoute la commande pendant un certain temps
            audio = recognizer.listen(source, timeout=5)

            # Utilisation de Google pour la reconnaissance vocale
            texte = recognizer.recognize_google(audio, language='fr-FR').lower()
            print(f"Texte reconnu : {texte}")  # Pour le débogage

            # Recherche d'une couleur dans le texte
            for couleur, couleur_hexa in couleur_mapping.items():
                if couleur in texte:
                    return JsonResponse({'couleur': couleur_hexa, 'nom': couleur})

        # Si aucune couleur n'est trouvée, retourner une erreur
        return JsonResponse({'error': 'Aucune couleur reconnue. Essayez une autre couleur.'})

    except sr.UnknownValueError:
        # Fallback pour le développement/démonstration
        couleur = random.choice(list(couleur_mapping.items()))
        return JsonResponse({'couleur': couleur[1], 'nom': couleur[0]})
    
    except sr.RequestError:
        # Fallback pour le développement/démonstration
        couleur = random.choice(list(couleur_mapping.items()))
        return JsonResponse({'couleur': couleur[1], 'nom': couleur[0]})
    
    except Exception as e:
        # Pour gérer toute autre exception
        return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'})