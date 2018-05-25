import pandas as pd

from numpy import array

test_data_file =  "testAirlines.csv"
test_file_raw = open(test_data_file, 'r')
test_raw_data = test_file_raw.readlines()[1:]
test_file_raw.close()

res_data_file = "part1.txt"
res_file_raw = open(res_data_file, 'r')
res_raw_data = res_file_raw.readlines()
res_file_raw.close()

def parse_interaction(line):
    #print (line)
    line_split = line.split(",")
    return line_split[5]

def output_interaction(line):
    line_split = line.split(",")
    res = "malo"
    if float(line_split[1]) == float(1):
        res = "normal"
    elif float(line_split[1]) == float(2):
        res = "bueno"
    return res


mapped_comments = array([parse_interaction(x) for x in test_raw_data])
output_mapped_comments = array([output_interaction(x) for x in res_raw_data])


for i in range(len(mapped_comments)):
    res = "No existe correlacion"
    first = ""
    if(int(mapped_comments[i]) < 4):
        first = "malo"
    elif(int(mapped_comments[i]) < 8):
        first = "normal"
    else:
        first = "bueno"
    if (first == output_mapped_comments[i]):
        res = "Existe correlacion"
    if res == "Existe correlacion":
    print (str(mapped_comments[i]) + "," + str(output_mapped_comments[i]) + "," + res)
