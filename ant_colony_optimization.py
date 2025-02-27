from functions import  *

def ACO(dane, liczba_iteracji, liczba_mrowek, alfa, beta, rho, Q):
    start_time = time.time()
    n_miast = dane.shape[0]
    feromony = np.ones((n_miast, n_miast))  # Tworzy macierz o wymiarze n wypełnioną jedynkami
    najlepsza_trasa = None
    najlepsza_odleglosc = np.inf
    najlepsze_dystanse_iteracji = []  # Lista do przechowywania najlepszych dystansów z każdej iteracji
    # Bo każda mrówka znajdzie swoją trase w każdej iteracji

    for iteracja in range(liczba_iteracji):
        wszystkie_trasy = []
        wszystkie_odleglosci = []

        # Mrówki tworzą trasy ( _ to nasza jedna mrówka)
        for _ in range(liczba_mrowek):
            trasa = [random.randint(0, n_miast - 1)]  # Losowy wybór miasta startowego
            while len(trasa) < n_miast:  # Dopóki nie odwiedzimy wszystkich miast
                ostatnie_miasto = trasa[-1]  # Ostatnie odwiedzone miasto
                dostepne_miasta = [miasto for miasto in range(n_miast) if miasto not in trasa]

                # Prawdopodobieństwo odwiedzenia każdego możliwego miasta jako kolejne
                # Obliczane to z odpowiednich wzorów (teoria)
                prawdopodobienstwa = []
                for miasto in dostepne_miasta:
                    # (ilość feromonu między miastem ostatnim a następnym) do potęgi alfa
                    tau = feromony[ostatnie_miasto, miasto] ** alfa

                    # atrakcyjność czyli (1/odległość) do potęgi beta
                    eta = (1 / dane[ostatnie_miasto, miasto]) ** beta if dane[ostatnie_miasto, miasto] != 0 else 0

                    prawdopodobienstwa.append(tau * eta)  # licznik = tau*eta (dodajemy do listy)

                # Teraz mianownik liczymy, taki sam dla wszystkich prawdopodobieństw
                # Jest to suma wszystkich tau*eta
                suma_prawdopodobienstw = sum(prawdopodobienstwa)

                # Obliczamy prawdopodobieństwa jako tau*eta / suma
                # Zabezpieczenie przed tym żeby nie dzielić przez 0
                if suma_prawdopodobienstw == 0:
                    prawdopodobienstwa = [1 / len(prawdopodobienstwa)] * len(prawdopodobienstwa)
                else:
                    prawdopodobienstwa = [p / suma_prawdopodobienstw for p in prawdopodobienstwa]

                # Wybór miasta na podstawie prawdopodobieństw (losujemy z odpowiednimi wagami)
                nastepne_miasto = random.choices(dostepne_miasta, weights=prawdopodobienstwa, k=1)[0]
                trasa.append(nastepne_miasto)

            # Zapisanie trasy i jej długości
            odleglosc = SumaOdleglosci(dane, trasa)
            wszystkie_trasy.append(trasa)
            wszystkie_odleglosci.append(odleglosc)

            # Aktualizacja najlepszej trasy
            if odleglosc < najlepsza_odleglosc:
                najlepsza_odleglosc = odleglosc
                najlepsza_trasa = trasa

        # Zapisanie najlepszego dystansu z tej iteracji
        # Żeby potem móc policzyć średnią odległość we wszystkich iteracjach
        najlepsza_odleglosc_iteracji = min(wszystkie_odleglosci)
        najlepsze_dystanse_iteracji.append(najlepsza_odleglosc_iteracji)

        # Feromony wyparowują
        # Mnożymy razy rho (w niektórych wzorach razy (1-rho) ale łatwiej interpretować po prostu rho)
        feromony *= (1 - rho)

        # Tutaj aktualizujemy feromony według odpowiedniego wzoru
        # Bierzemy pod uwagę feromony z poprzedniej iteracji (te przemnożone razy rho czyli już trochę wyparowały) oraz feromony zostawione w tej iteracji (sumujemy po kolei między miastami na trasie)

        # zip tworzy pary z elementow tych list
        for trasa, odleglosc in zip(wszystkie_trasy, wszystkie_odleglosci):
            for i in range(len(trasa) - 1):
                # suma feromonów po kolei między dwoma kolejnymi miastami na trasie, Q to stała
                feromony[trasa[i], trasa[i + 1]] += Q / odleglosc
            feromony[trasa[-1], trasa[0]] += Q / odleglosc  # Powrót do miasta startowego

    # Obliczenie całkowitego czasu wykonania
    end_time = time.time()
    czas_wykonania = end_time - start_time

    # Wyświetlenie wyników
    srednia_odleglosc = np.mean(najlepsze_dystanse_iteracji)
    print(f"Najlepsza odległość: {najlepsza_odleglosc:.4f}")
    print(f"Najlepsza trasa: {najlepsza_trasa}")
    print(f"Średnia odległość: {srednia_odleglosc:.4f}")
    print(f"Czas wykonania: {czas_wykonania:.2f} s")