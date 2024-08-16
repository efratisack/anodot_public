#from nltk.metrics import jaccard_distance
import pandas as pd
from tqdm import tqdm
import ast
import os
from datetime import date
import time
from main import run_main
import numpy as np
from globals import data_path, dataset_file_name, advanced_logic

num_of_tests = 1
wanted_num_of_queries = 100
specific_queries_to_run = [] # [19,20,21,22,23,24,25] # [57,66,69,77,79,87]


# =============================================================================
# loading queries
#synthetic_data_path = r"synthetic_data\\"
#file_name = 'ambiguous queries test.csv' # 'ambiguous queries test.csv' #'synthetic_queries.csv'

dataset_file_path = os.path.join(data_path, dataset_file_name)

# validation_set_path = synthetic_data_path + file_name
df_temp = pd.read_csv(dataset_file_path)
df_temp = df_temp.drop(columns=['num'])
df_temp['dimensions'] = df_temp['dimensions'].apply(ast.literal_eval)
df_temp['__index'] = df_temp.index
num_of_queries = min(len(df_temp), wanted_num_of_queries)

if len(specific_queries_to_run) > 0:
    df_temp = df_temp.loc[specific_queries_to_run]
    queries_to_run = specific_queries_to_run
else:
    queries_to_run = list(range(0, num_of_queries)) # [57,66,69,77,79,87]

df_temp = df_temp.loc[queries_to_run]

# =============================================================================
# shuffling and cutting queries
df = df_temp.sample(frac=1).reset_index(drop=True)
num_of_queries = min(len(df_temp), wanted_num_of_queries)
user_queries = df['Query'].to_list()

# =============================================================================
# run over all queries
def calculate_jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def to_list(value):
    if not isinstance(value, list):
        return [value]
    return value

def calculate_accuracy_row(row):
    true_label_dict = row['true_label']

    predictions = [row[f'prediction {j}'] for j in range(8) if
                   f'prediction {j}' in row and isinstance(row[f'prediction {j}'], dict)]

    accuracies = []

    for prediction_dict in predictions:

        # Calculate accuracy for each parameter
        param_accuracies = []

        for key in true_label_dict:
            if key != 'alert_dimensions':
                param_accuracies.append(true_label_dict[key] == prediction_dict.get(key, None))
            else:
                param_accuracies.append(
                    calculate_jaccard_similarity(true_label_dict[key], prediction_dict.get(key, [])))

        accuracies.append(np.prod(param_accuracies))

    return max(accuracies) if accuracies else 0


start_time = time.time()
for i in range(num_of_tests):
    #variables for results collecting
    id_pred = []
    type_pred = []
    direction_pred = []
    measure_pred = []
    measure_explanation = []
    dimensions_pred = []
    dimensions_explanation = []
    ambiguity_id = []
    ambiguity_id_score = []
    ambiguity_measure = []
    ambiguity_measure_score = []
    ambiguity_dimensions = []
    ambiguity_dimensions_score = []
    predictions_count = []
    prediction_columns = [[] for _ in range(8)] # maximum possible number of predicted parameters (2 IDs, 2 measures for each ID, 2 dimension set for every measure)
    pred_results = {}

    #run all user queries in validation dataset
    for user_query in tqdm(user_queries):
        try:
            search_expression = run_main(user_query, interactive_app=False)
            #print(search_expression)

        except Exception as e:
            print(f"An error occurred: {user_query}")
            search_expression = [{
                'ds_ID': 'NA',
                'alert_type': 'NA',
                'alert_direction': 'NA',
                'alert_measure': ['NA'],
                'measure_reasoning': 'NA',
                'alert_dimensions': ['NA'],
                'dimensions_reasoning': 'NA',
                'alert_title': 'NA',
                'ambiguity_id': 'NA',
                'ambiguity_id_score': 'NA',
                'ambiguity_measure': 'NA',
                'ambiguity_measure_score': ['NA'],
                'ambiguity_dimensions': 'NA',
                'ambiguity_dimensions_score': ['NA']
            }
            ]

        # collecting retrieved values
        id_pred.append([item['ds_ID'] for item in search_expression])
        type_pred.append([item['alert_type'] for item in search_expression])
        direction_pred.append([item['alert_direction'] for item in search_expression])
        measure_pred.append([item['alert_measure'] for item in search_expression])
        dimensions_pred.append([item['alert_dimensions'] for item in search_expression])
        if advanced_logic:
            measure_explanation.append([item['measure_reasoning'] for item in search_expression])
            dimensions_explanation.append([item['dimensions_reasoning'] for item in search_expression])
            ambiguity_id.append([item['ambiguity_id'] for item in search_expression])
            ambiguity_id_score.append([item['ambiguity_id_score'] for item in search_expression])
            ambiguity_measure.append([item['ambiguity_measure'] for item in search_expression])
            ambiguity_measure_score.append([item['ambiguity_measure_score'] for item in search_expression])
            ambiguity_dimensions.append([item['ambiguity_dimensions'] for item in search_expression])
            ambiguity_dimensions_score.append([item['ambiguity_dimensions_score'] for item in search_expression])

        parameters_list_to_columns = []
        for predicted_parameter_set in search_expression:
            ds_id = predicted_parameter_set['ds_ID']
            alert_type = predicted_parameter_set['alert_type']
            alert_direction = predicted_parameter_set['alert_direction']
            alert_measures = predicted_parameter_set['alert_measure']
            alert_dimensions_list = predicted_parameter_set['alert_dimensions']

            if isinstance(alert_dimensions_list[0], list):
                # dimensions is a list of lists
                for alert_measure in alert_measures:
                    for alert_dimensions in alert_dimensions_list:
                        parameters = {
                            'ds_ID': ds_id,
                            'alert_type': alert_type,
                            'alert_direction': alert_direction,
                            'alert_measure': alert_measure,
                            'alert_dimensions': alert_dimensions
                            }
                        parameters_list_to_columns.append(parameters)
            else:
                # It's a single list
                for alert_measure in to_list(alert_measures):
                    parameters = {
                        'ds_ID': ds_id,
                        'alert_type': alert_type,
                        'alert_direction': alert_direction,
                        'alert_measure': alert_measure,
                        'alert_dimensions': alert_dimensions_list
                    }
                    parameters_list_to_columns.append(parameters)

        #print(parameters_list_to_columns)
        for j in range(len(parameters_list_to_columns)):
            prediction_columns[j].append(parameters_list_to_columns[j])

        # fill empty prediction columns
        for j in range(len(parameters_list_to_columns), len(prediction_columns)):
            prediction_columns[j].append(None)

        # print(parameters_list_to_columns, len(parameters_list_to_columns))

        predictions_count.append(len(parameters_list_to_columns))

    #saving values in dataframe columns
    df[f'id_pred'] = id_pred
    df[f'type_pred'] = type_pred
    df[f'direction_pred'] = direction_pred
    df[f'dimensions_pred'] = dimensions_pred
    df[f'measure_pred'] = measure_pred
    if advanced_logic:
        df[f'ambiguity_id_pred'] = ambiguity_id
        df[f'ambiguity_id_accuracy'] = df.apply(lambda row: row[f'ambiguity_id_pred'][0] == row['ambiguity_id'], axis=1)
        df[f'ambiguity_id_score'] = ambiguity_id_score
        df[f'ambiguity_measure_pred'] = ambiguity_measure
        df[f'ambiguity_measure_accuracy'] = df.apply(lambda row: row[f'ambiguity_measure_pred'][0] == row['ambiguity_measure'], axis=1)
        df[f'ambiguity_measure_score'] = ambiguity_measure_score
        df[f'ambiguity_dimensions_pred'] = ambiguity_dimensions
        df[f'ambiguity_dimensions_accuracy'] = df.apply(lambda row: row[f'ambiguity_dimensions_pred'][0] == row['ambiguity_dimensions'], axis=1)
        df[f'ambiguity_dimensions_score'] = ambiguity_dimensions_score
        df['measure_explanation'] = measure_explanation
        df['dimensions_explanation'] = dimensions_explanation

    df['predictions_count'] = predictions_count

    df['true_label'] = df.apply(lambda row: {
        'ds_ID': row['id'],
        'alert_type': row['type'],
        'alert_direction': row['direction'],
        'alert_measure': row['measure'],
        'alert_dimensions': row['dimensions'],
    }, axis=1)

    for j in range(len(prediction_columns)):
        if len(prediction_columns[j]) > 0:
            df[f'prediction {j}'] = prediction_columns[j]

    df[f'accuracy'] = df.apply(calculate_accuracy_row, axis=1)

# =============================================================================
# saving results
# Rearrange rows
df = df.sort_values(by='__index').reset_index(drop=True)

# add percentage to df
for i in range(num_of_tests):
    if advanced_logic:
        accuracy_columns = ['accuracy', 'ambiguity_id_accuracy', 'ambiguity_measure_accuracy', 'predictions_count']
    else:
        accuracy_columns = ['accuracy', 'predictions_count']
    percent_true = df[accuracy_columns].mean().to_frame().T #Calculate the percentage of True values for boolean columns
    percent_true.index = ['% True']
    df = pd.concat([percent_true, df], ignore_index=False) # Concatenate the percentage row with the original DataFrame

# Rearrange columns By Desired column order
if advanced_logic:
    sorted_cols = [
        '__index','accuracy','Query','true_label','type','type_pred','direction','direction_pred','id','id_pred',
        'measure','measure_pred','measure_explanation','dimensions','dimensions_pred','dimensions_explanation','ambiguity_id','ambiguity_id_pred',
        'ambiguity_id_accuracy','ambiguity_id_score','ambiguity_measure','ambiguity_measure_pred','ambiguity_measure_accuracy','ambiguity_measure_score','ambiguity_dimensions','ambiguity_dimensions_pred','ambiguity_dimensions_accuracy','ambiguity_dimensions_score','predictions_count',
        'prediction 0','prediction 1','prediction 2','prediction 3','prediction 4','prediction 5','prediction 6','prediction 7',
    ]
else:
    sorted_cols = [
        '__index','accuracy','Query','true_label','type','type_pred','direction','direction_pred','id','id_pred',
        'measure','measure_pred','dimensions','dimensions_pred','predictions_count',
        'prediction 0','prediction 1','prediction 2','prediction 3','prediction 4','prediction 5','prediction 6','prediction 7',
    ]

df = df[sorted_cols]

end_time = time.time()
execution_time = end_time - start_time

#saving dataframe with pred for error analysis
print(f"Execution time: {execution_time} seconds")
#print(results_acc)
if num_of_queries <= 2:
    print(df)
else:
    today_date = date.today().strftime('%Y-%m-%d')
    filename = f'Total_Accuracy_Test_{today_date}.xlsx'

    #df.to_excel(synthetic_data_path + 'DataStreamId_accuracy_test_clean.xlsx', index=False, engine='openpyxl')
    df.to_excel(os.path.join(data_path, filename), index=False, engine='openpyxl')
