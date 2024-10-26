import networkx as nx
import csv

# Création du graphe en fonction des connexions entre stations
def CreationGraphe():
    
    G = nx.Graph() 
    with open('connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            G.add_edge(Station1, Station2, temps=int(temps))
    
    return G
# Parcours en profondeur
def dfs(graph, start, SommetVisite=None):
    if SommetVisite is None:
        SommetVisite = set()
    SommetVisite.add(start)
    for Voisin in graph.neighbors(start):
        if Voisin not in SommetVisite:
            dfs(graph, Voisin, SommetVisite)
    return SommetVisite
    
# Fonction pour vérifier la connexité du réseau
def Connexite(G):
    print("Analyse du réseau de métro parisien:")
    print(f"Nombre de stations: {G.number_of_nodes()}")
    print(f"Nombre de connexions: {G.number_of_edges()}\n")
       
    # Prendre une station de départ (la première station du graphe ici)
    StationDepart = list(G.nodes())[0]
    Liaison = dfs(G, StationDepart)
    
    if len(Liaison) == G.number_of_nodes():
        print("Le réseau est connexe!")
        print(f"Diamètre du réseau: {nx.diameter(G)} stations")
        
    else:
        print("Le réseau n'est pas connexe!")
        print(f"Stations atteignables depuis la station de départ: {len(Liaison)}")
        print(f"Stations non atteignables: {G.number_of_nodes() - len(Liaison)}")

G = CreationGraphe()
Connexite(G)