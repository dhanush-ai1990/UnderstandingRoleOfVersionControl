#Progrom for studying Developer Version control, testing and  build behaviour based
# on time of the day for msr challenge data 2018.


import sqlite3
from collections import Counter
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc,rcParams
def plot_bar_from_counter(data):
	""""
	This function creates a bar plot from a counter.

	:param counter: This is a counter object, a dictionary with the item as the key
	 and the frequency as the value
	:param ax: an axis of matplotlib
	:return: the axis wit the object in it
	"""
	counter= Counter(data)
	plt.figure(figsize=(18,14))
	sns.set()
	sns.set_style("dark")
	sns.set_style("white")


	frequencies = counter.values()
	names = counter.keys()
	x_coordinates = np.arange(len(counter))
	plt.bar(x_coordinates, frequencies, align='center',color='#CD5C5C')
	plt.xticks(x_coordinates,names)
	return plt






db_file='/Volumes/LLL/events.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor1=conn.cursor()
cursor2=conn.cursor()
SQL = "Select  idesessionuuid from vc_action;"
cursor.execute(SQL)
SQL = "Select  idesessionuuid from targets;"
cursor1.execute(SQL)
SQL = "Select  idesessionuuid from testcases;"
cursor2.execute(SQL)
vc_id=[]
target_id=[]
testcases_id=[]
for row in cursor:
	vc_id.append(row[0])
for row in cursor1:
	target_id.append(row[0])
for row in cursor2:
	testcases_id.append(row[0])

vc_id=set(vc_id)
target_id=set(target_id)
testcases_id=set(testcases_id)
print len(testcases_id)
matched = vc_id & target_id
matched = list(matched)
matched_git_testcases= vc_id & testcases_id
matched_git_testcases= list(matched_git_testcases)
print len(matched_git_testcases)

cursor.close()
cursor1.close()
cursor2.close()

cursor = conn.cursor()
SQL = "Select * from vctypes"
cursor.execute(SQL)
vc_dict={}
for row in cursor:
	vc_dict[int(row[0])] = row[1]
cursor.close()

#Lets see what time of day developers do various actions like build, test and git actions.
"""
cursor = conn.cursor()
cursor1=conn.cursor()
cursor2=conn.cursor()
SQL="Select triggeredat,successful from targets;"
SQL1="Select executedat,actiontype from vc_action"
SQL2 = "Select triggeredat,result from testcases;"
cursor.execute(SQL)
cursor1.execute(SQL1)
cursor2.execute(SQL2)

times={'early_morning':0,'morning':0,'afternoon':0,'evening':0,'night':0,'late night':0}
"""
"""
early_morning: 06-08:59Hrs
morning:09-11:59Hrs
afternoon:12-15:59
evening: 16-18:59
night:19-21:59
latenight: 22-05:59

"""
"""
times={'early_morning':0,'morning':0,'afternoon':0,'evening':0,'night':0,'late night':0}
for row in cursor1:
	#if int(row[1])==0 or int(row[1])==1 or int(row[1])==4:
	#	continue 
	if not (int(row[1])==7):
		continue
	triggerTime= int(re.sub("[^0-9]", "", row[0][0:19])[-6:][0:2])
	if triggerTime >6 and triggerTime <9:
		times['early_morning'] +=1
	elif triggerTime >8 and triggerTime <12:
		times['morning'] +=1
	elif triggerTime >11 and triggerTime <16:
		times['afternoon'] +=1
	elif triggerTime >15 and triggerTime <19:
		times['evening'] +=1
	elif triggerTime >18 and triggerTime <22:
		times['night'] +=1
	else:
		#print triggerTime
		times['late night'] +=1


A= times.keys()
B=times.values()
#print A
#print B
plt.figure(figsize=(16,14))
sns.set()
sns.set_style("dark")
sns.set_style("white")
x_coordinates = np.arange(len(times))
plt.bar(x_coordinates, B, align='center',color='#F39C12')
plt.xticks(x_coordinates,A)
plt.xticks(rotation=90)
plt.title("When Developers Merge their code")
plt.xlabel('Time of the Day')
plt.ylabel('Count ')
plt.savefig("MergeCode_times.png", dpi=300)


cursor.close()
cursor1.close()
cursor2.close()
"""



cursor = conn.cursor()
cursor1=conn.cursor()
cursor2=conn.cursor()
SQL="Select idesessionuuid,triggeredat,successful from targets;"
SQL1="Select idesessionuuid,executedat,actiontype from vc_action"
SQL2 = "Select idesessionuuid,triggeredat,result from testcases;"
cursor.execute(SQL)
cursor1.execute(SQL1)
cursor2.execute(SQL2)

git_data={}
git_count=0
for row in cursor1:
	if row[0] in matched_git_testcases:
		git_count+=1
		if row[0] in git_data:
			git_data[row[0]].append([re.sub("[^0-9]", "", row[1][0:19]),row[2]])
		else:
			git_data[row[0]]=[[re.sub("[^0-9]", "", row[1][0:19]),row[2]]]



test_data={}
test_count=0
for row in cursor2:
	if row[0] in matched_git_testcases:
		test_count+=1
		if row[0] in test_data:
			test_data[row[0]].append([re.sub("[^0-9]", "", row[1][0:19]),row[2]])
		else:
			test_data[row[0]]=[[re.sub("[^0-9]", "", row[1][0:19]),int(row[2])]]

print len(matched_git_testcases)
print len(git_data)
print len(test_data)
print git_count
print test_count
from datetime import datetime, date, time

git_action =[]
global_minimum =0
count_of_tests=0
times=[]
under_one_minute =0
under_one_hour=0
temp_count=0
i=1
for id1 in matched_git_testcases:
	for test in test_data[id1]:
		#Running for Successful test cases.
		if (test[1] == 1):
			continue
		print i
		i+=1
		flag=False
		a= (test[0])
		time_of_test =datetime(int(a[0:4]),int(a[4:6]),int(a[6:8]),int(a[8:10]),int(a[10:12]),int(a[12:14]))
		minimum=9999999999
		minimum_git_action=""
		for git in git_data[id1]:
			a= (git[0])
			time_of_git =datetime(int(a[0:4]),int(a[4:6]),int(a[6:8]),int(a[8:10]),int(a[10:12]),int(a[12:14]))
			if time_of_git > time_of_test:
				flag=True
				diff = (time_of_git - time_of_test).total_seconds()
				if minimum >diff:
					minimum=diff
					minimum_git_action=vc_dict[int(git[1])]
		
		if flag:
			times.append(minimum)
			if minimum <60:
				under_one_minute+=1	
			if minimum<3600:
				under_one_hour+=1
			global_minimum+= minimum
			git_action.append(minimum_git_action)
			count_of_tests+=1


print test_count
print count_of_tests
print len(git_action)

print "under_one_minute"
print under_one_minute
print "under_one_hour"
print under_one_hour
print "average time for git action in hours"
global_minimum= global_minimum/(float(count_of_tests))
print global_minimum/3600
print "number of times git followed by a Failed test"
print count_of_tests

plot=plot_bar_from_counter(git_action)
plt.xticks(rotation=90)
plot.title("Most Common Git action after a Failed test")
plt.xlabel('Git Action')
plt.ylabel('Count ')
plot.savefig("git_action_after_FailedTest.png", dpi=300)

#Plot for time difference.
times=[i for i in times if i <11000]
plt.figure()
plt.hist(times, normed=False,histtype='bar',bins=100,color='#4A235A')
plt.title("Histogram showing time delta between a Failed TestCase and Next Git action")
plt.xlabel('time in seconds')
plt.ylabel('Frequency ')
plt.savefig("Variation_timeofGitaction_after_TestCaseFail.png", dpi=300)







