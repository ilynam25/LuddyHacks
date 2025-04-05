import pandas as pd
import random as rand

df = pd.read_csv('coursemaphackathon.csv')

# print(df.head())
dax = df.iloc[0, 3] 
print(dax)
dax=dax.split('],\n')
# print(dax)
# print('hi')
daxclean=[]
for i in range(len(dax)):
    if ']' in dax[i]:
        p=dax[i]
        p=p.replace(']','').replace('\n','').replace('[','')
        daxclean.append(p)
    else:
        daxclean.append(dax[i][1:])
print(daxclean)
# dic={}
# for i in dax:
#     a=i[0:-3]
#     dic[a]=dax


# times = pd.read_excel('Spring2022-Fall2024 schedule of class bulletin/soc4228.xls',engine = 'xlrd', header = None)
# time = pd.read_csv('Dataparsing/timespractice.csv')

# print(time.head())

interests = ['Nutrition', 'South America', 'Pop Culture', 'Legal Issues', 'Teaching', 'Journalism', 'Nutrition', 'Sustainability',
            'Finance', 'Nature', 'Conflict Resolution', 'Video Games', 'Math', 'Human Behavior', 'Literature', 'Crafts',
            'Technology', 'Movies', 'Nature', 'Journalism\n', 'Fitness', 'Forensics', 'Central America', 'Language', 
            'Science', 'Marketing', 'Asia', 'Fashion', 'Business', 'Music', 'Philosophy', 'History', 'Internet', 
            'Children', 'Travel', 'Media', 'Photography', 'Design', 'Environment', 'Food', 'Music', 'Security', 
            'Video Games', 'Religion', 'Sports', 'Healthcare', 'Data Analysis', 'Helping People', 'Performance', 
            'Finance', 'Legal Issues', 'North America', 'Animals', 'Sustainability', 'Management', 'Programming', 
            'Art', 'Design', 'Writing', 'South America', 'Leadership', 'Culture',
            'Fashion', 'Photography', 'Counseling', 'Media',
            'Rehabilitation', 'Performance', 'News', 'Human Rights', 'Philosophy', 
            'Management', 'Pop Culture', 'Math', 'Communication', 'Language', 'Public Relations', 
            'News', 'Teaching', 'Science', 'Art', 'Religion', 'Programming', 'Marketing', 'Europe', 
            'International', 'History', 'Rehabilitation', 'Movies', 'Technology', 'Government', 
            'Leadership', 'Africa', 'Human Behavior', 'Gender and LGBTQ+', 'Human Rights', 'International', 
            'Helping People', 'Europe', 'Security', 'Literature', 'North America', 'Africa']

sample_interests = []
for i in range(4):
    d=rand.choice(interests)
    sample_interests.append(d)
print(sample_interests)

course_map_list=[]
for i in daxclean:
    if ',' in i:
        db=i
        # print(db)
        db=list(i.split(','))
        # print(db)
        l=rand.choice(db)
        course_map_list.append(l)
    else:
        course_map_list.append(i)
print('-----------------------------------------------------------------------')
print(course_map_list)
print('-----------------------------------------------------------------------')