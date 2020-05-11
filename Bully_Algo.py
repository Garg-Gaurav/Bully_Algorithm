import random
import sys
import re
import matplotlib.pyplot as plt
import time


count=0
process_list={}
process_list_count={}
max_process=0
command_list={'list','kill','reload','display'}
display_performance={}


def file_process_init(file):
    process_file=open(file,'r')
    delimiters=",|_|\n"
    for list in process_file:
        regex_list=re.split(delimiters,list)
        process_list.update({regex_list[0]:regex_list[1]})
        process_list_count.update({regex_list[0]:(regex_list[1]+"_"+str(count))})


def bully_algo(max_process):
    start=time.perf_counter()
    for key in process_list_count.keys():
        if(int(max_process)<int(key)):
            max_process=key

    for key,val in process_list_count.items():
        process_details=val.split('_')
        ele_count=int(process_details[1])
        ele_count+=1
        process_name=process_details[0]+'_'+str(ele_count)

        process_list_count.update({key:process_name})
    end=time.perf_counter()
    total_time=end-start
    display_performance.update({total_time: len(process_list_count)})
    return max_process,time


def reload_process(file):
    process_file = open(file, 'r')
    delimiters = ",|_|\n"
    for list in process_file:
        regex_list = re.split(delimiters, list)
        if(regex_list[0] in process_list_count.keys()):
            pass
        else:
            process_list_count.update({regex_list[0]: (regex_list[1] + "_" + str(0))})
            process_list.update({regex_list[0]: regex_list[1]})


def display_data():
    for key,val in process_list_count.items():
        print(key,",",val)

def display_process_cordinator(max_prcocess):
    print('Coordinator: ',max_process,":",process_list_count.get(max_process))

def kill_process(id):
    del process_list_count[id]
    del process_list[id]

def display_graph():
    y_data = display_performance.values()
    x_data = display_performance.keys()

    plt.bar(y_data, x_data, align='center', alpha=0.5)
    plt.ylabel('Election Time')
    plt.xlabel('No of Processes')
    plt.title('Programming language usage')

    plt.show()


if __name__ == "__main__":
    file=str(sys.argv[1])
    file_process_init(file)
    display_data()
    print("Applying Bully-Algorithm generates below result:")
    max_process,time=bully_algo(max_process)
    display_data()
    display_process_cordinator(max_process)
    print("This program implements the bully algorithm, with below functionality:\n"
          "Operation (command)\n"
          "list  (list)\n"
          "kill  (kill id)\n"
          "reload (reload)\n"
          "Display (display)")
    while (True):
        command = input()
        command = command.split(' ')
        if command[0].lower() in command_list:
            if(command[0].lower()=='list'):
                display_data()
                display_process_cordinator(max_process)
            elif(command[0].lower()=='kill'):
                kill_process(command[1])
                if(command[1]==max_process):
                    max_process,time=bully_algo(0)
                    print("Election was initiated by id: ",random.choice(list(process_list_count)))
                display_data()
                display_process_cordinator(max_process)
            elif(command[0].lower()=='reload'):
                reload_process(file)
                display_data()
                print("Re-Electing the coordinator:")
                max_process,time=bully_algo(max_process)
                display_data()
                display_process_cordinator(max_process)
            elif(command[0].lower()=='display'):
                display_graph()

        else:
            print('Please enter the valid operation')