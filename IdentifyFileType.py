from os import listdir

mypath = input("Enter path: ")
file_list = listdir(mypath)
#print(file_list)

dark_list = list()
flat_list = list()
bias_list = list()
light_list = list()

for i in file_list:
    if i.find("Dark") >= 0 or i.find("dark") >=0:
        dark_list.append(i)
    elif i.find("Flat") >= 0 or i.find("flat") >= 0:
        flat_list.append(i)
    elif i.find("Bias") >= 0 or i.find("bias") >= 0:
        bias_list.append(i)
    else:
        light_list.append(i)

#print("dark elements:", dark_list)
elements = dict()
elements["dark"] = len(dark_list)
elements["bias"] = len(bias_list)
elements["flat"] = len(flat_list)
elements["light"] = len(light_list)

print("Found", elements["dark"], "dark images,", elements["bias"], "bias images,",
      elements["flat"], "flat images and", elements["light"], "light images.")