from general import create_datasets_from_file_sheets
from other import rename_columns
from convert import convert_columns
from delete import delete_rows_where_equal



instructions = {
    "Esperance_de_vie" : [
        {
            "name" : rename_columns,
            "args" : [
                {
                    "Espérance de vie sans incapacité femme" : "esperance_femme_sans_incapacite",
                    "Espérance de vie femme" : "esperance_femme",
                    "Espérance de vie sans incapacité homme" : "esperance_homme_sans_incapacite",
                    "Espérance de vie homme" : "esperance_homme"
                }
            ]

        },
        {
            "name" : delete_rows_where_equal,
            "args" : ["esperance_femme_sans_incapacite", "nd"]

        },
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : "int",
                "esperance_femme_sans_incapacite" : "decimal_1", 
                "esperance_femme" : "decimal_1",
                "esperance_homme_sans_incapacite" : "decimal_1", 
                "esperance_homme" : "decimal_1"
            }]
        }
    ]
}


create_datasets_from_file_sheets("MSPR - Sante.xlsx", instructions)