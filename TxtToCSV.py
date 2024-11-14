import csv

def create_station_csv(data):
    """Create stations.csv with format: id;nom;ligne;terminus;zone"""
    stations = []
    
    # Parse stations (lines starting with V)
    for line in data.split('\n'):
        if line.startswith('V'):
            # Split line and remove the 'V' prefix
            parts = line.split(' ', 1)  # Split on first space to separate V prefix
            if len(parts) < 2:
                continue
                
            # Split remaining parts on semicolon
            station_info = parts[1].strip().split(';')
            if len(station_info) >= 3:
                # Extract ID from the station name
                station_name_parts = station_info[0].strip().split(' ')
                station_id = station_name_parts[0]  # Get the ID
                station_name = ' '.join(station_name_parts[1:])  # Get the rest as name
                
                ligne = station_info[1].strip()
                terminus = station_info[2].strip()
                zone = station_info[3].strip() if len(station_info) > 3 else "0"
                
                stations.append([station_id, station_name, ligne, terminus, zone])
    
    # Write to CSV
    with open('utils/stations.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['id', 'nom', 'ligne', 'terminus', 'zone'])
        writer.writerows(stations)

def create_edges_csv(data):
    """Create connections.csv with format: station1;station2;temps"""
    edges = []
    
    # Parse edges (lines starting with E)
    for line in data.split('\n'):
        if line.startswith('E'):
            # Split line and remove the 'E' prefix
            parts = line.split(' ')
            if len(parts) >= 4:
                station1 = parts[1]
                station2 = parts[2]
                temps = parts[3]
                edges.append([station1, station2, temps])
    
    # Write to CSV
    with open('utils/connections.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['station1', 'station2', 'temps'])
        writer.writerows(edges)

# Example usage:
with open('metroo.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    create_station_csv(data)
    create_edges_csv(data)