import polib

def load_po_file(file_path):
    """Funkcja wczytująca plik .po i zwracająca listę wpisów (msgid)"""
    po = polib.pofile(file_path)
    return {entry.msgid: entry for entry in po}

def compare_po_files(file_a, file_b):
    """Funkcja porównująca wpisy z dwóch plików .po i zwracająca różnice"""
    entries_a = load_po_file(file_a)
    entries_b = load_po_file(file_b)

    missing_in_b = {msgid: entry for msgid, entry in entries_a.items() if msgid not in entries_b}

    return missing_in_b

def generate_diff_po_file(missing_entries, output_file_path):
    """Funkcja generująca nowy plik .po z brakującymi wpisami"""
    diff_po = polib.POFile()

    for entry in missing_entries.values():
        diff_po.append(entry)

    # Zapisanie różnicowego pliku .po
    diff_po.save(output_file_path)


# Ścieżki do plików .po
file_a_path = 'sale_2.po'
file_b_path = 'addons/sale/i18n/pl.po'
output_diff_po_path = 'sale_2_diff.po'

# Porównanie plików
missing_entries = compare_po_files(file_a_path, file_b_path)

# Generowanie różnicowego pliku .po
generate_diff_po_file(missing_entries, output_diff_po_path)

print(f"Różnicowy plik .po został zapisany jako: {output_diff_po_path}")
