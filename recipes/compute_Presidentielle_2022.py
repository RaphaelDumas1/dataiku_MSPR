from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Presidentielle_2022",
        "functions": []
    },
    {
        "name": "Presidentielle_2017",
        "functions": []
    },
    {
        "name": "Presidentielle_2012",
        "functions": []
    },
    {
        "name": "Presidentielle_2007",
        "functions": []
    },
    {
        "name": "Presidentielle_2002",
        "functions": []
    },
    {
        "name": "Presidentielle_1995",
        "functions": []
    }
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Presidentielle.xlsx", datasets, [])
