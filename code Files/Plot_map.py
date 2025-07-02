import folium
from Cordinates import node_coordinates

# Initialize map centered roughly at campus center
center_lat = 22.3195
center_lng = 87.3050
campus_map = folium.Map(location=[center_lat, center_lng], zoom_start=16)

# Add nodes as markers
for node, (lat, lng) in node_coordinates.items():
    folium.CircleMarker(
        location=(lat, lng),
        radius=6,
        popup=node.upper(),
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(campus_map)
#Edges Data
edges_data = [
    ("rk", "rp", 60),
    ("rk", "ms", 300),
    ("ms", "llr", 270),
    ("llr", "mmm", 100),
    ("mmm", "lbs", 260),
    ("lbs", "pth", 500),
    ("pth", "nhr", 140),
    ("nhr", "azd", 30),
    ("azd", "snv", 900),
    ("ncrc", "cic", 950),
    ("cic", "ct", 600),
    ("gymk", "snv", 500),
    ("ms", "mb", 360),
    ("rk", "mb", 320),
    ("rp", "mb", 270),
    ("nhr", "pfc", 200),
    ("azd", "pfc", 150),
    ("pth", "pfc", 90),
    ("ms", "gymk", 500),
    ("llr", "gymk", 400),
    ("mmm", "gymk", 450),
    ("lbs", "pfc", 200),
    ("gymk", "mb", 700),
    ("mb", "ct", 500),
    ("snv", "ct", 200)
]


# Add edges as lines
for u, v, dist in edges_data:
    if u in node_coordinates and v in node_coordinates:
        points = [node_coordinates[u], node_coordinates[v]]
        folium.PolyLine(points, color='green', weight=3, opacity=0.7).add_to(campus_map)

# Save map to HTML file
campus_map.save('campus_map.html')
print("Map saved as campus_map.html")
