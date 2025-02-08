import json
import os

DATABASE_PATH = './data.json'

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
            
def todo_exists(todos, todo_id):
    return todo_id in [todo['id'] for todo in todos]        