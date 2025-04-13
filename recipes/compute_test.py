# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()
plugin = client.get_plugin("excel-sheet-importer")
print(plugin.list_usages())