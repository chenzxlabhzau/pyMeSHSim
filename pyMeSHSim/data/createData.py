"""
.. note::
    This module is useful for developer, general user can skip this module
    It provides methods creating the data set.
"""
# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import sys
from .dataDB import dataDB
import pandas as pd
import bcolz as bz
import os
import logging
import copy
import re


class getCuiFunc(object):
    """Get data from umls database.

    | This is the base class of createBcolzData.
    | It provides interface to get MeSH information from UMLS Metathesaurus.
    """

    def __init__(self):
        self.DBclient = dataDB()

    def getSemanticType(self, cui=None):
        """Get the semantic type of a UMLS concept.

        **parameter**

        cui: string

        **return**

        string
        """
        sqlcmd = "select distinct(TUI) from MRSTY where CUI = '%s';" % (cui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        semanticTypeID = result[0]
        sqlcmd = "select ABR from SRDEF where UI='%s'" % (semanticTypeID)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        semanticType = result[0]
        return semanticType

    def getTreeCode(self, cui=None, dui=None):
        """Get MeSH tree code from a UMLS concept or a MeSH concept.

        **parameter**

        cui: string

        dui: string

        **return**

        list of string
        """
        if cui is not None:
            sqlcmd = "select distinct(ATV) from MRSAT where ATN = 'MN' and CUI = '%s';" % (cui)
        else:
            cui = self.getCUIfromMeshID(dui=dui)
            sqlcmd = "select distinct(ATV) from MRSAT where ATN = 'MN' and CUI = '%s';" % (cui)
        result = self.DBclient.fetch_all(sql_cmd=sqlcmd)
        if len(result) > 1:
            d = []
            for line in result:
                d.append(line[0])
        elif len(result) == 1:
            d = [result[0][0]]
        else:
            d = []
        return d

    def getMeSHID(self, cui=None):
        """Get the MeSH concept from an UMLS concept.

        This function can only get the mesh ID from the preferred concept CUI.

        **parameter**

        cui: string

        **return**

        string
        """
        sqlcmd = "select distinct(CODE) from MRSAT where ATN = 'MN' and CUI = '%s';" % (cui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        if result is None:
            return None
        MeSHID = result[0]
        return MeSHID



    def getMeSHIDFromTH(self, cui=None):
        """Get the MeSH descriptor ID or SCR ID.

        This function will be used only when getMeSHID has no result.

        **parameter**

        cui: string

        **return**

        string
        """
        sqlcmd = "select distinct(CODE) from MRSAT where ATN = 'TH' and CUI = '%s';" % (cui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        if result is None:
            return None
        MeSHID = result[0]
        return MeSHID


    def getCUIfromMeshID(self, dui=None):
        """Get the UMLS concept from a MeSH concept.

        This function will not return all the CUI of a MeSH descriptor. it will only
        return the preffered concept's CUI.

        *parameter*

        dui: string

        **return**

        string
        """
        sqlcmd = "select distinct(CUI) from MRSAT where ATN = 'MN' and CODE = '%s';" % (dui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        if result is None:
            return None
        cui = result[0]
        return cui

    def getAllCUIsFromMeshID(self, dui=None):
        """This function will return all the CUI of a MeSH descriptor.

        **parameter**

        dui: string

        **return**

        string
        """
        sqlcmd = "select distinct(CUI) from MRSAT where ATN = 'TH' and CODE = '%s';" % (dui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        if result is None:
            return None
        return result


    def getPreferredName(self, cui=None):
        """Get the preferred name of an UMLS concept.

        **parameter**

        cui : string

        **return**

        string
        """
        sqlcmd = "select distinct STR from MRCONSO where CUI='%s' and TS='P'" % (cui)
        result = self.DBclient.fetch_one(sql_cmd=sqlcmd)
        preferred_name = result[0]
        return preferred_name

    def getCodeForNoneTreeConcept(self, cui=None):
        """This function used to fetch the UMLSID for relation narrow concept.

        **parameter**

        cui: string

        **return**

        string
        """
        MeSHID = self.getMeSHID(cui=cui)
        if MeSHID is not None:
            print ("Note: %s has a main header Dui\n")
            return MeSHID
        else:
            sql_cmd = "select distinct CODE from MRSAT where ATN = 'TH' and CUI='%s'" % cui
            result = self.DBclient.fetch_one(sql_cmd=sql_cmd)
            if result is None:
                return None
            return result[0]

    def getQualifierID(self, cui=None):
        """ This function used to get the qualifier id of a umls concept.

        **parameter**

        cui: string

        **return**

        string
        """
        sql_cmd = "select distinct CODE from MRSAT where ATN = 'TERMUI' and CUI='%s'" % cui
        result = self.DBclient.fetch_one(sql_cmd=sql_cmd)
        if result is None:
            return None
        return result[0]


class createBcolzData(getCuiFunc):
    """A class to construct the base data.

    This class include several functions, which used to create different tables.

    | mainly 6 tables:
    | 1. parent child relation table
    | 2. RN and RB relation table
    | 3. main heading detail data table
    | 4. RN detail data table
    | 6. supplement main heading table
    | 7. offspring and ancestor table
    """

    # {'cui': 'C1256745', 'semtypes': 'inpr', 'tree_code': [], 'MeSHID': None, 'preferred_name': 'Check Tag',
    # 'isNarrowConcept': None, 'relations': None}
    # {'cui': 'C1256741', 'semtypes': 'inpr', 'tree_code': [], 'MeSHID': None,
    # 'preferred_name': 'Topical Descriptor', 'isNarrowConcept': None, 'relations': None}
    # {'cui': 'C1256739', 'semtypes': 'inpr', 'tree_code': [], 'MeSHID': None,
    # 'preferred_name': 'MeSH Descriptors', 'isNarrowConcept': None, 'relations': None}
    # {'cui': 'C1256743', 'semtypes': 'inpr', 'tree_code': [], 'MeSHID': None,
    # 'preferred_name': 'Publication Type', 'isNarrowConcept': None, 'relations': None}
    def __init__(self, log_file_name="createData.log"):
        self.DBclient = dataDB()
        getCuiFunc.__init__(self)
        self.categoryDict = {"C0002784": "E",
                             "C0002807": "A",
                             "C0003186": "I",
                             "C2930671": "G",
                             "C0007995": "D",
                             "C0012674": "C",
                             "C0018689": "N",
                             "C0020158": "K",
                             "C0021424": "L",
                             "C1256748": "B",
                             "C2930672": "H",
                             "C1256749": "F",
                             "C1256750": "J",
                             "C1256743": "V",
                             "C2720181": "Z"
                             }
        self.logger = None

    @staticmethod
    def initLog(log_file_name=None):
        """Static method used to initalize the logger."""

        if os.path.exists(log_file_name):
            os.system("rm %s" % log_file_name)
        instance_name = os.path.basename(log_file_name)
        logger = logging.getLogger(instance_name)
        formatter = logging.Formatter('%(asctime)s %(filename)s : %(levelname)s %(message)s')
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter
        logger.addHandler(file_handler)
        # logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def createParentChildRelTable(self, rel="PAR"):
        """Construct the parent-child relation table, and top concept description table.

        | Parent-child relation table has three columns "Child", "Parent", "Category".
        | All MeSH concepts in this table is a subnode in the MeSH tree structure.

        | Top description table contains the MeSH category infomation, and the top MeSH concept in each category
        """
        self.logger = self.initLog(log_file_name="createParentChildRel.log")
        sys.stderr.write("Running the create parents function\n")
        sql_str = "select distinct CUI1,CUI2 from MRREL where REL='%s'" % (rel)
        result = self.DBclient.fetch_all(sql_cmd=sql_str)

        sys.stderr.write("We selected %s items from umls database\n" % len(result))
        handle = open("ParentChildRel.tsv", "w")
        handle.write("Child\tParent\tCategory\n")
        handle_top = open("topDescription.tsv", "w")
        for item in result:
            cui1 = item[0]
            cui2 = item[1]

            # Log the cuis which has no dui, most of them are "MeSH Category" concept
            Dui1 = self.getMeSHID(cui=cui1)
            if Dui1 is None:
                pName1 = self.getPreferredName(cui=cui1)
                self.logger.warning("The child cui %s, %s has no MeSH id\n" % (cui1, pName1))

            Dui2 = self.getMeSHID(cui=cui2)
            if Dui2 is None:
                pName2 = self.getPreferredName(cui=cui2)
                if Dui1 is not None:
                    catAbbr = self.getCategoryOfTreecode(cui=cui1)
                    if len(catAbbr) > 1:
                        cateString = ",".join(catAbbr)
                    else:
                        cateString = str(catAbbr[0])
                    self.logger.warning("The parent cui %s, %s has no MeSH id, its child dui is %s, category abbrevation is %s\n" % (cui2, pName2, Dui1, cateString))
                else:
                    continue

            # These are some supplymentals items, we do not save them, so pass
            if Dui1 is None and Dui2 is not None:
                pName1 = self.getPreferredName(cui=cui1)
                pName2 = self.getPreferredName(cui=cui2)
                # sys.stderr.write(
                #     "cui1 %s, %s has no dui, but cui2 %s, %s has dui %s\n" % (cui1, pName1, cui2, pName2, Dui2))
                continue

            """
            # these are mainly root concept, most of cui1 is MeSH category
            if Dui1 is None and Dui2 is None:
                sys.stderr.write("these %s and %s two cuis have no Dui.\n" % (cui1, cui2))
            """

            # Pass the Dui1 is None, Detail see the log file
            if Dui1 is None:
                continue

            # Pass all MeSH Qualifiers data
            if Dui1.startswith("Q"):
                #sys.stderr.write("Dui1 %s start with Q\n" % Dui1)
                continue
            if Dui2 is not None and Dui2.startswith("Q"):
                #sys.stderr.write("Dui2 %s start with Q\n" % Dui2)
                continue

            treeCode1 = self.getTreeCode(cui=cui1)
            treeCode2 = self.getTreeCode(cui=cui2)

            if len(treeCode1) == 0:
                # this msg will not print out, it means all dui1 has tree code
                sys.stderr.write("Child concept dui1 %s has no tree code\n" % Dui1)

            # The category should mainly take both treecode1 and treecode2 into account
            # Because the same concept in different category, its children will be diffirent, vice versa
            # When we get children or parents of a concept, we need denote the category
            if len(treeCode1) >= 1:
                firstLetter1 = []
                for code1 in treeCode1:
                    letter1 = code1[0]
                    firstLetter1.append(letter1)
                category1 = list(set(firstLetter1))

            if len(treeCode2) >= 1:
                firstLetter2 = []
                for code2 in treeCode2:
                    letter2 = code2[0]
                    firstLetter2.append(letter2)
                category2 = list(set(firstLetter2))

            """
            # Save the top concept
            if cui2 == "C1256741" or cui2 == "C1256739":
                # this C1256741 has 13 category,
                name = self.getPreferredName(cui=cui1)
                handle_t.write(cui1 + "\t" + name + "\n")
            """

            # While Dui2 is None, means Dui1 is a top concept, we need save this data in top MeSH table
            if Dui2 is None:
                if len(category1) == 1:
                    cat = category1[0]
                    tree_code = treeCode1[0]
                    handle_top.write(Dui1 + "\t" + tree_code + "\t" + cui2 + "\t" + cat + "\t" + pName2 + "\n")
                elif len(category1) > 1:
                    #in fact no concetp is top level in two category
                    for code2 in treeCode2:
                        if len(code2.split(".")) > 1:
                            pass
                        else:
                            letter2 = code2[0]
                            handle_top.write(Dui1 + "\t" + code2 + "\t" + cui2 + "\t" + letter2 + "\t" + pName2 + "\n")
                continue

            # Main part of these table
            if Dui1 is not None and Dui2 is not None:
                if len(category1) == 0:
                    logging.warning("category1 is None, something wrong!!!\n")
                    exit(1)
                if len(category2) == 0:
                    logging.warning("category2 is None, something wrong!!!\n")
                    exit(1)
                else:
                    for cat in category1:
                        for cat2 in category2:
                            if cat == cat2:
                                handle.write(Dui1 + "\t" + Dui2 + "\t" + cat + "\n")
        handle.close()
        handle_top.close()
        sys.stderr.write("Done the create parents function\n")
        return None

    def parseParentChildLog(self):
        """Get all category and its abbreviation.

        This data will be store as attributes in MainHeadingDetailData table.
        """

        logFile = "createParentChildRel.log"
        handle = open(logFile, "r")
        allCategory = {}
        for line in handle:
            result = re.search("cui C(\d+), (.*) \(MeSH Category\) .* category abbrevation is (.*)", line)
            if result is None:
                continue
            cat = result.groups()[1]
            abbr = result.groups()[2]
            if len(abbr) > 1:
                continue
            if cat in allCategory:
                continue
            else:
                allCategory[abbr] = cat
        for ab in allCategory.keys():
            print(ab + " : " + allCategory[ab] + "\n")
        return allCategory

    def getDiseaseTopDescriptors(self):
        """Get top descriptors in disease category.

        This data will be store as attributes in MainHeadingDetailData table.
        """
        sys.stderr.write("Running get the disease top descriptors\n")
        inputFile = "MainHeadingDetailData.tsv"
        handle = open(inputFile, "r")
        diseaseTopDescriptors = {}
        for line in handle:
            array = line.split("\t")
            category = array[4]
            if category != "C":
                continue
            topCode = array[2]
            if len(topCode.split(".")) > 1:
                continue
            prefferName = array[3]
            if topCode in diseaseTopDescriptors:
                sys.stderr.write("something is wrong!!!\n")
                exit(1)
            diseaseTopDescriptors[topCode] = prefferName
            print("%s : %s\n" % (topCode, prefferName))
        sys.stderr.write("Done get the disease top descriptors\n")
        return diseaseTopDescriptors


    def checkParentData(self):
        """This method used to compare the data with "MeSH.Hsa.eg.db"

        We get the data in R packages "meshes", store all its mesh concept in uniqueconcept.tsv
        """
        df1 = pd.read_table("ParentChildRel.tsv", sep="\t", header='infer', names=["Child", "Parent", "Category"])
        li1 = set(list(df1["Child"]) + list(df1["Parent"]))
        # this data from meshes
        df2 = pd.read_table("uniqueConcept.tsv", names=['concept'])
        li2 = set(df2["concept"])
        conjunc = li1.intersection(li2)
        # concept in li1, but not in li2
        diff_li1 = li1.difference(li2)
        # concept in li2, but not in li1
        diff_li2 = li2.difference(li1)
        """
        diffSort = sorted(diff_li1)
        treeCodeList = []
        # handle = open("dataInMeshtblNotInUMLS.tsv", "w")
        for line in diffSort:
            # filter long Dui, which added recently, filter out Q, which is qualify concept
            if len(line) != 7 or line.startswith("Q"):
                sys.stderr.write("some data is wrong!")
                continue
            else:
                treeCode = self.getTreeCode(dui=line)
                treeCodeList.append(treeCode)
        """
        # mainly diffirence
        sys.stderr.write("our total data len: %s\n" % len(li1))
        sys.stderr.write("meshes total data len: %s\n" % len(li2))
        sys.stderr.write("items shared: %s\n" % len(conjunc))
        sys.stderr.write("items only in our data: %s\n" % len(diff_li1))
        sys.stderr.write("items only in meshes: %s\n" % len(diff_li2))
        print(diff_li2)
        return

    def createRNandRBRelTable(self):
        """This method used to create the RNandRBRel table.

        In fact, we mainly focus on the disease category.

        | There are several situation for RN and RB concept.
        | In UMLS, we can select out:
        | 1. Dxxxxxx None
        | 2. None    Dxxxxxx
        | 3. Dxxxxxx Dxxxxxx
        | 4. None    None
        | these four combination
        | for situation 1, this data should be obtained, left is RB, right is RN
        | for situation 2, this data should also be obtained
        | for situation 3, this data should be exclude
        | for situation 4, this data should be exclude
        """
        self.logger = self.initLog(log_file_name="createRNandRBRelTable.log")
        sys.stderr.write("running the createRNandRBRelTable function\n")
        sql_str = "select distinct CUI1, CUI2 from MRREL where REL='%s'" % ("RN")
        result = self.DBclient.fetch_all(sql_cmd=sql_str)
        # RNtoRB is majority file
        handle = open("RNandRBRel.tsv", "w")
        handle.write("RNconcept\tRBconcept\tCategory\n")
        # this file has only one item
        handle_2 = open("RBtoRN.tsv", "w")
        handle_2.write("RNconcept\tRBconcept\n")

        for line in result:
            cui1 = line[0]
            cui2 = line[1]
            dui1 = self.getMeSHID(cui=cui1)
            dui2 = self.getMeSHID(cui=cui2)

            if dui1 is None and dui2 is None:
                srcDui1 = self.getCodeForNoneTreeConcept(cui=cui1)
                srcDui2 = self.getCodeForNoneTreeConcept(cui=cui2)
                # if cui1 and cui2 has no MN attribute, interesting all srcDui start with "C"
                # and in this situation, almost all srcDui1 == srcDui2, only 7 exceptions
                self.logger.warning("cui1 %s and cui2 %s both has no dui, (%s, %s)\n" % (cui1, cui2, srcDui1, srcDui2))
                continue

            if dui1 is not None and dui2 is not None:
                #these descriptor will not save in data set
                #self.logger.warning("both cui1 and cui2 have dui: %s, %s\n" % (dui1, dui2))
                continue

            if dui1 is not None and dui2 is None:
                #in this situation, we can get many cui2 concept start with "D"
                code2 = self.getCodeForNoneTreeConcept(cui=cui2)
                if code2 is None:
                    #qualifierID = self.getQualifierID(cui=cui2)
                    #sys.stderr.write("the narrow concept cui2 %s has no MeSH id, qualifier: %s\n" % (cui2, qualifierID))
                    #if cui has no TH attribute,then it is a qualifier
                    continue

                if code2.startswith("D"):
                    #some mesh qualifier has no MN attribute, but has TH attribute
                    continue

                category = self.getCategoryOfTreecode(cui=cui1)
                if category is None:
                    sys.stderr.write("dui1 %s has no tree code\n" % dui1)
                    exit(1)

                for c in category:
                    handle.write("%s\t%s\t%s\n" % (code2, dui1, c))

            #thi is a very small case, mainly dui1 == dui2, and we do not need this pair
            if dui1 is None and dui2 is not None:
                code1 = self.getCodeForNoneTreeConcept(cui=cui1)
                if code1 is None:
                    continue
                handle_2.write("%s\t%s\n" % (dui2, code1))

        handle.close()
        handle_2.close()
        sys.stderr.write("We selected %s items from mysql database" % len(result))
        sys.stderr.write("Done the create RNtoRB function\n")
        return

    def checkRNData(self):
        """Check the RN data."""

        logFile = "createRNandRBRelTable.log"
        import re
        n = 0
        for line in open(logFile, "r"):
            result = re.search("\((.*), (.*)\)$", line)
            if result is None:
                continue
            src1 = result.groups()[0]
            src2 = result.groups()[1]
            if src1 != src2:
                print("%s and %s\n" % (src1, src2))
            else:
                n = n + 1
        print(str(n) + "\n")

    def createSupMainHeadingDetailData(self):
        """Create the supplement detail information for main heading descriptors.

        | As the UMLS ID to MeSH ID is not "one to one", but "more to one"
        | In main heading detail table, we include only preffered umls id
        | In this table, we fill in the remainder
        """
        sys.stderr.write("running the create supplement Main Heading detail data function\n")
        # create detail information for parents table

        fileOne = "ParentChildRel.tsv"
        df1 = pd.read_table(fileOne, header="infer", sep="\t")
        meshID = list(df1["Child"]) + list(df1["Parent"])
        # unique mesh id
        meshID = list(set(meshID))
        supHandle = open("supplementMainHeading.tsv", "w")
        supHandle.write("MeSHID\tUMLSID\n")

        sql_cmd = "select distinct CUI,CODE from MRSAT where ATN='TH';"
        result = self.DBclient.fetch_all(sql_cmd=sql_cmd)
        duiDict = {}
        for line in result:
            cui = line[0]
            dui = line[1]
            if dui in duiDict:
                duiDict[dui].append(cui)
            else:
                duiDict[dui] = [cui]

        for mesh in meshID:
            dui = mesh
            cuis = duiDict[dui]
            if cuis is None:
                sys.stderr.write("something wrong!!!!\n")
                exit(1)
            for cui in cuis:
                supHandle.write("%s\t%s\n" % (mesh, cui))
        sys.stderr.write("Done the create supplement Main Heading detail data function\n")
        return


    def getCategoryOfTreecode(self, cui=None):
        """Get the MeSH concept category from its tree code.

        **parameter**

        cui: string

        **return**

        None if no tree code, otherwise a list of string
        """
        treeCode = self.getTreeCode(cui=cui)
        if len(treeCode) == 0:
            return None
        if len(treeCode) >= 1:
            letterList = []
            for code in treeCode:
                letterList.append(code[0])
            letterList = list(set(letterList))
            return letterList

    def createMainHeadingDetailData(self):
        """Create the detail information for main heading descriptors.

        This table include the mesh id, correspondent umls id, but only include the UMLS id which has MN attribute.
        """
        sys.stderr.write("running the create Main Heading detail data function\n")
        # parse the ic frequence from file icfrequency.default.dat
        # this file is obtained from perl module UMLS::Similarity
        #ICfile = "icfrequency.default.dat"
        ICfile = "MeSH_IC.tsv"
        freqDandle = open(ICfile, "r")
        ICdict = {}
        for line in freqDandle:
            [icdui, freq] = line.strip("\n").split("<>")
            ICdict[icdui] = freq

        # create detail information for parents table
        fileOne = "ParentChildRel.tsv"
        df1 = pd.read_table(fileOne, header="infer", sep="\t")
        meshID = list(df1["Child"]) + list(df1["Parent"])
        # unique mesh id
        meshID = list(set(meshID))

        handle_Total = open("MainHeadingDetailData.tsv", "w")
        handle_Total.write("MeSHID\tUMLSID\tTree_Code\tPreferred_Name\tCategory\tFrequence\tSemantic_Type\n")
        for mesh in meshID:
            if mesh[0] == "D":
                dui = mesh
                cui = self.getCUIfromMeshID(dui=mesh)
                treeCode = self.getTreeCode(cui=cui)
                if len(treeCode) == 0:
                    print (mesh)
                    print ("treeCode is err")
                    exit(1)
                preferredName = self.getPreferredName(cui=cui)
                category = self.getCategoryOfTreecode(cui=cui)
                if category is None:
                    print ("category is wrong!")
                    exit(1)
                if dui in ICdict:
                    Frequence = ICdict[dui]
                else:
                    Frequence = 0
                semtypes = self.getSemanticType(cui=cui)
            else:
                #now no cui in parentAndChildRel table
                dui = ""
                cui = mesh
                treeCode = self.getTreeCode(cui=cui)
                if len(treeCode) == 0:
                    treeCode = ""
                    print ("the cui %s tree code is None" % cui)
                    continue
                preferredName = self.getPreferredName(cui=cui)
                category = self.getCategoryOfTreecode(cui=cui)
                if category is None:
                    if cui in self.categoryDict:
                        category = self.categoryDict[cui]
                    else:
                        print ("somthing is wrong in cui %s category" % (cui))
                        continue
                if cui in ICdict:
                    Frequence = ICdict[cui]
                else:
                    Frequence = 0
                semtypes = self.getSemanticType(cui=cui)
            # write data
            if len(treeCode) > 1:
                for tc in treeCode:
                    handle_Total.write(
                        "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (dui, cui, tc, preferredName, tc[0], Frequence, semtypes))
            if len(treeCode) == 1:
                tc = treeCode[0]
                handle_Total.write(
                    "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (dui, cui, tc, preferredName, tc[0], Frequence, semtypes))
            if len(treeCode) == 0:
                print (mesh)
                continue
                # handle_Total.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (dui, cui, tc, preferredName, tc[0], Frequence, semtypes))
        handle_Total.close()
        sys.stderr.write("Done the create main heading detail data function\n")
        return None


    def createRNDetailData(self):
        """Create RN concept detail information table.

        | This function will only create detail information of the RNconcept included in RNandRBRel table.
        | All RNConcept start with "C".
        | A RNconcept usually corresponding to several UMLS concept
        """
        sys.stderr.write("running the create RN detail data function\n")
        fileTwo = "RNandRBRel.tsv"
        df2 = pd.read_table(fileTwo, header="infer", sep="\t")
        SDUIList = list(df2["RNconcept"])
        SDUIList = list(set(SDUIList))

        handle_RN = open("RNDetailData.tsv", "w")
        handle_RN.write("MeSHID\tUMLSID\tPreferred_Name\tSemantic_Type\n")
        #sql_cmd = "select distinct CUI,CODE from MRSAT where STYPE='SDUI';"

        sql_cmd = "select distinct CUI,CODE from MRSAT where ATN='TH';"
        result = self.DBclient.fetch_all(sql_cmd=sql_cmd)
        duiDict = {}
        for line in result:
            cui = line[0]
            dui = line[1]
            if dui in duiDict:
                duiDict[dui].append(cui)
            else:
                duiDict[dui] = [cui]

        for SDUI in SDUIList:
            cuis = duiDict[SDUI]
            if cuis is None:
                sys.stderr.write("something wrong!!!!\n")
                exit(1)
            for Cui in cuis:
                preferredName = self.getPreferredName(cui=Cui)
                semtypes = self.getSemanticType(cui=Cui)
                handle_RN.write("%s\t%s\t%s\t%s\n" % (SDUI, Cui, preferredName, semtypes))
        # handle_Total.close()
        handle_RN.close()
        sys.stderr.write("Done the create RN detail data function\n")
        return

    def createOffspringAndAncestorRel(self):
        """This function used to create the offspring and ancestor relation of main heading descriptors.

        It is based on tne ParentChildRel.tsv
        """

        sys.stderr.write("Running create offspring and ancestor rel table\n")
        inputFile = "ParentChildRel.tsv"
        df1 = pd.read_table(inputFile, header="infer", sep="\t")

        #construct parents dict
        parentsDict = {}
        for index, row in df1.iterrows():
            if row["Category"] in parentsDict:
                if row["Child"] in parentsDict[row["Category"]]:
                    parentsDict[row["Category"]][row["Child"]] += [(row["Parent"])]
                else:
                    parentsDict[row["Category"]][row["Child"]] = [(row["Parent"])]
            else:
                parentsDict[row["Category"]] = {}
                parentsDict[row["Category"]][row["Child"]] = [(row["Parent"])]


        outputFile = "offspringAndAncestorRel.tsv"
        handle = open(outputFile, "w")
        handle.write("Offspring\tAncestor\tCategory\n")
        for index, row in df1.iterrows():
            category = row["Category"]
            child = row["Child"]
            parents = parentsDict[category][child]
            contmp = list(copy.deepcopy(parents))
            searchedcon = []
            while contmp:
                interCon = []
                for con in contmp:
                    if con in searchedcon:
                        continue
                    searchedcon.append(con)
                    if con in parentsDict[category]:
                        parent = parentsDict[category][con]
                    else:
                        parent = None
                    if parent is not None:
                        interCon = interCon + parent
                contmp = list(set(interCon))
            for ances in searchedcon:
                handle.write("%s\t%s\t%s\n" % (child, ances, category))
        sys.stderr.write("Done create offspring and ancestor rel table\n")
        return

    def constructBcolz(self):
        """This funtion will convert above tables in bcolz format."""

        sys.stderr.write("Running the construct Bcolz function\n")
        file1 = "ParentChildRel.tsv"
        file2 = "RNandRBRel.tsv"
        file3 = "MainHeadingDetailData.tsv"
        file4 = "RNDetailData.tsv"
        file5 = "supplementMainHeading.tsv"
        file6 = "offspringAndAncestorRel.tsv"
        dataPath = "/home/luozhihui/PycharmProjects/pyMeSHSim/pyMeSHSim/data/testData"

        # file 1 process ParentChildRel.tsv
        df1 = pd.read_table(file1, header="infer", sep="\t")
        df1.sort_values(["Category", "Child"], inplace=True)
        df1 = df1.reset_index(drop=True)

        categotyDict = {}
        for C in set(df1["Category"]):
            dftmp = df1[df1["Category"] == C]
            start = min(dftmp.index)
            end = max(dftmp.index)
            categotyDict[C] = (start, end)
        bz1 = bz.ctable.fromdataframe(df1, rootdir=os.path.join(dataPath, "ParentChildRel"), mode="w")
        bz1.attrs["myattr"] = categotyDict
        bz1.flush()

        # file 2 process RNandRBRel.tsv
        df2 = pd.read_table(file2, header="infer", sep="\t")
        df2.sort_values(["Category", "RNconcept"], inplace=True)
        df2 = df2.reset_index(drop=True)

        categotyDict = {}
        for C in set(df2["Category"]):
            dftmp = df2[df2["Category"] == C]
            start = min(dftmp.index)
            end = max(dftmp.index)
            categotyDict[C] = (start, end)
        bz2 = bz.ctable.fromdataframe(df2, rootdir=os.path.join(dataPath, "RNandRBRel"), mode="w")
        bz2.attrs["myattr"] = categotyDict
        bz2.flush()

        # file 3 process MainHeadingDetailData.tsv
        df3 = pd.read_table(file3, header="infer", sep="\t")
        df3.sort_values(["Category", "MeSHID"], inplace=True)
        df3 = df3.reset_index(drop=True)
        categotyDict = {}
        for C in set(df3["Category"]):
            dftmp = df3[df3["Category"] == C]
            start = min(dftmp.index)
            end = max(dftmp.index)
            categotyDict[C] = (start, end)

            # set disease category semantic type
            if C == "C":
                semanticTypes = list(set(dftmp["Semantic_Type"]))

        bz3 = bz.ctable.fromdataframe(df3, rootdir=os.path.join(dataPath, "MainHeadingDetailData"), mode="w")
        bz3.attrs["myattr"] = categotyDict
        bz3.attrs["DiseaseCategoryST"] = semanticTypes
        # print (semanticTypes)
        bz3.attrs["allCategory"] = self.parseParentChildLog()
        bz3.flush()

        # file 4 process RNDetailData.tsv
        # it has no Category columns, so we don't give myattr
        df4 = pd.read_table(file4, header="infer", sep="\t")
        bz4 = bz.ctable.fromdataframe(df4, rootdir=os.path.join(dataPath, "RNDetailData"), mode="w")
        bz4.flush()

        #file 5 process supplementMainHeading.tsv
        df5 = pd.read_table(file5, header="infer", sep="\t")
        bz5 = bz.ctable.fromdataframe(df5, rootdir=os.path.join(dataPath, "supplementMainHeading"), mode="w")
        bz5.flush()

        #file 6 process the offspring and ancestor relation file
        df6 = pd.read_table(file6, header="infer", sep="\t")
        df6.sort_values(["Category", "Offspring"], inplace=True)
        df6 = df6.reset_index(drop=True)

        #define myattr
        categotyDict = {}
        for C in set(df6["Category"]):
            dftmp = df6[df6["Category"] == C]
            start = min(dftmp.index)
            end = max(dftmp.index)
            categotyDict[C] = (start, end)
        bz6 = bz.ctable.fromdataframe(df6, rootdir=os.path.join(dataPath, "offspringAndAncestorRel"), mode="w")
        bz6.attrs["myattr"] = categotyDict
        bz6.flush()

        sys.stderr.write("Done the construct bcolz function\n")
        return None
