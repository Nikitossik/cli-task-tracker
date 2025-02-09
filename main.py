import argparse
from utils import *
from datetime import date, time, datetime, tzinfo

"""
    add desc [DESC] --status --deadline
    update id [ID] --desc --status --deadline
    delete id [ID]
    list - все
    list --status [s,s,s] --deadline --sort-by --asc
"""

class DeadlineAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        
        no_deadline_keywords = {'unset'}
        
        deadline_value = ""
        
        if len(values) > 2:
            raise argparse.ArgumentError(None, "deadline must contain maximum 2 values")
        elif len(values) == 1 and values[0].lower() in no_deadline_keywords:
            deadline_value = "no"
        else:
            date_str = " ".join(values)
            deadline_value = parse_date(date_str)
            
        setattr(namespace, self.dest, deadline_value)

def do_add(args):
    
        todos = load_data()
        
        todos.append({
            "id": get_next_id(todos),
            "description": " ".join(args.desc),
            "status": 'todo',
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "deadline": "" if args.deadline == 'no' else str(args.deadline)
        })
                
        save_data(todos)
                
        print("Todo added successfully!")
        
def do_update(args):
        todos = load_data()
        
        todo = todos[args.id]
        
        if args.desc:
            todo['description'] = " ".join(args.desc)
            
        if args.deadline:
            todo["deadline"] = "" if args.deadline == 'no' else str(args.deadline)
            
        todo['status'] = args.status
        todo['updatedAt'] = datetime.now().isoformat()
                
        save_data(todos)
            
        print(f"Update result:\n {todo}")

def do_delete(args):
        todos = load_data()
        
        todos.pop(args.id)
        
        save_data(todos)
        
        print(f"Todo with id {args.id} deleted successfully")
        
def do_list(args):
    todos = load_data()
    
    pass
        
COMMANDS_MAP = {
    'add': {
        "handler": do_add,
        "help": "Add a TODO item",
        "args": [
            {
                "names": ['desc'],
                "type": str,
                "nargs": "+",
                "help": 'Description of the TODO',
            },
            {
                "names": ['--deadline', '-dl'],
                "nargs": "*",
                "help": 'Deadline date of the TODO in ISO8601 format', 
                "action": DeadlineAction,
                "default": ""
            }
        ]
    },
    'update': {
        "handler": do_update,
        "help": "Update a TODO item",
        "args": [
            {
                "names": ['id'],
                "type": validate_id,
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
            },
            {
                "names": ['--deadline', '-dl'],
                "nargs": "*",
                "help": 'Deadline date of the TODO in ISO-8601 format', 
                "action": DeadlineAction,
                "default": ""
            }
        ]
    },
    'delete': {
        "handler": do_delete,
        "help": "Delete a TODO item by id",
        "args": [
            {
                "names": ['id'],
                "type": validate_id,
                "help": 'Numeric todo id to delete'
            }
        ]
    },
    "list": {
        "handler": do_list,
        "help": "List TODO items based on filter and sorting parameters",
        "args": [
            
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
    