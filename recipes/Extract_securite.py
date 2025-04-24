from general import create_datasets_from_file_sheets
from convert import convert_columns 
from other import pivot



instructions = {
    "Administration_penitentiaire" : [
        {
             "name" : pivot,
             "args" : ["Année"]
        },
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int',
                 "Personnes prises en charge" : 'int',
                 "Mesures en cours" : 'int',
                 "Sursis1" : 'int',
                 "Travail d'interet general (tig)2" : 'int',
                 "Liberations conditionnelles3" : 'int',
                 "Autres mesures" : 'int'
             }]
        }, 
    ],
    "Delinquance" : [
        {
             "name" : convert_columns,
             "args" : [{
                 "Année" : 'int', 
                 "nombre": 'int',
                 "insee_pop": 'int',
                 "insee_pop_millesime": 'int',
                 "insee_log": 'int',
                 "insee_log_millesime": 'int'
             }]
        }
    ]
}



create_datasets_from_file_sheets("MSPR - Securite.xlsx", instructions)
