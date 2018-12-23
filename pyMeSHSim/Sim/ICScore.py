# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
from __future__ import division
import sys
from copy import deepcopy
from collections import defaultdict
from math import log
from ..data import dataDB
from .MeSHProcess import MeSHProcess
import bcolz as bz

class InformationContent(MeSHProcess):
    """This class implement the IC based similarity."""

    def __init__(self):
        MeSHProcess.__init__(self)
        self.propagationDict = {}

    def _allMaxFreqDict(self):
        """This method is used to construct the MainHeadingDetailData.

        | This is not a frequently used method.
        | Before release, we have runned this method. so usrs can skip this one
        """
        maxIDInCategory = {}
        for category in self.allCategory:
            if category not in self.MainHeadingDetailDataInCategory:
                df = self.getMainHeadingDetailData(category=category)
                self.MainHeadingDetailDataInCategory[category] = df
            else:
                df = self.MainHeadingDetailDataInCategory[category]

            id = df["MeSHID"]
            value_tmp = df["Frequence"][df["Frequence"] != 0]

            maxIndex = value_tmp.idxmin()
            maxIDInCategory[category] = id[maxIndex]
        bz1 = bz.open(rootdir=self._MainHeadingDetailDataFilePath)
        bz1.attrs["maxIDInCategory"] = maxIDInCategory
        bz1.flush()

    def getFreqDict(self, category="C"):
        """Get the IC frequence from MainHeadingDetailData.

        **parameter**

        category: String
            one of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all').
            It can't be None.

            default: "C".

        **return**

        defaultdict
        """
        if category is None:
            sys.stderr.write("invalid category value\n")
            exit(1)


        if category not in self.MainHeadingDetailDataInCategory:
            df = self.getMainHeadingDetailData(category=category)
            self.MainHeadingDetailDataInCategory[category] = df
        else:
            df = self.MainHeadingDetailDataInCategory[category]

        id = df["MeSHID"]
        value = df["Frequence"]
        sumOfFreq = sum(value)
        freqValue = value.apply(lambda x: x/sumOfFreq)
        FreqDict = defaultdict(lambda: "N/A", zip(id, freqValue))
        return FreqDict

    def getICDict(self, category="C"):
        """This method used to check whole IC value.

        It takes long time.

        **parameter**

        category: String
            one of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all').
            It can't be None.

            default: "C".

        **return**

        dict
        """
        freqDict = self.getFreqDict(category=category)
        dd = deepcopy(freqDict)
        ICDict = {}
        for dui in dd.keys():
            #children = self.getDescendant(dui=dui, category=category)
            children = self.getOffspringConceptID(dui=dui, category=category)
            if children is None:
                children = [dui]
            else:
                children = children + [dui]
            freqTotal = 0
            for child in children:
                if freqDict[child] == "N/A":
                    sys.stderr.write("%s has no freq value\n" % child)
                freqTotal = freqTotal + freqDict[child]
            if 0 < freqTotal <= 1:
                ICDict[dui] = -1 * log(freqTotal, 10)
            else:
                sys.stderr.write("dui %s IC value %s is wrong\n" % (dui, freqTotal))
                ICDict[dui] = 0
        return ICDict

    def getMeSHIC(self, dui=None, category="C"):
        """This method used to get IC value from a MeSH ID.

        **parameter**

        dui: String
            MeSH ID.
            start with "D".

        category: String
            one of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all').
            It can't be None.

            default: "C".

        **return**

        float
        """
        if dui.startswith("C"):
            sys.stderr.write("narrow MeSH concept has no IC value\n")
            exit(1)
        freqDict = self.getFreqDict(category=category)
        children = self.getDescendant(dui=dui, category=category)
        freqTotal = 0
        for child in children:
            freqTotal = freqTotal + freqDict[child]
        if 0 < freqTotal <= 1:
            IC = -1 * log(freqTotal, 10)
        else:
            sys.stderr.write("dui %s IC value %s is wrong\n" % (dui, freqTotal))
            IC = 0
        return IC

    def _getMaxICInCategory(self, category=None):
        """Get the max ic concept in one category.

        This is a normalization value.
        """
        if category not in self.maxIDInCategory:
            sys.stderr.write("can't get max IC in category: %s \n" % category)
            exit(1)
        maxIC = self.getMeSHIC(dui=self.maxIDInCategory[category], category=category)
        return maxIC


    def findLeastCommonSubsumerbyTreeCode(self, dui1=None, dui2=None, category=None):
        """This method used to find the least common subsumer by treeCode.

        **parameter**

        dui1: string
            mesh ID.

        dui2: String
            mesh ID.

        category: String
            mesh category.

        **return**

        list of string
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

        treeCode1 = self.getMeSHTreecode(dui=dui1)
        treeCode2 = self.getMeSHTreecode(dui=dui2)

        if treeCode1 == []:
            sys.stderr.write("the concept %s has no tree code\n"% dui1)
            return None
        if treeCode2 == []:
            sys.stderr.write("the concept %s has no tree code\n"% dui2)
            return None

        subsumerDuis = []
        for code1 in treeCode1:
            if code1[0] != category:
                continue
            for code2 in treeCode2:
                if code2[0] != category:
                    continue
                dui = self.compareTreecode(code1=code1, code2=code2)
                subsumerDuis.append(dui)
        return list(set(subsumerDuis))

    def compareTreecode(self, code1=None, code2=None):
        """Get shared part of two tree code.

        **parameter**

        code1: String
            MeSH tree code.

        code2: String
            MeSH tree code.


        **return**

        list of dui
        """
        array1 = code1.split(".")
        array2 = code2.split(".")
        num = min(len(array1), len(array2))
        for i in range(0, num):
            if i == 0:
                if array1[i] != array2[i]:
                    commom = None
                    break
                else:
                    commom = 0
            else:
                if array1[i] == array2[i]:
                    commom = commom + 1
                else:
                    break

        if commom is None:
            #return the disease catagory, this can be improved
            return "topConcept"
        else:
            commom = commom + 1
            treeCode = ".".join(array1[0 : commom])
            dui = self.getDuiFromTreeCode(treeCode=treeCode)
            return dui

    def findLeastCommonSubsumerbyAncestor(self, dui1=None, dui2=None,category=None):
        """This method used to find the least common subsumer by ancestor.

        **parameter**

        dui1: string
            mesh ID.

        dui2: String
            mesh ID.

        category: String
            mesh category.

        **return**

        list of string
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

        ancestor1 = self.getAncestors(dui=dui1, category=category)
        ancestor2 = self.getAncestors(dui=dui2, category=category)
        common = set(ancestor1).intersection(set(ancestor2))
        if len(common) == 0:
            return "topConcept"
        else:
            return common

    def simil(self, dui1=None, dui2=None, category=None):
        """The ic algorithm."""

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
            return (1, 1, 1, 1)

        maxic = self._getMaxICInCategory(category=category)
        ic1 = self.getMeSHIC(dui=dui1, category=category) / float(maxic)
        ic2 = self.getMeSHIC(dui=dui2, category=category) / float(maxic)
        if ic1 <= 0 or ic2 <= 0:
            return -1
        # get the LeastCommonSubsumer

        subsumerDuis = self.findLeastCommonSubsumerbyTreeCode(dui1=dui1, dui2=dui2, category=category)
        # get the lowest ic, because ic has been converted with - log 10,so the bigger value has lower ic
        ictmp = 0
        # duitmp = None

        for dui in subsumerDuis:
            if dui == "topConcept":
                icValue = 0
            else:
                icValue = self.getMeSHIC(dui=dui, category=category)
            if icValue > ictmp:
                ictmp = icValue
                # duitmp = dui
        ictmp = ictmp/ maxic
        res = ictmp
        lin = 2*ictmp / (ic1 + ic2)
        jiang = 1 - min(1, ic1 + ic2 - 2*ictmp)
        rel = lin * (1 - (10**(- ictmp * maxic)))
        return (res, lin, jiang, rel)

    def calICSimilarity(self, dui1=None, dui2=None, category=None, method=None):
        """Calculating the term similarity based on information content.

        **parameter**

        dui1: String
            MeSH ID, limit to main headings.

        dui1: String
            MeSH ID, limit to main headings.

        category: String
            A MeSH category.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').
            It can't be None.

        method: String
            one value in ["lin", "res", "jiang", "rel"].

        **return**

        float
        """
        (res, lin, jiang, rel) = self.simil(dui1=dui1, dui2=dui2, category=category)
        if method not in ["lin", "res", "jiang", "rel"]:
            sys.stderr.write("program has no method %s\n" % method)
            exit(1)
        if method == "lin":
            return lin
        if method == "res":
            return res
        if method == "jiang":
            return jiang
        if method == "rel":
            return rel



