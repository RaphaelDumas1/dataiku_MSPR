from sqlalchemy import create_engine, inspect, text
import dataiku
from dataiku import Dataset
import pandas as pd

datasets_names = [
    "Esperance_de_vie",
    "Taux_scolarisation",
    # "annuaire_des_ecoles_en_france",
    "Administration_penitentiaire", 
    # "Delinquance", 
    # "Presidentielles",
    "Taux_de_chomage",
    "Repartition_des_contrats",
    "Categorie_metiers",
    "Nombre_de_salarie",
    # "Evolution_trimestrielle_emploi",
    "Logement", 
    "Type_logement",
    "Categorie_logement", 
    "Statut_occupation_logement",
    "Composition_menage",
    "Nombre_enfant",
    "Nombre_detranger",
    #"Quotient_familiale",
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
    # "Legislatives"
]

tables = [
    {
        "name": "dim_annee",
        "columns": {
            "annee": "annee"
        },
        "id": None,
        "add": {}
    },
    {
        "name": "fait_administration_penitentiaire",
        "columns": {
            "personnes prises en charge" : "nombre_pris_en_charge",
            "mesures en cours" : "nombre_en_cours",
            "sursis1" : "nombre_sursis",
            "travail d'interet general (tig)2" : "nombre_travaux_interet_general",
            "liberations conditionnelles3" : "nombre_liberations_conditionnelles",
            "autres mesures" : "autres"
        },
        "id": None,
        "add": {"dim_annee_id" : "dim_annee"}
    },
    {
        "name": "fait_menage",
        "columns": {
            "ensemble_logements": "total",
            "- hommes seuls" : "homme_seul",
            "- femmes seules" : "femme_seule",
            "- un couple avec enfant(s)" : "couple_avec_enfant",
            "- un couple sans enfant" : "couple_sans_enfant",
            "- une famille monoparentale" : "famille_monoparentale",
            "aucun enfant" : "sans_enfant",
            "1 enfant" : "un",
            "2 enfants" : "deux",
            "3 enfants" : "trois",
            "4 enfants ou plus" : "quatre_et_plus"
        },
        "id": None,
        "add": {"dim_annee_id" :"dim_annee"}
    },
    {
        "name": "fait_demographique",
        "columns": {
            "population": "total",
            "population homme" : "nombre_hommes",
            "population femme" : "nombre_femmes",
            "taux de natalite" : "taux_natalite",
            "taux de deces" : "taux_mortalite",
            "immigres" : "nombre_immigrant",
            "etrangers" : "nombre_etranger",
            "homme_total" : "esperance_homme",
            "femmes_sans_incapacite" : "esperance_femme_sans_incapacite",
            "femme_total" : "esperance_femme",
            "homme_sans_incapacite" : "esperance_homme_sans_incapacite"
        },
        "id": None,
        "add": {"dim_annee_id": "dim_annee"}
    },
    {
        "name": "fait_economie",
        "columns": {
            "produit interieur brut (pib)": "pib_total",
            "importations de biens et de services" : "taux_importation",
            "depense de consommation finale" : "taux_consommation",
            "depense de consommation finale dont menages" : "taux_consommation_menages",
            "depense de consommation finale dont administrations publiques" : "taux_consommation_gouvernement",
            "formation brute de capital fixe" : "taux_investissement",
            "formation brute de capital fixe dont societes et entreprises individuelles non financieres" : "taux_investissement_entreprises",
            "formation brute de capital fixe dont administrations publiques" : "taux_investissement_gouvernement",
            "formation brute de capital fixe dont menages hors entrepreneurs individuels" : "taux_investissement_menages",
            "exportations de biens et de services" : "taux_exportations",
            "demande interieure hors stocks" : "taux_demande_interieure",
            "impot" : "moyenne_impot",
            "taux d'inflation" : "taux_inflation"
        },
        "id": None,
        "add": {"dim_annee_id" : "dim_annee"}
    },
    {
        "name": "fait_travail",
        "columns": {
            "salaire net": "salaire",
            "agriculteurs exploitants" : "nombre_agriculteurs",
            "artisans, commercants, chefs entreprise" : "nombre_artisans",
            "cadres et professions intellectuelles superieures" : "nombre_cadres",
            "professions intermediaires" : "nombre_professions_intermediaires",
            "employes" : "nombre_employes",
            "ouvriers" : "nombre_ouvriers",
            "retraites" : "nombre_retraites",
            "autres personnes sans activite professionnelle" : "nombre_sans_emploi",
            "cdi" : "nombre_cdi",
            "cdd" : "nombre_cdd",
            "taux" : "taux_chomage"
        },
        "id": None,
        "add": {"dim_annee_id" : "dim_annee"}
    },
    {
        "name": "fait_logement",
        "columns": {
            "nombre de logements": "total",
            "maisons" : "nombre_maisons",
            "appartements" : "nombre_appartements",
            "autres logements" : "nombre_autres",
            "proprietaires" : "nombre_proprietaires",
            "locataires" : "nombre_locataires",
            "- dont locataires d'un logement hlm loue vide" : "nombre_hlm",
            "loges gratuitement" : "nombre_logements_gratuit",
            "residences principales" : "nombre_residences_principales",
            "resid. secondaires et log. occasionnels" : "nombre_residences_secondaires",
            "logements vacants" : "nombre_logements_vacants"
        },
        "id": None,
        "add": {"dim_annee_id" : "dim_annee"} 
    }
]

def buildInsertQuery(table_name, row=None, mapping={}, columns_to_add={}, returning=None):
    print("hop", table_name)

    
    
    values_dict = {}
    if row is not None:
        # print(row.index, mapping)
        values_dict = {sql_col: row[df_col] for df_col, sql_col in mapping.items()}
        
    values_dict.update(columns_to_add)
    
    columns_str = ", ".join(values_dict.keys())
    placeholders = ", ".join([f":{col}" for col in values_dict.keys()])
    
    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
    """
    
    if returning:
        query += f"\nRETURNING {returning}"

    return {
        "query": text(query),
        "params": values_dict,
        "returning": returning
    }

def executeQueries(conn, queries):
    result_id = None

    try:
        for q in queries:
            query = q["query"]
            params = q["params"]
            returning = q["returning"]
            
            result = None
            if params is not None :
                result = conn.execute(query, params)
            else :
                conn.execute(query)
                
            conn.commit()

            if returning:
                result_id = result.scalar()
                
    except Exception as e:
        print("except", query, e, params, returning)
        conn.rollback()
    print("good", query, params, returning)
    return result_id
    
engine = create_engine('postgresql://postgres:test@host.docker.internal:5432/MSPR')

delinquance_ids = {}
age_ids = {}
election_type_ids = {}
etiquette_politique_ids = {}
final_df = None

for ds_name in datasets_names:
    ds = dataiku.Dataset(ds_name)
    df = ds.get_dataframe()
    
    if final_df is None:
        final_df = df  # première itération, on initialise
    else:
        final_df = pd.merge(final_df, df, on="annee", how="outer")  # merge avec le reste

with engine.connect() as conn:
    
    # TABLE dim_age
    
    queries = [
        {"query" : text(f"DELETE FROM dim_age;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_delinquance;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_type_election;"), "params" : None, "returning" : None}, 
        {"query" : text(f"DELETE FROM dim_etiquette_politique;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM dim_delinquance_has_fait_demographique;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM fait_demographique_has_dim_age;"), "params" : None, "returning" : None},
        {"query" : text(f"DELETE FROM fait_participation;"), "params" : None, "returning" : None}
    ]

    ds_repartition_age = dataiku.Dataset("Repartition_age")
    ds_taux_scolarisation = dataiku.Dataset("Taux_scolarisation")
    df_repartition_age = ds_repartition_age.get_dataframe()
    df_taux_scolarisation = ds_taux_scolarisation.get_dataframe()
    labels_repartition_age = [col for col in df_repartition_age.columns if col != "annee"]
    labels_taux_scolarisation = [col for col in df_taux_scolarisation.columns if col != "annee"]
    labels = labels_repartition_age + labels_taux_scolarisation

    for label in labels: 
        queries.append(buildInsertQuery("dim_age", None, {}, {"repartition_age" : label}, 'id'))
        age_ids.update({label : executeQueries(conn, queries)})
        queries = []
    
    # TABLE dim_type_election
    
    type_elections = ["legislative", "presidentielle"]
    for election in type_elections: 
        queries.append(buildInsertQuery("dim_type_election", None, {}, {"nom_election" : election}, 'id'))
        election_type_ids.update({election : executeQueries(conn, queries)})
        queries = []
    
    # TABLE dim_etiquette_politique
    
    political_labels = ["Blank", "Far_Right", "Right", "Center", "Left", "Far_Left", "Green"]
    for label in political_labels: 
        queries.append(buildInsertQuery("dim_etiquette_politique", None, {}, {"etiquette_politique" : label}, 'id'))
        etiquette_politique_ids.update({label : executeQueries(conn, queries)})
        queries = []
    
    # Main iteration
    
    for index, row in final_df.iterrows():
        for table in tables:
            table_name = table["name"]
            columns = table["columns"]
            add = table["add"]
            
            # Delete old datas
            if(row["annee"] == 2006): 
                queries.append({"query" : text(f"DELETE FROM {table_name};"), "params" : None, "returning" : None},)
            
            # Add new columns
            to_add = {}
            for key, value in add.items():
                for ref_table in tables:
                    if value == ref_table["name"] and ref_table["id"] is not None:
                        value = ref_table["id"] 
                
                to_add.update({key : value})
                    
            queries.append(buildInsertQuery(table_name, row, columns, to_add, 'id'))        
            table["id"] = executeQueries(conn, queries)
            queries = []
            
            
            if(table_name == "fait_demographique"):
                ds_delinquance = dataiku.Dataset("Delinquance")
                df_delinquance = ds_delinquance.get_dataframe()               
                df_delinquance_filtered = df_delinquance[df_delinquance['annee'] == row["annee"]]
                
                for i, r in df_delinquance_filtered.iterrows():
                    
                    # TABLE dim_delinquance
                    
                    # If delinquance doesnt exist
                    if r["indicateur"] not in delinquance_ids:
                        
                        delinquance_columns = {
                            "unite_de_compte" : "type_delinquance",
                            "indicateur" : "indicateur",
                        }

                        queries.append(buildInsertQuery("dim_delinquance", r, delinquance_columns, {}, 'id'))
                        delinquance_ids.update({r["indicateur"] : executeQueries(conn, queries)})
                        queries = []
                    
                    # TABLE dim_delinquance_has_fait_demograhique
                    
                    delinquance_demographique_mapping = {
                        "dim_delinquance_id" : delinquance_ids[r["indicateur"]],
                        "fait_demographique_id" : table["id"],   
                    }
                    
                    queries.append(buildInsertQuery("dim_delinquance_has_fait_demographique", r, {"nombre" : "total"}, delinquance_demographique_mapping))
                    executeQueries(conn, queries)    
                    queries = []
                
                # TABLE fait_demographique_has_dim_age
                
                df_repartition_age_filtered = df_repartition_age[df_repartition_age['annee'] == row["annee"]]
                row_unique = df_repartition_age_filtered.iloc[0]
                
                for col in row_unique.index:
                    if col != "annee":
                        col_mapping = {
                            "dim_age_id" : age_ids[col],
                            "fait_demographique_id" : table["id"],
                            "total" : row_unique[col]
                        }
                        queries.append(buildInsertQuery("fait_demographique_has_dim_age", row, {}, col_mapping))
                executeQueries(conn, queries)
                queries = []
                
            # TABLE fait_scolarisation   
                
            df_taux_scolarisation_filtered = df_taux_scolarisation[df_taux_scolarisation['annee'] == row["annee"]]
            row_unique = df_taux_scolarisation_filtered.iloc[0]
            
            year_id = 0
            for ref_table in tables:
                if ref_table["name"] == "dim_annee" and ref_table["id"] is not None:
                    year_id = ref_table["id"] 
                    
            for col in row_unique.index:
                if col != "annee":
                    col_mapping = {
                        "dim_age_id" : age_ids[col],
                        "dim_annee_id" : year_id,
                        "total" : row_unique[col]
                    }
                    queries.append(buildInsertQuery("fait_scolarisation", row, {}, col_mapping))
            executeQueries(conn, queries)
            queries = []
            
            # TABLE fait_participation
            
            ds_legislative = dataiku.Dataset("Legislatives")
            df_legislative = ds_legislative.get_dataframe()               
            df_legislative_filtered = df_legislative[df_legislative['année'] == row["annee"]]
            
            if len(df_legislative_filtered) > 0:
                for ii, rr in df_legislative_filtered.iterrows():
                    print("hip", rr["couleur"], etiquette_politique_ids, delinquance_ids, age_ids, election_type_ids, year_id)
                    col_mapping = {
                        "dim_annee_id" : year_id,
                        "dim_type_election_id" : election_type_ids["legislative"],
                        "dim_etiquette_politique_id" : etiquette_politique_ids[rr["couleur"]],
                    }
                    queries.append(buildInsertQuery("fait_participation", rr, {"voix": "total"}, col_mapping))
                    queries = []
                        
                        
            ds_presidentielle = dataiku.Dataset("Presidentielles")
            df_presidentielle = ds_presidentielle.get_dataframe()               
            df_presidentielle_filtered = df_presidentielle[df_presidentielle['année'] == row["annee"]]

            if len(df_presidentielle_filtered) > 0:
                for ii, rr in df_presidentielle_filtered.iterrows():
                    col_mapping = {
                        "dim_annee_id" : year_id,
                        "dim_type_election_id" : election_type_ids["presidentielle"],
                        "dim_etiquette_politique_id" : etiquette_politique_ids[rr["couleur"]],
                    }
                    queries.append(buildInsertQuery("fait_participation", rr, {"voix": "total"}, col_mapping))
                    queries = []