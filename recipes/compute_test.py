# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()
plugin = client.get_plugin("excel-sheet-importer")
runnables = plugin.list_runnables()
for r in runnables:
    print("Runnable ID:", r["id"])
    print("Label:", r["label"])
    print("Description:", r.get("description", ""))
    print("---")