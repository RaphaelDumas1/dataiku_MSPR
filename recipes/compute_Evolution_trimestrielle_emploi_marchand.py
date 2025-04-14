# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
Datas = dataiku.Folder("aPmnwurD")
Datas_info = Datas.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

Evolution_trimestrielle_emploi_marchand_df = ... # Compute a Pandas dataframe to write into Evolution_trimestrielle_emploi_marchand
Taux_de_chomage_df = ... # Compute a Pandas dataframe to write into Taux_de_chomage
Repartition_des_contrats_df = ... # Compute a Pandas dataframe to write into Repartition_des_contrats
Categorie_metiers_df = ... # Compute a Pandas dataframe to write into Categorie_metiers


# Write recipe outputs
Evolution_trimestrielle_emploi_marchand = dataiku.Dataset("Evolution_trimestrielle_emploi_marchand")
Evolution_trimestrielle_emploi_marchand.write_with_schema(Evolution_trimestrielle_emploi_marchand_df)
Taux_de_chomage = dataiku.Dataset("Taux_de_chomage")
Taux_de_chomage.write_with_schema(Taux_de_chomage_df)
Repartition_des_contrats = dataiku.Dataset("Repartition_des_contrats")
Repartition_des_contrats.write_with_schema(Repartition_des_contrats_df)
Categorie_metiers = dataiku.Dataset("Categorie_metiers")
Categorie_metiers.write_with_schema(Categorie_metiers_df)
