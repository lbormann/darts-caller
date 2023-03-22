import os
import re

def sanitize_line(line):
    # Sonderzeichen und Zahlen am Anfang und am Ende einer Zeile entfernen
    line = re.sub(r'^[\d.#_\-?´|+]+', '', line)
    line = re.sub(r'[\d.#_\-?´|+]+$', '', line)

    # Sonderzeichen und Zahlen, die nicht am Anfang und Ende einer Zeile stehen, behandeln
    line = re.sub(r'[\d#_\-?´|+]', '', line)
    line = re.sub(r'\.', ' ', line)
    
    # Zeilen entfernen, die weniger als 3 Zeichen lang sind oder leer sind
    if len(line.strip()) < 3:
        return None

    return line.strip()

def get_script_directory():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir


if __name__ == "__main__":
    script_dir = get_script_directory()

    with open(os.path.join(script_dir, "playerlist.txt"), "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    sanitized_lines = set()
    for line in lines:
        sanitized_line = sanitize_line(line)
        
        # Überspringe leere Zeilen oder Zeilen mit einer Zeichenlänge kleiner 3
        if sanitized_line is None:
            continue
        
        # Doppelte Zeilen entfernen (ignoriere Groß-/Kleinschreibung)
        sanitized_line_lower = sanitized_line.lower()
        if sanitized_line_lower not in sanitized_lines:
            sanitized_lines.add(sanitized_line_lower + ";;")

    with open(os.path.join(script_dir, "playerliste_sanitized.txt"), "w", encoding="utf-8") as outfile:
        for line in sanitized_lines:
            outfile.write(line + '\n')
