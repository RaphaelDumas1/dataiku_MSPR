# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

client = dataiku.api_client()
project = client.get_project("MSPR")

plugin = project.get_plugin("excel-sheet-importer")