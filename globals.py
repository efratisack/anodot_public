LANGCHAIN_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
apikey = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # enter your key here
GPT_MODEL = 'gpt-4o'

data_path = 'synthetic_data'

interactive_app = True
ambiguous_ds_en = True
Demo_mode = True
advanced_logic = True

if Demo_mode:
    datastreams_file_name = 'Demo_data_streams.json'  #'20_data_streams.json', 'data_streams.json'
else:
    if ambiguous_ds_en:
        datastreams_file_name = '20_data_streams.json'
        dataset_file_name = 'ambiguous queries test.csv'
    else:
        datastreams_file_name = 'data_streams.json'
        dataset_file_name = 'synthetic_queries.csv'
verbous = True
