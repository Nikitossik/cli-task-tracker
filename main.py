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
        
        print(parser)
        print(namespace)
        print(values)

        # resulting_datetime = datetime.now()
        
        # if len(values) == 1:
        #     resulting_datetime = parse_single_datetime(values[0])
        # elif len(values) == 2:
        #     resulting_datetime = parse_double_datetime(values)
        # else:
        #     raise argparse.ArgumentError(None, "deadline must contain maximum 2 values")
        
        setattr(namespace, self.dest, values)

"""
        либо сделать action который будет проверять массив [date, time]
        либо задавать дедлайн как datetime YYYY-MM-DD 
    """

def do_add(args):
    
        todos = load_data()
        
        print(args)
        
        # todos.append({
        #     "id": get_next_id(todos),
        #     "description": " ".join(args.desc),
        #     "status": 'todo',
        #     "createdAt": datetime.now().isoformat(),
        #     "updatedAt": datetime.now().isoformat(),
        #     "deadline": str(args.deadline)
        # })
                
        # save_data(todos)
                
        # print("Todo added successfully!")
        
def do_update(args):
        todos = load_data()
        
        todo = todos[args.id]
        
        if args.desc:
            todo['description'] = " ".join(args.desc)
            
        todo['status'] = args.status
        todo['updatedAt'] = datetime.now().isoformat()
                
        save_data(todos)
            
        print(f"Update result:\n {todo}")

def do_delete(args):
        todos = load_data()
        
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
                "help": 'Description of the TODO',
            },
            {
                "names": ['--deadline-date', '-dd'],
                # "nargs": "*",
                "help": 'Deadline date of the TODO in ISO8601 format', 
                "action": DeadlineAction,
                "dest": 'deadline',
                # "default": datetime(date.today().year, date.today().month, date.today().day, 23,59,59)
                "default": date.today()
            },
            {
                "names": ['--deadline-time', '-dt'],
                # "nargs": "*",
                "help": 'Deadline date of the TODO in ISO8601 format', 
                "action": DeadlineAction,
                "dest": 'deadline',
                # "default": datetime(date.today().year, date.today().month, date.today().day, 23,59,59)
                "default": time(23,59,59)
            },
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
                "nargs": 2,
                "type": validate_datetime,
                "help": 'Deadline date of the TODO in ISO8601 format', 
                "default": date.today()
            },
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
    