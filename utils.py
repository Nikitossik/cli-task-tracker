import json
import os
import argparse
from datetime import datetime, time, timedelta

DATABASE_PATH = './data.json'

# parameter validation functions

def validate_id(id):
    todo_id = int(id)
    todos = load_data()
    
    if not todo_id in [todo['id'] for todo in todos]:
        raise argparse.ArgumentTypeError(None, f"Todo with id {id} does not exit")
    
    return todo_id        

def check_for_keywords(date_str):
    
    allowed_keywords = {'today', 'tomorrow'}
    date_str = date_str.lower()
    parts = date_str.split()
    
    if not parts[0] in allowed_keywords:
        raise argparse.ArgumentError(None, f"Invalid keyword provided. Choose from {allowed_keywords}")
    
    now = datetime.now()
    base_date = now.date() if parts[0] == "today" else now.date() + timedelta(days=1)
    deadline_time = time(23, 59, 59)
    
    if len(parts) == 2:
        try:
            deadline_time = time.fromisoformat(parts[1])
        except ValueError:
            raise argparse.ArgumentError(None, "Invalid time format. Use HH:MM:SS.")
    
    datetime_obj = datetime.combine(base_date, deadline_time)
        
    if datetime_obj < now:
        raise argparse.ArgumentError(None, "This datetime is alrady expired. Try setting for later")

    return datetime_obj

def parse_date(date_str):
    
    now = datetime.now()

    try:
        # try converting the date from ISO-8601 first
        datetime_obj = datetime.fromisoformat(date_str)
    except ValueError:
        # if wasn't converted successfully - try searching for keywords
        try:
            return check_for_keywords(date_str)
        except argparse.ArgumentError as err:
            raise err
    else:
        # split the date string and check if the second part (time) is set explicitly
        
        date_str_parts = date_str.replace("T", " ").split()
        
        if len(date_str_parts) == 1:
            # if not - then set the end of the day
            datetime_obj = datetime_obj.replace(hour=23, minute=59, second=59)

        # check if date is expired
        if datetime_obj < now:
            raise argparse.ArgumentError(None, "This datetime is alrady expired. Try setting for later")

        return datetime_obj
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
        