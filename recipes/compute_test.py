# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()

# Lister tous les plugins installés
plugins = client.list_plugins()

for plugin in plugins:
    print(f"Plugin ID: {plugin['id']}, Plugin Label: {plugin['label']}")