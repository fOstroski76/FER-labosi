import argparse
import heapq

# definitions

class Node :

    def __init__(self, state, cost, neighbourNodes,parentNode=None) :
        self.state = state
        self.cost = cost
        self.neighbourNodes = neighbourNodes # "succ"
        self.parentNode = parentNode
        self.heuristics = 0

    def __lt__(self, other) :
        return self.cost < other.cost

def run_bfs(startingState,endGoalStates,statesCostsEtcDict) :

    print("# BFS")
    open = list()
    visited = set()
    
    goalReached = list()

    for key in  statesCostsEtcDict.keys() :
        statesCostsEtcDict[key].sort() # heapify skida jednu sekundu?
        node =  Node(key,0,statesCostsEtcDict[key],None)
        
        if node.state == startingState :
            open.append(node)


    while len(open) != 0 :

        popped = open.pop(0)
        a = popped.state
        visited.add(a)
        
        if popped.state in endGoalStates :
            goalReached.append(popped)

            break
        
        

        for el in popped.neighbourNodes :
            
            obj = Node(el[0],0,statesCostsEtcDict[el[0]],None)
            obj.cost = obj.cost + int(el[1])
            
            obj.parentNode = popped
            obj.cost = obj.cost + obj.parentNode.cost
            
            if obj.state not in visited :
                open.append(obj)
            
        
    try :
        print("[FOUND_SOLUTION]: yes")   

        path = list()
        goalStateCopy = goalReached[0]
        path.append(goalReached[0].state)
        
        while goalStateCopy.parentNode :
                goalStateCopy = goalStateCopy.parentNode
                path.append(goalStateCopy.state)
                
        pathway = (" => ".join(path[::-1]))
    
    except (IndexError) :
        print("[FOUND_SOLUTION]: no")
    
    print("[STATES_VISITED]: {}".format(len(visited)))
    print("[PATH_LENGTH]: {}".format(len(path)))
    print("[TOTAL_COST]: {}".format('%.01f' % goalReached[0].cost))
    print("[PATH]: {}".format(pathway))

    return goalReached[0].cost

def run_ucs(startingState,endGoalStates,statesCostsEtcDict,wantOutputs) :
    if wantOutputs :
        print("# UCS")

    open = list()
    visited = set()
    
    goalReached = list()

    for key in  statesCostsEtcDict.keys() :
        node =  Node(key,0,statesCostsEtcDict[key],None)
        
        if node.state == startingState :
            open.append(node)

    heapq.heapify(open)
    
    while len(open) != 0 :

        popped = heapq.heappop(open) 
        a = popped.state
        visited.add(a)
        
        if popped.state in endGoalStates :
            goalReached.append(popped)

            break
        
        for el in popped.neighbourNodes :
            
            obj = Node(el[0],0,statesCostsEtcDict[el[0]],None)
            obj.cost = obj.cost + int(el[1])
            obj.parentNode = popped
            obj.cost = obj.cost + obj.parentNode.cost
            
            if obj.state not in visited :
                heapq.heappush(open,obj) #open.append(obj)

    try :
        if wantOutputs:
            print("[FOUND_SOLUTION]: yes")   

        path = list()
        goalStateCopy = goalReached[0]
        path.append(goalReached[0].state)
        
        while goalStateCopy.parentNode :

                goalStateCopy = goalStateCopy.parentNode
                path.append(goalStateCopy.state)
                
        pathway = (" => ".join(path[::-1]))
    
    except (IndexError) :
        print("[FOUND_SOLUTION]: no")
    
    if wantOutputs :
        print("[STATES_VISITED]: {}".format(len(visited)))
        print("[PATH_LENGTH]: {}".format(len(path)))
        print("[TOTAL_COST]: {}".format('%.01f' % goalReached[0].cost))
        print("[PATH]: {}".format(pathway))

    return goalReached[0].cost

def run_astar(startingState,endGoalStates,statesCostsEtcDict,heuristicsDict) :
    
    open = list()
    visited = list()
    goalReached = list()
            
    for key in  statesCostsEtcDict.keys() :
        statesCostsEtcDict[key].sort()
        node =  Node(key,0,statesCostsEtcDict[key],None)
        node.heuristics = heuristicsDict[node.state]
     
        if node.state == startingState :
            open.append(node)


    heapq.heapify(open)
    
    while len(open) != 0 :

        popped = open.pop(0)
        a = popped.state
        visited.append(popped)
        
        if popped.state in endGoalStates :
            goalReached.append(popped)

            break
        
    
        for el in popped.neighbourNodes :
            
            obj = Node(el[0],0,statesCostsEtcDict[el[0]],None)
            obj.heuristics = heuristicsDict[obj.state]
            obj.cost = obj.cost + int(el[1])
            obj.parentNode = popped
            obj.cost = obj.cost + obj.parentNode.cost 
            
            for e in visited + open :
                if e.state == obj.state :
                    if e.cost < obj.cost :
                        pass

                    else :
                        try :
                            open.remove(e)
                        except (IndexError, ValueError) :
                            visited.remove(e)
            

            open.append(obj)
            open = heapq.nsmallest(len(open), open, key= lambda obj: (obj.cost + int(obj.heuristics)))
            
    try :
        print("[FOUND_SOLUTION]: yes")   

        path = list()
        goalStateCopy = goalReached[0]
        path.append(goalReached[0].state)
        

        while goalStateCopy.parentNode :

                goalStateCopy = goalStateCopy.parentNode
                path.append(goalStateCopy.state)
                
        pathway = (" => ".join(path[::-1]))
    
    except (IndexError) :
        print("[FOUND_SOLUTION]: no")
    
    print("[STATES_VISITED]: {}".format(len(visited)))
    print("[PATH_LENGTH]: {}".format(len(path)))
    print("[TOTAL_COST]: {}".format('%.01f' % goalReached[0].cost))
    print("[PATH]: {}".format(pathway))

    return goalReached[0].cost

# parsing the input

parser = argparse.ArgumentParser()

parser.add_argument('--alg',type=str,choices=['bfs','ucs','astar'])
parser.add_argument('--ss',type=str)
parser.add_argument('--h',type=str)
parser.add_argument('--check-optimistic',action='store_true')
parser.add_argument('--check-consistent',action='store_true')

args = parser.parse_args()

# initialisation of other variables

run_optimisation_check = False
run_consistency_check = False

startingState = None
endGoalStates = set()

heuristicsDict = dict()
statesCostsEtcDict = dict()

# processing the args

if args.ss :
    with open(args.ss,'r') as searchSpace :
        contents = searchSpace.readlines()

        firstChecked = False
        secondChecked = False

        for line in contents :
            if line.startswith("#") :
                pass

            elif firstChecked == False or secondChecked == False :

                if firstChecked == True  and secondChecked == False :
                    endGoalStates = line.strip().split(" ")
                    secondChecked = True
                    

                if firstChecked == False :
                    startingState = line.strip()
                    firstChecked = True
                    
            else :
               tempList = list() 
               if line.split(":")[1] != '\n' :
                for el in line.split(":")[1].strip().split(" ") :
                   
                    tempTuple = (el.split(",")[0],el.split(",")[1])
                    tempList.append(tempTuple)

               statesCostsEtcDict[line.split(":")[0]] = tempList
                

if args.h :
    with open(args.h,'r') as heuristics :
        contents2 = heuristics.readlines()
        for line in contents2 :
            if line.startswith("#") :
                pass

            else :
                heuristicsDict[line.split(":")[0]] = line.split(":")[1].strip()
        

if args.alg :

    if args.alg == 'bfs'  :
        run_bfs(startingState,endGoalStates,statesCostsEtcDict)
    
    elif args.alg == 'ucs' :
        run_ucs(startingState,endGoalStates,statesCostsEtcDict,wantOutputs=True)
    
    elif args.alg == 'astar' :
        print("# A-STAR",args.h)
        run_astar(startingState,endGoalStates,statesCostsEtcDict,heuristicsDict)

if args.check_optimistic :
    print("# HEURISTIC-OPTIMISTIC {}".format(args.ss))

    allStates = list()
    for key in statesCostsEtcDict.keys() :
        allStates.append(key)

    isOptimistic = True
    for state in allStates :
        oneCost = run_ucs(startingState=state,endGoalStates=endGoalStates,statesCostsEtcDict=statesCostsEtcDict,wantOutputs=False)
        if  int(heuristicsDict[state])  <= int(oneCost) :
            print("[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(state,'%.01f' % int(heuristicsDict[state]),'%.01f' % int(oneCost)))

        else :
            isOptimistic = False
            print("[CONDITION]: [ERR] h({}) <= h*: {} <= {}".format(state,'%.01f' % int(heuristicsDict[state]),'%.01f' % int(oneCost)))
    
    if isOptimistic :
        print("[CONCLUSION]: Heuristic is optimistic.")
    
    else :
        print("[CONCLUSION]: Heuristic is not optimistic.")

if args.check_consistent :
    print("# HEURISTIC-CONSISTENT {}".format(args.ss))

    isConsistent = True
    
    for key in statesCostsEtcDict.keys() :
        for tuple in statesCostsEtcDict[key] :

            if int(heuristicsDict[key]) <= int(int(tuple[1]) + int(heuristicsDict[tuple[0]])) :
                print("[CONDITION]: [OK] h({}) <= h({}) + c: {} <= {} + {}".format(key,tuple[0],'%.01f' % int(heuristicsDict[key]),'%.01f' % int(heuristicsDict[tuple[0]]),'%.01f' % int (tuple[1])))

            else :
                isConsistent = False
                print("[CONDITION]: [ERR] h({}) <= h({}) + c: {} <= {} + {}".format(key,tuple[0],'%.01f' % int(heuristicsDict[key]),'%.01f' % int(heuristicsDict[tuple[0]]),'%.01f' % int (tuple[1])))
    
    
    if isConsistent :
        print("[CONCLUSION]: Heuristic is consistent.")

    else :
        print("[CONCLUSION]: Heuristic is not consistent.")
  