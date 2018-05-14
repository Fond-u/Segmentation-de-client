"""file containing the function"""
import datetime as dt
import numpy as np

def convert_data_for_model(data_in, data_out, client):
    """fonction qui construit le format explotable pour les modeles"""
    df_client = data_in
    df_client_pos = df_client[df_client.Quantity > 0]
    df_client_neg = df_client[df_client.Quantity < 0]
    #build local
    if len(df_client.Country.unique()) == 1:
        if df_client.Country.unique() == 'United Kingdom':
            data_out.loc[client, 'local'] = 1
    else:
        print('Probleme : verifier le pays du client', client)
    #build depense totale reelle
    data_out.loc[client, 'dep_tot'] = sum(df_client.Quantity * df_client.UnitPrice)
    # build depense positive
    data_out.loc[client, 'dep_pos'] = sum(df_client_pos.Quantity * df_client_pos.UnitPrice)
    #build depense negative (annulation)
    data_out.loc[client, 'dep_neg'] = sum(df_client_neg.Quantity * df_client_neg.UnitPrice)
    #build commande
    data_out.loc[client, 'nb_com'] = len(df_client_pos.InvoiceNo.unique())
    #build commande d'annulation
    data_out.loc[client, 'nb_an'] = len(df_client_neg.InvoiceNo.unique())
    #build depense max
    data_out.loc[client, 'dep_max'] = max(df_client_pos.Quantity * df_client.UnitPrice)
    #build depense min
    data_out.loc[client, 'dep_min'] = min(df_client_pos.Quantity * df_client.UnitPrice)
    #build nombre de produit
    data_out.loc[client, 'nbpr_tot'] = (df_client_pos.shape[0])
    #build nombre de produit annulé
    data_out.loc[client, 'nbpr_ann'] = (df_client_neg.shape[0])
    #build nombre de produit different
    data_out.loc[client, 'nbpr_diff'] = (len(df_client_pos.StockCode.unique()))
    #build depence par commande
    data_out.loc[client, 'dep_com'] = (data_out.loc[client,
                                                    'dep_tot'])/(data_out.loc[client, 'nb_com'])
    #build depence par prod
    data_out.loc[client, 'dep_prod'] = (data_out.loc[client,
                                                     'dep_tot'])/ (data_out.loc[client, 'nbpr_tot'])
    #build prod par commande
    data_out.loc[client, 'nbp_com'] = (data_out.loc[client,
                                                    'nbpr_tot'])/(data_out.loc[client, 'nb_com'])
    # simulons la date de l'etude au 1er janvier 2012.
    now = dt.datetime(2012, 1, 1, 8, 0)
    now.timestamp()
    #build derniere commande
    data_out.loc[client, 'last_com'] = \
        (now.timestamp() - \
        df_client_pos.InvoiceDate.max().timestamp())/(60*60*24)
    #build freq_commande
    date_timestamp = [x.timestamp() for x in df_client_pos.InvoiceDate.value_counts().index]
    date_timestamp = sorted(date_timestamp)
    delta_t = list(date_timestamp)
    del delta_t[0]
    del date_timestamp[-1]
    delta_t = np.array(delta_t) - np.array(date_timestamp)
    if len(delta_t) != 0:
        data_out.loc[client, 'freq_com'] = (60*60*24)/(np.mean(delta_t))
    else:
        data_out.loc[client, 'freq_com'] = 0
    #build periode
    data_out.loc[client, 'peri_com'] = \
        (df_client_pos.InvoiceDate.max().timestamp() - \
        df_client_pos.InvoiceDate.min().timestamp())/(60*60*24)
    return data_out
