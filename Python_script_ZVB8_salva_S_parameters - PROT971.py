# MR - 14.12.2023
#
# Script python che legge da Network Analyzer Rohde Schwarz ZVB8:
# un file parametri S dal CH1 e lo salva su directory del Network Analyer (su cartella definita come costante)
# e salva le tracce S11 ed S22 su file CSV per successiva lettura con apposito script
#
# Python_script_Misura_Pout_vs_Pin_E4436B_EXA_N9010A_gpib
import time
import pyvisa
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import csv

# Predispongo la futura apertura del file dialog tkinter senza GUI
root = tk.Tk()
root.withdraw()

########################################################################################
# Impostazioni GPIB strumenti
ZVB8_gpib_addr = 20


# Impostazioni setup di misura


# Imposto tempo di attesa (s) per consentire la stabilizzazione della misura (almeno 0.4s)
attesa=2
########################################################################################


# Apre gestore VISA e crea gli alias degli strumenti in VISA
rm = pyvisa.ResourceManager()
Vector_NA = rm.open_resource('GPIB1::'+str(ZVB8_gpib_addr)+'::INSTR')


# Identificazione strumenti per verificare la loro connessione
print('### IDENTIFICAZIONE STRUMENTI CONNESSI ###')
print("Il Network Analyzer connesso è: ")
print()
print(Vector_NA.query("*IDN?"))
print("Il Network Analyzer connesso è: ")
print()
print('########################################')
print()

# Network Analyzer - SETUP =============================


# Generatore RF- Faccio qualcosa (es. Seleziono Ch1 / Tr1 come attiva)
Vector_NA.write("CALC1:PAR:SEL 'Trc1';")

# Network Analyzer - Attendo che non abbia operazioni pendenti
ans=Vector_NA.query("*OPC?")

#############################################################
# Dialogo per selezionare file di tipo CSV su cui salvare i dati
root.filename = tk.filedialog.asksaveasfilename(initialdir = "Download",initialfile='SPar_'+'.csv',title = "Select file",filetypes = (("Excel - CSV file","*.csv"),("all files","*.*")))
#############################################################

# Chiedo all'utente numero progressivo antenna in misura
# ind_ant = simpledialog.askinteger("Progressivo Antenna in misura...",
# "Indica il numero progresso (ID) dell'antenna in misura", parent=root, minvalue=0, # parent changed...
# maxvalue=100000)

# Inizializzo lista per misure
Freq_MHz=list([])
Tr1_S11_dB=list([])
Tr7_S21_dB=list([])

# Leggo array di frequenze di misura (MHz): Seleziono Traccia /  Leggo l'array di frequenze
Vector_NA.write("CALC1:PAR:SEL 'Trc1';")
Freq_Hz=Vector_NA.query("CALC1:DATA:STIM?")
Freq_Hz=Freq_Hz.split(",")

# Leggo Tr1 - S11: Seleziono Traccia / Imposto formato / Leggo l'array di dati
Vector_NA.write("CALC1:PAR:SEL 'Trc1';")
Vector_NA.write("CALC1:FORM MLOG;")
Tr1_S11_dB=Vector_NA.query("CALC1:DATA? FDAT;")
Tr1_S11_dB=Tr1_S11_dB.split(",")
# Network Analyzer - Attendo che non abbia operazioni pendenti
ans=Vector_NA.query("*OPC?")

# Leggo Tr6 - S21: Seleziono Traccia / Imposto formato / Leggo l'array di dati
Vector_NA.write("CALC2:PAR:SEL 'Trc6';")
Vector_NA.write("CALC2:FORM MLOG;")
Tr6_S21_dB=Vector_NA.query("CALC2:DATA? FDAT;")
Tr6_S21_dB=Tr6_S21_dB.split(",")

# Riporto la Traccia 1 come attiva
Vector_NA.write("CALC1:PAR:SEL 'Trc1';")

# Network Analyzer - Attendo che non abbia operazioni pendenti
ans=Vector_NA.query("*OPC?")

# Scrittura su disco del Network del file Parametri S, porte 1 e 2, nella directory indicata e con nome file indicato
# Directory_NA="'D:20231214 Misure Ant Biband 068'"
# Vector_NA.write(":MMEMory:CDIRectory '"+Directory_NA+"';")
# Vector_NA.write(":MMEMory:STORe:TRACe:PORTs 1, '"+root.filename.rsplit("/",1)[1].rsplit(".",1)[0]+".s2p"+"', COMPlex, 1, 2")

# Scrittura su file CSV dei dati misurati, prima intestazione poi i dati
with open(root.filename.rsplit("/",1)[0]+"/"+root.filename.rsplit("/",1)[1].rsplit(".",1)[0]+".csv", mode='w', newline='') as file_csv:
    file_csv_writer = csv.writer(file_csv, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_csv_writer.writerow(["Frequenza (Hz)","Traccia 1 - S11 (dB)", 'Traccia 7 - S21 (dB)'])
    
    for i in range(0,len(Freq_Hz)):
        file_csv_writer.writerow([format(float(Freq_Hz[i]),'10.0f'),format(float(Tr1_S11_dB[i]),'10.2f'),format(float(Tr6_S21_dB[i]),'10.2f')])