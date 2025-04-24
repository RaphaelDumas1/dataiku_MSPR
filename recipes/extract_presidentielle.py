from general import create_datasets_from_file_sheets



instructions = {
    "Presidentielle_2022" : [],
    "Presidentielle_2017" : [],
    "Presidentielle_2012" : [],
    "Presidentielle_2007" : [],
    "Presidentielle_2002" : [],
    "Presidentielle_1995" : []
}



create_datasets_from_file_sheets("MSPR - Presidentielle.xlsx", instructions)