import re

with open('CPFW01_20190302_2322.conf', 'r') as f:
    data = f.read()

# find the vdom name in conf to a list
foundvdom = re.findall(r'\n*(config\svdom.*?\nconfig\ssystem\ssettings)\n*', data, re.M | re.S)
# find the content of each vdom to a list
foundcontent = re.findall(r'\n*(config\svdom.*?\nend\nend\n)\n*', data, re.M | re.S)

# create a vdom list
vdomList=[]
for i in range(0, len(foundvdom)):
	name = foundvdom[i].split('\n')[1].rstrip()[5:]
	vdomList.append(name)

# write to each file
for i in range(1, len(foundcontent)+1):
	print vdomList[i-1]
	open(vdomList[i-1]+'.txt', 'w').write(foundcontent[i-1])