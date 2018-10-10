# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import sys, copy
#from ..data.dataDB import dataDB
from ..data.duiFunc import duiFunc
from ..metamapWrap.Concept import Concept
#from ..metamapWrap.MetamapInterface import MetaMap

class MeSHProcess(duiFunc):
    """This calss contains methods that can search MeSH ID by diffirent relation.

    | Such as child, parent, narrow, broad, ancestor, decendant...
    | This class inherit the duiFunc class.
    """
    def __init__(self):
        duiFunc.__init__(self)

    @staticmethod
    def getMeSHConcept(cui=None, dui=None, tree_code=None):
        """
        **parameter**
        ----------
        cui: String
            UMLS ID.

        dui: String
            MeSH ID.

        tree_code: String
            MeSH tree number.

        **return**

        list

        see also
        ----------
        pyMeSHSim.metamapWrap.Concept
        """
        concept = Concept.MeSHConcept(cui=cui, dui=dui, tree_code=tree_code)
        return concept

    def _getParentOrchildConceptID(self, dui=None, data=None, category=None, rel=None):
        """From MeSH ID get its parents or children concepts MeSHID.

        **parameter**

        rel: String
            One value in ["PAR", "CHD"].

        data: DataFrame
            default None.

        category: String
            The category of the dui, if you make sure the dui belong to what category, you can set this parameter.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').


        **return**

        a list of MeSH ID
        """
        if rel not in ["PAR", "CHD"]:
            sys.stderr.write("invalid rel\n")
            exit(1)

        if rel == "PAR":
            column  = "Parent"
        if rel == "CHD":
            column = "Child"

        # if has no category, means it not main heading concept
        if category is None:
            sys.stderr.write("category can't be none\n")
            exit(1)

        if isinstance(category, list):
            sys.stderr.write("can't input a list as category\n")
            exit(1)

        if category not in self.allCategory:
            sys.stderr.write("category %s not in category list.\n" % category)
            exit(1)

        if data is not None:
            pa = data[column][data["MeSHID"] == dui]
            if pa.empty:
                return None
            else:
                return list(set(pa))

        if category not in self.parChdRelDataInCategory:
            df = self.getRelData(data="ParentChildRel", category=category)
            self.parChdRelDataInCategory[category] = df
        else:
            df = self.parChdRelDataInCategory[category]

        if rel == "PAR":
            res = df[column][df["Child"] == dui]
        else:
            res = df[column][df["Parent"] == dui]

        if res.empty:
            return None
        else:
            return list(set(res))



    def getParentsConceptID(self, dui=None, data=None, category=None):
        """From MeSH ID get its parent concepts MeSHID.

        | We only return the parent concept in only one category, so when use this method, category must be denoted.
        | If you don't know the category of one MeSH descriptor. please see getCategory method in duiFunc.

        parameter
        ----------
        dui: String
            MeSH ID.

        data: Pandas dataFrame
            Where to search the parent dui from.

            default: None.

        category: String
            The category of the dui, if you make sure the dui belong to what category, you can set this parameter.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').

        **return**

        list of String
        """
        return self._getParentOrchildConceptID(dui=dui, data=data, category=category, rel="PAR")

    def getChildrenConceptID(self, dui=None, category=None, data=None):
        """From MeSH ID get its children concepts MeSHID.

        | We only return the children concepts in only one category, so when use this method, category must be denoted.
        | If you don't know the category of one MeSH descriptor. please see getCategory method in duiFunc.


        **parameter**

        dui: String
            MeSH ID.

        data: Pandas dataFrame
            Where to search the children dui from.

            default: None

        category: String
            The category of the dui, if you make sure the dui belong to what category, you can set this parameter.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').

        **return**

        list of String
        """
        return self._getParentOrchildConceptID(dui=dui, data=data, category=category, rel="CHD")

    def getTopConceptID(self, dui=None):
        """This method is used to return the top MeSH ID of some MeSH concept.

        | eg. D012559(Schizophrenia)
        | Belong to {'D001523': 'Disorders, Mental'}

        **parameter**

        dui: String
            MeSH ID.
            Main heading concept, starts with "D".

        **return**

        dict.
        key is MeSH id, value is preffered name.
        """

        treeCode = self.getMeSHTreecode(dui=dui)
        if treeCode is None:
            sys.stderr.write("Dui %s has no top descriptor.\n" % dui)
            return None
        topConcepts = {}
        for tree in treeCode:
            topTreeNum = tree.split(".")[0]
            concept = self.getDuiFromTreeCode(treeCode=topTreeNum)
            name = self.getPrefferedName(dui=concept)
            if concept not in topConcepts:
                topConcepts[concept] = name
        return topConcepts

    def getAncestors(self, dui=None, category=None):
        """This method will return all ancestors of a MeSH concept.

        **parameter**

        dui: String
            MeSH ID.
            Main heading concept, starts with "D".

        **return**

        list of string.
        Store MeSH ID.
        """
        parents = self.getParentsConceptID(dui=dui, category=category)
        contmp = copy.deepcopy(parents)
        searchedcon = [dui]
        while contmp:
            interCon = []
            for con in contmp:
                if con in searchedcon:
                    continue
                searchedcon.append(con)
                parents = self.getParentsConceptID(dui=con, category=category)
                if parents is not None:
                    interCon = interCon + parents
            contmp = list(set(interCon))
        return searchedcon

    def getDescendant(self, dui=None, category=None, data=None):
        """This method will return all decendant of a mesh concept.

        **parameter**

        dui: String
            MeSH ID.
            Main heading concept, starts with "D".

        category: String
            The category of the dui, if you make sure the dui belong to what category, you can set this parameter.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').

        **return**

        list of string
        Store MeSH ID.
        """
        children = self.getChildrenConceptID(dui=dui, category=category, data=data)
        contmp = copy.deepcopy(children)
        searchedcon = [dui]
        while contmp:
            interCon = []
            for con in contmp:
                if con in searchedcon:
                    continue
                searchedcon.append(con)
                children = self.getChildrenConceptID(dui=con, category=category, data=data)
                if children is not None:
                    interCon = interCon + children
            contmp = list(set(interCon))
        return searchedcon


    def _getAncestorsOrDescendentConceptID(self, dui=None, category=None, rel=None):
        """From MeSH ID get its ancestor or offspring concepts MeSHID.

        **parameter**

        rel: String
            One value in ["ANC", "OFF"].

        **return**

        a list of MeSH ID
        """

        if rel not in ["OFF", "ANC"]:
            sys.stderr.write("invalid rel\n")
            exit(1)

        if rel == "ANC":
            column = "Ancestor"
        if rel == "OFF":
            column = "Offspring"

        if category is None:
            sys.stderr.write("category can't be none\n")
            exit(1)

        if isinstance(category, list):
            sys.stderr.write("can't input a list as category\n")
            exit(1)

        if category not in self.allCategory:
            sys.stderr.write("category %s not in category list.\n" % category)
            exit(1)

        if not self.checkDui(dui=dui):
            exit(1)

        if dui.startswith("C"):
            sys.stderr.write("SCR record has no ancestor\n")
            exit(1)

        if category not in self.offspringAncestorDataInCategory:
            df = self.getOffspringAncestorData(category=category)
            self.offspringAncestorDataInCategory[category] = df
        else:
            df = self.offspringAncestorDataInCategory[category]

        if rel == "ANC":
            res = df[column][df["Offspring"] == dui]
        else:
            res = df[column][df["Ancestor"] == dui]

        if res.empty:
            return None
        else:
            return list(set(res))

    def getAncestorsConceptID(self, dui=None, category=None):
        return self._getAncestorsOrDescendentConceptID(dui=dui, category=category, rel="ANC")

    def getOffspringConceptID(self, dui=None, category=None):
        return self._getAncestorsOrDescendentConceptID(dui=dui, category=category, rel="OFF")

    def _convertToBroadOrNarrowConceptID(self, dui=None, rel=None):
        """From MeSH ID get its broader or narrow concept MeSHID.

        **parameter**

        rel: String
            One value in ["RB", "RN"].

        **return**

        a list of MeSH ID
        """
        if rel not in ["RB", "RN"]:
            sys.stderr.write("invalid rel\n")
            exit(1)

        if rel == "RB":
            column = "RBconcept"
        if rel == "RN":
            column = "RNconcept"

        if not self.checkDui(dui=dui):
            sys.stderr.write("Dui %s is an invalid MeSH id\n" % dui)
            exit(1)

        if self.RNRBRelData is None:
            df = self.getRelData(data="RNandRBRel")
            self.RNRBRelData = df
        else:
            df = self.RNRBRelData

        if rel == "RB":
            Con = df[column][df["RNconcept"] == dui]
        else:
            Con = df[column][df["RBconcept"] == dui]
        return list(set(Con))


    def convertToBroad(self, dui=None):
        """This method will return all broader concept of a narrow mesh concept.

        **parameter**

        dui: String
            MeSH ID.
            Narrow concept, starts with "C".

        **return**

        list of string
        Store MeSH ID.
        """
        return self._convertToBroadOrNarrowConceptID(dui=dui, rel="RB")

    def convertToNarrow(self, dui=None):
        """This method will return all narrow concept of a broad mesh concept.

        **parameter**

        dui: String
            MeSH ID.
            Broader concept, starts with "D".

        **return**

        list of string
        Store MeSH ID.
        """
        return self._convertToBroadOrNarrowConceptID(dui=dui, rel="RN")



    #def getAllTopConceptofCategory(self, category):





