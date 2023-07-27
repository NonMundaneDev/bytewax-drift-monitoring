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


current_data =pd.read_csv('app/data/training_data.csv')

def generate_dashboard(ref_data) -> str:
    """
    Generates a data drift dashboard of the Kolmogorov-Smirnov (KS) test.

    Args:
        ref_data (list): list of data in a window
    Returns:
        str: The path to the generated dashboard file.
    """
    dashboard_name = "app/static/file.html"

    ref_label, reference_dataset= ref_data
    
    report = Report(metrics=[
        DataDriftPreset(drift_share=0.05,stattest='ks',stattest_threshold=0.05),
        TargetDriftPreset()
        ])
   
    df_reference_dataset =pd.DataFrame(reference_dataset)
    df_reference_dataset_clean = df_reference_dataset.apply(pd.to_numeric, errors='ignore')
    report.run(reference_data=df_reference_dataset_clean.drop(columns='label'), current_data=current_data.drop(columns='label'))

    report.save_html(dashboard_name)
    
    logging.info(f"Dashboard saved to {dashboard_name}")
    return ('result', dashboard_name)


