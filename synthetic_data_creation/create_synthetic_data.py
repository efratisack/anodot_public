import json

def load_synthetic_data_streams(data_streams_path):
    with open(data_streams_path, 'r') as file:
        data_streams = json.load(file)
    return data_streams
