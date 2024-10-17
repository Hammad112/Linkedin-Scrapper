def clean_data(data):
    
    return {key: value for key, value in data.items() if value != 'N/A'}