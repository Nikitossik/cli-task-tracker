import cmd
import argparse
import json
import os

"""
    [
        {
            "id": 0,
            "title": str,
            "desc": str,
            "status": [todo, in-progress, done],
            "createdAt": date,
            "updatedAt": date
        }
    ]
"""

DATABASE_PATH = './data.json'

todos = []

parser = argparse.ArgumentParser(exit_on_error=False)
parser.add_argument('id', type=int, nargs='?')
parser.add_argument('--title', '-t', type=str, nargs="*")
parser.add_argument('--desc', '-d', type=str, nargs="*", default="")
parser.add_argument('--status', '-s', type=str, choices=['todo', 'in-progress', 'done'], default='todo')   

# subparsers = parser.add_subparsers(help='Main commands of Task CLI') 

# update_parser = subparsers.add_parser('update', help="Update a todo item by id")
# update_parser.add_argument('id', type=int, help='Numeric id of the todo item')

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
            
class TaskCLI(cmd.Cmd):
    prompt = 'task-tracker '
    intro = 'Welcome to Task Tracker CLI. Type "help" for available commands.'

    def do_list(self, line):
        """Prints all todos"""

        todos = load_data()
        print(todos)
    
    # check if id exists
    # check id --title is not empty
    
    def do_update(self, line):
        """Updates the todo item"""
        
        todos = load_data()
        
        # try:
            
        #     args = parser.parse_args(line.split())
        #     print(args)
            
        #     if not args.id:
        #         raise argparse.ArgumentError('argument id: argument is required')
        # except (argparse.ArgumentError) as err:
        #     print(err)
        # else: 
            

    # new id is maximum id + 1, not from len
    def do_add(self, line):
        """Adds the todo item"""
        
        todos = load_data()
        
        try:
            args = parser.parse_args(line.split())
            print(args)
            
            if not args.title or len(args.title) == 0:
                raise ValueError('argument --title/-t: argument must not be empty')
            
        except (argparse.ArgumentError, ValueError) as err:
            print(err)
        else:
            todos.append({
                "id": len(todos) + 1,
                "title": " ".join(args.title),
                "desc": args.desc,
                "status": args.status
            })
                
            save_data(todos)
                
            print("Todo added successfully!")
    
    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':
    
    if not os.path.exists(DATABASE_PATH) or os.stat(DATABASE_PATH).st_size == 0:
        save_data([])

    TaskCLI().cmdloop()