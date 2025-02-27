from functions import  *

def NearestNeighbor(dane, start):


    liczba_miast = len(dane)
    nieodwiedzone = list(range(liczba_miast))  # Lista wszystkich miast
    nieodwiedzone.remove(start)  # Usuń miasto startowe z listy nieodwiedzonych
    obecne_miasto = start  # Aktualne miasto
    kolejnosc_miast = [start]  # Kolejność odwiedzania miast
    suma_odleglosci = 0  # Długość trasy

    while nieodwiedzone:
        # Znajdź najbliższe miasto
        najblizsze_miasto = min(nieodwiedzone, key=lambda miasto: dane[obecne_miasto, miasto])
        suma_odleglosci += dane[obecne_miasto, najblizsze_miasto]  # Dodaj odległość
        kolejnosc_miast.append(najblizsze_miasto)  # Dodaj miasto do trasy
        nieodwiedzone.remove(najblizsze_miasto)  # Usuń miasto z listy nieodwiedzonych
        obecne_miasto = najblizsze_miasto  # Ustaw nowe miasto jako obecne

    # Dodaj powrót do miasta startowego
    suma_odleglosci += dane[obecne_miasto, start]
    kolejnosc_miast.append(start)

    return kolejnosc_miast, suma_odleglosci

def UruchomNearestNeighbor(dane, liczba_startow):
    najlepsza_trasa = None
    najlepsza_odleglosc = float('inf')

    for start in range(liczba_startow):  # Powtarzamy algorytm dla wielu losowych punktów startowych
        trasa = list(range(dane.shape[0]))  # Pobieramy indeksy miast
        random.shuffle(trasa)  # Losowe mieszanie indeksów miast
        miasto_startowe = trasa[0]  # Pierwszy element po przetasowaniu jako start

        kolejnosc, dystans = NearestNeighbor(dane, miasto_startowe)

        if dystans < najlepsza_odleglosc:  # Aktualizacja najlepszego rozwiązania
            najlepsza_odleglosc = dystans
            najlepsza_trasa = kolejnosc

    print("\nNajlepsze rozwiązanie:")
    print(f"Najlepsza długość trasy: {najlepsza_odleglosc}")
    print(f"Najlepsza trasa: {najlepsza_trasa}")

UruchomNearestNeighbor(dane48, 48)