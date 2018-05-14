"""fichier pour lancer le programme contient la fonction main"""
# coding: utf-8
import os
import random
from models import AnalysisInput
from config import CLIENT

def main():
    """fonction main"""
    os.system("cls")
    print('chargement du fichier complet...\n')
    continuer = 1
    analyse_file = AnalysisInput('all')
    analyse_file.data_from_csv(CLIENT)
    print('Le fichier contient {} client(s).'.format(analyse_file.get_nb_customers()))
    while continuer:
        print('\n')
        num_client = random.choice(analyse_file.get_customers())
        horizon_temp = analyse_file.horizon_temporel_one(num_client)
        print('le client {} a été sélectionné aléatoirement.'.format(num_client))
        num_com = input('Limiter les commandes au premier achat : Taper 1,\n' +
                        'Limiter les commandes aux deux premiers achats : Taper 2,\n' +
                        'Sinon taper directement entrer pour conserver toutes les commandes.\n')
        horizon_temp = analyse_file.horizon_temporel_one(num_client, num_com)
        final_data = horizon_temp.build_data()
        try:
            lab = final_data.get_val(num_client)
        except:
            print('erreur num client, restart.')
            continue
        print()
        print('label du vrai clusteur : ', lab)
        if num_com == '1':
            print('Prediction du modèle entrainé sur',
                  'le premier achat: cluster {}.'.format(final_data.predict1()))
            print('Prediction du modèle entrainé sur',
                  '2 achats: cluster {}.'.format(final_data.predict2()))
            print('Prediction du modèle entrainé sur',
                  'l\'enssemble des achats: cluster {}.'.format(final_data.predictn()))
        elif num_com == '2':
            print('Prediction du modèle entrainé sur',
                  '2 achats: cluster {}.'.format(final_data.predict2()))
            print('Prediction du modèle entrainé sur',
                  'l\'enssemble des achats: cluster {}.'.format(final_data.predictn()))
        else:
            print('Prediction du modèle entrainé sur',
                  'l\'enssemble des achats: cluster {}.'.format(final_data.predictn()))
        lettre = input('Voulez-vous continuer ?\nTaper "X" pour quitter sinon "entrer".')
        if lettre.upper() == 'X':
            continuer = 0



if __name__ == '__main__':
    main()
