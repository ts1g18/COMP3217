# This class will implement a method to create plots of all abnormal data
import pandas


# this method reads all of the user tasks from COMP3217CW2Input.xlsx
# returns all user&task ids, ready times, deadlines, maximum scheduled energy per hour and energy demand
def read_tasks():
    # COMP3217CW2Input.xlsx contains the user task information
    task_file = pandas.read_excel('COMP3217CW2Input.xlsx', sheet_name='User & Task ID')
    # print(task_file)
    user_tasks = task_file['User & Task ID'].tolist()
    ready_time = task_file['Ready Time'].tolist()
    deadline = task_file['Deadline'].tolist()
    max_energy_per_hour = task_file['Maximum scheduled energy per hour'].tolist()
    energy_demand = task_file['Energy Demand'].tolist()

    # this array will contain all tasks and each task is an array itself
    all_tasks = []

    for i in range(len(user_tasks)):
        task = [ready_time[i], deadline[i], max_energy_per_hour[i], energy_demand[i]]

        all_tasks.append(task)

    # print(user_tasks)

    # read predicted labels
    testing_results = pandas.read_csv('TestingResults.txt', header=None)
    testing_results_no_labels = testing_results.drop(24, axis=1)
    # print(testing_results)
    x = testing_results_no_labels.values.tolist()
    y = testing_results[24].tolist()

    return all_tasks, user_tasks, x, y


read_tasks()
