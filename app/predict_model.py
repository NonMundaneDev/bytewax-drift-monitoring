# from joblib import load

import pickle
from joblib import dump, load 
import pandas as pd
import numpy as np



# #load the model
# pipeline_loaded = load('./app/model/pipeline_model.joblib')

# Create an inference function
# def predict(text):
#     # print(pipeline_loaded.predict([text]))
#     return str(pipeline_loaded.predict([text]))


loaded_model = load("app/model/rdfmodel.joblib.dat")

def predict_d(data):
    res = loaded_model.predict_proba([data])
    result = dict(zip(loaded_model.classes_, [round(x) for x in res[0]]))
    # Retrieve key-value pairs where value > 0.7
    filtered_dict = {str(key): value for key, value in result.items() if value > 0.7}
    return filtered_dict