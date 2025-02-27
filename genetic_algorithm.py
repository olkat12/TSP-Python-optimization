from functions import  *

def InicjalizacjaPopulacji(dane, wielkosc_populacji):
    populacja = []  # Tworzymy pustą listę na trasy

    for _ in range(wielkosc_populacji):  # Powtarzamy tyle razy, ile tras chcemy wygenerować
        trasa = list(range(dane.shape[0]))  # Tworzymy listę indeksów miast (np. dla dane48 [0, 1, 2, ..., 47])
        random.shuffle(trasa)  # Mieszamy kolejność miast, aby trasa była losowa
        populacja.append(trasa)  # Dodajemy trasę do populacji

    return populacja  # Zwracamy całą populację (listę losowych tras)


def OcenaPopulacji(dane, populacja):
    return [SumaOdleglosci(dane, trasa) for trasa in populacja]
    # Dla każdej trasy w populacji wywołujemy funkcję SumaOdleglosci,
    # która oblicza całkowitą długość trasy na podstawie macierzy odległości "dane"
    # wynik to lista, gdzie kazdy element odpowiada dlugości jednej trasy


def Turniej(populacja, oceny):
    rodzice = []  # Lista do przechowywania wybranych rodziców

    for _ in range(len(populacja)):  # Pętla działa tyle razy, ile wynosi liczba osobników w populacji
        # Losowanie 10 uczestników do turnieju
        uczestnicy = random.sample(list(zip(populacja, oceny)),
                                   10)  # zip łączy dwie listy (populacja i oceny) w pary, później tworzona jest z tego lista
        # Wybieramy uczestnika z lepszym wynikiem (najmniejsza wartość oceny, czyli najkrótsza trasa)
        najlepszy_uczestnik = min(uczestnicy, key=lambda x: x[
            1])  # Każdy uczestnik to para: (trasa, ocena), lambda x: x[1] oznacza, że patrzymy na drugi element pary (x[1]), czyli ocenę
        # Dodajemy trasę zwycięzcy turnieju do listy rodziców
        rodzice.append(najlepszy_uczestnik[0])

    return rodzice  # Zwracamy listę wybranych rodziców


def Ruletka(populacja, oceny):
    rodzice = []  # Lista, w której będą przechowywani wybrani rodzice
    suma_fitness = sum(1 / ocena for ocena in oceny)  # Oblicza sumę odwrotności ocen (fitness) populacji
    # Mniejsze oceny (odległości) oznaczają lepsze rozwiązania, więc odwrotność oceny daje wyższy fitness dla lepszych rozwiązań
    prawdopodobienstwa = [(1 / ocena) / suma_fitness for ocena in
                          oceny]  # Oblicza prawdopodobieństwo wyboru jednostki na podstawie jej oceny (fitness)
    # Im mniejsza ocena, tym większe prawdopodobieństwo wyboru

    # Pętla wybierająca rodziców na podstawie obliczonych prawdopodobieństw
    for _ in range(len(populacja)):
        # Wybór jednostki z populacji na podstawie prawdopodobieństw
        wybór = random.choices(populacja, weights=prawdopodobienstwa, k=1)[
            0]  # Wybierany jest jeden rodzic, dlatego k=1, [0] oznacza, że w zmiennej zapisywany jest pierwszy element czyli trasa
        # Dodanie wybranego rodzica do listy 'rodzice'
        rodzice.append(wybór)

    # Zwrócenie listy wybranych rodziców
    return rodzice


def KrzyzowaniePMX(rodzic1, rodzic2):
    rozmiar = len(rodzic1)  # Określenie długości (rozmiaru) chromosomu
    # Wybieranie dwóch punktów krzyżowania losowo
    punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))
    # print(f"Punkty krzyżowania: {punkt1}, {punkt2}")

    potomek = [None] * rozmiar  # Tworzenie pustego chromosomu potomka o tej samej długości

    # Kopiowanie segmentu z rodzica 1 do potomka
    potomek[punkt1:punkt2 + 1] = rodzic1[punkt1:punkt2 + 1]

    # Wstawianie pozostałych genów z rodzica 2 do potomka, unikając powtórzeń
    for i in range(rozmiar):
        if potomek[i] is None:  # Jeśli w danym miejscu potomka nie ma jeszcze wartości
            if rodzic2[i] not in potomek:  # Jeśli gen z rodzica 2 nie został jeszcze wstawiony
                potomek[i] = rodzic2[i]  # Wstawiamy gen z rodzica 2
            else:  # Jeśli gen z rodzica 2 już istnieje w potomstwie, należy znaleźć jego zamiennik
                el = rodzic2[i]  # Bierzemy gen z rodzica 2
                # Szukamy odpowiedniego elementu, który nie występuje w potomstwie
                while el in potomek:
                    el = rodzic2[rodzic1.index(el)]  # Znajdujemy element w rodzicu 2, który nie występuje w potomku
                potomek[i] = el  # Wstawiamy odpowiedni gen

    return potomek  # Zwracamy wygenerowanego potomka


def KrzyzowanieOX(rodzic1, rodzic2):
    rozmiar = len(rodzic1)  # Określenie długości (rozmiaru) chromosomu
    # Wybieranie dwóch punktów krzyżowania losowo
    punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))
    # print(f"Punkty krzyżowania: {punkt1}, {punkt2}")

    potomek = [None] * rozmiar  # Tworzenie pustego chromosomu potomka o tej samej długości

    # Kopiowanie segmentu z rodzica 1 do potomka
    potomek[punkt1:punkt2 + 1] = rodzic1[punkt1:punkt2 + 1]

    # Wstawianie pozostałych genów z rodzica 2 do potomka, unikając powtórzeń
    indeks = punkt2 + 1  # Zaczynamy wstawiać geny od miejsca tuż po punkcie 2 krzyżowania
    for i in range(rozmiar):
        if rodzic2[i] not in potomek:  # Jeśli gen z rodzica 2 jeszcze nie został wstawiony do potomka
            # Znajdujemy pierwszy wolny indeks w potomstwie, aby wstawić element
            while potomek[indeks % rozmiar] is not None:  # Jeśli indeks jest już zajęty, przechodzimy do następnego
                # Jeśli indeks = rozmiar, to zaczyna liczyć od zera, np. indeks = 6, rozmiar = 6, 6 % 6 = 0, czyli przechodzimy do początku chromosomu
                indeks += 1  # Przesuwamy indeks w prawo
            potomek[indeks % rozmiar] = rodzic2[i]  # Wstawiamy gen w wolne miejsce
    return potomek  # Zwracamy wygenerowanego potomka


def Mutacja(trasa, prawdopodobienstwo):
    # Sprawdzamy, czy zostanie przeprowadzona mutacja, na podstawie prawdopodobieństwa
    if random.random() < prawdopodobienstwo:
        # Losowanie dwóch różnych miast (indeksów) z trasy
        miasto1, miasto2 = random.sample(range(len(trasa)), 2)
        # Zamiana miejscami dwóch miast na trasie (Swap)
        trasa[miasto1], trasa[miasto2] = trasa[miasto2], trasa[miasto1]

    return trasa


def NowaPopulacja(dane, populacja, oceny, prawd_krzyzowania, prawd_mutacji, dobór_rodziców, krzyżowanie):
    # Wybór rodziców na podstawie zadanej metody doboru
    rodzice = dobór_rodziców(populacja, oceny)
    nowa_populacja = []  # Inicjalizacja nowej populacji

    # Generowanie nowych osobników (potomków) w parach
    for i in range(0, len(populacja), 2):
        rodzic1, rodzic2 = rodzice[i], rodzice[i + 1]

        # Decyzja o krzyżowaniu na podstawie prawdopodobieństwa
        if random.random() < prawd_krzyzowania:
            potomek1 = krzyżowanie(rodzic1, rodzic2)  # Krzyżowanie rodziców
            potomek2 = krzyżowanie(rodzic2, rodzic1)  # Krzyżowanie rodziców
        else:
            potomek1, potomek2 = rodzic1[:], rodzic2[
                                             :]  # Kopiowanie bez krzyżowania, czyli rodzice stają się potomkami w nowej populacji

        # Mutacja potomków z określonym prawdopodobieństwem
        nowa_populacja.append(Mutacja(potomek1, prawd_mutacji))
        nowa_populacja.append(Mutacja(potomek2, prawd_mutacji))

    return nowa_populacja  # Zwrócenie nowej populacji


def AlgorytmGenetyczny(dane, wielkosc_populacji, liczba_pokolen, prawd_krzyzowania, prawd_mutacji, dobór_rodziców,
                       krzyżowanie):
    # Inicjalizacja początkowej populacji
    populacja = InicjalizacjaPopulacji(dane, wielkosc_populacji)
    # Ocena populacji (obliczenie długości trasy każdego rozwiązania w populacji)
    oceny = OcenaPopulacji(dane, populacja)

    # Inicjalizacja zmiennych
    najlepsza_trasa = None
    najlepsza_odleglosc = float('inf')
    suma_najlepszych_odleglosci = 0

    # Pętla po pokoleniach
    for pokolenie in range(liczba_pokolen):
        # Tworzenie nowej populacji
        nowa_populacja = NowaPopulacja(dane, populacja, oceny, prawd_krzyzowania, prawd_mutacji, dobór_rodziców,
                                       krzyżowanie)
        populacja = nowa_populacja  # Przypisanie nowej populacji do aktualnej
        # Ocena nowej populacji (odległości rozwiązań)
        oceny = OcenaPopulacji(dane, populacja)

        # Aktualizacja najlepszego rozwiązania (najmniejsza odległość)
        najlepszy_indeks = np.argmin(
            oceny)  # Znalezienie indeksu najlepszego rozwiązania, np.argmin znajduje indeks rozwiązania o najmniejszej odległości
        if oceny[najlepszy_indeks] < najlepsza_odleglosc:
            najlepsza_odleglosc = oceny[najlepszy_indeks]  # Aktualizacja najlepszej odległości
            najlepsza_trasa = populacja[najlepszy_indeks]  # Aktualizacja najlepszej trasy

        # Sumowanie odległości najlepszego rozwiązania w każdym pokoleniu
        suma_najlepszych_odleglosci += oceny[najlepszy_indeks]

    # Obliczanie średniej odległości najlepszego rozwiązania
    srednia_najlepsza_odleglosc = suma_najlepszych_odleglosci / liczba_pokolen

    # Zwracamy najlepszą trasę, jej odległość oraz średnią odległość w populacjach
    return najlepsza_trasa, najlepsza_odleglosc, srednia_najlepsza_odleglosc


# Obliczenie całkowitego czasu wykonania
start_time = time.time()
trasa, odleglosc, srednia_odleglosc = AlgorytmGenetyczny(dane48, 1000, 2000, 0.9, 0.1, Turniej, KrzyzowanieOX)
end_time = time.time()
czas_wykonania = end_time - start_time

