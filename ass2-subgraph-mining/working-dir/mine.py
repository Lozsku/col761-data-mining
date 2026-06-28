import os
import time
import matplotlib.pyplot as plt
support_list = [5, 10, 25, 50, 95]

fsglist = []
gspanlist = []
gastonlist = []

for support in support_list:
    
    #execute the algo for FSG
    command = "./fsg -s " + str(support) + " " + "fsg1.txt"
    st = time.time()
    os.system(command)
    end = time.time()

    fsglist.append(end-st)

for support in support_list:
    
    #execute the algo for GASTON
    tempfile = open("gaston-graphs1.txt","r")
    for line in tempfile:
        count = int(line)
        break
    print(count)
    tempfile.close()
    supval = float(support*count/100)
    
    command = "./gaston " + str(supval)+ " gaston1.txt " + " gaston-output1.txt"
    st = time.time()
    os.system(command)
    end = time.time()
    gastonlist.append(end-st)
    

for support in support_list:
    
    #execute the algo for GSPAN
    supval = float(support/100)
    st = time.time()
    command = "./gSpan-64 -f gspan1.txt" + " -s " + str(supval) + " -o"
    os.system(command)
    end = time.time()
    gspanlist.append(end-st)

print(fsglist)
print(gspanlist)
print(gastonlist)

plt.plot(support_list,fsglist,label = "FSG")
plt.plot(support_list,gspanlist,label = "GSPAN")
plt.plot(support_list,gastonlist,label = "GASTON")
plt.xlabel("support")
plt.ylabel("Runtimes")
plt.title("Runtime vs Support for various algorithms")
plt.legend()
plt.savefig('runtime3.png')
