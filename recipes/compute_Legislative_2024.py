from utils import create_datasets_from_file_sheets

datasets = [
    {
        "name": "Legislative_2024",
        "functions": []
    },
    {
        "name": "Legislative_2022",
        "functions": []
    },
    {
        "name": "Legislative_2017",
        "functions": []
    },
    {
        "name": "Legislative_2012",
        "functions": []
    },
    {
        "name": "Legislative_2007",
        "functions": []
    },
    {
        "name": "Legislative_2002",
        "functions": []
    },
    {
        "name": "Legislative_1997",
        "functions": []
    },
    {
        "name": "Legislative_1993",
        "functions": []
    },
]

create_datasets_from_file_sheets("MSPR", "Datas", "MSPR - Legislative.xlsx", datasets, [])
