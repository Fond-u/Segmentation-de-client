"""file containing the class"""
import pandas as pd
import numpy as np
from utils import convert_data_for_model
from config import MODEL_1, MODEL_2, MODEL_N, ETIQ, SC_1, SC_2, SC_N
from sklearn.externals import joblib

class FinalData:
    """class qui applique les modeles de prediction"""
    def __init__(self, data):
        self.data = data
        self.modele_1 = joblib.load(MODEL_1)
        self.modele_2 = joblib.load(MODEL_2)
        self.modele_n = joblib.load(MODEL_N)
        self.scaler1 = joblib.load(SC_1)
        self.scaler2 = joblib.load(SC_2)
        self.scalern = joblib.load(SC_N)

    def get_data(self):
        """retourne les données"""
        return self.data

    def get_nb_com(self):
        """retourne le nombre de commande"""
        return self.data.nb_com.values

    def get_val(self, num_client):
        """retourne le label du client"""
        etiquette = joblib.load(ETIQ)
        return etiquette[num_client]

    def predict1(self):
        """retourne la prediction du modele pour 1 commande"""
        data_np = self.data.values
        data_sc = self.scaler1.transform(data_np)
        return self.modele_1.predict(data_sc)

    def predict2(self):
        """retourne la prediction du modele pour 2 commandes"""
        data_np = self.data.values
        data_sc = self.scaler2.transform(data_np)
        return self.modele_2.predict(data_sc)

    def predictn(self):
        """retourne la prediction du modele pour toutes les commandes"""
        data_np = self.data.values
        data_sc = self.scalern.transform(data_np)
        return self.modele_n.predict(data_sc)


class SetHorizonTemporel:
    """class de conversion des données """
    def __init__(self, df, client):
        self.df_client = df
        self.df_client_pos = self.df_client[self.df_client.Quantity > 0]
        self.num_client = client
        self.nb_com = len(self.df_client.InvoiceNo.unique())
        self.nb_prod = self.df_client_pos.shape[0]

    def get_nb_com(self):
        """retourne le nombre de commandes du client"""
        return self.nb_com

    def get_nb_prod(self):
        """retourne le nombre de produits achetter par le client"""
        return self.nb_prod

    def get_ht(self):
        """retourne les données horizon temporel"""
        return self.df_client

    def build_data(self):
        """met en forme et retourne les données exploitable par les algo de prediction"""
        col = ['local', 'dep_tot', 'dep_pos', 'dep_neg', 'dep_com', 'dep_prod',
               'nb_com', 'nb_an', 'dep_max', 'dep_min',
               'nbpr_tot', 'nbpr_ann', 'nbpr_diff', 'nbp_com',
               'last_com', 'freq_com', 'peri_com']
        data_client = pd.DataFrame(np.zeros((1, 17)), columns=col, index=[self.num_client])
        data_client = convert_data_for_model(self.df_client, data_client, self.num_client)
        dc_final = FinalData(data_client)
        return dc_final


class AnalysisInput:
    """Class qui gere le fichier d'entré """
    def __init__(self, name):
        self.name = name
        self.cust = []
        self.ht_dic = {}
        self.dataframe = pd.DataFrame()

    def data_from_csv(self, csv_file):
        """charge les données"""
        self.dataframe = pd.read_csv(csv_file, sep="\t", low_memory=False)
        self.dataframe.InvoiceDate = pd.to_datetime(self.dataframe.InvoiceDate)

    def get_nb_customers(self):
        """retourne le nombre de client"""
        self.cust = self.dataframe.CustomerID.unique()
        return len(self.cust)

    def get_customers(self):
        """retourne la liste des clients"""
        if len(self.cust) == 0:
            self.get_nb_customers()
        return self.cust

    def limit_1com(self, client):
        """limit les données au premier achat"""
        df_temp = self.dataframe[self.dataframe.CustomerID == client]
        df_temp = df_temp[df_temp.Quantity > 0]
        df_temp = df_temp[df_temp.InvoiceDate == df_temp.InvoiceDate.min()]
        return df_temp

    def limit_2com(self, client):
        """limit les données au 2 premiers achats"""
        df_temp = self.dataframe[self.dataframe.CustomerID == client]
        df_work = df_temp.copy()
        df_temp = df_temp[df_temp.Quantity > 0]
        df_temp2 = df_temp[df_temp.InvoiceDate == df_temp.InvoiceDate.min()]
        for inv in df_temp2.InvoiceNo.unique():
            df_work = df_work[df_work.InvoiceNo != inv]
        df_temp3 = df_work[df_work.InvoiceDate == df_work.InvoiceDate.min()]
        df_temp = pd.concat([df_temp2, df_temp3])
        return df_temp

    def horizon_temporel_one(self, client, limit=0):
        """appelle la class horizon temporel et retourne l'instance"""
        if limit == 1:
            df_temps = self.limit_1com(client)
        elif limit == 2:
            df_temps = self.limit_2com(client)
        else:
            df_temps = self.dataframe[self.dataframe.CustomerID == client]
        horizon_temp = SetHorizonTemporel(df_temps, client)
        return horizon_temp
