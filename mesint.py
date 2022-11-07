import random
import math
import time

def main():
    pauses=[]
    max_interations,max_tests,seed,work,machine,numpauses,pauses=readinput()
    random.seed(seed)
    generate_work(max_interations,max_tests,machine,work,pauses,numpauses)

def readinput():
    finput=open("config.txt", "r")

    pauses=[]
    useless=finput.readline()
    SEED=int(finput.readline())
    useless=finput.readline()
    MAX_ITERATION = int(finput.readline())
    useless=finput.readline()
    MAX_TEST_PER_ITERATION = int(finput.readline())
    useless=finput.readline()
    WORK = int(finput.readline())
    useless=finput.readline()
    MACHINE = int(finput.readline())
    useless=finput.readline()
    PAUSES = int(finput.readline())
    useless=finput.readline()
    for i in range(PAUSES):
        useless=finput.readline()
        useless=useless.replace('\n','')
        splitted=useless.split("-")
        pauses+=[splitted]
    finput.close()


    
    print("Number of machines: ",MACHINE)
    print("Number of work: ",WORK)
    print("Number of iterations: ",math.factorial(WORK))
    print("Iterations will be checked: ",MAX_ITERATION*MAX_TEST_PER_ITERATION)

    
    return MAX_ITERATION,MAX_TEST_PER_ITERATION,SEED,WORK,MACHINE,PAUSES,pauses

def generate_work(MAX_ITERATION,MAX_TEST_PER_ITERATION,MACHINE,WORK,pauses,numpauses):
    BEST = 0
    BEST_ALLTIME = 0
    ITERATIONS = 0
    BESTWAY = []
    base = []
    data= []
    Matrix = [[0 for x in range(MACHINE)] for y in range(WORK)]
    
    f = open("log.txt", "w")
    for i in range (WORK):
        f.write("J"+str(i)+"\t")
    f.write("\n")
    for macs in range(MACHINE):
        for jobs in range(WORK):
            Matrix[jobs][macs]=random.randint(1,10)
            f.write(str(Matrix[jobs][macs]))
            f.write("\t")
        f.write("\n")

    print("Generated datas and logs can be found in log.txt")
    
    for i in range(WORK):
        base+=[i]
    
    f.write("Base lineup: "+printarr(base)+"\n")
    BESTWAY = base.copy()
    print("Starting simulated anneling...")
    for i in range(MAX_ITERATION):
        for p in range(MAX_TEST_PER_ITERATION):
            data = base.copy()
            a= random.randint(0,WORK-1)
            b= random.randint(0,WORK-1)
            while a==b:
                a= random.randint(0,WORK-1)
                b= random.randint(0,WORK-1)
            temp=data[a]
            data[a]=data[b]
            data[b]=temp
            #f.write("Try new base: "+printarr(data)+"\n")
            result,BEST,BEST_ALLTIME,BESTWAY,time=anneling_start(MACHINE,WORK,Matrix,data,BEST,BEST_ALLTIME,BESTWAY,pauses,numpauses)
            if result==1:
                base=data.copy()
                f.write("Found new best time: "+printarr(data)+" with "+str(BEST)+ "time\n")
            elif result==0:
                temp=pow(0.95,ITERATIONS)*100000
                if random.random()<math.exp((BEST_ALLTIME-time)/temp):
                    f.write("New Worse base found and accepted: "+printarr(data)+" with "+str(time)+ "time. Chance: "+str(math.exp((BEST_ALLTIME-time)/temp))+"\n")
                    base=data.copy()
                    BEST=time
                else:
                    f.write("New Worse base found and declined: "+printarr(data)+" with "+str(time)+" Chance: "+str(math.exp((BEST_ALLTIME-time)/temp))+"\n")
            ITERATIONS+=1
    f.write("\n\n\nThe best way: "+str(printarr(BESTWAY))+"with time: "+str(BEST_ALLTIME))
    print("Best way: ",str(printarr(BESTWAY)), "\nTime: ",BEST_ALLTIME)
    f.close()

def anneling_start(MACHINE,WORK,Matrix,works,BEST,BEST_ALLTIME,BESTWAY,pauses,numpauses):
    Current_work = [-1 for x in range(MACHINE)]
    Current_done = [0 for x in range(MACHINE)]
    for i in range(MACHINE):
        Current_work[i]=Matrix[works[0]][i]

    
    time = -1
    ann_best=BEST
    ann_all=BEST_ALLTIME
    best_way = BESTWAY.copy()


    
    while Current_done[MACHINE-1]!=WORK:
        time+=1
        for i in range(MACHINE):
            if Current_work[i]==0:
                Current_done[i]+=1
                if Current_done[i]>=WORK:
                    Current_done[i]=WORK
                else:
                    Current_work[i]=Matrix[works[Current_done[i]]][i]
                    if i==0 and checkwork(time,Current_work[i],pauses,numpauses):
                        Current_work[i]-=1
                    else:
                        if Current_done[i-1]>Current_done[i]  and checkwork(time,Current_work[i],pauses,numpauses):
                            Current_work[i]-=1
            else:
                if i==0:
                    if checkwork(time,Current_work[i],pauses,numpauses):
                        Current_work[i]-=1
                else:
                    if Current_done[i-1]>Current_done[i] and checkwork(time,Current_work[i],pauses,numpauses):
                        Current_work[i]-=1
        

    if ann_best == 0:
        ann_best = time

        
    if ann_all == 0:
        ann_all = ann_best

        
    if ann_best >time:
        ann_best = time
        if ann_all > ann_best:
            ann_all = ann_best
            best_way=works.copy()
        return 1,ann_best,ann_all,best_way,time

    
    if ann_best == time:
        return 2,ann_best,ann_all,best_way,time

    
    return 0,ann_best,ann_all,best_way,time

def checkwork(time,current_work,pauses,numpauses):
    for i in range(numpauses):
        if time>=int(pauses[i][1]):
            continue
        if time<=int(pauses[i][0]) and time+current_work<=int(pauses[i][0]):
            continue
        if time>=int(pauses[i][0]) and time<=int(pauses[i][1]):
            return False
        if time+current_work>=int(pauses[i][0]) and time+current_work<=int(pauses[i][1]):
            return False
        if time<=int(pauses[i][0]) and time+current_work>=int(pauses[i][1]):
            return False
    return True


def printarr(array):
    string=""
    j=0
    for i in array:
        string+="J"+str(array[j])+" "
        j+=1
    return string

if __name__ == "__main__":
    main()
