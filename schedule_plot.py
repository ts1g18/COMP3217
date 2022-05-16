from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# this function reads the data from the excel file using pandas
def readData():
    # Read user task information from excel file
    excel_file = pd.read_excel('COMP3217CW2Input.xlsx', sheet_name='User & Task ID')
    #get each task number, ready time, deadline, maximum energy per hour, energy demand from the COMP3217CW2Input.xlsx file and store them in a list
    task_number = excel_file['User & Task ID'].tolist()
    ready_time = excel_file['Ready Time'].tolist()
    deadline = excel_file['Deadline'].tolist()
    max_energy_per_hour = excel_file['Maximum scheduled energy per hour'].tolist()
    energy_demand = excel_file['Energy Demand'].tolist()
    # we need an array to store all of the tasks (an array of arrays)
    all_tasks = []
    task_names = []

    # for each task organize its task number, ready time, deadline, max energy per hour, energy demand and task number and add them to the array of all tasks
    for i in range(len(ready_time)):
        task = []
        task.append(ready_time[i])
        task.append(deadline[i])
        task.append(max_energy_per_hour[i])
        task.append(energy_demand[i])
        task_names.append(task_number[i])

        all_tasks.append(task)

    # Read the testing results and add the data to lists
    testing_results = pd.read_csv('TestingResults.txt', header=None)
    y_testing_results = testing_results[24].tolist()
    testing_results = testing_results.drop(24, axis=1)
    x_testing_results = testing_results.values.tolist()

    return all_tasks, task_names, x_testing_results, y_testing_results


def createLPModel(tasks, task_names):
    '''Function to create an LP model for the scheduling problem'''

    # Variables
    task_vars = []
    c = []
    eq = []

    # create LP problem model for Minimization
    model = LpProblem(name="scheduling-problem", sense=LpMinimize)

    # Loop through list of tasks
    for ind, task in enumerate(tasks):
        n = task[1] - task[0] + 1
        temp_list = []
        # Loop between ready_time and deadline for each task
        # Creates LP variables with given constraints and unique names
        for i in range(task[0], task[1] + 1):
            x = LpVariable(name=task_names[ind] + '_' + str(i), lowBound=0, upBound=task[2])
            temp_list.append(x)
        task_vars.append(temp_list)

    # Create objective function for price (to minimize) and add to the model
    for ind, task in enumerate(tasks):
        for var in task_vars[ind]:
            price = price_list[int(var.name.split('_')[2])]
            c.append(price * var)
    model += lpSum(c)

    # Add additional constraints to the model
    for ind, task in enumerate(tasks):
        temp_list = []
        for var in task_vars[ind]:
            temp_list.append(var)
        eq.append(temp_list)
        model += lpSum(temp_list) == task[3]

    # Return model to be solved in main function
    return model


# Plot hourly energy usage for community
def plot(model, count):
    hours = [str(x) for x in range(0, 24)]
    pos = np.arange(len(hours))
    users = ['user1', 'user2', 'user3', 'user4', 'user5']
    color_list = ['midnightblue', 'mediumvioletred', 'mediumturquoise', 'gold', 'linen']
    plot_list = []

    # Create lists to plot usage
    for user in users:
        temp_list = []
        for hour in hours:
            hour_list_temp = []
            task_count = 0
            for var in model.variables():
                if user == var.name.split('_')[0] and str(hour) == var.name.split('_')[2]:
                    task_count += 1
                    # print('{} {} {} {}'.format(user, hour, var, var.value()))
                    hour_list_temp.append(var.value())
            temp_list.append(sum(hour_list_temp))
        plot_list.append(temp_list)

    # Show as a bar chart stacked by user
    plt.bar(pos, plot_list[0], color=color_list[0], edgecolor='black', bottom=0)
    plt.bar(pos, plot_list[1], color=color_list[1], edgecolor='black', bottom=np.array(plot_list[0]))
    plt.bar(pos, plot_list[2], color=color_list[2], edgecolor='black',
            bottom=np.array(plot_list[0]) + np.array(plot_list[1]))
    plt.bar(pos, plot_list[3], color=color_list[3], edgecolor='black',
            bottom=np.array(plot_list[0]) + np.array(plot_list[1]) + np.array(plot_list[2]))
    plt.bar(pos, plot_list[4], color=color_list[4], edgecolor='black',
            bottom=np.array(plot_list[0]) + np.array(plot_list[1]) + np.array(plot_list[2]) + np.array(plot_list[3]))

    plt.xticks(pos, hours)
    plt.xlabel('Hour')
    plt.ylabel('Energy Usage (kW)')
    plt.title('Energy Usage Per Hour For All Users\nDay %i' % count)
    plt.legend(users, loc=0)
    # plt.show()
    plt.savefig('plots\\' + str(count) + '.png')
    plt.clf()

    return plot_list


tasks, task_names, x_data, y_labels = readData()

for ind, price_list in enumerate(x_data):
    # Schedule and plot abnormal guideline pricing curves
    if y_labels[ind] == 1:
        # Solve returned LP model fro scheduling solution
        model = createLPModel(tasks, task_names)
        answer = model.solve()
        # Print LP model stats
        print(answer)
        # Plot hourly usage for scheduling solution
        plot(model, ind + 1)
