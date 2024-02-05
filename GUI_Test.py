import tkinter as tk
from tkinter import ttk
from geopy.distance import geodesic
from gmplot import gmplot


class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Map Distance Calculator")

        # Variables for user input
        self.primary_icon_location = None
        self.secondary_icon_locations = []

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Google Map initialization
        self.gmap_frame = tk.Frame(self.root)
        self.gmap_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input area
        self.primary_icon_label = tk.Label(self.root, text="Primary Icon Location:")
        self.primary_icon_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.primary_icon_entry = tk.Entry(self.root, width=30)
        self.primary_icon_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.secondary_icon_label = tk.Label(self.root, text="Secondary Icon Locations (comma-separated):")
        self.secondary_icon_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.secondary_icon_entry = tk.Entry(self.root, width=30)
        self.secondary_icon_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Calculate Distance button
        self.calculate_distance_button = tk.Button(self.root, text="Calculate Distance",
                                                   command=self.calculate_distance)
        self.calculate_distance_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Output area
        self.result_label = tk.Label(self.root, text="Distance: N/A")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def create_map(self):
        gmap = gmplot.GoogleMapPlotter.from_geocode("0,0")
        return gmap

    def plot_icons(self, gmap):
        if self.primary_icon_location:
            gmap.marker(self.primary_icon_location[0], self.primary_icon_location[1], color='red')

        for location in self.secondary_icon_locations:
            gmap.marker(location[0], location[1], color='blue')

    def calculate_distance(self):
        primary_icon_coords = self.get_coordinates(self.primary_icon_entry.get())
        secondary_icon_coords = self.get_coordinates(self.secondary_icon_entry.get())

        if not primary_icon_coords or not secondary_icon_coords:
            tk.messagebox.showerror("Error", "Invalid input. Please check the coordinates.")
            return

        self.primary_icon_location = primary_icon_coords
        self.secondary_icon_locations = secondary_icon_coords

        gmap = self.create_map()
        self.plot_icons(gmap)

        distance = self.calculate_total_distance(primary_icon_coords, secondary_icon_coords)
        self.result_label.config(text=f"Total Distance: {distance:.2f} km")

        gmap.draw("map.html")  # Save the map as an HTML file

    def get_coordinates(self, entry_text):
        try:
            lat, lon = map(float, entry_text.split(","))
            return lat, lon
        except ValueError:
            return None

    def calculate_total_distance(self, primary_coords, secondary_coords):
        total_distance = 0
        for secondary_coord in secondary_coords:
            distance = geodesic(primary_coords, secondary_coord).kilometers
            total_distance += distance
        return total_distance


if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
