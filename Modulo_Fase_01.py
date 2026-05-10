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

# =============================================================
# =============================================================
#
#parametri di configurazione
import Modulo_Configurazione as pd_config

# =============================================================
# =============================================================
#
#funzioni comuni
import Modulo_Common as pd_common




# ===================================================================================
# ===================================================================================
#
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
        pd_common.SalvaDataset(df_anno,nomefile,True)



# ===================================================================================
# ===================================================================================
#
def UnioneFileCsvPerAnno(prefisso_file_Senza_Anno: str):   
   folderdati = pd_common.GetFolderDati()
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
   pd_common.SalvaDataset(risultato, f"{prefisso_file_Senza_Anno}_All",True)


# ===================================================================================
# ===================================================================================
#
# logica di estrazione e salvataggio report per singolo anno
def RecuperaESalvaDatiIstatSingoloAnno(codiceReport:str, anno: int, prefisso_file:str):

    RecuperaESalvaDatiPerAnno(f"https://situas-servizi.istat.it/publish/reportspooljson?pfun={codiceReport}",
                              anno,
                              prefisso_file)
    
# ===================================================================================
# ===================================================================================
#
# logica di estrazione dei dati per periodo di analisi
def RecuperaESalvaDatiIstat(codiceReport:str, prefisso_file:str, ambito: str ):
    inizio_anno: int = pd_config.GetAnnoInizioAnalisi() 
    nr_anni: int = pd_config.GetNrAnniAnalisi()

    #considero una finestra temporale di 10 anni.
    print(f"Avvio esportazione dati {ambito} per anno")
    anno_esportazione= inizio_anno
    while anno_esportazione < (inizio_anno+ nr_anni+1):
        print(f"Elaborazione dati regione anno {anno_esportazione}")
        RecuperaESalvaDatiIstatSingoloAnno(codiceReport,anno_esportazione,prefisso_file)
        anno_esportazione= anno_esportazione+1

    print("Fine esportazione dati {ambito} per anno")



   
# ===================================================================================
# ===================================================================================
#
# logica di estrazione dei dati per periodo di analisi
def RecuperaESalvaDatiIstatUnicaRichiesta(urlUnico:str, prefisso_file:str, ambito: str ):
    print(f"Avvio esportazione dati {ambito} per anno")
    RecuperaESalvaDatiUnicaRichiesta(urlUnico,prefisso_file)
    print("Fine esportazione dati {ambito} per anno")





# ===================================================================================
# ===================================================================================
#
# recupera dato da API e lo salva
def RecuperaESalvaDatiUnicaRichiesta(urlUnico : str, prefisso_nome_file: int):

    print('   Recupero  dati '+ urlUnico)
    #eseguo la richiesta con Verbo Http GET e con l'aggiunta dell'header nella sezione della richiesta 
    rq_api = api.get(urlUnico)
    
    #lettura risposta
    status_code_risposta= rq_api.status_code
    print (f"      status_code_risposta : {status_code_risposta}")
    if(status_code_risposta!=200):
        print(f'      errore richiesta api: status_code_risposta : {status_code_risposta}')
    else:
        print('      Converto i dati json ricevuti in DataFrame')
        df_unico = pd.DataFrame.from_dict(rq_api.json()['resultset'])

        nomefile=f"{prefisso_nome_file}_All" 
        print(f'      Salvo i dati in CSV su FS. Nome file={nomefile}')
        pd_common.SalvaDataset(df_unico,nomefile,True)