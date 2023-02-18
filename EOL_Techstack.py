#import some important libraries
import csv
from csv import reader
from csv import writer

import glob
import datetime
from datetime import datetime
from datetime import date
import os

#current working directory where all script files are stored
pwd = os.getcwd()

#create a list to store csv data
list_to_store_csv_data = []


#change directory where all csv files are located
os.chdir('../')
os.chdir('Csv_Files')
cwd = os.getcwd()

#store the path of CSV files in dir_path
dir_path = cwd

#read only csv files
list_of_paths_of_csv_files =  glob.glob(dir_path + "/*.csv")

#create 2 output files in Script_Files directory, one for Already Expired and other for close to expiry
EOL_Techstack_Output1 = os.path.join(pwd, 'EOL_Techstack_Output1.csv')
EOL_Techstack_Output2 = os.path.join(pwd, 'EOL_Techstack_Output2.csv')

#create header of output files
header_of_output_file = ['Client','Environment','TechStack','Version','EOL','Days remaining for EOL']

#read all the csv files present in above cwd and append lines one by one in list to store csv_file data
for file in list_of_paths_of_csv_files:
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) #skip header rows
        for line in csv_reader:
            #print(line)
            list_to_store_csv_data.append(line)


#today's date
curr_date = date.today()

#take column of EOL date in separate list
list_of_date_column = []
for i in range(0,len(list_to_store_csv_data)):
    list_of_date_column.append(list_to_store_csv_data[i][4]) #4th column is where EOL dates are present


#to convert dates which is stored in string format to integer take another list
list_to_separate_date = []
for i in range(0,len(list_of_date_column)):
    var=(list_of_date_column[i].split("/"))
    list_to_separate_date.append(var)

#print(list_to_separate_date)
#for calculation take another list and calculate delta
list_for_calculation = []
for i in range(0,len(list_to_separate_date)):
    if(len(list_to_separate_date[i])==3):
        mm = int(list_to_separate_date[i][0])
        dd = int(list_to_separate_date[i][1])
        yyyy = int(list_to_separate_date[i][2])
        dt = date(yyyy,mm,dd)
        delta = ((dt-curr_date).days)
        list_for_calculation.append(delta)
    else:
        list_for_calculation.append('NA')

#add column of remaining  days of EOL to list
for i in range(0,len(list_to_store_csv_data)):
        list_to_store_csv_data[i].append(list_for_calculation[i])

#print(*list_to_store_csv_data,sep="\n")


#create two lists to separate those which have remaining EOL days less than 180 but not expired
final_output_list1 = []
final_output_list2 = []

for i in range(0, len(list_to_store_csv_data)):
    if((type(list_to_store_csv_data[i][5])==int) and list_to_store_csv_data[i][5] < 0):
        final_output_list1.append(list_to_store_csv_data[i])

#print(final_output_list1)
for i in range(0, len(list_to_store_csv_data)):
    if((type(list_to_store_csv_data[i][5])==int) and (list_to_store_csv_data[i][5] > 0 and list_to_store_csv_data[i][5] <180 )):
        final_output_list2.append(list_to_store_csv_data[i])

#take function to append data of final_output_list1 and final_output_list2 in output_files
def add_column_in_output_file(EOL_Techstack_Output1,final_output_list1,row1):
    with open(EOL_Techstack_Output1,'w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output, lineterminator='\n')
        csv_writer.writerow(row1)
        for row in final_output_list1:
                csv_writer.writerow(row)

#call of function
add_column_in_output_file(EOL_Techstack_Output1,final_output_list1,header_of_output_file)
add_column_in_output_file(EOL_Techstack_Output2,final_output_list2,header_of_output_file)

