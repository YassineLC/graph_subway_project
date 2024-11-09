import networkx as nx
import csv
from math import inf
import matplotlib.pyplot as plt
import numpy as np
import spicy as sp
import matplotlib.image as mpimg
import unicodedata

def CreationGraphe():
    G = nx.Graph()
    with open('connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            G.add_edge(Station1, Station2, temps=int(temps))
    return G

def lecture_stations():
    """
    Stocke les informations des stations dans un dictionnaire
    """
    stations = {}
    with open('stations.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            id_station = str(int(row[0]))
            stations[id_station] = {'nom': row[1], 'ligne': row[2], 'terminus': row[3]}
    return stations

def parcours_profondeur(graph, start, SommetVisite=None):
    if SommetVisite is None:
        SommetVisite = set()
    SommetVisite.add(start)
    for Voisin in graph.neighbors(start):
        if Voisin not in SommetVisite:
            parcours_profondeur(graph, Voisin, SommetVisite)
    return SommetVisite

def Connexite(G):
    """
    Utilise un parcours en profondeur pour déterminer si le graphe est connexe
    """
    print("Analyse du réseau de métro parisien:")
    print(f"Nombre de stations: {G.number_of_nodes()}")
    print(f"Nombre de connexions: {G.number_of_edges()}\n")
    
    # Prendre une station de départ (la première station du graphe ici)
    StationDepart = list(G.nodes())[0]
    Liaison = parcours_profondeur(G, StationDepart)
    
    if len(Liaison) == G.number_of_nodes():
        print("Le réseau est connexe!")
        print(f"Diamètre du réseau: {nx.diameter(G)} stations")
    else:
        print("Le réseau n'est pas connexe!")
        print(f"Stations atteignables depuis la station de départ: {len(Liaison)}")
        print(f"Stations non atteignables: {G.number_of_nodes() - len(Liaison)}")

def plus_court_chemin(graph, start, end):
    """
    Utilise l'algorithme de Bellman-Ford pour trouver le plus court chemin entre deux stations
    """
    distances = {node: inf for node in graph.nodes()}
    predecesseurs = {node: None for node in graph.nodes()}
    distances[start] = 0
    
    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if distances[u] + data['temps'] < distances[v]:
                distances[v] = distances[u] + data['temps']
                predecesseurs[v] = u
            if distances[v] + data['temps'] < distances[u]:
                distances[u] = distances[v] + data['temps']
                predecesseurs[u] = v
    print(distances)  
    """On vérifie si end est un numéro de station ou un nom de station"""
    if distances[end] == inf:
        return "Pas de chemin trouvé"
        
    chemin = []
    station = end
    while station is not None:
        chemin.append(station)
        station = predecesseurs[station]
    chemin.reverse()
    
    stations = lecture_stations()
    resultat = []
    parcours = []
    
    ligne_courante = stations[chemin[0]]['ligne']
    resultat.append(f"- Vous êtes à {stations[start]['nom']}.")
    parcours.append(stations[start]['nom'])
    
    for i in range(1, len(chemin)):
        station_courante = chemin[i]
        nouvelle_ligne = stations[station_courante]['ligne']
        
        if nouvelle_ligne != ligne_courante:
            resultat.append(f"- À {stations[chemin[i-1]]['nom']}, prenez la ligne {nouvelle_ligne}.")
            parcours.append(stations[chemin[i-1]]['nom'])
            ligne_courante = nouvelle_ligne
    
    resultat.append(f"- Vous devriez arriver à {stations[end]['nom']} en {formater_temps(distances[end])}.")
    parcours.append(stations[end]['nom'])
    
    return "\n".join(resultat)

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
        if secs == 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ({secondes} secondes)"
        else:
            return f"{minutes} minute{'s' if minutes > 1 else ''} et {secs} seconde{'s' if secs > 1 else ''} ({secondes} secondes)"
    else:
        return f"{secs} seconde{'s' if secs > 1 else ''}"

def trouver_id(nom_station):
    """
    Permet de trouver l'identifiant d'une station à partir de son nom
    """
    stations = lecture_stations()
    ids = []
    for id_station, info in stations.items():
        if info['nom'] == nom_station:
            ids.append(id_station)
    if len(ids) == 1:
        return ids[0]
    elif len(ids) > 1:
        print(f"Plusieurs lignes de metro sont disponibles à {nom_station}:")
        for id_station in ids:
            print(f"- {stations[id_station]['nom']} (ligne {stations[id_station]['ligne']})")
        ligne = input("Veuillez préciser la ligne (uniquement le numéro) : ")
        for id_station in ids:
            if stations[id_station]['ligne'] == ligne:
                return id_station
    return None

def arbre_couvrant_prim_poids_min(graph):
    """
    Utilise l'algo de Prim et affiche graphiquement l'arbre couvrant de poids minimal
    """
    nodes = list(graph.nodes())
    mst_set = set()
    mst_edges = []
    edge_weights = {node: inf for node in nodes}
    edge_weights[nodes[0]] = 0
    parent = {node: None for node in nodes}

    while len(mst_set) < len(nodes):
        current_node = min((node for node in nodes if node not in mst_set), key=lambda node: edge_weights[node])
        mst_set.add(current_node)

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['temps']
            if neighbor not in mst_set and weight < edge_weights[neighbor]:
                edge_weights[neighbor] = weight
                parent[neighbor] = current_node

    for node in nodes:
        if parent[node] is not None:
            mst_edges.append((parent[node], node))

    arbre = nx.Graph()
    arbre.add_edges_from(mst_edges)
    pos = nx.kamada_kawai_layout(arbre)
    plt.figure(figsize=(12, 8))
    nx.draw(arbre, pos, with_labels=True, font_weight='bold', node_size=50, node_color='skyblue', font_size=8)
    plt.title("Arbre couvrant de poids minimal")
    plt.show()
    return arbre

def correct_encoding(name):
    corrections = {
        "Ã‰": "É",
        "Ã©": "é",
        "Ã¨": "è",
        "Ã§": "ç",
        "A‰": "É", 
        "A©": "é",  
        "Ã¢": "â"
    }
    for wrong, correct in corrections.items():
        name = name.replace(wrong, correct)
    return name


def interface_metro_parisien():
    # Chargement de l'image de la carte du métro parisien
    img = mpimg.imread('metrof_r.png')
    G = CreationGraphe()
    station_positions = {}
    with open('pospoints.csv', 'r') as f:
        for line in f:
            x, y, station_id = line.strip().split(';')
            station_positions[station_id] = (int(x), int(y))
    
    # Initialisation de la figure
    fig, ax = plt.subplots()
    ax.imshow(img)
    
    # Affichage des stations sur la carte
    for station_id, (x, y) in station_positions.items():
        ax.plot(x, y, 'o', color='red', markersize=5)
    
    # Variables pour stocker les stations de départ et d'arrivée
    start_station = None
    end_station = None
    
    def on_click(event):
        nonlocal start_station, end_station
        
        # Obtenir la station la plus proche du clic
        clicked_pos = (event.xdata, event.ydata)
        nearest_station = min(station_positions.keys(),
                              key=lambda s: np.linalg.norm(np.array(station_positions[s]) - np.array(clicked_pos)))
            # Affichage pour débogage
        print(f"Nom de station avant normalisation : '{nearest_station}'")
        
        # Normalisation
        nearest_station = correct_encoding(nearest_station)
        
        # Affichage après normalisation
        print(f"Nom de station après normalisation : '{nearest_station}'")

        if start_station is None:
            start_station = nearest_station
            print(f"Station de départ sélectionnée : {start_station}")
        elif end_station is None:
            end_station = nearest_station
            print(f"Station d'arrivée sélectionnée : {end_station}")
            
            # Calcul et affichage du plus court chemin
            path_info = plus_court_chemin(G, trouver_id(start_station), trouver_id(end_station))
            print(path_info)
            
            # Extraction des stations dans le chemin
            chemin = path_info.split('\n')
            chemin_ids = [start_station] + [line.split()[-1] for line in chemin if "prenez" in line] + [end_station]
            
            # Tracer le chemin sur la carte
            for i in range(len(chemin_ids) - 1):
                x1, y1 = station_positions[chemin_ids[i]]
                x2, y2 = station_positions[chemin_ids[i+1]]
                ax.plot([x1, x2], [y1, y2], color='blue', linewidth=2)
            
            plt.draw()
            
        # Réinitialisation pour une nouvelle sélection
        else:
            start_station, end_station = None, None
    
    def afficher_acpm(event):
        # Calculer et afficher l'ACPM (Arbre couvrant de poids minimal)
        arbre = arbre_couvrant_prim_poids_min(G)
        
        # Affichage de l'ACPM sur la carte
        for u, v in arbre.edges():
            x1, y1 = station_positions[u]
            x2, y2 = station_positions[v]
            ax.plot([x1, x2], [y1, y2], color='green', linewidth=1, linestyle='--')
        
        plt.draw()
    
    # Connexion des événements pour les clics
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Ajout d'un bouton pour afficher l'ACPM (utilise la touche 'a')
    fig.canvas.mpl_connect('key_press_event', lambda event: afficher_acpm(event) if event.key == 'a' else None)
    
    plt.show()

# Exécution de l'interface
interface_metro_parisien()

G = CreationGraphe()
# depart = trouver_id('Strasbourg Saint-Denis')
# arrivee = trouver_id('Villejuif, P. Vaillant Couturier')
# print(plus_court_chemin(G, depart, arrivee))
# print("\n")
Connexite(G)
arbre = arbre_couvrant_prim_poids_min(G)
# print(f"Nombre de stations dans l'arbre couvrant minimal: {arbre.number_of_nodes()}")
