import argparse
from custom_actions import MultipleStatusAction, DeadlineAction
from utils import validate_id

CLI_ARGUMENTS = {
    "id": {
        "names": ["id"],
        "type": validate_id,
        "help": "Numeric id of the task (required).",
    },
    "status": {
        "names": ["--status", "-st"],
        "type": str,
        "help": "Status of the task. Available statuses are: %(choices)s. Defaults to %(default)s",
        "choices": ["todo", "in-progress", "done"],
        "default": "todo",
    },
    "filter_status": {
        "names": ["--status", "-st"],
        "type": str,
        "nargs": "*",
        "action": MultipleStatusAction,
        "help": "Status of the task. Available statuses are: %(choices)s. Defaults to %(default)s",
        "choices": ["todo", "in-progress", "done", "all"],
        "default": "all",
    },
    "sort-by": {
        "names": ["--sort-by", "-s"],
        "help": "Field of sorting",
        "choices": ["id", "description", "deadline", "createdAt", "updatedAt"],
        "default": "id",
    },
    "descending": {
        "names": ["--descending", "-dsc"],
        "help": "Descending order of sort. By default set to False",
        "action": "store_true",
        "default": False,
    },
    "desc_positional": {
        "names": ["desc"],
        "type": str,
        "nargs": "+",
        "help": "Task description (required).",
        "default": "",
    },
    "desc_optional": {
        "names": ["--desc", "-d"],
        "type": str,
        "nargs": "+",
        "help": "Task description.",
        "default": "",
    },
    "deadline": {
        "names": ["--deadline", "-dl"],
        "nargs": "*",
        "help": """Task deadline (default - empty string) in following formats:
                ISO 8601 (`YYYY-MM-DDTHH:MM:SS`, `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DD`),
                string (`today`, `tomorrow` and ISO 8601 time is optional),
                string (`unset`, `no`, `false`) - erasing deadline. 
                If time is not specified, it defaults to the end of the day (23:59:58). 
                If the date is expired compared to the present moment, than the error is raised.
                """,
        "action": DeadlineAction,
        "default": "",
    },
}

ARGUMENT_PARSER_OPTIONS = {
    "exit_on_error": False,
    "prog": "python main.py",
    "formatter_class": argparse.RawTextHelpFormatter,
    "description": """
Task Tracker CLI is a simple command-line tool for managing tasks. It supports \x1b[1;37;40madding, updating, deleting, and listing\x1b[0m tasks 
with \x1b[1;37;40mfilters and sorting.\x1b[0m
    """,
}
