from functions import  *
def Redukcja_geom(T, alpha):
    return alpha * T


def Redukcja_powolna(T, alpha):
    return T / (1 + alpha * T)


# Simulated annealing (wyżarzanie) z kryterium stopu T_koncowa
def SA_T_koncowa(dane, T_koncowa, sasiedztwo, T_poczatkowa, redukcja_temp, alpha):
    T = T_poczatkowa
    trasa = list(range(dane.shape[0]))
    random.shuffle(trasa)
    obecna_odleglosc = SumaOdleglosci(dane, trasa)  # Obecna odległość to najlepsza odległość którą znaleziono

    suma_odleglosci = obecna_odleglosc
    liczba_iteracji = 1

    start_time = time.time()  # Rozpocznij pomiar czasu

    while T > T_koncowa:  # dopóki T jest większa od zadane T końcowej
        nowa_trasa = sasiedztwo(trasa)
        odleglosc = SumaOdleglosci(dane, nowa_trasa)
        diff_odleglosc = odleglosc - obecna_odleglosc

        # Jeśli nowa odległość jest mniejsza lub jeśli jest większa,
        # ale losowa liczba (0,1) jest mniejsza od wartości wyliczonej ze wzoru,
        # to przyjmujemy to rozwiązanie
        # Wzór e^(-roznica / T)
        if odleglosc <= obecna_odleglosc or random.random() < math.exp(-diff_odleglosc / T):
            obecna_odleglosc = odleglosc  # aktualizujemy obecną (najlepszą) odległość
            trasa = nowa_trasa

        suma_odleglosci += obecna_odleglosc
        liczba_iteracji += 1

        T = redukcja_temp(T, alpha)  # Tu redukujemy temperaturę według jednego ze wzorów

    end_time = time.time()
    czas_wykonania = end_time - start_time
    print(f"Czas wykonania: {czas_wykonania:.2f} s")
    return obecna_odleglosc, trasa


lista = []
for i in range(30):
    najlepsza_odleglosc, najlepsza_trasa = SA_T_koncowa(dane48, T_koncowa=0.0000001, sasiedztwo=Inversion,
                                                        T_poczatkowa=250, redukcja_temp=Redukcja_geom, alpha=0.99)
    print("Najlepsza trasa:", Dodaj_jeden(najlepsza_trasa))
    print("Odległość najlepszej trasy:", najlepsza_odleglosc)
    lista.append(najlepsza_odleglosc)  # Dodaj odległość do listy

# Oblicz średnią odległość
srednia = sum(lista) / len(lista)
print("Średnia odległość najlepszych tras:", srednia)
