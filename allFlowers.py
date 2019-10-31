#!/usr/bin/python
# This code will provide a python function that will return an ordered 
# list of distinct rotation systems for an n flower given n as an input.

# Need to make all the rotations 0 based. First vertex is labeled 0
# and first edge is labeled 0.

# This function rotates a list to the left by n thus, term n becomes 
# term 0, term m becomes term m - n and term 0 becomes term len - n.
def rotate(inputList,n):
	List1 = inputList[0:n];
	List2 = inputList[n:len(inputList)];
	List2.extend(List1);
	return List2;

# Temporarily defined variable to see the number of each genus for
# each flower.
totalCount = 0;
ourGenus = 2;

# We begin by writing a function to place a rotation system in proper
# form. We define "proper form" in such a way that two rotation systems
# on a flower are equivalent iff their proper form representations are
# identical.

def makeProper(inputList):
	temp = min(inputList);
	# mins will be an array holding all minimum indexes of inputList
	mins = [];
	for i in range(0,len(inputList)):
		if (inputList[i] == temp):
			mins.append(i);
	# proper form has the smallest interval in the front thus any 
	# rotation of the rotation system with one of the mins at the
	# beginning may be the proper form.
	properForm = inputList;
	for i in range(0,len(mins)):
		temp2 = rotate(inputList,mins[i]);
		for j in range(0,len(temp2)):
			if (properForm[j] > temp2[j]):
				properForm = temp2;
				break;
			if (properForm[j] < temp2[j]):
				break;
	# print properForm;
	return properForm;

# The following function converts a rotation system to a gap sequence
# representation.
def rottogap(inputList):
	temp = [0]*len(inputList);
	for i in range(0,len(inputList)):
		if (temp[i] == 0):
			for j in range(i+1,len(inputList)):
				if (inputList[j] == inputList[i]):
					temp2 = j - i;
					break;
			temp[i] = temp2;
			temp[i+temp2] = len(inputList) - temp2;
	# print temp;
	return temp;

# The following function converts a gap sequence representation to a 
# rotation system.
def gaptorot(inputList):
	temp = [0]*len(inputList);
	current = 1;
	for i in range(0,len(inputList)):
		if (temp[i] == 0):
			temp[i] = current;
			temp[i+inputList[i]] = current;
			current = current+1;
	# print temp;
	return temp;

# Transforms a rotation to a reduced gap sequence representation.
def rottoredgap(inputList):
	newList = inputList[:];
	temp = [];
	for i in range(0,len(newList)):
		if (newList[i] != -1):
			for j in range(i+1,len(newList)):
				if (newList[j] == newList[i]):
					temp.append(j - i);
					newList[j] = -1;
					newList[i] = -1;
					break;
	# print temp;
	return temp;

# Transforms a gap representation of a rotation system to a reduced gap
# representation.
def gaptoredgap(inputList):
	newList = inputList[:];
	temp = [];
	for i in range(0,len(newList)):
		if (newList[i] != 0):
			temp.append(newList[i]);
			newList[i + newList[i]] = 0;
			newList[i] = 0;
	# print temp;
	return temp;

# Transforms a reduced gap to a rotation system	
def redgaptorot(inputList):
	rotation = [0]*(len(inputList)*2);
	current = 0;
	index = 1;
	for i in range(0, len(inputList)):
		while (rotation[current] != 0):
			current += 1;
		rotation[current] = index;
		rotation[current+inputList[i]] = index;
		index += 1;
	# print rotation;
	return rotation;

# Transforms a reduced gap sequence to a gap sequence
def redgaptogap(inputList):
	gap = [0]*(len(inputList)*2);
	current = 0;
	for i in range(0,len(inputList)):
		while (gap[current] != 0):
			current += 1;
		gap[current] = inputList[i];
		gap[current + gap[current]] = 2*len(inputList) - gap[current];
	# print gap;
	return gap;

# The following function is the first tricky function employed for the 
# overall purpose of finding all rotation systems seperating a given 
# genus surface. The input of this function is an integer that is 2*n 
# where n is the number of leaves of the flower graph under consideration.
# The function below will traverse the tree of all possible rotation 
# systems of the n flower and print them out. What makes this function so
# tricky is it has both iterative and recursive components. Also, we are
# able to prune the tree with our code which also serves to obfuscate the 
# code. The search is of rotation systems in reduced gap form because 
# this form provides us with initially the smallest number of 
# possibilities. Nevertheless some of the rotation systems returned are
# repeats.
class AllRots(object):
    def __init__(*arg):
        self = arg[0]
        self.genus = ourGenus
        if arg[1]:
            flowerNum = arg[1];
        if arg[2]:
            self.genus = arg[2];
        self.current = [0]*flowerNum;
        self.current[0] = 1;
        self.totalCount = 0;
        self.flowerNum = flowerNum;
        self.genusCalc = [0]*4*flowerNum;
        self.minSorted = [];
        for j in range(0, (flowerNum + 1)/2):
   	    # This is going to be a smallest to largest gap 
	    # depth first search. So we will initialize the
	    # rotation vector as such.
            self.current[0] = 1 + j*2;
            level = 1;
            self.number = j + 1;
            rotation = [0]*2*flowerNum;
            rotation[0] = 1;
            rotation[self.current[0]] = 1;
            spot = 0;
            self.findAllRedGap(rotation,spot,level);	
	# Now we will define a recursive subfunction. We will want 
	# rotation, and spot to update recursively,
	# but number, current, and level to update iteratively.
        def findAllRedGap(self,rotation, spot,level):
            newrot = rotation[:];
            if (level == len(self.current)):
                # We are done, we print the results. To be 
                # replaced with our main logic.
                #print self.current;
                finalTemp = redgaptogap(self.current);
                if (self.getGenus(finalTemp) == self.genus):
                    self.totalCount += 1;
                    self.minSorted.append(makeProper(finalTemp));
                    return;
            # Here we will attempt to increment the current level
            temp = self.current[0];
            while (newrot[spot] != 0):
                spot += 1;
            while ((temp <= self.flowerNum*2 - self.current[0])and(spot + temp < len(newrot))and(newrot[spot+temp] != 0)):
                temp += 2;
            if (temp + spot < len(newrot)): 
                newrot[spot] = 1;
                newrot[spot + temp] = 1;
                self.number = 1;
                self.current[level] = temp;
                level += 1;
                self.findAllRedGap(newrot,spot,level);
            else :
                return;	
            for i in range(0,len(self.current) - level):
                # Here we will attempt to increment number
                if (level + self.number - 1 == len(self.current)):
                    self.number = 1;
                    return;
                temp = self.current[level - 1] + 2;
                self.number += 1;
                newrot[spot + self.current[level - 1]] = 0;
            while (spot + temp < len(newrot))and(newrot[spot + temp] != 0):
                temp += 2;
                if (spot + temp < len(newrot)):
                    self.current[level - 1] = temp;
                    newrot[spot + temp] = 1;
                    self.findAllRedGap(newrot,spot,level);
                else:
                    return;

    # converts a Gap sequence to a long in base 2*flowernumber. This is to
    # facilitate the sorting mechanism. We will try this for now, if this doesn't
    # work, we will make our very own indexed list data structure.
    # Sorts the results and removes duplicates
    def sortResults(self):
        newResults = [];
        self.minSorted = sorted(self.minSorted);
        for i in range(0,len(self.minSorted)):
            if (i == len(self.minSorted) - 1) or (cmp(self.minSorted[i],self.minSorted[i+1]) != 0):
                newResults.append(self.minSorted[i]);
            self.minSorted = newResults;

    def getGenus(self, gapSeq):
        genus = 0;
        current = 1;
        for k in range(0,self.flowerNum*4):
            if ( k % 2 == 0):
                self.genusCalc[k] = gapSeq[k/2];
            else :
                self.genusCalc[k] = 0;
            while current < 4*self.flowerNum:
                cycle = current;
                while self.genusCalc[cycle] == 0:
                    self.genusCalc[cycle] = 1;
                    cycle = (cycle + (self.genusCalc[(cycle+1)%(4*self.flowerNum)]+1)*2)%(4*self.flowerNum);
                genus += 1;
                while (current < 4*self.flowerNum) and (self.genusCalc[current] != 0):
                    current += 2;
        return (self.flowerNum - 1 + genus)/2 -1;	


			
	
input = [0,2,3,0,5,3,2,4,4,5];
print("Proper");
makeProper(input);
print("rotation to gap");
rottogap(input);
print("rotation to reduced gap");
rottoredgap(input);
print("rotation to gap to reduced gap");
gaptoredgap(rottogap(input));
print("rotation to gap to proper to rotation");
gaptorot(makeProper(rottogap(input)));
print("rotation to reduced gap to rotation");
redgaptorot(rottoredgap(input));
print("rotation to reduced gap to gap to rotation");
gaptorot(redgaptogap(rottoredgap(input)));
print("Starting chaos:");
#myFlower = AllRots(12);
#myFlower.sortResults();
#print len(myFlower.minSorted);
