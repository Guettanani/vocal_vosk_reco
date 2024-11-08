# #!/usr/bin/env python3

# import json
# import os
# import sys
# import asyncio
# import websockets
# import logging
# import sounddevice as sd
# import argparse
# import requests

# #############################################################################
# import json

# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     La chaîne doit contenir un message partiel en format JSON.
#     """
#     try:
#         # Trouver le début de la partie JSON dans la chaîne
#         debut_json = chaine.find('{')
        
#         # Si on trouve la partie JSON, extraire cette partie
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             # Charger la chaîne JSON sous forme d'objet Python
#             data = json.loads(json_str)
            
#             # Récupérer la valeur de la clé "partial" si elle existe
#             if "partial" in data:
#                 return data["partial"]
#             else:
#                 return "Aucun message essentiel trouvé."
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError:
#         return "Erreur lors de l'analyse du JSON."
# #############################################################################
# def envoyer_message_ollama(message):
#     """
#     Envoie un message à Ollama via une requête HTTP et renvoie la réponse.
#     """
#     url = "http://ollama:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "prompt": message,
#         # "config": {"param1": "valeur1", "param2": "valeur2"}  # Configuration spécifique à Ollama si nécessaire
#     }
#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama: {e}")
#         return "Erreur lors de la communication avec Ollama."
# #############################################################################



# def int_or_str(text):
#     """Helper function for argument parsing."""
#     try:
#         return int(text)
#     except ValueError:
#         return text

# def callback(indata, frames, time, status):
#     """This is called (from a separate thread) for each audio block."""
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# async def run_test():
#     url = f"{http://ollama:11434}/api/generate"
#     with sd.RawInputStream(samplerate=args.samplerate, blocksize = 4000, device=args.device, dtype='int16',
#                            channels=1, callback=callback) as device:

#         async with websockets.connect(args.uri) as websocket:
#             await websocket.send('{ "config" : { "sample_rate" : %d } }' % (device.samplerate))

#             while True:
#                 data = await audio_queue.get()
#                 await websocket.send(data)
#                 commande = await websocket.recv()
#                 message_reçu = extraire_message_essentiel(commande)
#                 #  # Envoi du message à Ollama et récupération de la réponse
#                 # reponse_ollama = envoyer_message_ollama(message_reçu)
#                 # Vérifier si le message n'est pas vide avant d'envoyer à Ollama
#                 if message_reçu.strip():
#                     reponse_ollama = envoyer_message_ollama(message_reçu)
#                     print(f"Réponse d'Ollama : {reponse_ollama}")
#                 else:
#                     print("Aucun message essentiel à envoyer à Ollama.")

#                 print (await websocket.recv())
#                 print(f"Réponse d'Ollama : {reponse_ollama}")

#             await websocket.send('{"eof" : 1}')
#             print (await websocket.recv())

# async def main():

#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(add_help=False)
#     parser.add_argument('-l', '--list-devices', action='store_true',
#                         help='show list of audio devices and exit')
#     args, remaining = parser.parse_known_args()
#     if args.list_devices:
#         print(sd.query_devices())
#         parser.exit(0)
#     parser = argparse.ArgumentParser(description="ASR Server",
#                                      formatter_class=argparse.RawDescriptionHelpFormatter,
#                                      parents=[parser])
#     parser.add_argument('-u', '--uri', type=str, metavar='URL',
#                         help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int_or_str,
#                         help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args(remaining)
#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     logging.basicConfig(level=logging.INFO)
#     await run_test()

# if __name__ == '__main__':
#     asyncio.run(main())


#!/usr/bin/env python3

# Importation des bibliothèques nécessaires
# import json  # pour le traitement des données JSON
# import os    # pour les interactions avec le système d'exploitation
# import sys   # pour l'interaction avec les arguments système
# import asyncio  # pour les opérations asynchrones
# import websockets  # pour la gestion des connexions WebSocket
# import logging  # pour la gestion des logs
# import sounddevice as sd  # pour la capture audio
# import argparse  # pour l'analyse des arguments de la ligne de commande
# import requests  # pour envoyer des requêtes HTTP

# #############################################################################
# # Fonction pour extraire le message essentiel d'une chaîne JSON partielle

# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     La chaîne doit contenir un message partiel en format JSON.
#     """
#     try:
#         # Trouver le début de la partie JSON dans la chaîne
#         debut_json = chaine.find('{')
        
#         # Si une partie JSON est trouvée, l'extraire
#         if debut_json != -1:
#             json_str = chaine[debut_json:]  # Extraire la chaîne JSON
#             data = json.loads(json_str)  # Convertir en objet Python
            
#             # Récupérer la valeur de la clé "partial" si elle existe
#             if "partial" in data:
#                 return data["partial"]  # Retourner le message partiel trouvé
#             else:
#                 return "Aucun message essentiel trouvé."
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError:
#         return "Erreur lors de l'analyse du JSON."
# #############################################################################

# # Fonction pour envoyer un message à Ollama et obtenir une réponse
# def envoyer_message_ollama(message):
#     """
#     Envoie un message à Ollama via une requête HTTP et renvoie la réponse.
#     """
#     url = "http://ollama:11434/api/generate"  # URL de l'API Ollama
#     headers = {'Content-Type': 'application/json'}  # En-tête HTTP pour le type JSON
#     payload = {
#         "prompt": message,  # Corps de la requête contenant le message à envoyer
#     }
#     try:
#         response = requests.post(url, headers=headers, json=payload)  # Envoie de la requête POST
#         response.raise_for_status()  # Lève une exception pour les erreurs HTTP
#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")  # Retourne la réponse
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama: {e}")  # Log de l'erreur
#         return "Erreur lors de la communication avec Ollama."
# #############################################################################

# # Fonction utilitaire pour l'analyse des arguments, permet d'accepter soit un entier soit une chaîne
# def int_or_str(text):
#     """Helper function for argument parsing."""
#     try:
#         return int(text)  # Tente de convertir le texte en entier
#     except ValueError:
#         return text  # Sinon, retourne le texte tel quel

# # Callback appelé pour chaque bloc audio capturé
# def callback(indata, frames, time, status):
#     """This is called (from a separate thread) for each audio block."""
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))  # Met les données audio dans la file d'attente

# # Fonction principale pour gérer les tests
# async def run_test():
#     url = f"http://localhost:11434/api/generate"  # URL pour envoyer les messages à Ollama
#     TAILLE_MINIMALE_MESSAGE = 10  # Taille minimale pour le message à envoyer

#     # Initialisation de la capture audio
#     with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                            channels=1, callback=callback) as device:

#         # Connexion au serveur WebSocket
#         async with websockets.connect(args.uri) as websocket:
#             # Envoie de la configuration du flux audio au serveur WebSocket
#             await websocket.send('{ "config" : { "sample_rate" : %d } }' % (device.samplerate))

#             # Boucle pour capturer et traiter chaque bloc audio
#             while True:
#                 data = await audio_queue.get()  # Récupère le bloc audio dans la file d'attente
#                 await websocket.send(data)  # Envoie les données audio au serveur WebSocket
#                 commande = await websocket.recv()  # Reçoit la réponse du serveur
#                 message_reçu = extraire_message_essentiel(commande)  # Extrait le message essentiel

#                 # Vérifie si le message est non vide et dépasse la taille minimale
#                 if message_reçu.strip() and len(message_reçu) >= TAILLE_MINIMALE_MESSAGE:
#                     reponse_ollama = envoyer_message_ollama(message_reçu)  # Envoie le message à Ollama
#                     print(f"Réponse d'Ollama : {reponse_ollama}")  # Affiche la réponse
#                 else:
#                     print("Message ignoré : soit vide ou trop court pour être envoyé à Ollama.")

#             await websocket.send('{"eof" : 1}')  # Indique la fin du flux audio
#             print(await websocket.recv())  # Reçoit la réponse finale du serveur WebSocket

# # Fonction principale pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(add_help=False)  # Initialisation de l'analyseur d'arguments
#     parser.add_argument('-l', '--list-devices', action='store_true',
#                         help='show list of audio devices and exit')  # Argument pour lister les périphériques audio
#     args, remaining = parser.parse_known_args()  # Analyse des arguments initiaux
#     if args.list_devices:
#         print(sd.query_devices())  # Affiche les périphériques audio disponibles
#         parser.exit(0)
        
#     parser = argparse.ArgumentParser(description="ASR Server",
#                                      formatter_class=argparse.RawDescriptionHelpFormatter,
#                                      parents=[parser])  # Réinitialisation de l'analyseur d'arguments
#     parser.add_argument('-u', '--uri', type=str, metavar='URL',
#                         help='Server URL', default='ws://localhost:2700')  # URL du serveur WebSocket
#     parser.add_argument('-d', '--device', type=int_or_str,
#                         help='input device (numeric ID or substring)')  # Sélection du périphérique audio
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)  # Taux d'échantillonnage
#     args = parser.parse_args(remaining)  # Récupère les arguments finaux

#     loop = asyncio.get_running_loop()  # Obtient la boucle d'événements asynchrones en cours
#     audio_queue = asyncio.Queue()  # Crée une file d'attente asynchrone pour les blocs audio

#     logging.basicConfig(level=logging.INFO)  # Configuration des logs pour afficher les messages de niveau INFO
#     await run_test()  # Appel de la fonction principale de test

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())  # Démarre le programme en utilisant la boucle d'événements asynchrones






#!/usr/bin/env python3

# import json  # pour le traitement des données JSON
# import os    # pour les interactions avec le système d'exploitation
# import sys   # pour l'interaction avec les arguments système
# import asyncio  # pour les opérations asynchrones
# import websockets  # pour la gestion des connexions WebSocket
# import logging  # pour la gestion des logs
# import sounddevice as sd  # pour la capture audio
# import argparse  # pour l'analyse des arguments de la ligne de commande
# import requests  # pour envoyer des requêtes HTTP
# import re
# #############################################################################
# # Fonction pour extraire le message essentiel d'une chaîne JSON partielle

# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     La chaîne doit contenir un message partiel en format JSON.
#     """
#     ##logging.debug(f"Chaîne reçue pour extraction du message essentiel : {chaine}")
#     try:
#         # Trouver le début de la partie JSON dans la chaîne
#         debut_json = chaine.find('{')
        
#         # Si une partie JSON est trouvée, l'extraire
#         if debut_json != -1:
#             json_str = chaine[debut_json:]  # Extraire la chaîne JSON
#             data = json.loads(json_str)  # Convertir en objet Python
#             ##logging.debug(f"Contenu JSON extrait : {data}")
            
#             # Récupérer la valeur de la clé "partial" si elle existe
#             if "partial" in data:
#                 ##logging.info(f"Message essentiel extrait : {data['partial']}")
#                 return data["partial"]  # Retourner le message partiel trouvé
#             else:
#                 ##logging.info("Clé 'partial' non trouvée dans les données JSON.")
#                 return "Aucun message essentiel trouvé."
#         else:
#             ##logging.warning("Format incorrect, partie JSON manquante.")
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         ##logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."
# #############################################################################
# def extract_responses(log_text):
#     # Regex pour capturer le champ "response" des messages JSON
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     # Recherche des réponses et les concatène
#     responses = re.findall(pattern, log_text)
#     # Joint les réponses pour former le texte complet
#     full_response = ''.join(responses)
#     return full_response.strip()
# # Fonction pour envoyer un message à Ollama et obtenir une réponse
# def envoyer_message_ollama(message):
#     """
#     Envoie un message à Ollama via une requête HTTP et renvoie la réponse.
#     """
#     url = "http://localhost:11434/api/generate"  # URL de l'API Ollama, utilisez 'localhost' si Ollama est local
#     headers = {'Content-Type': 'application/json'}  # En-tête HTTP pour le type JSON
#     payload = {
#         "model" : "neural-chat",
#         "prompt": message,  # Corps de la requête contenant le message à envoyer
#     }
#     logging.info(f"Envoi du message à Ollama : {message}")
#     ##logging.debug(f"Payload envoyé à Ollama : {json.dumps(payload)}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)  # Envoie de la requête POST
#         response.raise_for_status()  # Lève une exception pour les erreurs HTTP
#         ##logging.debug(f"Réponse brute de l'API Ollama : {response.text}")
#         result = extract_responses(response.text)
#         logging.info(f"Réponse extraite : {result}")
#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")  # Retourne la réponse
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")  # Log de l'erreur
#         return "Erreur lors de la communication avec Ollama."
# #############################################################################

# # Fonction utilitaire pour l'analyse des arguments, permet d'accepter soit un entier soit une chaîne
# def int_or_str(text):
#     """Helper function for argument parsing."""
#     try:
#         return int(text)  # Tente de convertir le texte en entier
#     except ValueError:
#         return text  # Sinon, retourne le texte tel quel

# # Callback appelé pour chaque bloc audio capturé
# def callback(indata, frames, time, status):
#     """Callback appelé pour chaque bloc audio capturé."""
#     if status:
#         logging.warning(f"Statut audio : {status}")  # Log les erreurs de statut audio
#     ##logging.debug(f"Bloc audio capturé avec {frames} frames.")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))  # Met les données audio dans la file d'attente

# # Fonction principale pour gérer les tests
# async def run_test():
#     TAILLE_MINIMALE_MESSAGE = 10  # Taille minimale pour le message à envoyer
#     ##logging.info(f"URL WebSocket : {args.uri}, URL API Ollama : http://localhost:11434/api/generate")

#     # Initialisation de la capture audio
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback) as device:
#             ##logging.info("Flux audio initialisé avec succès.")

#             # Connexion au serveur WebSocket
#             async with websockets.connect(args.uri) as websocket:
#                 ##logging.info(f"Connecté au WebSocket à l'URL {args.uri}")
#                 # Envoie de la configuration du flux audio au serveur WebSocket
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % (device.samplerate))

#                 # Boucle pour capturer et traiter chaque bloc audio
#                 while True:
#                     data = await audio_queue.get()  # Récupère le bloc audio dans la file d'attente
#                     ##logging.debug("Données audio récupérées de la file d'attente et prêtes à être envoyées.")
#                     await websocket.send(data)  # Envoie les données audio au serveur WebSocket
#                     ##logging.info("Données audio envoyées au serveur WebSocket.")

#                     commande = await websocket.recv()  # Reçoit la réponse du serveur
#                     ##logging.debug(f"Message reçu du serveur WebSocket : {commande}")
#                     message_reçu = extraire_message_essentiel(commande)  # Extrait le message essentiel

#                     # Vérifie si le message est non vide et dépasse la taille minimale
#                     if message_reçu.strip() and len(message_reçu) >= TAILLE_MINIMALE_MESSAGE:
#                         ##logging.info("Message reçu à envoyer à Ollama.")
#                         reponse_ollama = envoyer_message_ollama(message_reçu)  # Envoie le message à Ollama
#                         ##logging.info(f"Réponse d'Ollama : {reponse_ollama}")
#                         print(f"Réponse d'Ollama : {reponse_ollama}")  # Affiche la réponse
#                     else:
#                         logging.info("Message ignoré : soit vide ou trop court pour être envoyé à Ollama.")

#                 await websocket.send('{"eof" : 1}')  # Indique la fin du flux audio
#                 print(await websocket.recv())  # Reçoit la réponse finale du serveur WebSocket

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction principale pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(add_help=False)  # Initialisation de l'analyseur d'arguments
#     parser.add_argument('-l', '--list-devices', action='store_true',
#                         help='show list of audio devices and exit')  # Argument pour lister les périphériques audio
#     args, remaining = parser.parse_known_args()  # Analyse des arguments initiaux
#     if args.list_devices:
#         print(sd.query_devices())  # Affiche les périphériques audio disponibles
#         parser.exit(0)
        
#     parser = argparse.ArgumentParser(description="ASR Server",
#                                      formatter_class=argparse.RawDescriptionHelpFormatter,
#                                      parents=[parser])  # Réinitialisation de l'analyseur d'arguments
#     parser.add_argument('-u', '--uri', type=str, metavar='URL',
#                         help='Server URL', default='ws://localhost:2700')  # URL du serveur WebSocket
#     parser.add_argument('-d', '--device', type=int_or_str,
#                         help='input device (numeric ID or substring)')  # Sélection du périphérique audio
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)  # Taux d'échantillonnage
#     args = parser.parse_args(remaining)  # Récupère les arguments finaux

#     loop = asyncio.get_running_loop()  # Obtient la boucle d'événements asynchrones en cours
#     audio_queue = asyncio.Queue()  # Crée une file d'attente asynchrone pour les blocs audio

#     logging.basicConfig(level=logging.DEBUG)  # Configuration des logs pour afficher les messages de niveau DEBUG
#     ##logging.info("Démarrage du programme avec les configurations initiales.")
#     ##logging.info(f"URI WebSocket : {args.uri}, Taux d'échantillonnage : {args.samplerate}, Périphérique : {args.device}")

#     await run_test()  # Appel de la fonction principale de test

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())  # Démarre le programme en utilisant la boucle d'événements asynchrones




# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")
# def est_phrase_complete(texte):
#     """
#     Vérifie si la phrase est complète avant de l'envoyer à Ollama.
#     """
#     # Analyse de la phrase avec le modèle de langage
#     doc = nlp(texte)

#     # Vérification de la longueur minimale
#     if len(texte) < 10:
#         return False

#     # Vérification de la présence de ponctuation en fin de phrase
#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True

#     # Détection des mots-clés indiquant une phrase incomplète
#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False

#     # Vérification du nombre de phrases
#     sentences = list(doc.sents)
#     if len(sentences) == 1 and sentences[0].text == texte:
#         return True

#     return False



# # Fonction pour extraire le message essentiel d'une chaîne JSON partielle
# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     La chaîne doit contenir un message partiel en format JSON.
#     """
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             if "partial" in data:
#                 return data["partial"]
#             else:
#                 return "Aucun message essentiel trouvé."
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire la réponse d'Ollama
# def extract_responses(log_text):
#     # Regex pour capturer le champ "response" des messages JSON
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     full_response = ''.join(responses)
#     return full_response.strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse
# def envoyer_message_ollama(message):
#     """
#     Envoie un message à Ollama via une requête HTTP et renvoie la réponse.
#     """
#     url = "http://localhost:11434/api/generate"  # URL de l'API Ollama
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "model": "neural-chat",
#         "prompt": message,
#     }
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
#         result = extract_responses(response.text)
#         logging.info(f"Réponse extraite : {result}")
#         logging.info(f"=====================================================================================================================================")
#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Callback appelé pour chaque bloc audio capturé
# def callback(indata, frames, time, status):
#     """Callback appelé pour chaque bloc audio capturé."""
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer les tests
# async def run_test():
#     TAILLE_MINIMALE_MESSAGE = 10

#     # Initialisation de la capture audio
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri) as websocket:
#                 # Envoie de la configuration du flux audio au serveur WebSocket
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % (args.samplerate))

#                 # Boucle pour capturer et traiter chaque bloc audio
#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)

#                     # if message_reçu.strip() and len(message_reçu) >= TAILLE_MINIMALE_MESSAGE:
#                     #     reponse_ollama = envoyer_message_ollama(message_reçu)
#                     #     print(f"Réponse d'Ollama : {reponse_ollama}")
#                     # else:
#                     #     # logging.info("Message ignoré : soit vide ou trop court pour être envoyé à Ollama.")
#                     #     logging.info("")
#                     if est_phrase_complete(message_reçu):
#                         reponse_ollama = envoyer_message_ollama(message_reçu)
#                         print(f"Réponse d'Ollama : {reponse_ollama}")
#                     else:
#                         logging.info("Message ignoré : phrase incomplète")
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction principale pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())


# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# def est_phrase_complete(texte):
#     """
#     Vérifie si la phrase est complète avant de l'envoyer à Ollama.
#     """
#     doc = nlp(texte)

#     if len(texte) < 10:
#         return False

#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True

#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False

#     sentences = list(doc.sents)
#     if len(sentences) == 1 and sentences[0].text == texte:
#         return True

#     return False

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     """
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     full_response = ''.join(responses)
#     return full_response.strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "model": "neural-chat",
#         "prompt": message,
#     }
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()

#         # Extraction et validation de la réponse JSON
#         result = extract_responses(response.text)
#         logging.info(f"Réponse extraite : {result}")
#         logging.info(f"=========================================================")
#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     TAILLE_MINIMALE_MESSAGE = 10

#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri) as websocket:
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 # Boucle pour capturer et traiter chaque bloc audio
#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)

#                     if est_phrase_complete(message_reçu):
#                         reponse_ollama = envoyer_message_ollama(message_reçu)
#                         print(f"Réponse d'Ollama : {reponse_ollama}")
#                     else:
#                         logging.info("Message ignoré : phrase incomplète")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())



# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# import pyttsx3  # Import du module pour la synthèse vocale

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# # Initialisation du moteur de synthèse vocale
# engine = pyttsx3.init()

# def est_phrase_complete(texte):
#     """
#     Vérifie si la phrase est complète avant de l'envoyer à Ollama.
#     """
#     doc = nlp(texte)

#     if len(texte) < 10:
#         return False

#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True

#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False

#     sentences = list(doc.sents)
#     if len(sentences) == 1 and sentences[0].text == texte:
#         return True

#     return False

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     """
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     full_response = ''.join(responses)
#     return full_response.strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "model": "neural-chat",
#         "prompt": message,
#     }
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()

#         # Extraction et validation de la réponse JSON
#         result = extract_responses(response.text)
#         logging.info(f"Réponse extraite : {result}")
#         logging.info(f"=========================================================")

#         # Utilisation du moteur de synthèse vocale pour lire la réponse d'Ollama
#         logging.info("Lecture de la réponse d'Ollama.")
#         engine.say(result)  # Prépare la réponse pour la synthèse vocale
#         engine.runAndWait()  # Exécute la lecture

#         return response.json().get("response", "Aucune réponse reçue d'Ollama.")
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     TAILLE_MINIMALE_MESSAGE = 10

#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri) as websocket:
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 # Boucle pour capturer et traiter chaque bloc audio
#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)

#                     if est_phrase_complete(message_reçu):
#                         reponse_ollama = envoyer_message_ollama(message_reçu)
#                         print(f"Réponse d'Ollama : {reponse_ollama}")
#                     else:
#                         logging.info("Message ignoré : phrase incomplète")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())



# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# import pyttsx3  # Pour la synthèse vocale

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Initialisation du moteur de synthèse vocale
# engine = pyttsx3.init()

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# def est_phrase_complete(texte):
#     """
#     Vérifie si la phrase est complète avant de l'envoyer à Ollama.
#     """
#     doc = nlp(texte)

#     if len(texte) < 10:
#         return False

#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True

#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False

#     sentences = list(doc.sents)
#     if len(sentences) == 1 and sentences[0].text == texte:
#         return True

#     return False

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     """
#     Extrait le message essentiel à partir de la chaîne donnée.
#     """
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     full_response = ''.join(responses)
#     return full_response.strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "model": "neural-chat",
#         "prompt": message,
#     }
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
        
#         # Vérifier si la réponse est du JSON valide
#         try:
#             data = response.json()
#             result = data.get("response", "Aucune réponse reçue d'Ollama.")
#         except json.JSONDecodeError:
#             # Si erreur de JSON, on essaie d'extraire les données au format texte
#             logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
#             result = extract_responses(response.text)

#         logging.info(f"Réponse extraite : {result}")
#         logging.info(f"=========================================================")

#         # Utilisation du moteur de synthèse vocale pour lire la réponse d'Ollama
#         logging.info("Lecture de la réponse d'Ollama.")
#         engine.say(result)  # Prépare la réponse pour la synthèse vocale
#         engine.runAndWait()  # Exécute la lecture

#         return result
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     TAILLE_MINIMALE_MESSAGE = 10

#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri, ping_interval=10) as websocket:  # ping toutes les 10 secondes
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 # Boucle pour capturer et traiter chaque bloc audio
#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)

#                     if est_phrase_complete(message_reçu):
#                         reponse_ollama = envoyer_message_ollama(message_reçu)
#                         print(f"Réponse d'Ollama : {reponse_ollama}")
#                     else:
#                         logging.info("Message ignoré : phrase incomplète")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())

# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# import pyttsx3  # Pour la synthèse vocale

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Initialisation du moteur de synthèse vocale avec un accent anglais
# engine = pyttsx3.init()
# for voice in engine.getProperty('voices'):
#     if 'en_GB' in voice.id:  # Accent britannique
#         engine.setProperty('voice', voice.id)
#         break

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# def est_phrase_complete(texte):
#     # Fonction pour vérifier si la phrase est complète
#     doc = nlp(texte)
#     if len(texte) < 10:
#         return False
#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True
#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False
#     sentences = list(doc.sents)
#     return len(sentences) == 1 and sentences[0].text == texte

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     return ''.join(responses).strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {"model": "neural-chat", "prompt": message}
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
        
#         try:
#             data = response.json()
#             result = data.get("response", "Aucune réponse reçue d'Ollama.")
#         except json.JSONDecodeError:
#             logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
#             result = extract_responses(response.text)

#         logging.info(f"Réponse extraite : {result}")
#         logging.info("Lecture de la réponse d'Ollama.")
#         engine.say(result)  # Prépare la réponse pour la synthèse vocale
#         engine.runAndWait()  # Exécute la lecture

#         return result
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri, ping_interval=10) as websocket:  # Ping toutes les 10 sec
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)
#                     if message_reçu != "Aucun message essentiel trouvé":
#                         if est_phrase_complete(message_reçu):
#                             reponse_ollama = envoyer_message_ollama("in very synthetic way, max two sentences, and summrize this : "+ message_reçu)
#                             print(f"Réponse d'Ollama : {reponse_ollama}")
#                         else:
#                             logging.info("Message ignoré : phrase incomplète")
#                     else:
#                         logging.info("Aucun message essentiel trouvé")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())

###################################################""
# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# from gtts import gTTS
# import os

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)
# audio_played = False
# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# def est_phrase_complete(texte):
#     # Fonction pour vérifier si la phrase est complète
#     doc = nlp(texte)
#     if len(texte) < 10:
#         return False
#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True
#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False
#     sentences = list(doc.sents)
#     return len(sentences) == 1 and sentences[0].text == texte

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     return ''.join(responses).strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# # def envoyer_message_ollama(message):
# #     url = "http://localhost:11434/api/generate"
# #     headers = {'Content-Type': 'application/json'}
# #     payload = {"model": "neural-chat", "prompt": message}
# #     logging.info(f"Envoi du message à Ollama : {message}")

# #     try:
# #         response = requests.post(url, headers=headers, json=payload)
# #         response.raise_for_status()
        
# #         try:
# #             data = response.json()
# #             result = data.get("response", "Aucune réponse reçue d'Ollama.")
# #         except json.JSONDecodeError:
# #             logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
# #             result = extract_responses(response.text)

# #         logging.info(f"Réponse extraite : {result}")
# #         logging.info("Lecture de la réponse d'Ollama.")
# #         synthese_vocale(result)  # Lecture de la réponse avec synthèse vocale gTTS

# #         return result
# #     except requests.exceptions.RequestException as e:
# #         logging.error(f"Erreur lors de la requête à Ollama : {e}")
# #         return "Erreur lors de la communication avec Ollama."
# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     # Limites de taille pour le message envoyé à Ollama
#     taille_min_message = 50  # Taille minimale du message (en caractères)
#     taille_max_message = 150  # Taille maximale du message (en caractères)

#     # Vérifier si le message est plus court que la taille minimale
#     if len(message) < taille_min_message:
#         logging.info(f"Le message est trop court ({len(message)} caractères), il sera complété.")
#         message = message.ljust(taille_min_message)  # Compléter le message avec des espaces

#     # Vérifier si le message dépasse la taille maximale
#     if len(message) > taille_max_message:
#         logging.info(f"Le message est trop long ({len(message)} caractères), il sera tronqué.")
#         message = message[:taille_max_message] + "..."  # Tronquer et ajouter une indication de coupure
#     if len(message) < taille_max_message and len(message) > taille_min_message :
#         url = "http://localhost:11434/api/generate"
#         headers = {'Content-Type': 'application/json'}
#         payload = {"model": "neural-chat", "prompt": message}
#         logging.info(f"Envoi du message à Ollama : {message}")

#         try:
#             response = requests.post(url, headers=headers, json=payload)
#             response.raise_for_status()
            
#             try:
#                 data = response.json()
#                 result = data.get("response", "Aucune réponse reçue d'Ollama.")
#             except json.JSONDecodeError:
#                 logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
#                 result = extract_responses(response.text)

#             logging.info(f"Réponse extraite : {result}")
#             logging.info("Lecture de la réponse d'Ollama.")
#             synthese_vocale(result)  # Lecture de la réponse avec synthèse vocale gTTS

#             return result
#         except requests.exceptions.RequestException as e:
#             logging.error(f"Erreur lors de la requête à Ollama : {e}")
#             return "Erreur lors de la communication avec Ollama."
# # Fonction de synthèse vocale utilisant gTTS
# def synthese_vocale(texte):
#     global audio_played
#     tts = gTTS(text=texte, lang='en')
#     tts.save("output.mp3")
#     os.system("start output.mp3")  # Pour Windows; utilisez "afplay output.mp3" sur macOS ou "xdg-open output.mp3" sur Linux
#     audio_played = True  # Indique qu'un fichier audio a été joué
# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri, ping_interval=10) as websocket:  # Ping toutes les 10 sec
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 # while True:
#                 while not audio_played:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)
#                     if message_reçu != "Aucun message essentiel trouvé":
#                         if est_phrase_complete(message_reçu):
#                             reponse_ollama = envoyer_message_ollama("in a very synthetic way," + message_reçu)
#                             print(f"Réponse d'Ollama : {reponse_ollama}")
#                         else:
#                             logging.info("Message ignoré : phrase incomplète")
#                     else:
#                         logging.info("Aucun message essentiel trouvé")
                
#                 await websocket.send('{"eof" : 1}')
#                 print("==================================================================")
#                 # print(await websocket.recv())
#                 commande = await websocket.recv() 

#                 try:
#                     # Affiche la chaîne JSON brute pour inspection
#                     print("Chaîne JSON brute reçue :", commande)

#                     # Convertit la chaîne JSON en dictionnaire
#                     commande = json.loads(commande)
#                     print("Dictionnaire JSON converti :", commande)  # Afficher le dictionnaire pour vérification

#                     # Vérifie la présence de 'text' ou de 'partial'
#                     message_text = commande.get('text') or commande.get('partial')
                    
#                     if message_text:
#                         print("Contenu du message :", message_text)
#                     else:
#                         print("Aucune clé 'text' ou 'partial' trouvée dans l'objet JSON.")

#                 except json.JSONDecodeError:
#                     print("Erreur lors de la conversion de la chaîne JSON.")


#                 print("==================================================================")

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())

###################################################

# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# from gtts import gTTS  # Pour la synthèse vocale
# import io
# import time
# import concurrent.futures

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# def est_phrase_complete(texte):
#     doc = nlp(texte)
#     if len(texte) < 10:
#         return False
#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True
#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False
#     sentences = list(doc.sents)
#     return len(sentences) == 1 and sentences[0].text == texte

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     return ''.join(responses).strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# # def envoyer_message_ollama(message):
# #     url = "http://localhost:11434/api/generate"
# #     headers = {'Content-Type': 'application/json'}
# #     payload = {"model": "neural-chat", "prompt": message}
# #     logging.info(f"Envoi du message à Ollama : {message}")

# #     try:
# #         response = requests.post(url, headers=headers, json=payload)
# #         response.raise_for_status()
        
# #         data = response.json()
# #         result = data.get("response", "Aucune réponse reçue d'Ollama.")

# #         logging.info(f"Réponse extraite : {result}")
# #         logging.info("Lecture de la réponse d'Ollama.")
# #         lire_texte(result)  # Utilisation de gTTS pour la synthèse vocale

# #         return result
# #     except requests.exceptions.RequestException as e:
# #         logging.error(f"Erreur lors de la requête à Ollama : {e}")
# #         return "Erreur lors de la communication avec Ollama."
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {"model": "neural-chat", "prompt": message}
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()

#         # Tente de charger uniquement la partie JSON, sinon capture les erreurs
#         try:
#             data = response.json()
#             result = data.get("response", "Aucune réponse reçue d'Ollama.")
#         except json.JSONDecodeError as e:
#             logging.error(f"Erreur lors de l'analyse JSON, réponse brute : {result}")
#             return "Erreur lors de l'analyse de la réponse d'Ollama."

#         logging.info(f"Réponse extraite : {result}")
#         logging.info("Lecture de la réponse d'Ollama.")
#         lire_texte(result)  # Utilisation de gTTS pour la synthèse vocale

#         return result

#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."
# # Fonction pour lire le texte avec gTTS
# def lire_texte(texte):
#     tts = gTTS(text=texte, lang='en')
#     audio_fp = io.BytesIO()
#     tts.write_to_fp(audio_fp)
#     audio_fp.seek(0)
#     sd.play(audio_fp.read(), samplerate=24000)  # Lecture audio avec sounddevice
#     sd.wait()  # Attend la fin de la lecture

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction pour traiter l'envoi à Ollama en utilisant un thread séparé
# def traitement_message_ollama(message):
#     reponse_ollama = envoyer_message_ollama("in very synthetic way, max two sentences, and summarize this : " + message)
#     print(f"Réponse d'Ollama : {reponse_ollama}")

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri, ping_interval=10) as websocket:
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 with concurrent.futures.ThreadPoolExecutor() as executor:
#                     while True:
#                         data = await audio_queue.get()
#                         await websocket.send(data)

#                         commande = await websocket.recv()
#                         message_reçu = extraire_message_essentiel(commande)
#                         if message_reçu != "Aucun message essentiel trouvé":
#                             if est_phrase_complete(message_reçu):
#                                 # Délai personnalisé et envoi dans un thread pour ne pas bloquer la WebSocket
#                                 executor.submit(traitement_message_ollama, message_reçu)
#                                 await asyncio.sleep(5)  # Attend 5 secondes avant d'écouter un autre message
#                             else:
#                                 logging.info("Message ignoré : phrase incomplète")
#                         else:
#                             logging.info("Aucun message essentiel trouvé")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())



# import json
# import requests
# import logging
# import re
# import argparse
# import asyncio
# import websockets
# import sounddevice as sd
# import spacy
# from gtts import gTTS
# import os
# from concurrent.futures import ThreadPoolExecutor

# # Configuration de logging pour afficher les messages INFO
# logging.basicConfig(level=logging.INFO)

# # Chargement du modèle de langage pré-entraîné
# nlp = spacy.load("en_core_web_sm")

# executor = ThreadPoolExecutor(max_workers=2)  # Crée un pool de threads

# def est_phrase_complete(texte):
#     doc = nlp(texte)
#     if len(texte) < 10:
#         return False
#     if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
#         return True
#     if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
#         return False
#     sentences = list(doc.sents)
#     return len(sentences) == 1 and sentences[0].text == texte

# # Fonction pour extraire un message JSON partiel
# def extraire_message_essentiel(chaine):
#     try:
#         debut_json = chaine.find('{')
#         if debut_json != -1:
#             json_str = chaine[debut_json:]
#             data = json.loads(json_str)
#             return data.get("partial", "Aucun message essentiel trouvé.")
#         else:
#             return "Format incorrect, partie JSON manquante."
#     except json.JSONDecodeError as e:
#         logging.error(f"Erreur lors de l'analyse du JSON : {e}")
#         return "Erreur lors de l'analyse du JSON."

# # Fonction pour extraire les réponses de l'API Ollama
# def extract_responses(log_text):
#     pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
#     responses = re.findall(pattern, log_text)
#     return ''.join(responses).strip()

# # Fonction pour envoyer un message à Ollama et obtenir une réponse JSON
# def envoyer_message_ollama(message):
#     url = "http://localhost:11434/api/generate"
#     headers = {'Content-Type': 'application/json'}
#     payload = {"model": "neural-chat", "prompt": message}
#     logging.info(f"Envoi du message à Ollama : {message}")

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
        
#         try:
#             data = response.json()
#             result = data.get("response", "Aucune réponse reçue d'Ollama.")
#         except json.JSONDecodeError:
#             logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
#             result = extract_responses(response.text)

#         logging.info(f"Réponse extraite : {result}")
        
#         # Lancer la synthèse vocale en arrière-plan
#         executor.submit(synthese_vocale, result)

#         return result
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Erreur lors de la requête à Ollama : {e}")
#         return "Erreur lors de la communication avec Ollama."

# # Fonction de synthèse vocale utilisant gTTS
# def synthese_vocale(texte):
#     tts = gTTS(text=texte, lang='en')
#     tts.save("output.mp3")
#     os.system("start output.mp3")

# # Callback pour capturer les blocs audio
# def callback(indata, frames, time, status):
#     if status:
#         logging.warning(f"Statut audio : {status}")
#     loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

# # Fonction principale pour gérer la communication WebSocket et les tests
# async def run_test():
#     try:
#         with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
#                                channels=1, callback=callback):
#             async with websockets.connect(args.uri, ping_interval=10) as websocket:
#                 await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

#                 while True:
#                     data = await audio_queue.get()
#                     await websocket.send(data)

#                     commande = await websocket.recv()
#                     message_reçu = extraire_message_essentiel(commande)
#                     if message_reçu != "Aucun message essentiel trouvé":
#                         if est_phrase_complete(message_reçu):
#                             executor.submit(envoyer_message_ollama, "in a very synthetic way, max two sentences, and summarize this : " + message_reçu)
#                         else:
#                             logging.info("Message ignoré : phrase incomplète")
#                     else:
#                         logging.info("Aucun message essentiel trouvé")
                
#                 await websocket.send('{"eof" : 1}')
#                 print(await websocket.recv())

#     except Exception as e:
#         logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

# # Fonction pour initialiser le programme et gérer les arguments
# async def main():
#     global args
#     global loop
#     global audio_queue

#     parser = argparse.ArgumentParser(description="ASR Server")
#     parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
#     parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
#     parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
#     args = parser.parse_args()

#     loop = asyncio.get_running_loop()
#     audio_queue = asyncio.Queue()

#     await run_test()

# # Point d'entrée du script
# if __name__ == '__main__':
#     asyncio.run(main())

import json
import requests
import logging
import re
import argparse
import asyncio
import websockets
import sounddevice as sd
import spacy
from gtts import gTTS
import os

# Configuration de logging pour afficher les messages INFO
logging.basicConfig(level=logging.INFO)
audio_played = False

# Chargement du modèle de langage pré-entraîné
nlp = spacy.load("en_core_web_sm")

def est_phrase_complete(texte):
    doc = nlp(texte)
    if len(texte) < 10:
        return False
    if doc[-1].is_punct and doc[-1].text in ['.', '!', '?']:
        return True
    if any(mot in texte for mot in ['euh', 'hmm', 'etc.']):
        return False
    sentences = list(doc.sents)
    return len(sentences) == 1 and sentences[0].text == texte

def extraire_message_essentiel(chaine):
    try:
        debut_json = chaine.find('{')
        if debut_json != -1:
            json_str = chaine[debut_json:]
            data = json.loads(json_str)
            return data.get("partial", "Aucun message essentiel trouvé.")
        else:
            return "Format incorrect, partie JSON manquante."
    except json.JSONDecodeError as e:
        logging.error(f"Erreur lors de l'analyse du JSON : {e}")
        return "Erreur lors de l'analyse du JSON."

def extract_responses(log_text):
    pattern = r'{"model":".+?","created_at":".+?","response":"(.*?)","done":(?:true|false)}'
    responses = re.findall(pattern, log_text)
    return ''.join(responses).strip()

def envoyer_message_ollama(message):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    payload = {"model": "neural-chat", "prompt": message}
    logging.info(f"Envoi du message à Ollama : {message}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        try:
            data = response.json()
            result = data.get("response", "Aucune réponse reçue d'Ollama.")
        except json.JSONDecodeError:
            logging.error("Réponse non JSON d'Ollama, utilisation du texte brut.")
            result = extract_responses(response.text)

        logging.info(f"Réponse extraite : {result}")
        logging.info("Lecture de la réponse d'Ollama.")
        # synthese_vocale(result)

        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête à Ollama : {e}")
        return "Erreur lors de la communication avec Ollama."
import time
def synthese_vocale(texte):
    global audio_played
    tts = gTTS(text=texte, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")
    audio_played = True
    time.sleep(30)


def traitement_message(commande):
    message = extraire_message_essentiel(commande)
    if message != "Aucun message essentiel trouvé.":
        if est_phrase_complete(message):
            taille_min_message = 25
            taille_max_message = 150
            if len(message) < taille_min_message:
                logging.info(f"Le message est trop court ({len(message)} caractères), il sera complété.")
                message = message.ljust(taille_min_message)

            if len(message) > taille_max_message:
                logging.info(f"Le message est trop long ({len(message)} caractères), il sera tronqué.")
                message = message[:taille_max_message] + "..."
            if len(message) < taille_max_message and len(message) > taille_min_message:
                reponse_ollama = envoyer_message_ollama("in a very very synthetic way," + message)
                reponse_ollama = envoyer_message_ollama("summarize this in one sentence:" + reponse_ollama)
                synthese_vocale(reponse_ollama)
                print(f"Réponse d'Ollama : {reponse_ollama}")
        else:
            logging.info("Message ignoré : phrase incomplète")
    else:
        logging.info("Aucun message essentiel trouvé")

def callback(indata, frames, time, status):
    if status:
        logging.warning(f"Statut audio : {status}")
    loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

async def run_test():
    try:
        with sd.RawInputStream(samplerate=args.samplerate, blocksize=4000, device=args.device, dtype='int16',
                               channels=1, callback=callback):
            async with websockets.connect(args.uri, ping_interval=10) as websocket:
                await websocket.send('{ "config" : { "sample_rate" : %d } }' % args.samplerate)

                while True:
                    data = await audio_queue.get()
                    await websocket.send(data)
                    # await asyncio.sleep(1)
                    commande = await websocket.recv()
                    traitement_message(commande)            
                await websocket.send('{"eof" : 1}')
                # print("==================================================================")
                # commande = await websocket.recv() 

                # try:
                #     print("Chaîne JSON brute reçue :", commande)
                #     commande = json.loads(commande)
                #     print("Dictionnaire JSON converti :", commande)
                #     message_text = commande.get('text') or commande.get('partial')
                    
                #     if message_text:
                #         print("Contenu du message :", message_text)
                #         # traitement_message(commande)
                #     else:
                #         print("Aucune clé 'text' ou 'partial' trouvée dans l'objet JSON.")

                # except json.JSONDecodeError:
                #     print("Erreur lors de la conversion de la chaîne JSON.")

                # print("==================================================================")

    except Exception as e:
        logging.error(f"Erreur lors de l'initialisation de la capture audio ou du WebSocket : {e}")

async def main():
    global args
    global loop
    global audio_queue

    parser = argparse.ArgumentParser(description="ASR Server")
    parser.add_argument('-u', '--uri', type=str, metavar='URL', help='Server URL', default='ws://localhost:2700')
    parser.add_argument('-d', '--device', type=int, help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
    args = parser.parse_args()

    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue()

    await run_test()

if __name__ == '__main__':
    asyncio.run(main())
