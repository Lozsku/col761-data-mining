import sys

input = sys.argv[1]
algo = sys.argv[2]
'''
    Given input format is
    #GraphId
    #nodes
    Series of node labels
    #edges
    Series of nodeid1 nodeid2 edgelabel
'''

file = open(input,"r")
if(algo=="GSPAN"):

    '''
        The format of graph for GSPAN algo is
        t # N
        v M L
        e P Q L
    '''
    outfile = open(r"gspan.txt","w+")
    graph_count = 0
    content = 0
    vertexid = 0
    dict = {} # map to assign nonnumeric labels a number
    curlabel = 0
    for line in file:

        if(line[len(line)-1] == "\n"):
            #print("HI "+ line)
            size = len(line)
            line = line[0:size-1]

        if(len(line) == 0):
            continue
        elif(line[0] == "#"):
            num = line[1:-1]
            outfile.write("t # "+ str(graph_count) + "\n")
            graph_count += 1
            vertexid = 0
        elif(line.isdigit()):
            if(content == 0):
                content = 1
            else:
                content = 0
        elif(content == 1):
            #reading vertices
            if(dict.get(line) == None):
                dict[line] = curlabel
                curlabel += 1
            
            outfile.write("v "+ str(vertexid) + " "+str(dict[line])+"\n")
            vertexid += 1
        elif(content == 0):
            #reading edges
            outfile.write("e "+ line + "\n")
    
    outfile.close()
    tempfile = open(r"gspan-graphs.txt","w+")
    tempfile.write(str(graph_count))
    tempfile.close()
elif(algo == "GASTON"):
    '''
        The format of graph for GASTON algo is
        t # N
        v M L
        e P Q L
    '''
    outfile = open(r"gaston.txt","w+")
    graph_count = 0
    content = 0
    vertexid = 0
    dict = {} # map to assign nonnumeric labels a number
    curlabel = 0
    for line in file:
        if(line[len(line)-1] == "\n"):
            #print("HI "+ line)
            size = len(line)
            line = line[0:size-1]

        
        if(len(line) == 0):
            continue
        elif(line[0] == "#"):
            num = line[1:-1]
            outfile.write("t # "+ str(graph_count) + "\n")
            graph_count += 1
            vertexid = 0
        elif(line.isdigit()):
            if(content == 0):
                content = 1
            else:
                content = 0
        elif(content == 1):
            #reading vertices
            if(dict.get(line) == None):
                dict[line] = curlabel
                curlabel += 1
            
            outfile.write("v "+ str(vertexid) + " "+str(dict[line])+"\n")
            vertexid+=1
        elif(content == 0):
            #reading edges
            outfile.write("e "+ line + "\n")
    
    outfile.close()
    tempfile = open(r"gaston-graphs.txt","w+")
    tempfile.write(str(graph_count))
    tempfile.close()


    # tempfile = open("gaston-graphs.txt","r")
    # for line in tempfile:
    #     count = int(line)
    #     break
    # print(count)
    # tempfile.close()

elif(algo == "FSG"):
    '''
        The format of graph for FSG algo is
        t
        v M L
        u P Q L
    '''
    outfile = open(r"fsg.txt","w+")
    graph_count = 0
    content = 0
    vertexid = 0
    dict = {} # map to assign nonnumeric labels a number
    curlabel = 0
    for line in file:
        if(line[len(line)-1] == "\n"):
            #print("HI "+ line)
            size = len(line)
            line = line[0:size-1]
        
        if(len(line) == 0):
            continue
        elif(line[0] == "#"):
            num = line[:-1]
            outfile.write("t\n")
            graph_count += 1
            vertexid = 0
        elif(line.isdigit()):
            if(content == 0):
                content = 1
            else:
                content = 0
        elif(content == 1):
            #reading vertices
            if(dict.get(line) == None):
                dict[line] = curlabel
                curlabel += 1
            
            outfile.write("v "+ str(vertexid) + " "+str(dict[line])+"\n")
            vertexid += 1
        elif(content == 0):
            #reading edges
            outfile.write("u "+ line + "\n")
    
    outfile.close()   
    tempfile = open(r"fsg-graphs.txt","w+")
    tempfile.write(str(graph_count))
    tempfile.close()    