# CLI Task Tracker
[Task Tracker](https://roadmap.sh/projects/task-tracker) project from [roadmap.sh](https://roadmap.sh/) with some additional tweaks. Tasks are stored in a local JSON file. 

# Data structure
This is the basic structure of the file:
```json
[
    {
        "id": 0,
        "description": "Wash dishes",
        "status": "todo",
        "createdAt": "2025-02-09T17:27:15.333563",
        "updatedAt": "2025-02-09T17:27:15.333563",
        "deadline": "2025-02-09 23:59:59"
    }
]
```

# Basic features
- **Adding the task**: Add the task with specified description.
- **Updating the task by ID**: Update the description and status of task by particular ID.
- **Deleting the task by ID**: Removing the task with particular ID.
- **Listing tasks**: Listing tasks in the console using different parameters.

# Additional features: 
- **Deadline date**: You can specify a deadline - the date before which the task should be completed.
- **Filtering by status**: Filter tasks from database based on status - todo, in-progress or done. Statuses can be also combined.
- **Filtering by deadline**: See all tasks that should be done before the specified deadline date.
- **Sorting**: Sort tasks by specified field: id, deadline date, creation date and last update date. Order can be ascending and descending.   

# Installation
1) Clone this repository:
```bash
git clone https://github.com/Nikitossik/cli-task-tracker
```
2) Go to the root directory:
```bash
cd cli-task-tracker
```
3) Install requirements:
```bash
pip install -r requirements.txt
```

# Usage and examples

## Adding

### Usage: 
```bash
python main.py add desc [desc ...] [--deadline [DEADLINE ...]]
```

### Basic task with description

```bash
python main.py add Wash dishes
```

### Task with deadline

**Set today's date**
```bash
python main.py add Wash dishes --deadline today  
```

**Set tomorrow's date**
```bash
python main.py add Wash dishes --deadline tomorrow
```

**Set specific date**
```bash
python main.py add Wash dishes --deadline 2025-12-31
```
> Note: By default if you don't specify time, than the end of the day is being set (23:59:59)

**Add specific time**
```bash
python main.py add Wash dishes --deadline today 12:00
python main.py add Wash dishes --deadline tomorrow 12:00
python main.py add Wash dishes --deadline 2025-12-31T12:00
python main.py add Wash dishes --deadline 2025-12-31 12:00
```

## Updating

### Usage: 
```bash
python main.py update id [--desc DESC [DESC ...]] [--status {todo,in-progress,done}] [--deadline [DEADLINE ...]]
```

**Mark as *in-progress***
```bash
python main.py update 0 --status in-progress
```

**Mark as *done***
```bash
python main.py update 0 --status done
```

**Change deadline**

The same way as in **Adding section**

```bash
python main.py update 0 --status in-progress --deadline tomorrow
```

**Unset deadline**

You can also unset deadline field with these keywords: unset, false, no

```bash
python main.py update 0 --status in-progress --deadline unset
```

## Deleting

### Usage: 
```bash
python main.py delete id
```

**Example**
```bash
python main.py delete 0
```

## Listing

### Usage: 
```bash
python main.py list [--status [{todo,in-progress,done,all} ...]] [--deadline [DEADLINE ...]]
                           [--sort-by {id,description,deadline,createdAt,updatedAt}] [--descending]
```

**List all**
```bash
python main.py list
```
> Note: At this point every parameter is set to it's default value, so all tasks are displayed

**Filter by status**

You can specify 1 or more statuses to display:
```bash
python main.py list --status todo
python main.py list --status todo in-progress
python main.py list --status in-progress done
```

**Filter by deadline**

Deadline format remains the same as in previous sections
```bash
python main.py list --deadline today 12:00
python main.py list --deadline tomorrow
python main.py list --deadline 2025-12-31 23:00
python main.py list --deadline unset
```

**Sorting**

Sorting is enabled for these fields: "id", "deadline", "createdAt", "updatedAt", where "id" is default. 
> `--descending` flag is set to False by default.
```bash
python main.py list --sort-by deadline
python main.py list --sort-by createdAt
python main.py list --sort-by updatedAt
python main.py list --sort-by deadline --descending
```
