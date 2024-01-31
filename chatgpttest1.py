import numpy as np
import ipywidgets as widgets
from ipyleaflet import Map, Marker, AwesomeIcon
from IPython.display import display

# Set initial location to Pearl Harbor
initial_location = [21.3445, -157.9746]  # Coordinates for Pearl Harbor

# Create the main map
m = Map(center=initial_location, zoom=15, layout=dict(height='600px'))

# Main icon
main_icon = Marker(
    location=initial_location,
    draggable=True,
    icon=AwesomeIcon(name='circle', marker_color='red', icon_color='white')
)

# Event handler for main icon drag and drop
def on_main_icon_move(event, main_icon):
    main_icon.location = event['new']

# Bind event handler to main icon
main_icon.observe(lambda event: on_main_icon_move(event, main_icon), names='location')

# Initialize secondary icons
secondary_icons = []

# Dictionary to store ship types for each secondary icon
secondary_ship_types = {}

def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 111320 / 0.9144  # Conversion from degrees to yards
    return distance

# Function to add a new ship icon
def add_ship(ship_color, ship_type):
    while True:
        # Generate random location within the map boundaries
        random_location = [
            initial_location[0] + np.random.uniform(-0.01, 0.01),
            initial_location[1] + np.random.uniform(-0.01, 0.01)
        ]

        # Check distance from existing icons
        too_close = False
        for icon in secondary_icons:
            distance = calculate_distance(icon.location, random_location)
            if distance < 100:
                too_close = True
                break

        if not too_close:
            break

    new_icon = Marker(
        location=random_location,
        draggable=True,
        icon=AwesomeIcon(name='circle', marker_color=ship_color, icon_color='white')
    )
    secondary_icons.append(new_icon)
    secondary_ship_types[new_icon] = ship_type
    m.add_layer(new_icon)

# Function to remove all ships from the map
def clear_ships(button):
    for icon in secondary_icons:
        m.remove_layer(icon)
    secondary_icons.clear()

# Add clear button
clear_button = widgets.Button(description="Clear Ships")
clear_button.on_click(clear_ships)

# Add clear button to the display
display(clear_button)

# Event handler to add a carrier icon
def add_carrier(button):
    add_ship('blue', 'Carrier')

# Event handler to add a cruiser icon
def add_cruiser(button):
    add_ship('green', 'Cruiser')

# Event handler to add a destroyer icon
def add_destroyer(button):
    add_ship('black', 'Destroyer')

# Event handler to add a supply ship icon
def add_supply_ship(button):
    add_ship('white', 'Supply Ship')

# Add secondary icon buttons
add_carrier_button = widgets.Button(description="Add Carrier")
add_carrier_button.on_click(add_carrier)
add_cruiser_button = widgets.Button(description="Add Cruiser")
add_cruiser_button.on_click(add_cruiser)
add_destroyer_button = widgets.Button(description="Add Destroyer")
add_destroyer_button.on_click(add_destroyer)
add_supply_ship_button = widgets.Button(description="Add Supply Ship")
add_supply_ship_button.on_click(add_supply_ship)

# Display buttons
ship_buttons = widgets.HBox([add_carrier_button, add_cruiser_button, add_destroyer_button, add_supply_ship_button])
display(ship_buttons)

# Display main icon on the map
m.add_layer(main_icon)

# Display the map
display(m)

# Display finalize ship location button
finalize_button = widgets.Button(description="Finalize Ship Location")
display(finalize_button)

# Text widget to display distances
distances_text = widgets.Textarea(layout={'height': '100px', 'width': '400px'})
display(distances_text)

# Event handler for finalizing ship location
def finalize_ship_location(button):
    # Move main icon to average position of 100 random movements within 50 yards of the original position
    main_icon_location = main_icon.location
    for _ in range(100):
        random_location = [
            main_icon_location[0] + np.random.uniform(-0.0005, 0.0005),
            main_icon_location[1] + np.random.uniform(-0.0005, 0.0005)
        ]
        distance = calculate_distance(main_icon_location, random_location)
        if distance <= 50:
            main_icon_location = random_location

    main_icon.location = main_icon_location

    # Calculate distances from main icon to all secondary icons
    distances = []
    for icon in secondary_icons:
        distance = calculate_distance(main_icon.location, icon.location)
        distances.append((secondary_ship_types[icon], distance))

    # Display distances in the text widget
    distances_text.value = "\n".join(f"{ship}: {distance:.2f} yards" for ship, distance in distances)

# Add event handler to finalize button
finalize_button.on_click(finalize_ship_location)