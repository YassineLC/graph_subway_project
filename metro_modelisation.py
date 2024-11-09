import networkx as nx
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches
from graph_algorithms import plus_court_chemin, arbre_couvrant_prim_poids_min

def CreationGraphe():
    G = nx.Graph()
    with open('utils/connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            G.add_edge(Station1, Station2, temps=int(temps))
    return G

def lecture_stations():
    stations = {}
    with open('utils/stations.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            id_station = str(int(row[0]))
            stations[id_station] = {'nom': row[1], 'ligne': row[2], 'terminus': row[3]}
    return stations

def formater_temps(secondes):
    heures = secondes // 3600
    minutes = (secondes % 3600) // 60
    secs = secondes % 60
    if heures > 0:
        if minutes == 0 and secs == 0:
            return f"{heures} heure{'s' if heures > 1 else ''} ({secondes} secondes)"
        elif secs == 0:
            return f"{heures} heure{'s' if heures > 1 else ''} et {minutes} minute{'s' if minutes > 1 else ''} ({secondes} secondes)"
        else:
            return f"{heures} heure{'s' if heures > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''} et {secs} seconde{'s' if secs > 1 else ''} ({secondes} secondes)"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} et {secs} seconde{'s' if secs > 1 else ''} ({secondes} secondes)"
    return f"{secs} seconde{'s' if secs > 1 else ''}"

def trouver_id(nom_station, ligne=None):
    stations = lecture_stations()
    for id_station, info in stations.items():
        if info['nom'] == nom_station and (ligne is None or info['ligne'] == ligne):
            return id_station
    return None

def correct_encoding(name):
    corrections = {"Ã‰": "É", "Ã©": "é", "Ã¨": "è", "Ã§": "ç", "A‰": "É", "A©": "é", "Ã¢": "â"}
    for wrong, correct in corrections.items():
        name = name.replace(wrong, correct)
    return name

def get_station_choice(station_name, pos_x, pos_y):
    ids = []
    lines = []
    for id_station, info in stations_dict.items():
        if info['nom'] == station_name:
            ids.append(id_station)
            lines.append(info['ligne'])

    if len(ids) == 1:
        return ids[0], lines[0]

    selected_id, selected_line = None, None

    choice_fig, ax_choice = plt.subplots(figsize=(4, len(ids) * 0.8))
    choice_fig.canvas.manager.set_window_title(f'Choix de ligne pour {station_name}')
    
    # Configurer les limites de l'axe
    ax_choice.set_xlim(0, 1)
    ax_choice.set_ylim(0, 1)
    ax_choice.axis('off')

    def on_click_choice(event):
        nonlocal selected_id, selected_line
        if event.inaxes != ax_choice:  # Vérifier si le clic est dans l'axe
            return
            
        # Convertir les coordonnées du clic en coordonnées de l'axe
        for i, (station_id, line) in enumerate(zip(ids, lines)):
            y_pos = 0.8 - i * 0.2
            # Vérifier si le clic est dans le rectangle du bouton
            if (0.2 <= event.xdata <= 0.8 and 
                y_pos <= event.ydata <= y_pos + 0.15):
                selected_id = station_id
                selected_line = line
                # Fermer la fenêtre après avoir sélectionné
                plt.close(choice_fig)
                break

    # Créer les boutons avec des rectangles
    button_patches = []
    for i, line in enumerate(lines):
        y_pos = 0.8 - i * 0.2
        button = patches.Rectangle((0.2, y_pos), 0.6, 0.15, 
                                 facecolor='lightgray',
                                 edgecolor='gray')
        ax_choice.add_patch(button)
        ax_choice.text(0.5, y_pos + 0.075, f'Ligne {line}', 
                      ha='center', va='center', 
                      fontsize=10)
        button_patches.append(button)

    choice_fig.canvas.mpl_connect('button_press_event', on_click_choice)
    plt.show()

    # Attendre que la fenêtre de choix soit fermée avant de retourner le choix
    return selected_id, selected_line


def interface_metro_parisien():
    img = mpimg.imread('utils/metrof_r.png')
    G = CreationGraphe()
    station_positions = {}
    with open('utils/pospoints.csv', 'r') as f:
        for line in f:
            x, y, station_id = line.strip().split(';')
            station_positions[station_id] = (int(x), int(y))
    
    fig, (ax_map, ax_text) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]}, figsize=(15, 18))
    ax_map.imshow(img)
    ax_text.axis('off')
    text_output = ax_text.text(0.05, 0.95, "Cliquez sur une station de départ...", verticalalignment='top', wrap=True, fontsize=10)
    
    for station_id, (x, y) in station_positions.items():
        ax_map.plot(x, y, 'o', color='red', markersize=5)

    start_station, start_line = None, None
    end_station, end_line = None, None
    stations_dict = lecture_stations()

    def update_text_output(message):
        text_output.set_text(message)
        plt.draw()

    def on_click(event):
        nonlocal start_station, start_line, end_station, end_line

        if event.inaxes != ax_map:
            return

        clicked_pos = (event.xdata, event.ydata)
        nearest_station = min(station_positions.keys(), key=lambda s: np.linalg.norm(np.array(station_positions[s]) - np.array(clicked_pos)))
        nearest_station_name = correct_encoding(nearest_station)

        if start_station is None:
            station_id, ligne = get_station_choice(nearest_station_name, event.x, event.y)
            if station_id:
                start_station = nearest_station_name
                start_line = ligne
                update_text_output(f"Station de départ sélectionnée : {start_station} (ligne {start_line})\nCliquez sur une station d'arrivée...")
        elif end_station is None:
            station_id, ligne = get_station_choice(nearest_station_name, event.x, event.y)
            if station_id:
                end_station = nearest_station_name
                end_line = ligne
                update_text_output(f"Calcul de l'itinéraire entre {start_station} et {end_station}...")

                start_id = trouver_id(start_station, start_line)
                end_id = trouver_id(end_station, end_line)
                chemin, temps = plus_court_chemin(G, start_id, end_id)

                resultat = ["Itinéraire :"]
                ligne_courante = stations_dict[chemin[0]]['ligne']
                resultat.append(f"- Départ : {stations_dict[chemin[0]]['nom']} (ligne {ligne_courante})")

                for i in range(1, len(chemin)):
                    station = chemin[i]
                    nouvelle_ligne = stations_dict[station]['ligne']
                    if nouvelle_ligne != ligne_courante:
                        resultat.append(f"- Changement à {stations_dict[chemin[i-1]]['nom']}")
                        resultat.append(f"  Prendre la ligne {nouvelle_ligne}")
                        ligne_courante = nouvelle_ligne

                resultat.append(f"- Arrivée : {stations_dict[chemin[-1]]['nom']}")
                resultat.append(f"\nTemps de trajet estimé : {formater_temps(temps)}")
                resultat.append("\nRecliquez n'importe où pour chercher un nouvel itinéraire")

                update_text_output('\n'.join(resultat))

                for i in range(len(chemin) - 1):
                    x1, y1 = station_positions[chemin[i]]
                    x2, y2 = station_positions[chemin[i + 1]]
                    ax_map.plot([x1, x2], [y1, y2], color='blue', linewidth=2)

                plt.draw()
        else:
            start_station = None
            start_line = None
            end_station = None
            end_line = None
            for line in ax_map.lines[:]:
                if line.get_color() == 'blue':
                    line.remove()
            update_text_output("Cliquez sur une station de départ...")
            plt.draw()

    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

stations_dict = lecture_stations()
interface_metro_parisien()
