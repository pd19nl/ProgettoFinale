# =============================================================
# =============================================================
#
# librerie di base
import numpy as np
import pandas as pd

# =============================================================
# =============================================================
#
# librerie fase recupero dati
import requests as api


# =============================================================
# =============================================================
#
# gestione file e folder e so
import os
import io
from io import StringIO
from os import listdir
from os.path import isfile, join

#ottengo il folder dove salvo i dati di tipo data
def GetFolderDati():
    folderdati = os.getcwd() 
    folderdati =folderdati+ "\\Data" 
    return folderdati


# cancella il file se esiste
def CancellaFileSeEsiste(fullfilename: str):
     # verifico se esiste una precedente versione del file
    if os.path.exists(fullfilename):
        print(f"         Il file '{fullfilename}' esiste, per cui lo rimuovo")
        #cancello il file
        os.remove(fullfilename)
    else:
        print(f"      Il file '{fullfilename}' non esiste")



# salva il file nella cartella (estensione csv la inserisce la funzione)
def SalvaDataset(dati: DataFrame, nomefile: str):
    full_file_name = GetFolderDati() +  f'/{nomefile}.csv'

    print(f"      path completo file:  {full_file_name}")
    CancellaFileSeEsiste(full_file_name)
    
    #salvo il file perchè sarà usato in seguito per tutti i processi successivi
    dati.to_csv(full_file_name)
    print(f"      Il file salvato {full_file_name}")


# recupera dato da API e lo salva
def RecuperaESalvaDatiPerAnno(urldatiSenzaFiltroAnno : str, anno: int,prefisso_nome_file: int):
    #url completo
    urldati_anno = urldatiSenzaFiltroAnno  + "&pdata=01/01/" + str(anno)

    print('   Recupero  dati anno '+ str(anno))
    #eseguo la richiesta con Verbo Http GET e con l'aggiunta dell'header nella sezione della richiesta 
    rq_anno = api.get(urldati_anno)
    
    #lettura risposta
    status_code_risposta= rq_anno.status_code
    print (f"      status_code_risposta : {status_code_risposta}")
    if(status_code_risposta!=200):
        print(f'      errore richiesta api: status_code_risposta : {status_code_risposta}')
    else:
        print('      Converto i dati json ricevuti in DataFrame')
        df_anno = pd.DataFrame.from_dict(rq_anno.json()['resultset'])

        #aggiungo il riferimento del dataset --importantinssimo
        df_anno['anno_riferimento'] = anno

        nomefile=f"{prefisso_nome_file}_{str(anno)}" 
        print(f'      Salvo i dati in CSV su FS. Nome file={nomefile}')
        SalvaDataset(df_anno,nomefile)



#aggregazione dataframe dei comuni
#per errore non lho fatto prima quando recuperavo il dataset per cui lo faccio ora
def UnioneOrizzontaleDataFrame(dataframe_a: DataFrame, dataframe_b: DataFrame):
    return pd.concat([dataframe_a,dataframe_b])



def UnioneFileCsvPerAnno(prefisso_file_Senza_Anno: str):   
   folderdati = GetFolderDati()
   #print(f"Cartella dati: {folderdati}")  ok testato

   elencoelementi =os.listdir(folderdati)
   #print(elencoelementi)  ok testato
   elencofiledaconcatenare=[]
   for e in elencoelementi:
      #print(e)   #ok testato
      fullfilename =os.path.join(folderdati, e)
      if(os.path.isfile(fullfilename)):
         #print("  e' un file")   #ok testato
         if (e.startswith(f"{prefisso_file_Senza_Anno}_20")):
            #print("  e' un file da gestire")   #ok testato
            elencofiledaconcatenare.append(fullfilename)

   #print(elencofiledaconcatenare)  ok testato
   #print (elencofiledaconcatenare[0]) ok testato

   #print(len(elencofiledaconcatenare)) ok testato
   risultato = pd.read_csv(elencofiledaconcatenare[0])
   for i in range(1, len(elencofiledaconcatenare)):
      #print(i) ok testato
      print(f'Concateno: {elencofiledaconcatenare[i]}')    #ok testato
      nuovofile = pd.read_csv(elencofiledaconcatenare[i])
      risultato = pd.concat([risultato,nuovofile])
     
   print(f"file: {prefisso_file_Senza_Anno}_All")
   SalvaDataset(risultato, f"{prefisso_file_Senza_Anno}_All")




def RecuperaESalvaDatiIstatSingoloAnno(codiceReport:str, anno: int, prefisso_file:str):

    RecuperaESalvaDatiPerAnno(f"https://situas-servizi.istat.it/publish/reportspooljson?pfun={codiceReport}",
                              anno,
                              prefisso_file)
    

def RecuperaESalvaDatiIstat(codiceReport:str, prefisso_file:str, ambito: str, inizio_anno: int, nr_anni: int, ):
    #considero una finestra temporale di 10 anni.
    print(f"Avvio esportazione dati {ambito} per anno")
    anno_esportazione= inizio_anno
    while anno_esportazione < (inizio_anno+ nr_anni+1):
        print(f"Elaborazione dati regione anno {anno_esportazione}")
        RecuperaESalvaDatiIstatSingoloAnno(codiceReport,anno_esportazione,prefisso_file)
        anno_esportazione= anno_esportazione+1

    print("Fine esportazione dati {ambito} per anno")