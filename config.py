"""Fichier de configuration"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR, "data")
CLIENT = os.path.join(DATADIR, "df_client.csv")
MODEL_1 = os.path.join(DATADIR, "mod_1achat.pkl")
MODEL_2 = os.path.join(DATADIR, "mod_2achats.pkl")
MODEL_N = os.path.join(DATADIR, "mod_nachats.pkl")
ETIQ = os.path.join(DATADIR, "etiquette.pkl")
SC_1 = os.path.join(DATADIR, "scaler1.pkl")
SC_2 = os.path.join(DATADIR, "scaler2.pkl")
SC_N = os.path.join(DATADIR, "scalern.pkl")
