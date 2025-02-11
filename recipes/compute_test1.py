# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
Legislative_1997 = dataiku.Dataset("Legislative_1997")
Legislative_1997_df = Legislative_1997.get_dataframe()
Legislative_2007 = dataiku.Dataset("Legislative_2007")
Legislative_2007_df = Legislative_2007.get_dataframe()
Legislative_2017 = dataiku.Dataset("Legislative_2017")
Legislative_2017_df = Legislative_2017.get_dataframe()
Legislative_2002 = dataiku.Dataset("Legislative_2002")
Legislative_2002_df = Legislative_2002.get_dataframe()
Legislative_2024 = dataiku.Dataset("Legislative_2024")
Legislative_2024_df = Legislative_2024.get_dataframe()
Legislative_1993 = dataiku.Dataset("Legislative_1993")
Legislative_1993_df = Legislative_1993.get_dataframe()
Legislative_2012 = dataiku.Dataset("Legislative_2012")
Legislative_2012_df = Legislative_2012.get_dataframe()
Legislative_2022 = dataiku.Dataset("Legislative_2022")
Legislative_2022_df = Legislative_2022.get_dataframe()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

test1_df = ... # Compute a Pandas dataframe to write into test1


# Write recipe outputs
test1 = dataiku.Dataset("test1")
test1.write_with_schema(test1_df)
