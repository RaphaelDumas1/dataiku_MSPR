# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()
project = client.get_default_project()

# Appel du runnable depuis un plugin
plugin = project.get_plugin("excel-sheet-importer")
runnables = plugin.list_runnables()

# Affiche tous les runnables
print(runnables)
