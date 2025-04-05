import pandas as pd
import numpy as np
import re
import csv

count = 0
res = []
with open("explore_programs\explore_programs_geneds_raw.txt") as file:
   # if count % 3 == 1:

    content = file.readlines()

    tag_set = set()

    for i in range(len(content)):
        if i % 3 == 1:
            tag_set.update(re.split(r'#', content[i])[1:])

print(tag_set)
print(len(tag_set))
    
    