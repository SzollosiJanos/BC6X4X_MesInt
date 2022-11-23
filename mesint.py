import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()

def main():
    array_of_pauses=[]
    number_of_max_iterations,number_of_max_tests_per_iteration,generation_seed,number_of_works,number_of_machines,number_of_pauses,array_of_pauses=read_from_file()
    file_output = open("log.txt", "w")
    print("Generated datas and logs can be found in log.txt")
    for i in range(len(generation_seed)):
        print("\n\n\n\n",i,". generation: \n\n\n")
        file_output.write("\n\n\n\n"+str(i)+". generation: \n\n\n")
        random.seed(int(generation_seed[i]))
        array_of_jobs = [[0 for x in range(int(number_of_machines[i]))] for y in range(int(number_of_works[i]))]
        array_of_jobs = generate_random_jobs(int(number_of_machines[i]),int(number_of_works[i]),file_output)
        start_search(int(number_of_max_iterations[i]),int(number_of_max_tests_per_iteration[i]),int(number_of_machines[i]),int(number_of_works[i]),array_of_pauses[i],int(number_of_pauses[i]),array_of_jobs,file_output)
    print("Done")
    file_output.close()
def read_from_file():
    file_input=open("config.txt", "r")
    generation_seed=[]
    array_of_pauses=[]
    number_of_max_iterations=[]
    number_of_max_tests_per_iteration=[]
    number_of_works=[]
    number_of_machines=[]
    number_of_pauses=[]
    
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    generation_seed+=input_data
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    number_of_max_iterations+=input_data
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    number_of_max_tests_per_iteration+=input_data
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    number_of_works+=input_data
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    number_of_machines+=input_data
    file_input.readline()
    input_data=file_input.readline().replace('\n','').split(" ")
    number_of_pauses+=input_data
    file_input.readline()
    for i in range(len(number_of_pauses)):
        splitted=file_input.readline().replace('\n','').split(" ")
        temp_of_pauses = []
        for k in splitted:
            splitt_of_splitted = k.split("-")
            temp_of_pauses.append(splitt_of_splitted)
        array_of_pauses.append(temp_of_pauses)
    file_input.close()
    return number_of_max_iterations,number_of_max_tests_per_iteration,generation_seed,number_of_works,number_of_machines,number_of_pauses,array_of_pauses


def generate_random_jobs(number_of_machines,number_of_works,file_output):
    array_of_jobs = [[0 for x in range(number_of_machines)] for y in range(number_of_works)]
    for i in range (number_of_works):
        file_output.write("J"+str(i)+"\t")
    file_output.write("\n")
    for macs in range(number_of_machines):
        for jobs in range(number_of_works):
            array_of_jobs[jobs][macs]=random.randint(1,10)
            file_output.write(str(array_of_jobs[jobs][macs]))
            file_output.write("\t")
        file_output.write("\n")
    return array_of_jobs

def start_search(number_of_max_iterations,number_of_max_tests_per_iteration,number_of_machines,number_of_works,array_of_pauses,number_of_pauses,array_of_jobs,file_output):
    global ax
    best_time_of_current_search = best_time_of_alltime_search = ITERATIONS = 0
    best_found_solution = []
    temp_best_found_solution = []
    base = []
    temp_base = []
    
    for i in range(number_of_works):
        base+=[i]

    
    file_output.write("Base lineup: "+print_array(base)+"\n")
    best_found_solution = base.copy()

    
    
    for i in range(number_of_max_iterations):
        for p in range(number_of_max_tests_per_iteration):
            temp_base,ITERATIONS,best_time_of_current_search,best_time_of_alltime_search,temp_best_found_solution=start_test(number_of_machines,number_of_works,array_of_jobs,best_time_of_current_search,best_time_of_alltime_search,best_found_solution,array_of_pauses,number_of_pauses,file_output,base,ITERATIONS)
            base=temp_base.copy()
            best_found_solution=temp_best_found_solution.copy()

    
    file_output.write("\n\n\nThe best way: "+str(print_array(best_found_solution))+"with time: "+str(best_time_of_alltime_search))
    print("Best way: ",str(print_array(best_found_solution)), "\nTime: ",best_time_of_alltime_search)


    
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

    machine_start = [[0 for x in range(int(number_of_works))] for y in range(int(number_of_machines))]
    machine_end = [[0 for x in range(int(number_of_works))] for y in range(int(number_of_machines))]

    for i in range(number_of_works):
        for r in range(number_of_machines):
            if i==0:
                if r==0:
                    machine_start[order_of_jobs[i]][r]=0
                    for k in range(number_of_pauses):
                        if not check_pauses_and_current_work(int(machine_start[order_of_jobs[i]][r]),array_of_jobs[order_of_jobs[i]][r],array_of_pauses,number_of_pauses,k):
                            machine_start[order_of_jobs[i]][r]=int(array_of_pauses[k][1])
                        elif int(array_of_pauses[k][1])>int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r]):
                            break
                else:
                    machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i]][r-1]
                    for k in range(number_of_pauses):
                        if not check_pauses_and_current_work(int(machine_start[order_of_jobs[i]][r]),array_of_jobs[order_of_jobs[i]][r],array_of_pauses,number_of_pauses,k):
                            machine_start[order_of_jobs[i]][r]=int(array_of_pauses[k][1])
                        elif int(array_of_pauses[k][1])>int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r]):
                            break
            else:
                if r==0:
                    machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i-1]][r]
                    for k in range(number_of_pauses):
                        if not check_pauses_and_current_work(int(machine_start[order_of_jobs[i]][r]),array_of_jobs[order_of_jobs[i]][r],array_of_pauses,number_of_pauses,k):
                            machine_start[order_of_jobs[i]][r]=int(array_of_pauses[k][1])
                        elif int(array_of_pauses[k][1])>int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r]):
                            break
                else:
                    if machine_end[order_of_jobs[i]][r-1] > machine_end[order_of_jobs[i-1]][r]:
                        machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i]][r-1]
                        for k in range(number_of_pauses):
                            if not check_pauses_and_current_work(int(machine_start[order_of_jobs[i]][r]),array_of_jobs[order_of_jobs[i]][r],array_of_pauses,number_of_pauses,k):
                                machine_start[order_of_jobs[i]][r]=int(array_of_pauses[k][1])
                            elif int(array_of_pauses[k][1])>int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r]):
                                break
                    else:
                        machine_start[order_of_jobs[i]][r]=machine_end[order_of_jobs[i-1]][r]
                        for k in range(number_of_pauses):
                            if not check_pauses_and_current_work(int(machine_start[order_of_jobs[i]][r]),array_of_jobs[order_of_jobs[i]][r],array_of_pauses,number_of_pauses,k):
                                machine_start[order_of_jobs[i]][r]=int(array_of_pauses[k][1])
                            elif int(array_of_pauses[k][1])>int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r]):
                                break
            machine_end[order_of_jobs[i]][r]=int(machine_start[order_of_jobs[i]][r])+int(array_of_jobs[order_of_jobs[i]][r])
            if mode:
                ax.bar(machine_start[order_of_jobs[i]][r], 1, width=array_of_jobs[order_of_jobs[i]][r],bottom=number_of_machines-r-1, edgecolor="white", linewidth=0.7,align='edge')

    time = machine_end[order_of_jobs[number_of_works-1]][number_of_works-1]
    temp_best_found_solution = best_found_solution.copy()
    
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

def check_pauses_and_current_work(time,current_work,array_of_pauses,number_of_pauses,i):
    if time>=int(array_of_pauses[i][0]) and time<=int(array_of_pauses[i][1]):
        return False
    if time+current_work>int(array_of_pauses[i][0]) and time+current_work<=int(array_of_pauses[i][1]):
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
