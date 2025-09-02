import os
parameter_dict = {}

script_dir = os.path.dirname(os.path.abspath(__file__))
dateipfad = os.path.join(script_dir, "jay.config")

with open(dateipfad, "r") as file:
    for line in file:
        line = line.strip()
        # Kommentarzeilen überspringen
        if line.startswith("#") or not line:
            continue
        # String an Doppelpunkt splitten
        if ":" in line:
            param, wert = line.split(":", 1)
            param = param.strip()
            wert = wert.strip()
            # Wert zu Parameter im Dictionary speichern
            parameter_dict[param] = wert

# Beispiel: Ausgabe aller Parameter und Werte
for key, value in parameter_dict.items():
    print(f"{key} = {value}")
