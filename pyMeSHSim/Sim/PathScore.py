# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
from copy import deepcopy
from .ICScore import InformationContent
import sys

class pathMethod(InformationContent):
    """This class implement the path based similarity."""
    def __init__(self):
        InformationContent.__init__(self)
        pass

    def pathSim(self, cui1=None, cui2=None):
        """Shortest path measurement."""
        if cui1 == cui2:
            return 1
        length = self.findShortestPath(cui1=cui1, cui2=cui2)
        if length < 0:
            return length
        else:
            return float(1)/length



    def findShortestPath(self, cui1=None, cui2=None):
        if cui1 == cui2:
            return 1
        visited1, visited2 = {}, {}
        concept1 = self.getMeSHConcept(cui=cui1)
        concept2 = self.getMeSHConcept(cui=cui2)
        stack1 = self.getRelated(concept=concept1)
        if stack1 is None:
            stack1 = []
        stack2 = self.getRelated(concept=concept2)
        if stack2 is None:
            stack2 = []

        #stack1 = deepcopy(rstack1)
        #stack2 = deepcopy(rstack2)

        directions1, directions2 = [], []
        relations1, relations2 = [], []
        paths1, paths2 = [], []
        pathLength1, pathLength2 = -1, -1

        for item in stack1:
            paths1.append([])
            directions1.append(0)
            relations1.append("PAR")

        for item in stack2:
            paths2.append([])
            directions2.append(0)
            relations2.append("PAR")

        while(len(stack1) >=1 or len(stack2)>=1):
            c1, c2 = "", ""
            path1, path2 = [], []
            direction1, direction2 = "", ""
            relation1, relation2 = "", ""
            #this is the most important variable
            tmpArray1, tmpArray2 = [], []
            distance1, distance2 = 0, 0
            cui1Flag, cui2Flag = 0, 0

            if len(stack1) >= 1:
                c1 = stack1.pop()
                path1 = paths1.pop()
                direction1 = directions1.pop()
                relation1 = relations1.pop()
                tmpArray1 = deepcopy(path1)
                tmpArray1.append(c1)
                distance1 = len(tmpArray1)
                cui1Flag = cui1Flag + 1

            if len(stack2) >= 1:
                c2 = stack2.pop()
                path2 = paths2.pop()
                direction2 = directions2.pop()
                relation2 = relations2.pop()
                tmpArray2 = deepcopy(path2)
                tmpArray2.append(c2)
                distance2 = len(tmpArray2)
                cui2Flag = cui2Flag + 1

            if c1 == cui2:
                pathLength1 = distance1 + 1
                if len(stack2 == 0):
                    return pathLength1
            if c2 == cui1:
                pathLength2 = distance2 + 1
                if len(stack1 == 0):
                    return pathLength2

            if pathLength1 > 0 and pathLength2 > 0:
                return min(pathLength1, pathLength2)

            if pathLength1 > 0 and pathLength1 <= (distance2 + 1):
                return pathLength1
            if pathLength2 > 0 and pathLength2 <= (distance1 + 1):
                return pathLength2

            flag1, flag2 = 0, 0
            if c1 in visited1:
                flag1 = flag1 + 1
            else:
                visited1[c1] = 1
            if c2 in visited2:
                flag2 = flag2 + 1
            else:
                visited2[c2] = 1
            if cui1Flag == 0:
                flag1 = flag1 + 1
            if cui2Flag == 0:
                flag2 = flag2 + 1

            if flag1 > 0 and flag2 > 0:
                continue

            dchange1, dchange2 = direction1, direction2
            C1 = self.getMeSHConcept(cui=c1)
            C2 = self.getMeSHConcept(cui=c2)
            if flag1 == 0 and dchange1 < 2:
                parents1 = self.getRelated(concept=C1, rel="PAR")
                if parents1 is None:
                    parents1 = []
            if flag2 == 0 and dchange2 < 2:
                parents2 = self.getRelated(concept=C2, rel="PAR")
                if parents2 is None:
                    parents2 = []
            #if parensts1 is [], it will not run the for loop
            for par1 in parents1:
                if par1 in tmpArray1:
                    continue
                stack1.insert(0, par1)
                paths1.insert(0, tmpArray1)
                relations1.insert(0, "PAR")
                directions1.insert(0, dchange1)

            for par2 in parents2:
                if par2 in tmpArray2:
                    continue
                stack2.insert(0, par2)
                paths2.insert(0, tmpArray2)
                relations2.insert(0, "PAR")
                directions2.insert(0, dchange2)

            dchange1 = direction1
            dchange2 = direction2

            if flag1 == 0 and dchange1 < 2:
                children1 = self.getRelated(concept1=C1, rel="CHD")
            if flag2 == 0 and dchange2 < 2:
                children2 = self.getRelated(concept=C2, rel="CHD")

            for child1 in children1:
                if child1 in tmpArray1:
                    continue
                stack1.insert(0, child1)
                paths1.insert(0, tmpArray1)
                relations1.insert(0, "CHD")
                directions1.insert(0, dchange1)

            for child2 in children2:
                if child2 in tmpArray2:
                    continue
                stack2.insert(0, child2)
                paths2.insert(0, tmpArray2)
                relations2.insert(0, "CHD")
                directions2.insert(0, dchange2)

        return -1

    def _getSV(self, dui=None, weight=0.7, category=None):
        """this is the base function of calPathSimilarity.

        **parameter**

        dui1: str
            MeSH ID.

        weight: float
            defaut is 0.7.

        category: str
            A MeSH category.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').
            It can't be None.

        **return**

        dict
        """

        parents = self.getParentsConceptID(dui=dui, category=category)
        if parents is None:
            return 1
        stack = deepcopy(parents)
        SVDict = {dui: 1}
        loopFlag = 1
        while stack is not None and len(stack) >= 1:
            stackTmp = deepcopy(stack)
            stack = []
            for con in stackTmp:
                SVDict[con] = 1 * weight**loopFlag
                par = self.getParentsConceptID(dui=con, category=category)
                if par is not None:
                    stack = stack + par
            loopFlag = loopFlag + 1
        return SVDict



    def calPathSimilarity(self, dui1=None, dui2=None, category=None):
        """Calculating the term similarity based on term path.

        This is the "wang" method.

        **parameter**

        dui1: str
            MeSH ID.

        dui2: str
            MeSH ID.

        category: String
            A MeSH category.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').
            It can't be None.

        **return**

        float
        """
        if category is None:
            sys.stderr.write("category can't be None\n")
            exit(1)

        if not self.checkDui(dui=dui1):
            sys.stderr.write("invalid MeSH ID in dui1\n")
            exit(1)

        if not self.checkDui(dui=dui2):
            sys.stderr.write("invalid MeSH ID in dui2\n")
            exit(1)

        if dui1.startswith("C") or dui2.startswith("C"):
            sys.stderr.write("narrow concept can't as inpput\n")
            exit(1)

        if dui1 == dui2:
            return 1

        if dui1 == dui2:
            return 1

        SV1 = self._getSV(dui=dui1, category=category)
        SV2 = self._getSV(dui=dui2, category=category)
        intersection = SV1.keys() & SV2.keys()
        interSV1 = sum([SV1[key] for key in intersection])
        interSV2 = sum([SV2[key] for key in intersection])
        allSV1 = sum(SV1.values())
        allSV2 = sum(SV2.values())
        score = float(interSV1 + interSV2) / (allSV1 + allSV2)
        return score

