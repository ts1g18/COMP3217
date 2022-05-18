# This class will implement a method to create plots of all abnormal data
import pandas


# this method reads all of the user tasks from COMP3217CW2Input.xlsx
# returns all user&task ids, ready times, deadlines, maximum scheduled energy per hour and energy demand
def read_tasks():
    # COMP3217CW2Input.xlsx contains the user task information
    task_file = pandas.read_excel('COMP3217CW2Input.xlsx', sheet_name='User & Task ID')
    # print(task_file)
    user_and_task_id = task_file['User & Task ID'].tolist()
    ready_time = task_file['Ready Time'].tolist()
    deadline = task_file['Deadline'].tolist()
    max_energy_per_hour = task_file['Maximum scheduled energy per hour'].tolist()
    energy_demand = task_file['Energy Demand'].tolist()
    return user_and_task_id, ready_time, deadline, max_energy_per_hour, energy_demand


read_tasks()
