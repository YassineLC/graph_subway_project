import csv
from math import inf
import heapq

# Création du graphe à partir des fichiers CSV
def creerGraphe():
    graph = {}
    with open('utils/connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            Station1, Station2, temps = int(Station1), int(Station2), int(temps)
            if Station1 not in graph:
                graph[Station1] = []
            if Station2 not in graph:
                graph[Station2] = []
            graph[Station1].append((Station2, temps))
            graph[Station2].append((Station1, temps))
    return graph

# Chargement des noms de stations et correspondance avec leurs IDs
def charger_stations():
    stations = {}
    with open('utils/stations.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Sauter l'en-tête
        for row in reader:
            id_station, nom, _, _, _ = row
            stations[int(id_station)] = nom
    return stations

# Algorithme de Prim pour trouver l'arbre couvrant minimum et retourner son poids total
def arbre_couvrant_prim(graph, stations):
    sommetDepart = next(iter(graph))
    visite = set([sommetDepart])
    edges = [(cost, sommetDepart, to) for to, cost in graph[sommetDepart]]
    heapq.heapify(edges)
    poids = 0  # Poids total de l'arbre couvrant minimum
    mst_edges = []  # Pour stocker les liaisons dans l'arbre couvrant minimum
    
    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visite:
            visite.add(to)
            poids += cost
            mst_edges.append((frm, to, cost))  # Ajouter la liaison trouvée
            for to_next, cost in graph[to]:
                if to_next not in visite:
                    heapq.heappush(edges, (cost, to, to_next))
    
    # Affichage des liaisons de l'arbre couvrant minimum avec noms des stations
    print("Liaisons de l'arbre couvrant minimum (ACPM) :")
    for frm, to, cost in mst_edges:
        print(f"Liaison {stations[frm]} -> {stations[to]} avec poids {cost}")
    
    return poids

# Vérification de la connexité avec DFS
def dfs(graph, debut, visite=None):
    if visite is None:
        visite = set()
    visite.add(debut)
    for voisins, _ in graph.get(debut, []):
        if voisins not in visite:
            dfs(graph, voisins, visite)
    return visite

def est_connexe(graph):
    stationDepart = next(iter(graph))
    stationsVisite = dfs(graph, stationDepart)
    return len(stationsVisite) == len(graph)

# Algorithme de Bellman-Ford utilisant les noms des stations
def belmann(graph, stations, debut_name, fin_name):
    # Conversion des noms en IDs
    debut = next((id for id, name in stations.items() if name == debut_name), None)
    fin = next((id for id, name in stations.items() if name == fin_name), None)
    
    if debut is None or fin is None:
        print(f"Station(s) non trouvée(s): {debut_name} ou {fin_name}")
        return None, inf
    
    distances = {node: inf for node in graph}
    predecesseurs = {node: None for node in graph}
    distances[debut] = 0
    
    for _ in range(len(graph) - 1):
        for node in graph:
            for voisins, weight in graph[node]:
                if distances[node] + weight < distances[voisins]:
                    distances[voisins] = distances[node] + weight
                    predecesseurs[voisins] = node
                    
    # Construction du chemin sans redondances
    path = []
    current = fin
    while current is not None:
        if current not in path:  # Éviter toutes les redondances
            path.insert(0, current)
        current = predecesseurs[current]
    
    if distances[fin] == inf:
        return None, inf
    
    path_names = [stations[node] for node in path]
    return path_names, distances[fin]

graphe = creerGraphe()
stations = charger_stations()

# Vérification de la connexité
if est_connexe(graphe):
    print("Le réseau est connexe !")
else:
    print("Le réseau n'est pas connexe.")

# Calcul du poids total minimum de l'arbre couvrant
mst_weight = arbre_couvrant_prim(graphe, stations)
print(f"Poids total de l'arbre couvrant minimum: {mst_weight}")

stationDepart_name = "Carrefour Pleyel"
fin_station_name = "Villejuif, Louis Aragon"
chemin, distance = belmann(graphe, stations, stationDepart_name, fin_station_name)
if chemin:
    print(f"Plus court chemin entre {stationDepart_name} et {fin_station_name}: {chemin} avec distance: {distance}")
else:
    print(f"Pas de chemin trouvé entre {stationDepart_name} et {fin_station_name}.")
