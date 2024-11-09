import networkx as nx
from math import inf
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