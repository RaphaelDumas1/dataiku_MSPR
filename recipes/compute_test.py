import dataiku
import pandas as pd
import openpyxl
import time
from io import BytesIO

folder_id = "Datas"
files_names = ["MSPR - Demographie.xlsx"]

def run(folder_id, files_names):

    # Get project and folder containing the Excel files
    client = dataiku.api_client()
    project = client.get_project()

    folder = dataiku.Folder(folder_id, project_key=project.project_key)
    folder_paths = [name.strip() for name in files_names.split(";") if name.strip()]

    # List the datasets in the project
    datasets_in_project = []
    for dataset in project.list_datasets():
        datasets_in_project.append(dataset.get('name'))

    for file_index, file_name in enumerate(folder_paths):
        with folder.get_download_stream(file_name) as file_handle:
            try:
                ss = openpyxl.load_workbook(BytesIO(file_handle.read()))
            except Exception:
                continue

        for sheet in ss.sheetnames:
            ss_sheet = ss[sheet]
            title = ss_sheet.title

            # Ensure the file name is in the title for the dataset (prepend if missing)
            if not file_name.split(".")[0] in title:
                title = file_name.replace("MSPR - ").split(".")[0] + "_" + sheet

            # Convert whitespace to underscores, remove unacceptable characters
            title = '_'.join(title.split())
            title = title.replace(')', '')
            title = title.replace('(', '')
            title = title.replace('/', '_')
            title = title.replace('.', '_')

            create_dataset = True
            if title in datasets_in_project:
                create_dataset = False
                project.get_dataset(title).clear()
            if create_dataset:
                dataset = project.create_dataset(
                    title,
                    'FilesInFolder',
                    params={
                        'folderSmartId': folder_id,
                        'filesSelectionRules': {
                            'mode': 'EXPLICIT_SELECT_FILES',
                            'explicitFiles': [file_name]
                        }
                    },
                    formatType='excel',
                    formatParams={"xlsx": True, "sheets": "*" + ss_sheet.title, 'parseHeaderRow': True}
                )

                with folder.get_download_stream(file_name) as file_handle:
                    df = pd.read_excel(BytesIO(file_handle.read()), sheet_name=ss_sheet.title, nrows=1000)
                    dataset.set_schema({'columns': [{'name': column, 'type': 'string'} for column, column_type in df.dtypes.items()]})

for name in files_names:
    run(folder_id, name)
