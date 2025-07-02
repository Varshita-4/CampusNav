import sys
import os
import osmnx as ox
import networkx as nx
import folium
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton,
    QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import webbrowser

campus_nodes = {
    "RK": (22.321099945181725, 87.30750998337037),
    "RP": (22.321040395629353, 87.3081644423425),
    "MS": (22.321129719945496, 87.30483313881538),
    "LLR": (22.321258743860938, 87.30314334720697),
    "MMM": (22.320896484106633, 87.3010995039457),
    "AZAD": (22.318926370023316, 87.29856213423984),
    "NEHRU": (22.319437510609248, 87.29906638952541),
    "SNV": (22.316757837935832, 87.30462293853499),
    "CIC": (22.317657903328058, 87.31147181952286),
    "CT": (22.317097130204523, 87.30705690349086),
    "NCRC": (22.31841589113766, 87.31717687898102),
    "PTH": (22.319601273697973, 87.29989787428511),
    "MB": (22.319682622955742, 87.30976057017541),
    "PFC": (22.319055395969645, 87.30012854427163),
    "GYMK": (22.319115060667883, 87.30275612111917),
    "LBS": (22.32086174681767, 87.30010172217364)
}

print("Downloading walking network graph for IIT Kharagpur...")
G = ox.graph_from_place("IIT Kharagpur, West Bengal, India", network_type='walk')

def get_nearest_node(lat, lng):
    return ox.distance.nearest_nodes(G, lng, lat)

mapped_nodes = {name: get_nearest_node(lat, lng) for name, (lat, lng) in campus_nodes.items()}

class CampusNavGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CampusNav - Shortest Path Finder")
        self.setGeometry(100, 100, 600, 350)
        self.init_ui()

    def init_ui(self):
        roboto = QFont("Roboto", 12)
        self.setFont(roboto)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f4f7"))  # light blue/gray
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        heading = QLabel("CampusNav")
        heading.setFont(QFont("Roboto", 30, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("color: #34495E;")  # dark blue-gray
        main_layout.addWidget(heading)

        src_label = QLabel("1. Where are you?")
        src_label.setFont(QFont("Roboto", 16))
        src_label.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(src_label)

        self.src_combo = QComboBox()
        self.src_combo.addItems(sorted(campus_nodes.keys()))
        self.src_combo.setFont(QFont("Roboto", 14))
        self.src_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #3498DB;
                border-radius: 8px;
                background-color: white;
                color: #2C3E50;
            }
            QComboBox:hover {
                border-color: #2980B9;
            }
            QComboBox:drop-down {
                border: none;
            }
        """)
        main_layout.addWidget(self.src_combo)

        dest_label = QLabel("2. Where do you want to go?")
        dest_label.setFont(QFont("Roboto", 16))
        dest_label.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(dest_label)

        self.dest_combo = QComboBox()
        self.dest_combo.addItems(sorted(campus_nodes.keys()))
        self.dest_combo.setFont(QFont("Roboto", 14))
        self.dest_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #3498DB;
                border-radius: 8px;
                background-color: white;
                color: #2C3E50;
            }
            QComboBox:hover {
                border-color: #2980B9;
            }
            QComboBox:drop-down {
                border: none;
            }
        """)
        main_layout.addWidget(self.dest_combo)

        self.btn_calc = QPushButton("Find Shortest Path")
        self.btn_calc.setFont(QFont("Roboto", 16, QFont.Bold))
        self.btn_calc.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.btn_calc.clicked.connect(self.find_path)
        main_layout.addWidget(self.btn_calc)

        self.lbl_distance = QLabel("")
        self.lbl_distance.setFont(QFont("Roboto", 16))
        self.lbl_distance.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_distance)

        self.setLayout(main_layout)

    def find_path(self):
        src = self.src_combo.currentText()
        dest = self.dest_combo.currentText()

        if src == dest:
            self.lbl_distance.setStyleSheet("color: #E74C3C;")  # red
            self.lbl_distance.setText("Source and destination cannot be the same.")
            return

        source_node = mapped_nodes[src]
        target_node = mapped_nodes[dest]

        try:
            path = nx.shortest_path(G, source_node, target_node, weight='length')
            length = nx.shortest_path_length(G, source_node, target_node, weight='length')
        except nx.NetworkXNoPath:
            self.lbl_distance.setStyleSheet("color: #E74C3C;")  # red
            self.lbl_distance.setText(f"No path found between {src} and {dest}.")
            return

        path_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]

        avg_lat = sum(lat for lat, lng in campus_nodes.values()) / len(campus_nodes)
        avg_lng = sum(lng for lat, lng in campus_nodes.values()) / len(campus_nodes)
        m = folium.Map(location=[avg_lat, avg_lng], zoom_start=16)

        for name, (lat, lng) in campus_nodes.items():
            folium.CircleMarker(location=(lat, lng), radius=5, color='blue', fill=True, fill_color='blue', popup=name).add_to(m)

        folium.PolyLine(path_coords, color='blue', weight=6, opacity=0.8).add_to(m)

        # Source and destination pins
        folium.Marker(location=campus_nodes[src],
                      popup=f"Source: {src}",
                      icon=folium.Icon(color='green', icon='play')).add_to(m)

        folium.Marker(location=campus_nodes[dest],
                      popup=f"Destination: {dest}",
                      icon=folium.Icon(color='red', icon='flag')).add_to(m)

        map_path = "campus_shortest_path.html"
        m.save(map_path)

        self.lbl_distance.setStyleSheet("color: #27AE60;")  # green
        self.lbl_distance.setText(f"Shortest Distance: {length:.2f} meters")

        webbrowser.open('file://' + os.path.realpath(map_path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CampusNavGUI()
    window.show()
    sys.exit(app.exec_())
