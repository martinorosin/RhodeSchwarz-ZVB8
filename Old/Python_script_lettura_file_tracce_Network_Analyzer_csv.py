# MR 14.12.2023
#
# Script python che legge un insieme di files csv formattato come segue
#
# FREQ      S11 (dB)     S21 (dB)
#
# che contiene tracce salvate da una misura a Network Analyzer
#
# e lo plotta su un grafico stile Matlab

import matplotlib.pyplot as plt
import csv
import tkinter as tk
from tkinter import filedialog
import math


### SETUP: variabili, ...

# Limit line verticali (MHz)
x1=429
x2=450
x3=863
x4=928

# Limit line orizzontale (dB)
y1= -6

# Range ricerca minimi (frequenze in MHz) e xlim plottaggi
range1_MHz=350,550
range2_MHz=700,1200

# Predispongo la futura apertura del file dialog tkinter senza GUI
root = tk.Tk()
root.withdraw()

# Dialogo per selezionare file MULTIPLI di tipo CSV da cui leggere i dati
root.filenames = tk.filedialog.askopenfilenames(initialdir = "Download",title = "Select file",filetypes = (("Excel - CSV file","*.csv"),("all files","*.*")))

# Predispone le liste per la lettura
Freq_Hz=list([])
S11_dB=list([])
S21_dB=list([])
# Liste che contengono tuple con: (frequenza del minimo in MHz, Valore del minimo): una per file e per range
S11_peak_range1_min=list([])
S11_peak_range2_min=list([])


# Leggo i dati dai file, uno alla volta e li salvo nelle liste
for filename in root.filenames:
    with open(filename) as csv_file:
        # Creo liste provvisorie per i dati del file ind-esimo
        lista_freq=list([])
        lista_S11_dB=list([])
        lista_S21_dB=list([])

        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                lista_freq.append(float(row[0]))
                lista_S11_dB.append(float(row[1]))
                lista_S21_dB.append(float(row[2]))

                line_count += 1
    
    # Aggiorno le liste con i dati del file ind-esimo, contenuti nelle liste provvisorie
    Freq_Hz.append(lista_freq)
    S11_dB.append(lista_S11_dB)
    S21_dB.append(lista_S21_dB)
    
    # Calcolo il minimo di S11 nei due range
    # RANGE1
    # DEBUG
    # print(range1_MHz[0]*1e6)

    # Freq_Hz_range1_from_ind=Freq_Hz.index(min([item for item in Freq_Hz if item >= range1_MHz[0]*1e6]))
    # Freq_Hz_range1_to_ind=Freq_Hz.index(max([item for item in Freq_Hz if item <= range1_MHz[1]*1e6]))
    # S11_peak_range1_min.append(Freq_Hz[lista_S11_dB.index(min(lista_S11_dB[Freq_Hz_range1_from_ind:Freq_Hz_range1_to_ind]))],min(lista_S11_dB[Freq_Hz_range1_from_ind:Freq_Hz_range1_to_ind]))


# # RANGE2
# Freq_Hz_range2_from_ind=Freq_Hz.index(min([item for item in Freq_Hz if item >= range2_MHz[0]*1e6]))
# Freq_Hz_range2_to_ind=Freq_Hz.index(max([item for item in Freq_Hz if item <= range2_MHz[1]*1e6]))

# S11_dB_range2_min=min(S11_dB[Freq_Hz_range2_from_ind:Freq_Hz_range2_to_ind])
# S11_dB_range2_min_freq=Freq_Hz[S11_dB.index(S11_dB_range2_min)]



# Aggiungo etichette e titoli alla figura #######################
plt.figure(figsize=(7, 7), layout='constrained')
plt.ylabel('S11 (dB)')
plt.xlabel('Freq (MHz)')
plt.title('S11 varie antenne (dB)')

plt.grid(True)

# Setto le griglie
plt.grid(True, which='major', color='k', linestyle='-',linewidth=1)
plt.grid(True, which='minor', color='k', linestyle='--',linewidth=0.5)
plt.minorticks_on()

# Setto xlim dei plot
# Range1 ...
#plt.xlim(range1_MHz[0],range1_MHz[1])
# ... oppure Range2 ...
#plt.xlim(range2_MHz[0],range2_MHz[1])
# ... oppure entrambi :)
plt.xlim(range1_MHz[0],range2_MHz[1])

# Setto ylim dei plot
plt.ylim(-35,5)

# Traccio le limit line verticali
plt.axvline(x = x1, color ='red', linewidth=1.5)
plt.axvline(x = x2, color ='red', linewidth=1.5)
plt.axvline(x = x3, color ='red', linewidth=1.5)
plt.axvline(x = x4, color ='red', linewidth=1.5)

# Traccio la limit line orizzontale
plt.axhline(y = y1, color ='green', linewidth=2)

# Plot delle tracce alle varie frequenze ##############################
for ind in range(0,len(root.filenames)):

    plt.plot([fr/1e6 for fr in Freq_Hz[ind]],S11_dB[ind],'o-',linewidth=1,markersize=1,label='S11 of '+ root.filenames[ind].rsplit("/",1)[1].rsplit(".",1)[0])



# plt.annotate('max = '+str(max(Pout_dBm))+' dBm', xy=(max(Pin_dBm), max(Pout_dBm)-0.5), xytext=(max(Pin_dBm)-2.75, max(Pout_dBm)-5),
#              arrowprops=dict(facecolor='magenta', shrink=0.05),
#              )

plt.legend()
plt.show()
