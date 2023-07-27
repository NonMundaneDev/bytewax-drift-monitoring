# from app.db import retrieve_Data,data_from_s3
import pandas as pd
import logging

from evidently import ColumnMapping

from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *

from evidently.calculations.stattests import StatTest
from evidently.test_suite import TestSuite
from evidently.tests import *





# def load_reference_data():
#     """
#     Loads the reference data from the "training_data.csv" file.

#     Returns:
#         pd.DataFrame: The reference data as a DataFrame.
#     """
#     reference_data = pd.read_csv("app/data/training_data.csv")
#     return reference_data


# def retrieve_all_data(number_of_row: int):
#     """
#     Retrieves both the reference data and the current data for data drift comparison.

#     Args:
#         number_of_row (int): The number of rows to retrieve for the current data.

#     Returns:
#         tuple: A tuple containing the reference data DataFrame and the current data DataFrame.
#     """
#     reference_data = load_reference_data()
#     current_data = retrieve_Data(number_of_row=number_of_row)
#     del reference_data['Unnamed: 0']  # Remove the "Unnamed: 0" column from the reference data
#     return reference_data, current_data


def generate_dashboard(ref_data) -> str:
    dashboard_name = "app/static/file.html"

    reference_data_label, reference_dataset= ref_data
    

    numerical_features = ["diarrhea", "itchy_nose", "itchy_eyes", "itchy_mouth", "itchy_inner_ear", "redness_of_eyes"]
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = numerical_features
    report = Report(metrics=[
        DataDriftPreset(stattest='ks'),
        TargetDriftPreset()
        ])
    # report = TestSuite(tests=[
    # TestShareOfDriftedColumns(stattest='ks'),
    # ])
    current_data =pd.read_csv('app/data/training_data.csv')
    df_reference_dataset =pd.DataFrame(reference_dataset)
    df_reference_dataset_clean = df_reference_dataset.apply(pd.to_numeric, errors='ignore')
    print(len(df_reference_dataset_clean))
    # reference_data, current_data = retrieve_all_data(number_of_row)
    report.run(reference_data=df_reference_dataset_clean.drop(columns='label'), current_data=current_data.drop(columns='label'))

    report.save_html(dashboard_name)
    # data_from_s3(method="post")
    
    logging.info(f"Dashboard saved to {dashboard_name}")
    return ('result', dashboard_name)



