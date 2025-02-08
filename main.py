import argparse
from utils import *

"""
    [
        {
            "id": 0,
            "desc": str,
            "status": [todo, in-progress, done],
            "createdAt": date,
            "updatedAt": date,
            "deadline": date
        }
    ]
    
    add desc [DESC] --status --deadline
    update id [ID] --desc --status --deadline
    delete id [ID]
    list - все
    list --status [s,s,s] --deadline --sort-by --asc
"""

def do_add(args):
        todos = load_data()
        
        todos.append({
            "id": get_next_id(todos),
            "description": " ".join(args.desc),
            "status": args.status
        })
                
        save_data(todos)
                
        print("Todo added successfully!")
        
def do_update(args):
        todos = load_data()
        
        if not todo_exists(todos, args.id):
            print(f"update: error: Todo with id {args.id} does not exit")
            return
        
        todo = todos[args.id]
        
        if args.desc:
            todo['description'] = " ".join(args.desc)
            
        todo['status'] = args.status
                
        save_data(todos)
            
        print(f"Update result:\n {todo}")

def do_delete(args):
        todos = load_data()
        
        if not todo_exists(todos, args.id):
            print(f"delete: error: Todo with id {args.id} does not exit")
            return
        
        todos.pop(args.id)
        
        save_data(todos)
        
        print(f"Todo with id {args.id} deleted successfully")
        
COMMANDS_MAP = {
    'add': {
        "handler": do_add,
        "help": "Add a TODO item",
        "args": [
            {
                "names": ['desc'],
                "type": str,
                "nargs": "+",
                "help": 'Description of the TODO'
            },
            {
                "names": ['--status', '-s'],
                "type": str,
                "nargs": "?",
                "help": 'Status of the TODO',
                "choices": ['todo', 'in-progress', 'done'], 
                "default": 'todo'
            }
        ]
    },
    'update': {
        "handler": do_update,
        "help": "Update a TODO item",
        "args": [
            {
                "names": ['id'],
                "type": int,
                "help": 'Numeric todo id to update'
            },
            {
                "names": ['--desc', '-d'],
                "type": str,
                "nargs": "+",
                "help": 'Description of the TODO'
            },
            {
                "names": ['--status', '-s'],
                "type": str,
                "help": 'Status of the TODO',
                "choices": ['todo', 'in-progress', 'done'], 
                "default": 'todo'
            }
        ]
    },
    'delete': {
        "handler": do_delete,
        "help": "Delete a TODO item by id",
        "args": [
            {
                "names": ['id'],
                "type": int,
                "help": 'Numeric todo id to delete'
            }
        ]
    }
}

def get_command(mapping=COMMANDS_MAP):
    
    parser = argparse.ArgumentParser(exit_on_error=False)

    subparsers = parser.add_subparsers(dest='command', help='Main commands of Task CLI') 
    
    for command, options in mapping.items():

        command_parser = subparsers.add_parser(command, help=options['help'])
        
        for arg in options['args']:
            names = arg.pop('names')
            command_parser.add_argument(*names, **arg)
    
    line_args = parser.parse_args()
    
    return mapping[line_args.command]['handler'], line_args
    

if __name__ == '__main__':
    
    if not os.path.exists(DATABASE_PATH) or os.stat(DATABASE_PATH).st_size == 0:
        save_data([])

    handler, args = get_command()
    
    handler(args)