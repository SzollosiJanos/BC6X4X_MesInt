import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()


PAUSES_ENABLED = 0

def main():
    array_of_pauses=[]
    number_of_max_iterations,number_of_max_tests_per_iteration,generation_seed,number_of_works,number_of_machines,number_of_pauses,array_of_pauses=read_from_file()
    random.seed(generation_seed)
    array_of_jobs = [[0 for x in range(number_of_machines)] for y in range(number_of_works)]
    array_of_jobs = generate_random_jobs(number_of_machines,number_of_works)
    start_search(number_of_max_iterations,number_of_max_tests_per_iteration,number_of_machines,number_of_works,array_of_pauses,number_of_pauses,array_of_jobs)


def read_from_file():
    file_input=open("config.txt", "r")

    array_of_pauses=[]
    file_input.readline()
    generation_seed=int(file_input.readline())
    generation_seed=420
    file_input.readline()
    number_of_max_iterations = int(file_input.readline())
    file_input.readline()
    number_of_max_tests_per_iteration = int(file_input.readline())
    file_input.readline()
    number_of_works = int(file_input.readline())
    number_of_works=5
    file_input.readline()
    number_of_machines = int(file_input.readline())
    number_of_machines=4
    file_input.readline()
    number_of_pauses = int(file_input.readline())
    file_input.readline()
    for i in range(number_of_pauses):
        splitted=file_input.readline().replace('\n','').split("-")
        array_of_pauses+=[splitted]
    file_input.close()

    
    print("Number of machines: ",number_of_machines)
    print("Number of work: ",number_of_works)
    print("Number of iterations: ",math.factorial(number_of_works))
    print("Iterations will be checked: ",number_of_max_iterations*number_of_max_tests_per_iteration)

    
    return number_of_max_iterations,number_of_max_tests_per_iteration,generation_seed,number_of_works,number_of_machines,number_of_pauses,array_of_pauses


def generate_random_jobs(number_of_machines,number_of_works):
    array_of_jobs = [[0 for x in range(number_of_machines)] for y in range(number_of_works)]
    file_output = open("log.txt", "w")
    for i in range (number_of_works):
        file_output.write("J"+str(i)+"\t")
    file_output.write("\n")
    array_of_jobs[0][0]=3
    array_of_jobs[1][0]=4
    array_of_jobs[2][0]=8
    array_of_jobs[3][0]=5
    array_of_jobs[4][0]=7

    array_of_jobs[0][1]=4
    array_of_jobs[1][1]=5
    array_of_jobs[2][1]=7
    array_of_jobs[3][1]=3
    array_of_jobs[4][1]=6

    array_of_jobs[0][2]=6
    array_of_jobs[1][2]=4
    array_of_jobs[2][2]=2
    array_of_jobs[3][2]=1
    array_of_jobs[4][2]=8

    array_of_jobs[0][3]=7
    array_of_jobs[1][3]=6
    array_of_jobs[2][3]=2
    array_of_jobs[3][3]=5
    array_of_jobs[4][3]=4

    print(array_of_jobs)
    print("Generated datas and logs can be found in log.txt")
    file_output.close()
    return array_of_jobs

def start_search(number_of_max_iterations,number_of_max_tests_per_iteration,number_of_machines,number_of_works,array_of_pauses,number_of_pauses,array_of_jobs):
    global ax
    best_time_of_current_search = best_time_of_alltime_search = ITERATIONS = 0
    best_found_solution = []
    temp_best_found_solution = []
    base = []
    temp_base = []
    
    base+=[0]
    base+=[1]
    base+=[2]
    base+=[3]
    base+=[4]
    print(base)

    file_output = open("log.txt", "a")
    file_output.write("Base lineup: "+print_array(base)+"\n")
    best_found_solution = base.copy()
    print("Starting simulated anneling...")

    
    temp_base,ITERATIONS,best_time_of_current_search,best_time_of_alltime_search,temp_best_found_solution=start_test(number_of_machines,number_of_works,array_of_jobs,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,file_output,base,ITERATIONS)
    base=temp_base.copy()
    best_found_solution=temp_best_found_solution.copy()

    
    file_output.write("\n\n\nThe best way: "+str(print_array(best_found_solution))+"with time: "+str(best_time_of_alltime_search))
    print("Best way: ",str(print_array(best_found_solution)), "\nTime: ",best_time_of_alltime_search)
    file_output.close()

    
    result,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,time=simulation(number_of_machines,number_of_works,array_of_jobs,best_found_solution,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,1)
    ax.set(xlim=(0, best_time_of_alltime_search), xticks=np.arange(0, best_time_of_alltime_search),
       ylim=(0, number_of_machines), yticks=np.arange(0, number_of_machines+1))
    plt.show()

def start_test(number_of_machines,number_of_works,array_of_jobs,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,file_output,base,ITERATIONS):
    data = []
    data = base.copy()
    temp_base = base.copy()
    a = random.randint(0,number_of_works-1)
    b = random.randint(0,number_of_works-1)
    
    while a==b:
         a = random.randint(0,number_of_works-1)
         b = random.randint(0,number_of_works-1)
    temp=data[a]
    data[a]=data[b]
    data[b]=temp
    
    result,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,time=simulation(number_of_machines,number_of_works,array_of_jobs,data,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,0)

    if result==1:
        temp_base=data.copy()
        file_output.write("Found new best time: "+print_array(data)+" with "+str(best_time_of_current_search)+ "time\n")
    elif result==0:
        temp=pow(0.95,ITERATIONS)*100000
        if temp==0:
            file_output.write("New Worse base found and declined: "+print_array(data)+" with "+str(time)+" Chance: 0\n")
        else:
            if random.random()<math.exp((best_time_of_alltime_search-time)/temp):
                file_output.write("New Worse base found and accepted: "+print_array(data)+" with "+str(time)+ "time. Chance: "+str(math.exp((best_time_of_alltime_search-time)/temp))+"\n")
                temp_base=data.copy()
                best_time_of_current_search=time
            else:
                file_output.write("New Worse base found and declined: "+print_array(data)+" with "+str(time)+" Chance: "+str(math.exp((best_time_of_alltime_search-time)/temp))+"\n")
    return temp_base,ITERATIONS+1,best_time_of_current_search,best_time_of_alltime_search,best_found_solution


def simulation(number_of_machines,number_of_works,array_of_jobs,order_of_jobs,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,mode):
    global ax
    Current_work = [-1 for x in range(number_of_machines)]
    Current_done = [0 for x in range(number_of_machines)]
    for i in range(number_of_machines):
        Current_work[i]=array_of_jobs[order_of_jobs[0]][i]

    
    time = -1
    temp_best_found_solution = best_found_solution.copy()
    
    while Current_done[number_of_machines-1]!=number_of_works:
        time+=1
        print(str(time))
        for i in range(number_of_machines):
            if Current_work[i]==0:
                print("Job done "+str(i))
                Current_done[i]+=1
                if Current_done[i]>=number_of_works:
                    Current_done[i]=number_of_works
                    Current_work[i]=-1
                else:
                    Current_work[i]=array_of_jobs[order_of_jobs[Current_done[i]]][i]
                    if i==0 and check_pauses_and_current_work(time,Current_work[i],array_of_pauses,number_of_pauses):
                        Current_work[i]-=1
                    else:
                        if Current_done[i-1]>Current_done[i]  and check_pauses_and_current_work(time,Current_work[i],array_of_pauses,number_of_pauses):
                            Current_work[i]-=1
                if mode==1:
                    
                    ax.bar(time-array_of_jobs[order_of_jobs[Current_done[i]-1]][i], 1, width=array_of_jobs[order_of_jobs[Current_done[i]-1]][i],bottom=number_of_machines-i-1, edgecolor="white", linewidth=0.7,align='edge')
            else:
                if i==0:
                    if check_pauses_and_current_work(time,Current_work[i],array_of_pauses,number_of_pauses):
                        Current_work[i]-=1
                else:
                    if Current_done[i-1]>Current_done[i] and check_pauses_and_current_work(time,Current_work[i],array_of_pauses,number_of_pauses):
                        Current_work[i]-=1
        

    if best_time_of_current_search == 0:
        best_time_of_current_search = time
        
    if best_time_of_alltime_search == 0:
        best_time_of_alltime_search = best_time_of_current_search
        
    if best_time_of_current_search > time:
        best_time_of_current_search = time
        if best_time_of_alltime_search > best_time_of_current_search:
            best_time_of_alltime_search = best_time_of_current_search
            temp_best_found_solution=order_of_jobs.copy()
        return 1,best_time_of_current_search,best_time_of_alltime_search,temp_best_found_solution,time

    if best_time_of_current_search == time:
        return 2,best_time_of_current_search,best_time_of_alltime_search,temp_best_found_solution,time
    
    return 0,best_time_of_current_search,best_time_of_alltime_search,temp_best_found_solution,time

def check_pauses_and_current_work(time,current_work,array_of_pauses,number_of_pauses):
    if PAUSES_ENABLED == 0:
        return True
    for i in range(number_of_pauses):
        if time>=int(array_of_pauses[i][1]):
            continue
        if time<=int(array_of_pauses[i][0]) and time+current_work<=int(array_of_pauses[i][0]):
            continue
        if time>=int(array_of_pauses[i][0]) and time<=int(array_of_pauses[i][1]):
            return False
        if time+current_work>=int(array_of_pauses[i][0]) and time+current_work<=int(array_of_pauses[i][1]):
            return False
        if time<=int(array_of_pauses[i][0]) and time+current_work>=int(array_of_pauses[i][1]):
            return False
    return True


def print_array(array):
    string=""
    j=0
    for i in array:
        string+="J"+str(array[j])+" "
        j+=1
    return string
if __name__ == "__main__":
    main()
