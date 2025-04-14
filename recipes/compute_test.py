from utils import create_datasets_from_file_sheets

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
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Demographie.xlsx", datasets, [])
