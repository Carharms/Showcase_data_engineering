#! 
"""To Do List - with command line functions
    Program uses command line arguements to add to, delete from, query, complete tasks,
    report on all tasks, and list current tasks"""

__author__ = "Carter Harms"
__copyright__ = "Copyright, 2023"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "harmsc@uchicago.edu"


import argparse
import pickle
import sys
import uuid
import datetime
import tabulate
from dateutil import parser as dtparser



class Task:

    """Representation of the Task class attributes
    Instance Attributes:
            - created - date
            - completed - date
            - name - string
            - unique id - number
            - priority - int value of 1, 2, or 3; 1 is default
            - due date - date, this is optional"""

    def __init__(self, name, priority=1):    

        # unique ID for each task
        self.unique_ID = uuid.uuid4()

        # task name/ task objective
        self.name = name
        # priority level of the task - 1-3
        self.priority = priority

        # datetime variables
        now = datetime.datetime.now()
        self.created = now
        self.due_date = None 
        self.completed = False     


class Tasks:
    '''Representation of the Tasks class functions and attributes
    Instance Atributes:
        - tasks = list of all current and past tasks created by to-do user

    '''

    def __init__(self, file):

        # if file exists within cwd opens and unpickles
        try:
            with open(file, "rb+") as f:
                dataset = pickle.load(f)
                self.tasks = list(dataset)
                
        # if file doesn't exist (first time) within cwd, creates empty list
        except EOFError:
            self.tasks = []
        except FileNotFoundError:
            self.tasks = []


   # Current status: operational
    def add(self, task_name, priority_num, due_date_num):
        '''
        Adds a task to the task list with associated values
        
        Args:
            specify in the command line to generate this list using "--add" 
            task_name: name of the task to accomplish
            priority number: task priority on a scale of 1-3
            due date: user input of when the task is due
            
        Returns:
            a new task added to the database of tasks'''

        new_task = Task(task_name)

        # set priority number
        if priority_num is not None:
            new_task.priority == 1
        else:
            new_task.priority == 1

        # set due date
        if due_date_num is not None:
            date_obj = dtparser.parse(due_date_num)
            new_task.due_date = date_obj
        else:
            new_task.due_date == None

        # add new task to the tasks database
        self.tasks.append(new_task)

        # confirm to the user a new task was created
        print(f"Created Task {new_task.unique_ID}")
    

    def list(self):
        '''
        Creates a list of all the current tasks that are not completed
        
        Args: 
            specify in the command line to generate this list using "--list"
            
        Returns:
            a tabulated list of all the current tasks'''

        # filter out all tasks that are complete
        incomplete_tasks = [task for task in self.tasks if task.completed == False]

        # Sort tasks by due date and priority
        age_calc_data = []
        empty_due_dated = []

        # create two lists - one with a valid due date and one without
        for task in incomplete_tasks:
            if task.due_date == None or task.due_date == "-":
                #task.due_date = "-"
                empty_due_dated.append(task)
            else:
                age_calc_data.append(task)

        # create an empty list 
        listing_tasks = []
        
        age_calc_data = [task for task in age_calc_data if task.due_date is not None]
        # sort all the tasks with a valid due date
        age_calc_data.sort(key=lambda task: (task.due_date, -task.priority), reverse=True)
        # sort all the tasks without a valid due date
        empty_due_dated.sort(key=lambda task: -task.priority, reverse=True)
        
        # combine the lists in a new order
        full_list = age_calc_data + empty_due_dated

        # format elements of the task to prepare for printing
        for task in full_list:
            time_now = datetime.datetime.now()

            # calculate time delta for Age column
            age_calc = time_now - task.created
            age = age_calc.days

            # create proper formatting for the Due Date column
            task_due_date = task.due_date
            try:
                task_due_date_str = dtparser.isoparse(str(task_due_date))
                task_due_date = task_due_date_str.strftime("%m-%d-%Y")
            except ValueError:
                task_due_date = "-"
            
            # create a list of all elements needed for each row in the output
            task_data = [task.unique_ID, age, task_due_date, task.priority, task.name]
            listing_tasks.append(task_data)

        # use the tabulate module to create a output list detailing all current tasks
        output= tabulate.tabulate(listing_tasks, headers=["ID","Age", "Due Date", "Priority", "Name"])
        print(output)
        

    def report(self):
        '''
        Creates a report of all tasks - both current and completed
        
        Args: 
            specify in the command line to generate this list using "--report"
            
        Returns:
            a tabulated list of all tasks'''

        # variable for all tasks
        all_tasks = [task for task in self.tasks]
        

        # sort tasks into 2 lists - one with valid due dates and one without
        age_calc_data = []
        empty_due_dated = []

        # filter tasks into one of the above lists
        for task in all_tasks:
            if task.due_date == None or task.due_date == "-":
                #task.due_date = "-"
                empty_due_dated.append(task)
            else:
                age_calc_data.append(task)

        # create an empty list
        listing_tasks = []

        
        age_calc_data = [task for task in age_calc_data if task.due_date is not None]
        # sort all the tasks with a valid due date
        age_calc_data.sort(key=lambda task: (task.due_date, -task.priority), reverse=True)
        # sort all the tasks without a valid due date
        empty_due_dated.sort(key=lambda task: -task.priority, reverse=True)
        
        # combine the lists in a new order
        full_report = age_calc_data + empty_due_dated

        
        # format elements of the task to prepare them for printing
        for task in full_report:
            time_now = datetime.datetime.now()

            # calculate time delta for Age column
            age_calc = time_now - task.created
            age = age_calc.days

            task_due_date = task.due_date

            # turns due_date into string and formats properly
            try:
                task_due_date_str = dtparser.isoparse(str(task_due_date))
                task_due_date = task_due_date_str.strftime("%m-%d-%Y")
            except ValueError:
                task_due_date = "-"
            
            # formatting Created variable and column
            task_created_date = task.created
            task_created_date_str = dtparser.isoparse(str(task_created_date))
            task_created_date = task_created_date_str.strftime("%a %b  %d %H:%M:%S %Z %Y")

            # formatting Completed variable and column
            task_closed_date = task.completed
            if task_closed_date == False:
                task_closed_date = "-"
            else:
                try:
                    task_closed_date_str = dtparser.isoparse(str(task_closed_date))
                    task_closed_date = task_closed_date_str.strftime("%a %b  %d %H:%M:%S %Z %Y")
                except ValueError:
                    task_closed_date

            # create a list of all the elements needed for each row in the output
            task_data = [task.unique_ID, age, task_due_date, task.priority, task.name, task_created_date, task_closed_date]
            listing_tasks.append(task_data)

        # use the tabulate module to create a output list detailing all current tasks
        output= tabulate.tabulate(listing_tasks, headers=["ID","Age", "Due Date", "Priority", "Name", "Created", "Completed"])
        print(output)
                   

    def delete(self, unique_ID):
        '''
        Deletes a specified task from the task list
        
        Args:
            unique_ID: specify the unique ID associated with the task to remove from the list
            
            specify in the command line to generate this list using "--delete"
            
        Returns:
            A confirmation message saying the deleted task is no longer in the task list'''

        # identify that if the command line input matches a task ID, it will be removed from the list
        for task in self.tasks:
            task_ID_obj = task.unique_ID
            task_ID_obj = str(task_ID_obj)
            if task_ID_obj == unique_ID:
                self.tasks.remove(task)
                self.pickle_tasks()
                break        
        print(f"Deleted task {unique_ID}")


    
    def done(self, unique_ID):
        '''
        Changes status of a task to complete
        
        Args:
            unique_ID: specify the unique ID associated with the task to set it as complete
            
            specify in the command line to generate this list using "--done"
            
        Returns:
            A confirmation message saying the task is marked as complete'''

        for task in self.tasks:
            task_ID_obj = task.unique_ID
            task_ID_obj = str(task_ID_obj)
            if task_ID_obj == unique_ID:
                task.completed = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Completed task {unique_ID}")
                
        
    
    def query(self, search):
        '''
        Queries task list
        
        Args:
            search term(s): the words or inputs entered by the user looking for a specific task
            
            specify in the command line to generate this list using "--query"
            
        Returns:
            A list of all the relevant tasks associated with the query input'''

        relevant_tasks = []
        
        # creates loop if multiple search words are entered
        for search_word in search:
            #creates loop for each task in task list
            for task in self.tasks:

                # format elements of the task to prepare for printing 
                if search_word in task.name:
                    created_date = task.created
                    time_now = datetime.datetime.now()
                    # calculates time delta for Age column
                    age_calc = time_now - created_date
                    age = age_calc.days

                    #turns due date into string and formats properly
                    task_due_date = task.due_date
                    try:
                        task_due_date_str = dtparser.isoparse(str(task_due_date))
                        task_due_date = task_due_date_str.strftime("%m-%d-%Y")
                    except ValueError:
                        task_due_date = "-"

                    # create a list of all the elements needed for each row in the output
                    task_data = [task.unique_ID, age, task_due_date, task.priority, task.name]
                    if task_data not in relevant_tasks:
                        relevant_tasks.append(task_data)

        # use the tabulate module to create a output list detailing all relevant tasks associated with the query term
        output= tabulate.tabulate(relevant_tasks, headers=["ID","Age", "Due Date", "Priority", "Name"])
        print(output)

    def pickle_tasks(self):
        '''
        Pickles a file
                    
        Returns:
            An invisible file named ".todo.pickle" in the cwd'''

        with open(".todo.pickle", "wb") as f:
            pickle.dump(self.tasks, f)

def main():

    # create a parser to analyze command line functions
    parser = argparse.ArgumentParser(prog="To-do list", description="Update your Todo list")

    # arguements for each command line input tied to the task list
    parser.add_argument('--add', type=str, required=False, help='a string to add to list')
    parser.add_argument('--due', type=str, help='a string with the due date of the tasks')
    parser.add_argument('--priority', type=int, help='priority level of the task')
    parser.add_argument('--delete', type=str, required=False, help='a string to delete from list')
    parser.add_argument('--list', action='store_true', help='a string to delete from list') 
    parser.add_argument('--report', action='store_true', help='a string to generate a report of all incomplete todo list tasks')
    parser.add_argument('--query', type=str, nargs= "+", required=False, help='a string to query data from full todo list')
    parser.add_argument('--done', type=str, required=False, help='a string to close the program')

    
    # parse command line
    args = parser.parse_args()

    # setting file and initializing Tasks class
    file = ".todo.pickle"
    task_list = Tasks(file)
    

    # Create While loop for adjustments 
    if args.add:
        task_list.add(args.add, args.priority, args.due)

    elif args.delete:
        task_list.delete(args.delete)
    
    elif args.list:
        task_list.list()
    
    elif args.report:
        task_list.report()

    elif args.query:
        task_list.query(args.query)
    
    elif args.done:
        task_list.done(args.done)

    
    task_list.pickle_tasks()
    sys.exit()
        

if __name__ == "__main__":
    main()

