# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()
plugin = client.get_plugin("excel-sheet-importer")
desc = plugin.get_definition()

# Parcourt les runnables
if "runnables" in desc:
    for runnable in desc["runnables"]:
        print("ID          :", runnable.get("id"))
        print("Label       :", runnable.get("label"))
        print("Description :", runnable.get("description", ""))
        print("-" * 30)
else:
    print("Ce plugin ne contient pas de runnables.")