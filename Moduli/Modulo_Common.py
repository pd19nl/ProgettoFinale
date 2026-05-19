# =============================================================
# =============================================================
#
# librerie di base
import numpy as np
import pandas as pd


# =============================================================
# =============================================================
#
# gestione file e folder e so
import os
import io
from io import StringIO
from os import listdir
from os.path import isfile, join

# =============================================================
# =============================================================
#
#parametri di configurazione
import Modulo_Configurazione as config


# ===================================================================================
# ===================================================================================
#
#ottengo il folder dove salvo i dati di tipo data
def GetFolderAnalisi():
    folderdati = os.getcwd() 
    folderdati =folderdati+ "\\Analisi" 
    return folderdati



# ===================================================================================
# ===================================================================================
#
#ottengo il folder dove salvo i dati di tipo data
def GetFolderDati():
    folderdati = os.getcwd() 
    folderdati =folderdati+ "\\Data" 
    return folderdati



# ===================================================================================
# ===================================================================================
#
# cancella il file se esiste
def CancellaFileSeEsiste(fullfilename: str):
     # verifico se esiste una precedente versione del file
    if os.path.exists(fullfilename):
        print(f"         Il file '{fullfilename}' esiste, per cui lo rimuovo")
        #cancello il file
        os.remove(fullfilename)
    else:
        print(f"      Il file '{fullfilename}' non esiste")


# ===================================================================================
# ===================================================================================
#
# salva il file nella cartella (estensione csv la inserisce la funzione)
def SalvaDataset(dati, nomefile: str, ambienteDati: bool):
    #full_file_name =  f'/{nomefile}.csv'
    full_file_name =  GetFolderDati()
    if (not ambienteDati):
        full_file_name =  GetFolderAnalisi()

    full_file_name +=  f'/{nomefile}.csv'

    print(f"      path completo file:  {full_file_name}")
    CancellaFileSeEsiste(full_file_name)
    
    #salvo il file perchè sarà usato in seguito per tutti i processi successivi
    dati.to_csv(full_file_name)
    print(f"      Il file salvato {full_file_name}")




# ===================================================================================
# ===================================================================================
#
#aggregazione dataframe dei comuni
#per errore non lho fatto prima quando recuperavo il dataset per cui lo faccio ora
def UnioneOrizzontaleDataFrame(dataframe_a, dataframe_b):
    return pd.concat([dataframe_a,dataframe_b])


# ===================================================================================
# ===================================================================================
#
#array to datase
def SalvaArray(datiArray, nomefile: str, ambienteDati: bool):
    dfArray = pd.DataFrame({
                            "row_num": range(len(datiArray)),
                            "valoreArray": datiArray
                        })
    SalvaDataset(dfArray,nomefile,ambienteDati)