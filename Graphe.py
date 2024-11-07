import networkx as nx
import csv
from math import inf
import matplotlib.pyplot as plt
import numpy as np
import spicy as sp

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
    arbre = nx.minimum_spanning_tree(graph)
    pos = nx.kamada_kawai_layout(arbre)
    plt.figure(figsize=(12, 8))
    nx.draw(arbre, pos, with_labels=True, font_weight='bold', node_size=50, node_color='skyblue', font_size=8)
    plt.title("Arbre couvrant de poids minimal")
    plt.show()
    return arbre

G = CreationGraphe()
depart = trouver_id('Strasbourg Saint-Denis')
arrivee = trouver_id('Villejuif, P. Vaillant Couturier')
print(plus_court_chemin(G, depart, arrivee))
print("\n")
Connexite(G)
arbre = arbre_couvrant_prim_poids_min(G)
print(f"Nombre de stations dans l'arbre couvrant minimal: {arbre.number_of_nodes()}")