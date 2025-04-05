import pandas as pd
import numpy as np
import re
import csv

hashmap = {}

with open(r"explore_programs/explore_programs_geneds_raw.txt") as file:
   # if count % 3 == 1:
    content = file.readlines()

    tag_set = set()

    for i in range(len(content)):
        if i % 3 == 2:

            if len(content[i].strip()) > 2:
           
                val = content[i].strip()

                #print(val)

                first = val[:2]
                second = val[2:]

                lst = [first, second]
             #   print("hi i got here")
             ##   print(first, second)
                for z in lst:
                  #  print(z, type(z))
                    if z not in hashmap:
                        hashmap[z.strip()] = [content[i-2][:], re.split(r'#', content[i-1])[1:]]
                    else:
                        hashmap[z.strip()].append([content[i-2][:], re.split(r'#', content[i-1])[1:]])

           #     print("I worked", hashmap)

            elif content[i].strip() not in hashmap:

                hashmap[content[i].strip()] = [[content[i-2][:], re.split(r'#', content[i-1])[1:]]]
             #   print(hashmap)
            else:

                hashmap[content[i].strip()].append([content[i-2][:], re.split(r'#', content[i-1])[1:]])
 
        if i % 3 == 1:
            tag_set.update(re.split(r'#', content[i])[1:])
           # print(re.split(r'#', content[i])[1:])

 #   print(tag_set)
#print(hashmap)

def recommended_class(interests, required):
    #Give it a list of interests, and of a string of required class, for example 'AH'
    #Then it chucks out a list [2, AAAD-A 132 Recent African American and African Diaspora Literature, ['Africa', 'Central America']]
    #The 2 represents number of interests matched, index 1 is class description, index 2 is  what matched.
    best_class = [1, 'classname']
    for i in hashmap[required]:
        count = 0
        reasons = []
        i[1][-1] = i[1][-1].strip()
        st = set(i[1])
        
        for j in interests:
            #print(j)
            if j in st:
                reasons.append(j)
                count += 1

        if count > best_class[0]:
            best_class = [count, i[0].strip(), reasons]

    
    return best_class



print(recommended_class(["Africa", "Central America"], 'AH'))