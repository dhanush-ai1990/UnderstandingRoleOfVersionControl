#Progrom for collecting stats from msr challenge data 2018.
import sqlite3
from collections import Counter
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar_from_counter(data):
	""""
	This function creates a bar plot from a counter.

	:param counter: This is a counter object, a dictionary with the item as the key
	 and the frequency as the value
	:param ax: an axis of matplotlib
	:return: the axis wit the object in it
	"""
	counter= Counter(data)
	plt.figure(figsize=(12,10))
	sns.set()
	sns.set_style("dark")
	sns.set_style("white")


	frequencies = counter.values()
	names = counter.keys()
	x_coordinates = np.arange(len(counter))
	plt.bar(x_coordinates, frequencies, align='center',color='#CD5C5C')
	plt.xticks(x_coordinates,names)
	return plt




def user_info():
	db_file='/Volumes/LLL/events.db'
	conn = sqlite3.connect(db_file)
	cursor = conn.cursor()
	SQL = "Select  * from users;"
	cursor.execute(SQL)
	positions ={}
	edu ={}
	positions[0]=0;positions[1]=0;positions[2]=0;positions[3]=0;positions[4]=0;positions[5]=0;
	edu[0]=0;edu[1]=0;edu[2]=0;edu[3]=0;edu[4]=0;edu[5]=0;edu[6]=0;
	progLevel ={}
	progLevel['beg'] =0
	progLevel['mid'] =0
	progLevel['high']=0
	progLevelid ={}
	progLevelid['beg'] =[]
	progLevelid['mid'] =[]
	progLevelid['high']=[]
	teamsolo1=0
	teamsmall1=0
	teamMedium1=0
	teamLarge1=0
	for row in cursor:
		profileid=row[0]
		education= row[1]
		edu[int(education)]+=1
		position=row[2]
		positions[int(position)]+=1
		projectscourses=row[3]
		projectspersonal=row[4]
		projectsSmall= row[5]
		projectsmedium = row[6]
		projectsLarge = row[7]
		teamsolo=int(row[8])
		teamsmall=int(row[9])
		teamMedium=int(row[10])
		teamLarge=int(row[11])
		codereviews=row[12]
		ProgLevel= int(row[13])
		userid=row[16]
		if ProgLevel >5:
			progLevel['high']+=1
			progLevelid['high'].append(userid)
			progLevelid['high'].append(profileid)


		elif ProgLevel >2:
			progLevel['mid']+=1
			progLevelid['mid'].append(userid)
			progLevelid['mid'].append(profileid)

		else:
			progLevel['beg']+=1
			progLevelid['beg'].append(userid)
			progLevelid['beg'].append(profileid)
			if teamsolo>0:
				teamsolo1+=1
			if teamsmall>0:
				teamsmall1+=1
			if teamMedium>0:
				teamMedium1+=1
			if teamLarge>0:
				teamLarge1+=1

		progCsharp=row[14]

	#print (progLevel)
	#print teamsolo1
	#print teamsmall1
	#print teamMedium1
	#print teamLarge1
	conn.close()
	return progLevelid


def built_targets(exp):
	"""
	"vsBuildActionBuild" -12662 are built events
	"vsBuildActionRebuildAll" -639
	"vsBuildActionClean" -263
	"vsBuildActionDeploy" -9
	"""

	"""
	"Debug"
	"Release"
	"Development"
	"DLL-Import Release"
	"Release with CouchDb"
	"Debug with CouchDb"
	"ReleaseWithCouchDb"
	"DebugWithCouchDb"
	"QA"
	"release"
	"DebugNet45"
	"staging"
	"produccion"
	"Debug-Any-CPU"
	"Debug_All"
	"Debug_IHE"
	"Staging"
	"Live"
	"CodeAnalysis"
	"test_int"
	"Local.Debug"
	"""
	experienced=[]
	experienced_success=[]
	mid=[]
	mid_success=[]
	beg=[]
	beg_success=[]
	total =[]
	success=[]
	db_file='/Volumes/LLL/events.db'
	conn = sqlite3.connect(db_file)
	cursor = conn.cursor()
	SQL = "Select  * from targetview;"
	cursor.execute(SQL)
	count=0
	for row in cursor:
		sessionid=row[0]
		conf=row[1]
		total.append(conf)
		succ =int(row[2])
		success.append(succ)
		if sessionid in exp['high']:
			experienced.append(conf)
			experienced_success.append(succ)
		elif sessionid in exp['mid']:
			mid.append(conf)
			mid_success.append(succ)
		elif sessionid in exp['beg']:
			beg.append(conf)
			beg_success.append(succ)
		else:
			count+=1
	#print Counter(total)
	plot=plot_bar_from_counter(total)
	plt.xticks(rotation=90)
	plot.title("Common Build Configurations")
	plt.xlabel('Build Configuration')
	plt.ylabel('Count ')
	plot.savefig("BuildConfiguration.png", dpi=300)
	print Counter(success)
	conn.close()


def versioncontrol():
	pass





db_file='/Volumes/LLL/events.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
SQL = "Select * from vctypes"
cursor.execute(SQL)
vc_dict={}
for row in cursor:
	vc_dict[int(row[0])] = row[1]
cursor.close()











#userids=user_info()
#built_targets(userids)



cursor = conn.cursor()
cursor1=conn.cursor()
SQL = "Select  idesessionuuid from vc_action;"
cursor.execute(SQL)
SQL = "Select  idesessionuuid from targets;"
cursor1.execute(SQL)
vc_id=[]
target_id=[]
for row in cursor:
	vc_id.append(row[0])
for row in cursor1:
	target_id.append(row[0])

vc_id=set(vc_id)
target_id=set(target_id)
matched = vc_id & target_id
matched = list(matched)
#print len(matched)

cursor.close()


cursor1.close()



#print vc_dict


cursor = conn.cursor()

SQL = "Select  idesessionuuid,actiontype from vc_action order by idesessionuuid ASC;"
cursor.execute(SQL)
action=[]
id1=[]
hold= ""
hold_sequence =""
sequence =[]
count=0
first =[]
last=[]
prev =""
number_of_time=0
last_three =[]
last_3 =[]
print "------------------------------------"
for row in cursor:
	if row[0] == hold:
		last_3.append(vc_dict[int(row[1])])
		prev = vc_dict[int(row[1])]
		if count <4:
			count+=1
			hold_sequence= hold_sequence +"->"+vc_dict[int(row[1])]
	else:
		if len(last_3) <3:
			last_three.append(last_3)
		else:
			last_three.append(last_3[-3:])
		last_3 =[]
		last_3.append(vc_dict[int(row[1])])
		first.append(vc_dict[int(row[1])])
		last.append(prev)
		sequence.append(hold_sequence)
		hold_sequence=""
		hold=row[0]
		hold_sequence= hold_sequence +"->"+vc_dict[int(row[1])]
		count=1
		prev =vc_dict[int(row[1])]
		id1.append(row[0])
	action.append(vc_dict[int(row[1])])


c= Counter(action)
counter_selected = 	c.most_common(10)
A=[]
B=[]
for item in counter_selected:
	A.append(item[0])
	B.append(item[1])
	#print item[0]+ "   "+ str(item[1])


plt.figure(figsize=(16,14))
sns.set()
sns.set_style("dark")
sns.set_style("white")
x_coordinates = np.arange(len(A))
plt.bar(x_coordinates, B, align='center',color='#117A65')
plt.xticks(x_coordinates,A)
plt.xticks(rotation=90)
plt.title("Most Common Git actions")
plt.xlabel('Git Action')
plt.ylabel('Count ')
plt.savefig("Common_git_actions_in_vc.png", dpi=300)




#print len(id1)
c= Counter(sequence)
counter_selected = 	c.most_common(10)
for item in counter_selected:
	print item[0]+ "   "+ str(item[1])
print("first")

c= Counter(first)
counter_selected = 	c.most_common(5)
A=[]
B=[]
for item in counter_selected:
	A.append(item[0])
	B.append(item[1])
	print item[0]+ "   "+ str(item[1])

plt.figure(figsize=(16,14))
sns.set()
sns.set_style("dark")
sns.set_style("white")
x_coordinates = np.arange(len(A))
plt.bar(x_coordinates, B, align='center',color='#117A65')
plt.xticks(x_coordinates,A)
plt.xticks(rotation=90)
plt.title("First Git action after starting new IDE session")
plt.xlabel('Git Action')
plt.ylabel('Count ')
plt.savefig("first_action.png", dpi=300)





print ("last")
print len(last)
c= Counter(last)
counter_selected = 	c.most_common(5)
print counter_selected



A=[]
B=[]
for item in counter_selected:
	A.append(item[0])
	B.append(item[1])
	print item[0]+ "   "+ str(item[1])

plt.figure(figsize=(16,14))
sns.set()
sns.set_style("dark")
sns.set_style("white")
x_coordinates = np.arange(len(A))
plt.bar(x_coordinates, B, align='center',color='#117A65')
plt.xticks(x_coordinates,A)
plt.xticks(rotation=90)
plt.title("Last Git action of a IDE session")
plt.xlabel('Git Action')
plt.ylabel('Count ')
plt.savefig("last_action.png", dpi=300)

print len(last_three)
temp=[]
for item in last_three:
	hold_sequence =""
	for git in item:
		hold_sequence=hold_sequence +"->"+git
	temp.append(hold_sequence)


c= Counter(temp)
counter_selected = 	c.most_common(5)
print counter_selected

cursor.close()
"""
#We have the sessions which are common with a version control and build target entry in matched.
cursor = conn.cursor()

SQL = "Select * from vc_action"
cursor.execute(SQL)

git_data={}
for row in cursor:
	if row[0] in matched:
		if row[0] in git_data:
			git_data[row[0]].append([re.sub("[^0-9]", "", row[3][0:19]),row[4]])
		else:
			git_data[row[0]]=[[re.sub("[^0-9]", "", row[3][0:19]),row[4]]]


cursor.close

cursor = conn.cursor()

SQL = "Select idesessionuuid,startedAt,successful from targets"
cursor.execute(SQL)
build_data={}
build_count=0
for row in cursor:
	if row[0] in matched:
		build_count+=1
		if row[0] in build_data:
			build_data[row[0]].append([re.sub("[^0-9]", "", row[1][0:19]),row[2]])
		else:
			build_data[row[0]]=[[re.sub("[^0-9]", "", row[1][0:19]),int(row[2])]]

#print len(matched)
#print len(git_data)
#print len(build_data)

from datetime import datetime, date, time

git_action =[]
global_minimum =0
count_of_builds=0
times=[]
under_one_minute =0
under_one_hour=0
temp_count=0
for id1 in matched:
	failed= False
	found_success_after_fail=False
	for build in build_data[id1]:
		flag=False
		a= (build[0])
		time_of_build =datetime(int(a[0:4]),int(a[4:6]),int(a[6:8]),int(a[8:10]),int(a[10:12]),int(a[12:14]))
		minimum=9999999999
		minimum_git_action=""
		if int(build[1]) ==0:
			failed= True
		if not failed:
			continue

		if found_success_after_fail:
			continue
		if failed and (int(build[1]) ==1):
			found_success_after_fail= True
		temp_count+=1
		for git in git_data[id1]:
			a= (git[0])
			time_of_git =datetime(int(a[0:4]),int(a[4:6]),int(a[6:8]),int(a[8:10]),int(a[10:12]),int(a[12:14]))
			if time_of_git > time_of_build:
				flag=True
				diff = (time_of_git - time_of_build).total_seconds()
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
			count_of_builds+=1
#print build_count
#print count_of_builds

#print len(git_action)

print "under_one_minute"
print under_one_minute
print "under_one_hour"
print under_one_hour
print "average time for git action in hours"
global_minimum= global_minimum/(float(count_of_builds))
print global_minimum/3600
print "number of times git followed by Successful build"
print count_of_builds

plot=plot_bar_from_counter(git_action)
plt.xticks(rotation=90)
plot.title("Most Common Git action after a Unsuccessful Build")
plt.xlabel('Git Action')
plt.ylabel('Count ')
plot.savefig("git_action_after_Success_after_fail.png", dpi=300)

#Plot for time difference.
times=[i for i in times if i <11000]
plt.figure()
plt.hist(times, normed=False,histtype='bar',bins=100,color='#4A235A')
plt.title("Histogram showing time delta between a Unsuccessful Build and Next Git action")
plt.xlabel('time in seconds')
plt.ylabel('Frequency ')
plt.savefig("Variation_timeofGitaction_after_BuildUnSucess.png", dpi=300)
"""








