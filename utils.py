import json
import os
import argparse
from datetime import datetime, date, time

DATABASE_PATH = './data.json'

# parameter validation functions

def validate_id(id):
    todo_id = int(id)
    todos = load_data()
    
    if not todo_id in [todo['id'] for todo in todos]:
        raise argparse.ArgumentTypeError(f"Todo with id {id} does not exit")
    
    return todo_id        

def validate_datetime(dateparts):
    
    print("datetime: ", dateparts)
    
    # date_part = date.fromisoformat(dateparts[0])
    # time_part = time.fromisoformat(dateparts[1])
    
    # combined_datetime = datetime.combine(date_part, time_part)
    # print(combined_datetime)
    # print(combined_datetime.isoformat())
    # return combined_datetime
    return dateparts

def check_for_keywords(datepart_string):
    allowed_keywords = ['today', 'tomorrow']
    
    datepart_string = datepart_string.lower()
    
    if datepart_string in allowed_keywords:
        pass
    else:
        pass

def parse_single_datetime(datepart_string):
    
    """
        how to find out if user specified time??
    """
    
    # try:
    #     datetime_date = datetime.fromisoformat(datepart_string)
        
    #     if datetime.now() > datetime_date:
    #         raise argparse.ArgumentError(None, f"This date is expired. Try to set specific time or another date")
        
    # except ValueError as err:
    #     # today/tommorow
    # except argparse.ArgumentError as err:
        
    # else:
        

def parse_double_datetime(datepart_string):
    pass

def load_data(file_path = DATABASE_PATH):
    
    # return initial state if file is empty or non-existent
    if not os.path.exists(DATABASE_PATH) or os.stat(DATABASE_PATH).st_size == 0:
        return []
    
    # get json content and return it
    with open(file_path) as file:
        data = json.load(file)
    return data
        
def save_data(data, file_path = DATABASE_PATH):
    
    # save new data array to json file 
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        
def get_next_id(todos):
    if not todos or len(todos) == 0:
        return 0
    
    return max([todo["id"] for todo in todos]) + 1
        