from general import create_datasets_from_file_sheets



instructions = {
    "Legislative_2024" : [],
    "Legislative_2022" : [],
    "Legislative_2017" : [],
    "Legislative_2012" : [],
    "Legislative_2007" : [],
    "Legislative_2002" : [],
    "Legislative_1997" : [],
    "Legislative_1993" : []
}



create_datasets_from_file_sheets("MSPR - Legislative.xlsx", datasets)
