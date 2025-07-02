#code to find all the streets in iitkgp
# import osmnx as ox
# import folium

# def plot_iitk_roads():
#     # Define the campus location
#     place_name = "IIT Kharagpur, West Bengal, India"

#     # Download walking network graph from OSM
#     print("Downloading walking network graph for IIT Kharagpur...")
#     G = ox.graph_from_place(place_name, network_type='walk')

#     # Convert graph edges to GeoDataFrame for easy access to geometry
#     edges = ox.graph_to_gdfs(G, nodes=False)

#     # Calculate center of campus for map initialization
#     center_lat = edges.geometry.centroid.y.mean()
#     center_lng = edges.geometry.centroid.x.mean()

#     # Create folium map centered on campus
#     m = folium.Map(location=[center_lat, center_lng], zoom_start=16)

#     # Add all road edges as blue polylines on the map
#     print("Adding roads to map...")
#     for _, edge in edges.iterrows():
#         # Only plot if geometry is LineString
#         if edge.geometry.geom_type == 'LineString':
#             # OSMNX geometry coordinates are (lng, lat)
#             coords = [(lat, lng) for lng, lat in edge.geometry.coords]
#             folium.PolyLine(coords, color='blue', weight=3, opacity=0.7).add_to(m)

#     # Save map to HTML file
#     map_filename = 'iitkgp_roads_map.html'
#     m.save(map_filename)
#     print(f"Map saved as {map_filename}. Open this file in a browser to view the campus roads.")

# if __name__ == "__main__":
#     plot_iitk_roads()
import osmnx as ox
import networkx as nx
import folium

# Define campus locations with lat/lng
campus_nodes = {
    "rk": (22.321099945181725, 87.30750998337037),
    "rp": (22.321040395629353, 87.3081644423425),
    "ms": (22.321129719945496, 87.30483313881538),
    "llr": (22.321258743860938, 87.30314334720697),
    "mmm": (22.320896484106633, 87.3010995039457),
    "azd": (22.318926370023316, 87.29856213423984),
    "nhr": (22.319437510609248, 87.29906638952541),
    "snv": (22.316757837935832, 87.30462293853499),
    "cic": (22.317657903328058, 87.31147181952286),
    "ct": (22.317097130204523, 87.30705690349086),
    "ncrc": (22.31841589113766, 87.31717687898102),
    "pth": (22.319601273697973, 87.29989787428511),
    "mb": (22.319682622955742, 87.30976057017541),
    "pfc": (22.319055395969645, 87.30012854427163),
    "gymk": (22.319115060667883, 87.30275612111917),
    "lbs": (22.32086174681767, 87.30010172217364)
}


# Download walking network graph for IIT Kharagpur
place_name = "IIT Kharagpur, West Bengal, India"
G = ox.graph_from_place(place_name, network_type='walk')

# Function to get nearest OSM node for a given lat/lng
def get_nearest_node(lat, lng):
    return ox.distance.nearest_nodes(G, lng, lat)

# Map campus locations to nearest OSM nodes
mapped_nodes = {name: get_nearest_node(lat, lng) for name, (lat, lng) in campus_nodes.items()}

# Example: shortest path from RK to MS
source = mapped_nodes["rk"]
target = mapped_nodes["ms"]

# Calculate shortest path by length (meters)
shortest_path = nx.shortest_path(G, source, target, weight='length')

# Extract lat/lng coordinates of nodes along the shortest path
path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

# Create folium map centered near the campus
center_lat = sum(lat for lat, lng in campus_nodes.values()) / len(campus_nodes)
center_lng = sum(lng for lat, lng in campus_nodes.values()) / len(campus_nodes)
m = folium.Map(location=[center_lat, center_lng], zoom_start=16)

# Add campus nodes as blue markers
for name, (lat, lng) in campus_nodes.items():
    folium.CircleMarker(location=(lat, lng), radius=6, color='blue', fill=True, fill_color='blue', popup=name.upper()).add_to(m)

# Add the shortest path as a red polyline following roads
folium.PolyLine(path_coords, color='red', weight=5, opacity=0.8).add_to(m)

# Save and show map
m.save('shortest_path_map.html')
print("Map saved as shortest_path_map.html")

