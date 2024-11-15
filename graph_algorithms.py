import csv
import heapq
from math import inf

# Création du graphe
def creerGraphe():
    graph = {}
    with open('utils/connections.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            Station1, Station2, temps = row
            temps = int(temps)
            if Station1 not in graph:
                graph[Station1] = []
            if Station2 not in graph:
                graph[Station2] = []
            graph[Station1].append((Station2, temps))
            graph[Station2].append((Station1, temps))
    return graph

# Lecture des stations
def lecture_stations():
    stations = {}
    with open('utils/stations.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            id_station = str(int(row[0]))
            stations[id_station] = {'nom': row[1], 'ligne': row[2]}
    return stations

# Vérification de la connexité
def dfs(graph, debut, visite=None):
    if visite is None:
        visite = set()
    visite.add(debut)
    for voisin, _ in graph.get(debut, []):
        if voisin not in visite:
            dfs(graph, voisin, visite)
    return visite

def est_connexe(graph):
    station_depart = next(iter(graph))
    stations_visitees = dfs(graph, station_depart)
    return len(stations_visitees) == len(graph)

# Algorithme de Prim pour trouver l'arbre couvrant minimum
def arbre_couvrant_prim(graph, stations):
    sommet_depart = next(iter(graph))
    visite = set([sommet_depart])
    edges = [(cost, sommet_depart, to) for to, cost in graph[sommet_depart]]
    heapq.heapify(edges)
    poids = 0
    mst_edges = []

    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visite:
            visite.add(to)
            poids += cost
            mst_edges.append((frm, to, cost))
            for to_next, cost in graph[to]:
                if to_next not in visite:
                    heapq.heappush(edges, (cost, to, to_next))

    print("Liaisons de l'arbre couvrant minimum :")
    for frm, to, cost in mst_edges:
        print(f"- {stations[frm]['nom']} -> {stations[to]['nom']} avec coût {cost}")

    return poids

# Algorithme de Bellman-Ford
def belmann(graph, stations, debut_id, fin_id):
    distances = {node: inf for node in graph}
    predecesseurs = {node: None for node in graph}
    distances[debut_id] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for voisin, poids in graph[node]:
                if distances[node] + poids < distances[voisin]:
                    distances[voisin] = distances[node] + poids
                    predecesseurs[voisin] = node

    if distances[fin_id] == inf:
        return None, inf

    chemin = []
    current = fin_id
    while current is not None:
        chemin.insert(0, current)
        current = predecesseurs[current]

    return chemin, distances[fin_id]

# Formater le temps en une représentation lisible
def formater_temps(secondes):
    minutes = (secondes % 3600) // 60
    return f"{minutes}min"

# Affichage de l'itinéraire Bellman-Ford
def afficher_itineraire(chemin, stations, temps):
    if chemin is None:
        print("Aucun chemin trouvé.")
        return

    resultat = ["Itinéraire :"]
    ligne_courante = stations[chemin[0]]['ligne']
    resultat.append(f"- Départ : {stations[chemin[0]]['nom']} (Ligne {ligne_courante})")

    for i in range(1, len(chemin)):
        station = chemin[i]
        nouvelle_ligne = stations[station]['ligne']
        if nouvelle_ligne != ligne_courante:
            resultat.append(f"- Changement à {stations[chemin[i - 1]]['nom']}")
            resultat.append(f"  Prendre la ligne {nouvelle_ligne}")
            ligne_courante = nouvelle_ligne

    resultat.append(f"- Arrivée : {stations[chemin[-1]]['nom']} (Ligne {ligne_courante})")
    resultat.append(f"Temps de trajet : {formater_temps(temps)}")

    print("\n".join(resultat))

# Menu principal
def menu():
    graphe = creerGraphe()
    stations = lecture_stations()

    while True:
        print("\nMenu principal :")
        print("1. Vérifier la connexité")
        print("2. Calculer l'arbre couvrant minimum (Prim)")
        print("3. Trouver le plus court chemin (Bellman-Ford)")
        print("4. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            if est_connexe(graphe):
                print("Le réseau est connexe.")
            else:
                print("Le réseau n'est pas connexe.")
        elif choix == "2":
            poids = arbre_couvrant_prim(graphe, stations)
            print(f"Poids total de l'arbre couvrant minimum : {poids}")
        elif choix == "3":
            station_depart = input("Entrez le nom de la station de départ : ")
            station_arrivee = input("Entrez le nom de la station d'arrivée : ")

            debut_id = next((id for id, data in stations.items() if data['nom'] == station_depart), None)
            fin_id = next((id for id, data in stations.items() if data['nom'] == station_arrivee), None)

            if debut_id and fin_id:
                chemin, temps = belmann(graphe, stations, debut_id, fin_id)
                afficher_itineraire(chemin, stations, temps)
            else:
                print("Station introuvable. Veuillez vérifier les noms.")
        elif choix == "4":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

# Lancer le programme
if __name__ == "__main__":
    menu()
