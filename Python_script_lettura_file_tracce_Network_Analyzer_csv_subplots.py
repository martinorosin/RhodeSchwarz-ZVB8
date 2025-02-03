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
import martino_pylib


### SETUP: variabili, ... ##########################

# Limit line verticali (MHz)
x1=862
x2=928
x3=2402
x4=2483

# Limit line orizzontale (dB)
y1= -6

# Range ricerca minimi (frequenze in MHz) e xlim plottaggi
range1_MHz=700,1000
range2_MHz=2000,3000

# Range assi y (dB) dei grafici
range_y_1_dB=[-35,5]
range_y_2_dB=[-35,5]

#####################################################


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
S11_peakmin_range1=list([])
S11_peakmin_range2=list([])


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
                lista_freq.append(float(row[0]))
                lista_S11_dB.append(float(row[1]))
                lista_S21_dB.append(float(row[2]))

                line_count += 1
    
    # Aggiorno le liste con i dati del file ind-esimo, contenuti nelle liste provvisorie
    Freq_Hz.append(lista_freq)
    S11_dB.append(lista_S11_dB)
    S21_dB.append(lista_S21_dB)
    
    # Calcolo il minimo di S11 nei due range e lo metto in lista come tupla (freq_Hz, valore)
    # RANGE1
    [Freq_Hz_range1_from_ind,Freq_Hz_range1_to_ind], valori = martino_pylib.trova_in_lista(lista_freq,[item*1e6 for item in range1_MHz])
   
    min_dB=min(lista_S11_dB[Freq_Hz_range1_from_ind:Freq_Hz_range1_to_ind])
    S11_peakmin_range1.append((lista_freq[lista_S11_dB.index(min_dB)]/1e6,min_dB))

    # RANGE2
    [Freq_Hz_range2_from_ind,Freq_Hz_range2_to_ind], valori = martino_pylib.trova_in_lista(lista_freq,[item*1e6 for item in range2_MHz])
    
    min_dB=min(lista_S11_dB[Freq_Hz_range2_from_ind:Freq_Hz_range2_to_ind])
    S11_peakmin_range2.append((lista_freq[lista_S11_dB.index(min_dB)]/1e6,min_dB))

# Predispongo due subplots: superiore per banda bassa ed inferiore per banda alta

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10,10))
fig.suptitle('S11 varie antenne (dB)')

# Sub-plot1:aggiungo etichette e titoli alla figura #######################
ax1.set_ylabel('S11 (dB)')
ax1.set_xlabel('Freq (MHz)')
ax1.title.set_text('Banda di Frequenze: '+str(range1_MHz[0])+' MHz to '+str(range1_MHz[1])+' MHz')

# Sub-plot2:aggiungo etichette e titoli alla figura #######################
ax2.set_ylabel('S11 (dB)')
ax2.set_xlabel('Freq (MHz)')
ax2.title.set_text('Banda di Frequenze: '+str(range2_MHz[0])+' MHz to '+str(range2_MHz[1])+' MHz')

# Sub_plot1: setto le griglie
ax1.grid(True)
ax1.grid(True, which='major', color='k', linestyle='-',linewidth=1)
ax1.grid(True, which='minor', color='k', linestyle='--',linewidth=0.2)
ax1.minorticks_on()

# Sub_plot2: setto le griglie
ax2.grid(True)
ax2.grid(True, which='major', color='k', linestyle='-',linewidth=1)
ax2.grid(True, which='minor', color='k', linestyle='--',linewidth=0.2)
ax2.minorticks_on()

# Setto xlim dei plot
ax1.set_xlim(range1_MHz)
ax2.set_xlim(range2_MHz)

# Setto ylim dei plot
ax1.set_ylim(range_y_1_dB)
ax2.set_ylim(range_y_2_dB)

# Subplot1: traccio le limit line verticali
ax1.axvline(x = x1, color ='red', linewidth=1.5, linestyle='--')
ax1.axvline(x = x2, color ='red', linewidth=1.5, linestyle='--')
ax1.axvline(x = x3, color ='red', linewidth=1.5, linestyle='--')
ax1.axvline(x = x4, color ='red', linewidth=1.5, linestyle='--')

# Subplot2: traccio le limit line verticali
ax2.axvline(x = x1, color ='red', linewidth=1.5, linestyle='--')
ax2.axvline(x = x2, color ='red', linewidth=1.5, linestyle='--')
ax2.axvline(x = x3, color ='red', linewidth=1.5, linestyle='--')
ax2.axvline(x = x4, color ='red', linewidth=1.5, linestyle='--')

# Traccio la limit line orizzontale
ax1.axhline(y = y1, color ='magenta', linewidth=2, linestyle='--')
ax2.axhline(y = y1, color ='magenta', linewidth=2, linestyle='--')

# Evidenzio l'area 'OK' per le curve delle antenne
ymax1 = (y1 - range_y_1_dB[0]) / (range_y_1_dB[1] - range_y_1_dB[0])
ymax2 = (y1 - range_y_2_dB[0]) / (range_y_2_dB[1] - range_y_2_dB[0])

ax1.axvspan(x1, x2, ymin = 0, ymax = ymax1, color='green', alpha=0.2)
ax1.axvspan(x3, x4, ymin = 0, ymax = ymax2, color='green', alpha=0.2)

ax2.axvspan(x1, x2, ymin = 0, ymax = ymax1, color='green', alpha=0.2)
ax2.axvspan(x3, x4, ymin = 0, ymax = ymax2, color='green', alpha=0.2)

# PLOTTO MOMENTANEAMENTE - ELIMINARE DOPO IL DEBUG
# plt.show()

# Plot delle tracce alle varie frequenze ##############################
for ind in range(0,len(root.filenames)):
    # Costruisco la legenda con le frequenze delle risonanze
    legenda_base='S11 of '+ root.filenames[ind].rsplit("/",1)[1].rsplit(".",1)[0]+': '
    legenda_low='1st res= '+'{:4.1f}'.format(S11_peakmin_range1[ind][0])+' MHz'
    legenda_up='2nd res= '+'{:4.1f}'.format(S11_peakmin_range2[ind][0])+' MHz'

    ax1.plot([fr/1e6 for fr in Freq_Hz[ind]],S11_dB[ind],'o-',
             linewidth=1,markersize=1,label=legenda_base+legenda_low)
    ax2.plot([fr/1e6 for fr in Freq_Hz[ind]],S11_dB[ind],'o-',
             linewidth=1,markersize=1,label=legenda_base+legenda_up)


# plt.annotate('max = '+str(max(Pout_dBm))+' dBm', xy=(max(Pin_dBm), max(Pout_dBm)-0.5), xytext=(max(Pin_dBm)-2.75, max(Pout_dBm)-5),
#              arrowprops=dict(facecolor='magenta', shrink=0.05),
#              )

ax1.legend()
ax2.legend()
fig.tight_layout()
plt.show()

while 0<1:
    pass