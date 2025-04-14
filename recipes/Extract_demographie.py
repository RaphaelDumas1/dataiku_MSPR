from utils import create_datasets_from_file_sheets, pivot_years, copy_years_range, columns_to_int

datasets = [
    {
        "name": "Nombre_detranger",
        "functions": []
    },
    {
        "name": "Quotient_familiale",
        "functions": []
    },
    {
        "name": "Taux_de_natalite",
        "functions": []
    },
    {
        "name": "Taux_de_mortalite",
        "functions": []
    },
    {
        "name": "Population",
        "functions": []
    },
    {
        "name": "Repartition_age",
        "functions": []
    },
    {
        "name": "Repartition_sexe",
        "functions": []
    },
    {
        "name": "Nombre_dimmigre",
        "functions": []
    },
    {
        "name": "Taux_de_pauvrete",
        "functions": []
    },
    {
        "name": "Evolution_population",
        "functions": [
            {
                 "name" : pivot_years,
                 "args" : None
            },
            {
                 "name" : copy_years_range,
                 "args" : None
            },
        ]
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
