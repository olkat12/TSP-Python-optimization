from functions import  *
def HillClimbing(dane, liczba_startow, liczba_iteracji, sasiedztwo, max_iteracje_bez_poprawy):
    start_time = time.time()
    najlepsza_trasa = None
    najlepsza_odleglosc = float('inf')  # początkowo bardzo duża wartość

    for start in range(liczba_startow):  # powtarzamy algorytm dla wielu punktów startowych
        trasa = list(range(dane.shape[0]))  # pobieramy indeksy
        random.shuffle(trasa)  # mieszamy indeksy - losowe miasto startowe

        obecna_odleglosc = SumaOdleglosci(dane, trasa)  # obliczamy początkową odległość dla danego startu
        iteracje_bez_poprawy = 0  # Liczymy iteracje bez poprawy

        for i in range(liczba_iteracji):  # iteracje dla konkretnego punktu startowego
            nowa_trasa = sasiedztwo(trasa)  # generujemy sąsiednią trasę
            odleglosc = SumaOdleglosci(dane, nowa_trasa)  # liczymy odległość nowej trasy

            if odleglosc < obecna_odleglosc:  # jeśli nowa trasa jest lepsza, aktualizujemy
                obecna_odleglosc = odleglosc
                trasa = nowa_trasa
                iteracje_bez_poprawy = 0  # Resetujemy licznik, bo znaleźliśmy lepszą trasę
            else:
                iteracje_bez_poprawy += 1  # Zwiększamy licznik iteracji bez poprawy

            if iteracje_bez_poprawy >= max_iteracje_bez_poprawy:
                # print(f"Zatrzymano algorytm po {max_iteracje_bez_poprawy} iteracjach bez poprawy.")
                break
         # Sprawdzamy, czy znaleźliśmy najlepszą trasę globalnie
        if obecna_odleglosc < najlepsza_odleglosc:  # jeśli najlepsza trasa z konkretnego startu jest lepsza, aktualizujemy
            najlepsza_odleglosc = obecna_odleglosc
            najlepsza_trasa = trasa


    end_time = time.time()
    czas_wykonania = end_time - start_time
    print(f"Czas wykonania: {czas_wykonania:.2f} s")
    return najlepsza_odleglosc, najlepsza_trasa


lista = []
for i in range(30):
    # HillClimbing(dane, liczba_startow, liczba_iteracji, sasiedztwo, max_iteracje_bez_poprawy):
    najlepsza_odleglosc, najlepsza_trasa = HillClimbing(dane48, 100, 10000, Inversion, 1000)
    print("Najlepsza trasa:", Dodaj_jeden(najlepsza_trasa))
    print("Odległość najlepszej trasy:", najlepsza_odleglosc)
    lista.append(najlepsza_odleglosc)  # Dodaj odległość do listy

# Oblicz średnią odległość
srednia = sum(lista) / len(lista)
print("Średnia odległość najlepszych tras:", srednia)