import argparse
import os
from utils import load_data, get_next_id, save_data, DATABASE_PATH
from config import CLI_ARGUMENTS, ARGUMENT_PARSER_OPTIONS
from datetime import datetime
from tabulate import tabulate


def print_todos(data, empty_message="No todos were found."):
    todo_data = [data] if type(data) is dict else data
    todo_lists = [list(todo.values()) for todo in todo_data]

    headers = [
        "ID",
        "Description",
        "Status",
        "Created at",
        "Last updated at",
        "Deadline",
    ]

    if len(todo_lists) == 0:
        print(empty_message)
    else:
        print(tabulate(todo_lists, headers=headers, tablefmt="grid"))


def do_add(args):
    todos = load_data()

    new_todo = {
        "id": get_next_id(todos),
        "description": " ".join(args.desc),
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
        "deadline": "" if args.deadline == "no" else str(args.deadline),
    }

    todos.append(new_todo)

    save_data(todos)

    print("\nNew todo created successfully:\n")
    print_todos(new_todo)


def do_update(args):
    todos = load_data()

    todo = todos[args.id]

    if args.desc:
        todo["description"] = " ".join(args.desc)

    if args.deadline:
        todo["deadline"] = "" if args.deadline == "no" else str(args.deadline)

    todo["status"] = args.status
    todo["updatedAt"] = datetime.now().isoformat()

    save_data(todos)

    print("\nTodo updated successfully:\n")
    print_todos(todo)


def do_delete(args):
    todos = load_data()

    todo = todos.pop(args.id)
    save_data(todos)

    print(f"\nTodo with id {args.id} deleted successfully:\n")
    print_todos(todo)


def do_list(args):
    todos = load_data()

    if args.status != "all":
        todos = [todo for todo in todos if todo["status"] in args.status]

    if args.deadline:
        if args.deadline == "no":
            todos = [todo for todo in todos if not todo["deadline"]]
        else:
            todos = [
                todo
                for todo in todos
                if datetime.fromisoformat(todo["deadline"]) <= args.deadline
            ]

    todos = sorted(todos, key=lambda todo: todo[args.sort_by], reverse=args.descending)

    print_todos(todos)


COMMANDS_MAP = {
    "add": {
        "handler": do_add,
        "help": "Adds a new task with a description (`desc`) and an optional deadline (`--deadline`).",
        "args": [CLI_ARGUMENTS["desc_positional"], CLI_ARGUMENTS["deadline"]],
    },
    "update": {
        "handler": do_update,
        "help": "Updates a task by id.",
        "args": [
            CLI_ARGUMENTS["id"],
            CLI_ARGUMENTS["desc_optional"],
            CLI_ARGUMENTS["status"],
            CLI_ARGUMENTS["deadline"],
        ],
    },
    "delete": {
        "handler": do_delete,
        "help": "Deletes a task by id.",
        "args": [CLI_ARGUMENTS["id"]],
    },
    "list": {
        "handler": do_list,
        "help": "List task items based on filter and sorting parameters.",
        "args": [
            CLI_ARGUMENTS["filter_status"],
            CLI_ARGUMENTS["deadline"],
            CLI_ARGUMENTS["sort-by"],
            CLI_ARGUMENTS["descending"],
        ],
    },
}


def get_handler(mapping=COMMANDS_MAP):
    parser = argparse.ArgumentParser(**ARGUMENT_PARSER_OPTIONS)

    subparsers = parser.add_subparsers(title="Available commands", dest="command")

    for command, options in mapping.items():
        command_parser = subparsers.add_parser(command, help=options["help"])

        for arg in options["args"]:
            arg_copy = dict(arg)
            names = arg_copy.pop("names")
            command_parser.add_argument(*names, **arg_copy)

    line_args = parser.parse_args()

    return mapping[line_args.command]["handler"], line_args


def main():
    if not os.path.exists(DATABASE_PATH) or os.stat(DATABASE_PATH).st_size == 0:
        save_data([])

    handler, args = get_handler()
    handler(args)


if __name__ == "__main__":
    main()
