import pandas as pd
import numpy as np
import random
import time
import math

# Wczytanie danych
dane48 = pd.read_csv('dane48.csv', index_col=[0],sep=";")
dane76 = pd.read_csv('dane76.csv', index_col=[0],sep=";")
dane127 = pd.read_csv('dane127.csv', index_col=[0],sep=";")

# Zamiana 0 na NA
dane48 = dane48.replace(0, np.nan).to_numpy()
dane76 = dane76.replace(0, np.nan).to_numpy()
dane127 = dane127.replace(0, np.nan).to_numpy()

def SumaOdleglosci(dane, kolejnosc_miast):
    trasa = 0
    for i in range(len(kolejnosc_miast) - 1):
        trasa += dane[kolejnosc_miast[i], kolejnosc_miast[i + 1]]
    trasa += dane[kolejnosc_miast[-1], kolejnosc_miast[0]]
    return trasa

def Swap(trasa):
    trasa_temp = trasa.copy()
    miasto1 = random.randint(0, len(trasa) - 1)
    miasto2 = random.randint(0, len(trasa) - 1)
    trasa[miasto1] = trasa[miasto2]
    trasa[miasto2] = trasa_temp[miasto1]
    return trasa

def Insert(trasa):
    miasto1 = random.randint(0, len(trasa) - 1)
    indeks = random.randint(0, len(trasa) - 1) # indeks na ktory wsadzic
    trasa.remove(miasto1)
    trasa.insert(indeks, miasto1)
    return trasa

def Inversion(trasa):
    indeks1 = random.randint(0, len(trasa) - 1)
    indeks2 = random.randint(0, len(trasa) - 1)
    if indeks1 > indeks2:
        indeks1, indeks2 = indeks2, indeks1
    nowa_trasa = trasa[:indeks1] + trasa[indeks1:indeks2+1][::-1] + trasa[indeks2+1:]
    return nowa_trasa

def Dodaj_jeden(lista):

    return [element + 1 for element in lista]



