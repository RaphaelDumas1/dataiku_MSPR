from general import create_datasets_from_file_sheets
from convert import convert_columns
from delete import delete_rows_where_not_equal, delete_columns_not_in_list
from fill import fill_empty_values, fill_empty_values_with_mean



instructions = {
    "Taux_scolarisation" : [
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : "int"
            }]
        },
    ],
    "annuaire_des_ecoles_en_france" : [
        {
            "name" : delete_rows_where_not_equal,
            "args" : ["code_departement", 35.0]
        },
        {
            "name" : delete_columns_not_in_list,
            "args" : [["identifiant_de_l_etablissement", "nom_etablissement", "nombre_d_eleves", "type_etablissement"]]
        },
        {
            "name" : fill_empty_values,
            "args" : [{"type_etablissement": "Inconnu"}]
        },
        {
            "name" : fill_empty_values_with_mean,
            "args" : [["nombre_d_eleves"]]
        },
        {
            "name" : convert_columns,
            "args" : [{
                "nombre_d_eleves" : "int"
            }]
        },
    ]
}



create_datasets_from_file_sheets("MSPR - Education.xlsx", instructions)