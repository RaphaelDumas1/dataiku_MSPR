from general import create_datasets_from_file_sheets
from other import rename_columns
from convert import convert_columns
from delete import delete_rows_where_equal



instruction = {
    "Esperance_de_vie" : [
        {
            "name" : rename_columns,
            "args" : [
                {
                    "Espérance de vie sans incapacité femme" : "femmes_sans_incapacite",
                    "Espérance de vie femme" : "femme_total",
                    "Espérance de vie sans incapacité homme" : "homme_sans_incapacite",
                    "Espérance de vie homme" : "homme_total"
                }
            ]

        },
        {
            "name" : delete_rows_where_equal,
            "args" : ["femmes_sans_incapacite", "nd"]

        },
        {
            "name" : convert_columns,
            "args" : [{
                "Année" : 'int',
                "femmes_sans_incapacite" : 'decimal_1', 
                "femme_total": 'decimal_1',
                "homme_sans_incapacite": 'decimal_1', 
                "homme_total" : 'decimal_1'
            }]
        }
    ]
}


create_datasets_from_file_sheets("MSPR - Sante.xlsx", instructions)