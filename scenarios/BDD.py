from sqlalchemy import create_engine, text
import pandas as pd
from database import execute_queries, insert_in_table_column_from_list, get_column_names_from_table, build_execute_insert_query
from utils import get_dataframe_from_dataset

#
# PostgreSQL environnement
#

USER = "postgres"
PASSWORD = "test"
HOST = "host.docker.internal"
PORT = "5432"
DB = "MSPR"

#
# Datas
#

datasets_to_merge = [
    "Esperance_de_vie",
    "Taux_scolarisation",
    "Administration_penitentiaire", 
    "Taux_de_chomage",
    "Repartition_des_contrats",
    "Categorie_metiers",
    "Nombre_de_salarie",
    "Logement", 
    "Type_logement",
    "Categorie_logement", 
    "Statut_occupation_logement",
    "Composition_menage",
    "Nombre_enfant",
    "Nombre_detranger",
    "Taux_de_natalite",
    "Taux_de_mortalite",
    "Population",
    "Repartition_age",
    "Repartition_sexe",
    "Nombre_dimmigre",
    "Taux_de_pauvrete",
    "Evolution_population",
    "Pib",
    "Inflation",
    "Salaire_moyen",
    "Impot_moyen", 
]


tables_to_insert = {
    "dim_annee" : {},
    "fait_administration_penitentiaire" : {},
    "fait_menage" : {
        "ensemble_menages": "total"
    },
    "fait_demographique" : {
        "population": "total"
    },
    "fait_economie" : {},
    "fait_travail" : {},
    "fait_logement" : {
        "nombre de logements": "total"
    }
}


ids = {
    "delinquance" : {},
    "age" : {},
    "type_election" : {
        "legislative" : None,
        "presidentielle" : None
    },
    "etiquette_politique" : {
        "Blank" : None, 
        "Far_Right" : None,
        "Right" : None, 
        "Center" : None, 
        "Left" : None, 
        "Far_Left" : None, 
        "Green" : None
    }
}


datasets_to_dataframes = {
    "Repartition_age" : None,
    "Taux_scolarisation" : None,
    "Delinquance" : None,
    "Legislatives" : None,
    "Presidentielles" : None
}

#
# Logic
#

# Initiate DB client
db = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")


# Merge all datasets in one based on year column
final_df = None
for dataset in datasets_to_merge:
    df = get_dataframe_from_dataset(dataset)
    
    if final_df is None:
        final_df = df
    else:
        final_df = pd.merge(final_df, df, on="annee", how="outer")

        
# Load other needed dataframes
for key in datasets_to_dataframes.keys():
    datasets_to_dataframes[key] = get_dataframe_from_dataset(key)


with db.connect() as conn:
    
    # Delete existing datas not present in merged dataframe
    delete_queries = [
        {"query" : text(f"DELETE FROM dim_age;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_delinquance;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_type_election;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_etiquette_politique;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM dim_delinquance_has_fait_demographique;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM fait_demographique_has_dim_age;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM fait_participation;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM fait_scolarisation;"), "params" : None, "returning" : None}
    ]
    execute_queries(conn, delete_queries)
    
    # TABLE dim_age
    
    ids["age"] = insert_in_table_column_from_list(conn, "dim_age", "repartition_age", ([col for col in datasets_to_dataframes["Repartition_age"].columns if col != "annee"]) + ([col for col in datasets_to_dataframes["Taux_scolarisation"] if col != "annee"]), "id")
    
    # TABLE dim_type_election
    
    ids["type_election"] = insert_in_table_column_from_list(conn, "dim_type_election", "nom_election", ids["type_election"].keys(), "id")
    
    # TABLE dim_etiquette_politique
    
    ids["etiquette_politique"] = insert_in_table_column_from_list(conn, "dim_etiquette_politique", "etiquette_politique", ids["etiquette_politique"].keys(), "id")
    
    # Iterate over rows (years) 
    for index, row in final_df.iterrows(): 
        year_id = None
        fait_demographique_id = None
        current_year_dataframes = {}

        # Filter dataframes for current row year
        for key, value in datasets_to_dataframes.items():
            current_year_dataframes.update({key : value[value['annee'] == row["annee"]]})
        
        # Iterate over tables
        for table_name, mapping in tables_to_insert.items():
            # Delete old datas

            if(index == 0): 
                execute_queries(conn, [{"query" : text(f"DELETE FROM {table_name};"), "params" : None, "returning" : None}])

            # MAIN TABLES
            
            table_column_names = get_column_names_from_table(conn, table_name)
            ds_to_db_mapping = {name: name for name in table_column_names if name not in ["id", "dim_annee_id"]} | mapping 
            
            id = build_execute_insert_query(conn, table_name, row, ds_to_db_mapping, 
                {"dim_annee_id" : year_id} if table_name != "dim_annee" else {}, 
                None if table_name not in ["dim_annee", "fait_demographique"] else 'id'
            )
            
            if table_name == "dim_annee":
                year_id = id             

            # OTHER TABLES
            
            if(table_name == "fait_demographique"):
                fait_demographique_id = id
                
                for _, r in current_year_dataframes["Delinquance"].iterrows():
                    
                    # TABLE dim_delinquance
                    
                    # If delinquance doesnt exist yet
                    if r["indicateur"] not in ids["delinquance"].keys():
                        ids["delinquance"].update({r["indicateur"] : build_execute_insert_query(conn, "dim_delinquance", r, {
                            "unite_de_compte" : "type_delinquance", 
                            "indicateur" : "indicateur"}, {}, 'id')
                        })
                    
                    # TABLE dim_delinquance_has_fait_demograhique

                    build_execute_insert_query(conn, "dim_delinquance_has_fait_demographique", r, {"nombre" : "total"}, {
                        "dim_delinquance_id" : ids["delinquance"][r["indicateur"]], 
                        "fait_demographique_id" : fait_demographique_id
                    })
                
                # TABLE fait_demographique_has_dim_age
                
                first_unique_row = current_year_dataframes["Repartition_age"].iloc[0]    
                for col in first_unique_row.index:
                    if col != "annee":
                        build_execute_insert_query(conn, "fait_demographique_has_dim_age", row, {}, {
                            "dim_age_id" : ids["age"][col],
                            "fait_demographique_id" : fait_demographique_id,
                            "total" : first_unique_row[col]
                        })
                
        # TABLE fait_scolarisation   

        first_unique_row = current_year_dataframes["Taux_scolarisation"].iloc[0]                 
        for col in first_unique_row.index:
            if col != "annee":
                build_execute_insert_query(conn, "fait_scolarisation", row, {}, {"dim_age_id" : ids["age"][col], "dim_annee_id" : year_id, "total" : first_unique_row[col]})

        # TABLE fait_participation

        if len(current_year_dataframes["Legislatives"]) > 0:
            for _, r in current_year_dataframes["Legislatives"].iterrows():
                build_execute_insert_query(conn, "fait_participation", r, {"voix": "total"}, {
                    "dim_annee_id" : year_id, 
                    "dim_type_election_id" : ids["type_election"]["legislative"],
                    "dim_etiquette_politique_id" : ids["etiquette_politique"][r["couleur"]]
                })


        if len(current_year_dataframes["Presidentielles"]) > 0:
            for _, r in current_year_dataframes["Presidentielles"].iterrows():
                build_execute_insert_query(conn, "fait_participation", r, {"voix": "total"}, {
                    "dim_annee_id" : year_id, 
                    "dim_type_election_id" : ids["type_election"]["presidentielle"], 
                    "dim_etiquette_politique_id" : ids["etiquette_politique"][r["couleur"]]
                })