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


    Matrix[0][0]=3
    Matrix[1][0]=4
    Matrix[2][0]=8
    Matrix[3][0]=5
    Matrix[4][0]=7

    Matrix[0][1]=4
    Matrix[1][1]=5
    Matrix[2][1]=7
    Matrix[3][1]=3
    Matrix[4][1]=6

    Matrix[0][2]=6
    Matrix[1][2]=4
    Matrix[2][2]=2
    Matrix[3][2]=1
    Matrix[4][2]=8

    Matrix[0][3]=7
    Matrix[1][3]=6
    Matrix[2][3]=2
    Matrix[3][3]=5
    Matrix[4][3]=4

    print(Matrix)
    print("Generated datas and logs can be found in log.txt")
    
    base+=[0]
    base+=[1]
    base+=[2]
    base+=[3]
    base+=[4]
    print(base)

    result,BEST,BEST_ALLTIME,BESTWAY,time=anneling_start(MACHINE,WORK,Matrix,base,BEST,BEST_ALLTIME,BESTWAY,pauses,numpauses)
    f.write("Base lineup: "+printarr(base)+"\n")
    BESTWAY = base.copy()
    print("Starting simulated anneling...")
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
        print(time)
        for i in range(MACHINE):
            if Current_work[i]==0:
                Current_done[i]+=1
                print("done job",i)
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

def printarr(array):
    string=""
    j=0
    for i in array:
        string+="J"+str(array[j])+" "
        j+=1
    return string
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

if __name__ == "__main__":
    main()
