from utils import create_datasets_from_file_sheets, columns_to_int, pivot, complete_with_inteprolate

instructions = {
    "Administration_penitentiaire" : [
        {
             "name" : pivot,
             "args" : ["Année"]
        },
        {
             "name" : columns_to_int,
             "args" : []
        }, 
        {
             "name" : complete_with_inteprolate,
             "args" : []
        },
    ],
    "Delinquance" : [
        {
             "name" : columns_to_int,
             "args" : [{"Année", "nombre", "insee_pop", "insee_pop_millesime", "insee_log", "insee_log_millesime"}]
        }
    ]
}

create_datasets_from_file_sheets("MSPR - Securite.xlsx", instructions)
