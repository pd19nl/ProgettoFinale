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
import Moduli.Modulo_Configurazione as pd_config

# =============================================================
# =============================================================
#
#funzioni comuni
import Moduli.Modulo_Common as pd_common


# CALCOLO INDICE DI PERFORMANCE
# MAE - MEAN ABSOLUTE ERROR - ERRORE ASSOLUTO MEDIO
# MAE_TEST
def mae(y_reali, y_predetti):
    return round(np.mean(np.abs(y_reali - y_predetti)), 2)



def confronto_mae(target_supervisionato, target_previsionale, ambiente:str):
    # MAE PREVISIONALE SU DATI DI TEST
    MAE_TEST_SORG =  mae(target_supervisionato , np.mean(target_supervisionato))

    # MAE PREVISIONALE SU DATI DI TRAINING
    MAE_TEST_PREV =  mae(target_supervisionato, np.mean(target_previsionale))

    print(f'MAE {ambiente} SORGENTE       : {MAE_TEST_SORG}')
    print(f'MAE {ambiente} PREVISIONALE  : {MAE_TEST_PREV}')


def arraytargetToDataframe(arrayTarget):
    dfforecast_target = df = pd.DataFrame({
        "row_num": range(len(arrayTarget)),
        "target": arrayTarget
    })
    return dfforecast_target