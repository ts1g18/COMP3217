# This class will implement a method to create plots of all abnormal data
import pandas

# this method reads all of the user tasks from COMP3217CW2Input.xlsx
# returns all user&task ids, ready times, deadlines, maximum scheduled energy per hour and energy demand
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

users = ['user1', 'user2', 'user3', 'user4', 'user5']


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


tasks = read_tasks()[0]
user_tasks = read_tasks()[1]


def generate_lp_model(tasks):
    prices = read_tasks()[2]
    decision_vars = []
    task_cost = []
    eq = []

    # Define the model, sense is set to LpMinimise by default
    lp_model = LpProblem(name='scheduling-problem')

    # Loop through list of tasks
    # get the ready_time, deadline and max_energy per hour for each task
    for counter, task in enumerate(tasks):
        time_slot = []
        ready_time = task[0]
        deadline = task[1]
        max_energy = task[2]
        # loop between the interval of ready_time and deadline since the appliance can only execute within this interval
        for i in range(ready_time, deadline + 1):
            # initialise the decision variables
            # add '_<number>' to create unique names for each task. e.g. user1_task1_20
            # upper limit is the max energy per hour
            x = LpVariable(name=user_tasks[counter] + '_' + str(i), lowBound=0, upBound=max_energy)
            time_slot.append(x)
        decision_vars.append(time_slot)

    # Add constraints
    for counter, task in enumerate(tasks):
        task_energy_demand = task[3]
        user_task_list = []
        for decision_var in decision_vars[counter]:
            user_task_list.append(decision_var)
        eq.append(user_task_list)
        # Calculate the sum of a list of linear expressions
        # add the obj function to the model
        # the sum should be equal to the task energy demand
        lp_model += lpSum(user_task_list) == task_energy_demand

    # Add the objective function to the model
    for counter, task in enumerate(tasks):
        prices_for_task = prices[counter]
        for decision_var in decision_vars[counter]:
            price = prices_for_task[int(decision_var.name.split('_')[2])]
            task_cost.append(price * decision_var)
    lp_model += lpSum(task_cost)

    return lp_model

# TODO:
# method to generate histograms for abnormal curves
# solve the schedule problem

read_tasks()
generate_lp_model(tasks)


