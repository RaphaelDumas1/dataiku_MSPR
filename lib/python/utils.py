import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO

def run(project_id, folder_id, file_name, exclude_sheets):
    client = dataiku.api_client()
    project = client.get_project(project_id)

    folder = dataiku.Folder(folder_id, project_key=project.project_key)

    datasets_in_project = []
    for dataset in project.list_datasets():
        datasets_in_project.append(dataset.get('name'))

    with folder.get_download_stream(file_name) as file_handle:
        try:
            ss = openpyxl.load_workbook(BytesIO(file_handle.read()))
        except Exception:
            print("tz")

    for sheet in ss.sheetnames:
        if sheet in exclude_sheets:
            continue

        ss_sheet = ss[sheet]
        title = ss_sheet.title
        title = '_'.join(title.split()).replace(')', '').replace('(', '').replace('/', '_').replace('.', '_')
        
        data = list(ss_sheet.values)
        headers = data[0]
        rows = data[1:]
        # Garder uniquement les colonnes dont l'en-tête n'est pas None ou vide
        valid_columns = [(i, h) for i, h in enumerate(headers) if h is not None and str(h).strip() != '']

        # Extraire les colonnes valides pour le DataFrame
        filtered_headers = [h for _, h in valid_columns]
        filtered_rows = [[row[i] for i, _ in valid_columns] for row in rows]

        # Construire le DataFrame propre
        df = pd.DataFrame(filtered_rows, columns=filtered_headers)
        test = dataiku.Dataset(title)
        test.write_with_schema(df)