from functions import  *

def Swap_TS(trasa, miasto1 = None, miasto2 = None):
    trasa_temp = trasa.copy()
    trasa[miasto1] = trasa[miasto2]
    trasa[miasto2] = trasa_temp[miasto1]
    return trasa

def Insert_TS(trasa, miasto1, miasto2):
    trasa_temp = trasa.copy()  # Tworzymy kopię trasy, aby nie modyfikować oryginału
    miasto1 = trasa_temp[miasto1] # Usuwamy miasto1 z trasy
    trasa_temp.remove(miasto1)
    trasa_temp.insert(miasto2, miasto1) # Wstawiamy miasto1 w miejsce miasto2
    return trasa_temp

def Inversion_TS(trasa, miasto1, miasto2):
    if miasto1 > miasto2:
        miasto1, miasto2 = miasto2, miasto1
    nowa_trasa = trasa[:miasto1] + trasa[miasto1:miasto2+1][::-1] + trasa[miasto2+1:]
    return nowa_trasa

def TS(dane, liczba_iteracji, sasiedztwo, dlugosc_tabu, max_iteracje_bez_poprawy):
    start_time = time.time()
    najlepsza_trasa = None # Najlepsza trasa (globalne rozwiązanie)
    najlepsza_odleglosc = float('inf')  # początkowo bardzo duża wartość
    wszystkie_odleglosci = []  # Lista do przechowywania odległości dla wszystkich startów


    trasa = list(range(dane.shape[0]))  # Pobranie indeksów miast
    random.shuffle(trasa)  # mieszamy indeksy - losowe miasto startowe

    obecna_odleglosc = SumaOdleglosci(dane, trasa)  # Obliczenie odległości początkowej
    lista_tabu = [] # Lista tabu przechowująca niedozwolone ruchy
    iteracje_bez_poprawy = 0 # Licznik iteracji bez poprawy rozwiązania

    for i in range(liczba_iteracji):   # Wykonywanie określonej liczby iteracji
        if iteracje_bez_poprawy >= max_iteracje_bez_poprawy:
            break  # Przerwanie, gdy osiągnięto maksymalną liczbę iteracji bez poprawy

        mozliwe_zamiany = [] # Lista możliwych zamian w bieżącej iteracji

        # Generowanie sąsiedztwa (par miast do zamiany)
        for miasto1 in range(len(trasa)):
            for miasto2 in range(miasto1 + 1, len(trasa)):  # Rozważamy tylko unikalne pary
                if [miasto1, miasto2] in lista_tabu or [miasto2, miasto1] in lista_tabu:
                    continue  # Jeśli para jest na liście tabu, pomijamy

                # Generowanie nowej trasy na podstawie zamiany miast
                trasa_copy = sasiedztwo(trasa.copy(), miasto1, miasto2)
                nowa_odleglosc = SumaOdleglosci(dane, trasa_copy)

                # Dodajemy możliwą zamianę do listy, jeśli spełnia warunki:
                # - Gdy ruch nie jest na liście tabu
                # - Gdy ruch jest na liście tabu, ale nowa odległość (nowa_odleglosc) jest lepsza niż dotychczasowe najlepsze globalne rozwiązanie (najlepsza_odleglosc)
                if [miasto1, miasto2] not in lista_tabu or nowa_odleglosc < najlepsza_odleglosc:
                    mozliwe_zamiany.append([nowa_odleglosc, miasto1, miasto2])

        if not mozliwe_zamiany:
            continue  # Jeśli nie ma możliwych zamian, pomijamy iterację

        # Wybór najlepszego ruchu (minimalizacja odległości)
        najlepsza_zamiana = min(mozliwe_zamiany, key=lambda x: x[0]) #Porównywanie za pomocą zerowego undeksu listy, czyli nowa_odleglosc

        # Aktualizacja trasy na podstawie najlepszego ruchu
        trasa = sasiedztwo(trasa, najlepsza_zamiana[1], najlepsza_zamiana[2]) # trasa oraz indeks miasta1 i miasta2
        lista_tabu.append([najlepsza_zamiana[1], najlepsza_zamiana[2]])

        # Usuwanie najstarszego ruchu z Tabu z powodu ograniczenie rozmiaru listy tabu
        if len(lista_tabu) > dlugosc_tabu:
            lista_tabu.pop(0)

        # Aktualizacja najlepszego globalnego rozwiązania
        obecna_odleglosc = SumaOdleglosci(dane, trasa)
        if obecna_odleglosc < najlepsza_odleglosc: # Sprawdzenie poprawy
            najlepsza_odleglosc = obecna_odleglosc
            najlepsza_trasa = trasa.copy() # Zapisanie nowej najlepszej trasy
            iteracje_bez_poprawy = 0  # Reset licznika iteracji bez poprawy
        else:
            iteracje_bez_poprawy += 1  # zwiększ licznik

    # Reset algorytmu, jeśli brak poprawy przez maksymalną liczbę iteracji
    if iteracje_bez_poprawy >= max_iteracje_bez_poprawy:
        trasa = list(range(dane.shape[0]))
        random.shuffle(trasa)
        obecna_odleglosc = SumaOdleglosci(dane, trasa)
        iteracje_bez_poprawy = 0  # Reset licznika po resecie

    # Dodanie końcowej odległości do listy wyników
    wszystkie_odleglosci.append(obecna_odleglosc)

    end_time = time.time()
    czas_wykonania = end_time - start_time
    print(f"Czas wykonania: {czas_wykonania:.2f} s")
    return najlepsza_trasa, najlepsza_odleglosc


lista = []
for i in range(30):
    trasa, odleglosc = TS(dane48, 1000, Inversion_TS, 6, 200)
    print("Najlepsza trasa:", Dodaj_jeden(trasa))
    print("Odległość najlepszej trasy:", odleglosc)
    lista.append(odleglosc)  # Dodaj odległość do listy

# Obliczanie średniej odległości
srednia = sum(lista) / len(lista)
print("Średnia odległość najlepszych tras:", srednia)