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
                 "personnes prises en charge" : 'int',
                 "mesures en cours" : 'int',
                 "sursis1" : 'int',
                 "travail d'interet general (tig)2" : 'int',
                 "liberations conditionnelles3" : 'int',
                 "autres mesures" : 'int'
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
