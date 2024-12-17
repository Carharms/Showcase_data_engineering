# Notes on Capstone

# each task will have a unique ID
    # create ID based on # of tasks + 1
# create a date stamp on when it was created
# create a date stamp on when it was completed (days inside task manager)
# add priority 
# due date optional date
# at end pickle data and close
# if completed do not print out / if uncomplete print out
# mark when task is done
# querying capabilities
# normalize inputs to lower

# Report purpose is debugging - used to print entire to do list

# two data objects - Class task and 
# save tasks data to disk in pickle save to ".todo.pickle" -. before makes it invisible
# format the output



def add(self, task_name, priority, due_date):

        # this needs to be adjusted
        new_task = Task(task_name)

        # use regex to find due date
        due_date_regex = r"--due (.*?)$"
        due_date = re.search(due_date_regex, due_date)
        if due_date == None:
            Task.due_date = "-"
        else:
            Task.due_date = due_date.group(1)

        # use regex to find priority
        priority_regex = r"--priority (\d)$"
        priority_level = re.search(priority_regex, priority)
        if priority_level == None:
            Task.priority = 1
        elif priority_level == 1:
            Task.priority = 1
        else:
            Task.priority = int(priority_level.group(1))


        # adjust this
        self.task_list.append(new_task)

        print(f"Created Task {new_task.unique_ID}")




# originally line 178 - paired with above

# Is command_line_str needed?
    #command_line_str = args.command



# original list sorting and printing
for task in task_list_current:
            if task.completed == False:
                if task.due_date == "-":
                    list_output_due_date_absent.append(task)
                elif task.due_date != "-":
                    list_output_due_date.append(task)
        
        # now you have two lists
        def print_list_due_date(list_output_due_date):
            print()
            for task in list_output_due_date:
                current_time = datetime.datetime.now
                age = current_time - task.created
                age = age.days
                task.append(age)