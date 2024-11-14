import networkx as nx
from math import inf
import csv
import matplotlib.pyplot as plt

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
    
    return chemin, distances[end]

def arbre_couvrant_prim_poids_min(graph):
    # Initialisation
    if not graph:
        raise ValueError("Le graphe ne doit pas être vide.")
        
    arbre = {}
    sommets = set(graph)
    sommet = list(sommets)[0]
    sommets.remove(sommet)
    arbre[sommet] = None  # Racine de l'arbre couvrant
    
    while sommets:
        aretes = []
        for s in arbre:
            aretes.extend(
                [(s, v, data['temps']) for v, data in graph[s].items() if v in sommets]
            )
        
        # Trouver l'arête de poids minimal connectant un sommet de l'arbre à un sommet hors de l'arbre
        u, v, poids = min(aretes, key=lambda x: x[2])
        arbre[v] = u
        sommets.remove(v)
        
    return arbre


def CreationGraphe():
    G = nx.Graph()
    with open('utils/connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            G.add_edge(Station1, Station2, temps=int(temps))
    return G

def afficher_graphique(arbre):
    # On utilise kamala kawai pour un affichage plus lisible
    pos = nx.kamada_kawai_layout(G)
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='skyblue', edge_color='grey', alpha=0.5)
    for v, u in arbre.items():
        if u is not None:
            #Affiche en rouge les arêtes de l'arbre couvrant en rouge, sinon en gris.
            plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'r', alpha=0.5, linewidth=3)
    plt.show()

# On va tester les fonctions
# G = CreationGraphe()
# Connexite(G)
# F = arbre_couvrant_prim_poids_min(G)
# print(f"Arbre couvrant de poids minimal: {F} arêtes") 
# afficher_graphique(F)

test_graph = {
    'A': {'B': {'temps': 2}, 'C': {'temps': 3}},
    'B': {'A': {'temps': 2}, 'C': {'temps': 1}, 'D': {'temps': 4}},
    'C': {'A': {'temps': 3}, 'B': {'temps': 1}, 'D': {'temps': 5}},
    'D': {'B': {'temps': 4}, 'C': {'temps': 5}}
}
arbre = arbre_couvrant_prim_poids_min(test_graph)
print("Arbre couvrant généré :", arbre)
