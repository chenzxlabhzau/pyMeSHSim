# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import bcolz as bz
import pandas as pd
import sys, os


class dataHandle():
    """This class is used to parse MeSH data, which stored in bcolz.

    | It contains 6 tables: parent child relation table, RN and RB relation table, main heading detail data table, and RN detail data table,
    | supplement main heading table, offspring and ancestor table.

    **parameters**

    path: string
        The directory path, which contain all the bcolz file.

    **attribute**

    dataPath: String
        The directory path, which contain all the bcolz file.

    _parentFilePath: String
        The path to table parents.

    _RNtoRBFilePath: String
        The path to table RNtoRB.

    _RNDataFilePath: String
        the path to table RNData.

    _totalDataFilePath: String
        the path to table totalData.

    allCategory: list
        contain all category in MeSH

    **see also**

    pyMeSHSim.data.createData
    """
    def __init__(self):
        path = os.path.realpath(__file__)
        self._dataPath = os.path.join(os.path.dirname(path), "testData")
        self._parChdRelFilePath = os.path.join(self._dataPath, "ParentChildRel")
        self._RNRBRelFilePath = os.path.join(self._dataPath, "RNandRBRel")
        self._RNDetailDataFilePath = os.path.join(self._dataPath, "RNDetailData")
        self._MainHeadingDetailDataFilePath = os.path.join(self._dataPath, "MainHeadingDetailData")
        self._supMainHeadingDetailDataFilePath = os.path.join(self._dataPath, "supplementMainHeading")
        self._offspringAncestorDataFilePath = os.path.join(self._dataPath, "offspringAndAncestorRel")
        #self.allCategory = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all']
        self.allCategory = list(self.getAllCategory().keys()) + ["all"]
        self.maxIDInCategory = self._getMaxIDInCategory()

    def getRelData(self, data=None, category="all"):
        """This method used to select data from table ParentChildRel or RNandRBRel.


        **parameter**

        data: String
            One of the value in ("ParentChildRel", "RNandRBRel").

            | ParentChildRel data is the tree structure core data, it cantains  all main heading descriptors
            | RNandRBRel data is the relation data, contians all Narrow concept and its Broarder concept
            | ParentChildRel table has three columns "Child", "Parent", "Category"
            | RNandRBRel table has three columns "RNconcept", "RBconcept", "Category"
            | default: None

        category: string
            | one of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all')
            | "all" means select all data

            | default: "all"

        **return**

        DataFrame object

        **see also**

        pandas.dataframe
        """
        dataSet = {"ParentChildRel": self._parChdRelFilePath, "RNandRBRel": self._RNRBRelFilePath}
        if data not in dataSet:
            sys.stderr.write("error: the data %s is not in our data\n" % data)
        else:
            filePath = dataSet[data]
            bz1 = bz.open(rootdir=filePath, mode="r")
        if category is None:
            category = "all"
        if category not in self.allCategory:
            sys.stderr.write("error: the category %s is not in our data." % category)
            exit(1)
        if category == "all":
            df1 = bz1.todataframe()
            return df1
        else:
            try:
                (start, end) = bz1.attrs["myattr"][category]
            except:
                sys.stderr.write("data %s has no category %s" % (data, category))
                exit(1)
            df1 = bz1.todataframe()
            end = end + 1
            dftmp = df1[start: end]
            return dftmp

    #def getTreeSubnodeDetailData(self, category="all"):
    def getMainHeadingDetailData(self, category="all"):
        """This method used to select data from table totalData.

        | MainHeadingDetailData table contains all information about descriptors in ParentChildRel table.
        | columns in this table is:
        | MeSHID, UMLSID, Tree_Code, Preferred_Name, Category, Frequence, Semantic_Type

        **parameter**

        category: string
            | one of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z', 'all')
            | "all" means select all data
            | default: "all"

        **return**

        DataFrame object
        """
        bz1 = bz.open(rootdir=self._MainHeadingDetailDataFilePath, mode="r")
        if category is None:
            category = "all"
        if category not in self.allCategory:
            sys.stderr.write("error: the category %s is not in our data.\n" % category)
            exit(1)
        if category == "all":
            df1 = bz1.todataframe()
            return df1
        else:
            try:
                (start, end) = bz1.attrs["myattr"][category]
            except:
                sys.stderr.write("data has no category %s" % category)
                exit(1)
            df1 = bz1.todataframe()
            end = end + 1
            dftmp = df1[start: end]
            return dftmp

    def getRNDetailData(self):
        """This method used to select data from table RNdetailData.

        | RNdetailData contains full information about the narrow concept in MeSH.

        | RNdetailData table has 4 columns:
        | MeSHID, UMLSID, Prefered_Name, Semantic_Type

        **return**

        dataframe object
        """

        bz1 = bz.open(rootdir=self._RNDetailDataFilePath, mode="r")
        df1 = bz1.todataframe()
        return df1


    def getParentTableSemantiTypes(self):
        """Get all semantic types from main heading concepts in disease category.

        **return**

        list
        """
        bz1 = bz.open(rootdir=self._MainHeadingDetailDataFilePath, mode="r")
        semanticTypes = bz1.attrs["DiseaseCategoryST"]
        return semanticTypes

    def getSupplementMainHeadingData(self):
        """Get supplementary main heading data."""
        bz1 = bz.open(rootdir=self._supMainHeadingDetailDataFilePath, mode="r")
        df1 = bz1.todataframe()
        return df1

    def getOffspringAncestorData(self, category="all"):
        """Get offsping and ancestor data."""

        bz1 = bz.open(rootdir=self._offspringAncestorDataFilePath, mode="r")
        if category is None:
            category = "all"
        if category not in self.allCategory:
            sys.stderr.write("error: the category %s is not in our data.\n" % category)
            exit(1)
        if category == "all":
            df1 = bz1.todataframe()
            return df1
        else:
            try:
                (start, end) = bz1.attrs["myattr"][category]
            except:
                sys.stderr.write("data has no category %s" % category)
                exit(1)
            df1 = bz1.todataframe()
            end = end + 1
            dftmp = df1[start: end]
            return dftmp

    def getAllCategory(self):
        """Get all category."""
        bz1 = bz.open(rootdir=self._MainHeadingDetailDataFilePath, mode="r")
        cateDict = bz1.attrs["allCategory"]
        return cateDict

    def _getMaxIDInCategory(self):
        """Get max IC terms."""
        bz1 = bz.open(rootdir=self._MainHeadingDetailDataFilePath, mode="r")
        cateDict = bz1.attrs["maxIDInCategory"]
        return cateDict

