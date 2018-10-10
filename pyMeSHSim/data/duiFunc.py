# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import re
import sys
from ..data.dataInterface import dataHandle


class duiFunc(dataHandle):
    """This is an base class for MeSH concept retrive its diffirent attribute.

    | It contains MeSH ID, UMLSID, Tree Code, Preffered Name, Category.
    | And allows the interconversion between them.

    **attribute**

    parChdRelData: dataframe or None
        data cache for parentData.

    MainHeadingDetailData: dataframe or None
        data cache for totalData.

    RNdetailData : dataframe
        data cache for RNData or None.

    RNtoRBData: dataframe or None
        data cache for RNtoRBData.
    """

    def __init__(self):
        dataHandle.__init__(self)
        self.parChdRelData = None
        self.MainHeadingDetailData = None
        self.RNDetailData = None
        self.RNRBRelData = None
        self.parChdRelDataInCategory = {}
        self.RNRBRelDataInCategory = {}
        self.offspringAncestorDataInCategory = {}
        self.MainHeadingDetailDataInCategory = {}

    def checkDui(self, dui=None):
        """Check the MeSH ID, if it is legal.

        | The MeSH heading concept starts with a capital letter "D",
        | SCR concepts start with "C",
        | usually followed with 6 digital number, or 9 digital number.

        **parameter**

        dui: string
            MeSH ID.

        **return**

        True or False.

        """
        # old mesh id
        regx = re.compile("^C|D[0-9][0-9][0-9][0-9][0-9][0-9]$")
        result = regx.match(dui)
        if result:
            return True
        # new mesh id
        regx = re.compile("^C|D[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$")
        result = regx.match(dui)
        if result:
            return True
        return False

    def checkCui(self, cui=None):
        """Check the UMLS ID, if it is legal.

        | The UMLS concept starts with a capital letter "C",
        | Usually followed with 7 digital number.

        **parameter**

        cui: String
            UMLS ID.

        **return**

        True or False.
        """
        regx = re.compile("^C[0-9][0-9][0-9][0-9][0-9][0-9][0-9]$")
        result = regx.match(cui)
        if result:
            return True
        return False

    def selectDataByDui(self, dui=None, selectCol=None, queryCol=None):
        """Selecting value in diffirent table.

        **parameter**

        dui: String
            MeSH ID.

        selectCol: String
            column names in MainHeadingDetailData and RNdetailData.

        queryCol: string
            column name in MainHeadingDetailData and RNdetailData.

        **return**

        None or list
        """
        if dui.startswith("D"):
            if self.MainHeadingDetailData is None:
                df = self.getMainHeadingDetailData()
                self.MainHeadingDetailData = df
            else:
                df = self.MainHeadingDetailData
            # semantictype is a series
            result = df[selectCol][df[queryCol] == dui]
            if result.empty:
                sys.stderr.write("Your string %s is not in the data\n" % dui)
                return None
            return list(set(result))

        if dui.startswith("C"):
            if self.RNDetailData is None:
                df = self.getRNDetailData()
                self.RNDetailData = df
            else:
                df = self.RNDetailData
            result = df[selectCol][df[queryCol] == dui]
            if result.empty:
                sys.stderr.write("your string %s is not in the data\n" % dui)
                return None
            return list(set(result))

    def selectDataByCui(self, cui=None, selectCol=None, queryCol=None):
        """Select value in diffirent pandas dataframe, not suggestion.

        **parameter**

        cui: String
            UMLS ID.

        selectCol: String
            column names in TreeSubnodeDetailData and RNdetailData.

        queryCol: string
            column name in TreeSubnodeDetailData and RNdetailData.

        **return**

        None or list
        """
        # retrive TreeSubnodeDetailData
        if self.MainHeadingDetailData is None:
            df = self.getMainHeadingDetailData()
            self.MainHeadingDetailData = df
        else:
            df = self.MainHeadingDetailData

        result = df[selectCol][df[queryCol] == cui]
        if result.empty:
            if selectCol == "Tree_Code":
                return None
            # retrive RNdetailData
            if self.RNDetailData is None:
                df = self.getRNDetailData()
                self.RNDetailData = df
            else:
                df = self.RNDetailData
            result = df[selectCol][df[queryCol] == cui]
            if result.empty:
                #sys.stderr.write("the string %s not in the MeSH data\n" % cui)
                return None
            return list(set(result))
        else:
            return list(set(result))

    def getSemanticType(self, dui=None, cui=None):
        """Useing mesh ID or UMLS ID to get the concept semantic type.

        We suggest to use dui retrive the semantic type.

        **parameter**

        dui: string
            MeSH ID.

        cui: string
            UMLS ID.

        **return**

        None or string.
        """
        if dui is None and cui is None:
            sys.stderr.write("please input a MeSH ID or a UMLS ID\n")
            exit(1)
        if dui is not None and cui is not None:
            sys.stderr.write("can't input both MeSH ID and UMLS ID, please select only one\n")
            exit(1)

        # for dui
        if dui is not None:
            if not self.checkDui(dui=dui):
                sys.stderr.write("this is an invalid MeSH ID\n")
                exit(1)
            result = self.selectDataByDui(dui=dui, selectCol="Semantic_Type", queryCol="MeSHID")
            if result is not None:
                return result[0]
            else:
                return result
        # for cui
        if cui is not None:
            if not self.checkCui(cui=cui):
                sys.stderr.write("this is an invalid UMLS ID\n")
                exit(1)

            # retrive TreeSubnodeDetailData
            result = self.selectDataByCui(cui=cui, selectCol="Semantic_Type", queryCol="UMLSID")
            if result is not None:
                return result[0]
            else:
                return result

    def getMeSHTreecode(self, dui=None, cui=None):
        """Use mesh ID or UMLS ID to get the concept tree code.

        **parameter**

        dui: string
            MeSH ID.

        cui: string
            UMLS ID.

        **return**

        None or list of string.
        """
        if cui is None and dui is None:
            sys.stderr.write("please input a MeSH ID or UMLS ID\n")
            exit(1)

        if dui is not None and cui is not None:
            sys.stderr.write("can't input both MeSH ID and UMLS ID, please select only one\n")
            exit(1)

        # for dui
        if dui is not None:
            if not self.checkDui(dui=dui):
                sys.stderr.write("this is an invalid MeSH ID\n")
                exit(1)
            if dui.startswith("C"):
                sys.stderr.write("no tree code for %s\n" % dui)
                # return None or exit(1)
                return None

            result = self.selectDataByDui(dui=dui, selectCol="Tree_Code", queryCol="MeSHID")
            return result

        # for cui

        if cui is not None:
            if not self.checkCui(cui=cui):
                sys.stderr.write("this is an invalid UMLS ID\n")
                exit(1)
            result = self.selectDataByCui(cui=cui, selectCol="Tree_Code", queryCol="UMLSID")
            return result

    def getMeSHIDbyUMLSID(self, cui=None):
        """Get MeSH ID from UMLS ID.

        | This function will query three tables:
        | MainHeadingDetailData
        | supplementMainHeadingDetailData
        | RNDetailData

        **parameter**

        cui: string
            UMLS ID.

        **return**

        None or string.
        """
        if not self.checkCui(cui=cui):
            sys.stderr.write("this is an invalid UMLS ID\n")
            exit(1)

        result = self.selectDataByCui(cui=cui, selectCol="MeSHID", queryCol="UMLSID")
        if result is None:
            MeSHID = self._queryDataInSupplementData(cui=cui)
            if MeSHID is None:
                MeSHID = self._queryDataInRNDetailData(cui=cui)
                return MeSHID
            else:
                return MeSHID
        else:
            MeSHID = result[0]
            return MeSHID

    def _queryDataInSupplementData(self, cui=None):
        """Query MeSH ID by UMLS ID in supplementMainHeadingData."""

        if not self.checkCui(cui=cui):
            sys.stderr.write("this is an invalid UMLS ID\n")
            exit(1)
        df1 = self.getSupplementMainHeadingData()
        result = df1["MeSHID"][df1["UMLSID"] == cui]
        if result.empty:
            return None
        else:
            MeSHID = list(set(result))[0]
            # print(MeSHID)
            # exit(1)
            return MeSHID

    def _queryDataInRNDetailData(self, cui=None):
        """Query MeSH ID by UMLS ID in RNDetailData."""

        if not self.checkCui(cui=cui):
            sys.stderr.write("this is an invalid UMLS ID\n")
            exit(1)
        df1 = self.getRNDetailData()
        result = df1["MeSHID"][df1["UMLSID"] == cui]
        if result.empty:
            return None
        else:
            MeSHID = list(set(result))[0]
            return MeSHID

    def getUMLSIDbyMeSHID(self, dui=None):
        """Get UMLS ID from MeSH ID.

        | This function only return the preferred UMLS concept.
        | Not the whole UMLS ID corresponding to the mesh descriptor.

        **parameter**

        dui: string
            MeSH ID.

        **return**

        None or string.
        """
        if not self.checkDui(dui=dui):
            sys.stderr.write("this is an invalid MeSH ID\n")
            exit(1)
        result = self.selectDataByDui(dui=dui, selectCol="UMLSID", queryCol="MeSHID")
        if result is None:
            return None
        else:
            UMLSID = result[0]
            return UMLSID

    def getPrefferedName(self, dui=None, cui=None):
        """Use mesh ID or UMLS ID to get the concept prefferd name.

        We suggest to use dui get preffered name.

        **parameter**

        dui: string
            MeSH ID.

        cui: string
            UMLS ID.

        **return**

        None or string.
        """
        if cui is None and dui is None:
            sys.stderr.write("please input a MeSH ID or UMLS ID\n")
            exit(1)

        if dui is not None and cui is not None:
            sys.stderr.write("can't input both MeSH ID and UMLS ID, please select only one\n")
            exit(1)

        if dui is not None:
            if not self.checkDui(dui=dui):
                sys.stderr.write("this is an invalid MeSH ID\n")
                exit(1)
            result = self.selectDataByDui(dui=dui, selectCol="Preferred_Name", queryCol="MeSHID")
            if result is not None:
                return result[0]
            else:
                return result

        if cui is not None:
            if not self.checkCui(cui=cui):
                sys.stderr.write("this is an invalid UMLS ID\n")
                exit(1)

            # retrive TreeSubnodeDetailData
            result = self.selectDataByCui(cui=cui, selectCol="Preferred_Name", queryCol="UMLSID")
            if result is not None:
                return result[0]
            else:
                return result

    def getCategory(self, dui=None, cui=None):
        """Get the concept category by MeSH id or UMLS ID.

        | For main heading concept, the category is its tree code first letter.
        | In fact, for NB concept, it has no tree code, so it will has no category, but in this module.
        | We classfy the RN concept to its RB concept's category.

        **parameter**

        dui: string
            MeSH ID.

        cui: string
            UMLS ID.

        **return**

        None or list of string.
        """
        if cui is None and dui is None:
            sys.stderr.write("please input a MeSH ID or UMLS ID\n")
            exit(1)

        if dui is not None and cui is not None:
            sys.stderr.write("can't input both MeSH ID and UMLS ID, please select only one\n")
            exit(1)

        # for cui
        if cui is not None:
            MeSHID = self.getMeSHIDbyUMLSID(cui=cui)
            dui = MeSHID
        # for dui
        if dui is not None:
            if not self.checkDui(dui=dui):
                sys.stderr.write("this is an invalid MeSH ID\n")
                exit(1)
            if dui.startswith("D"):
                if self.MainHeadingDetailData is None:
                    df = self.getMainHeadingDetailData()
                    self.MainHeadingDetailData = df
                else:
                    df = self.MainHeadingDetailData
                # semantictype is a series
                result = df["Category"][df["MeSHID"] == dui]
                if result.empty:
                    sys.stderr.write("your string %s is not in the data\n" % dui)
                    return None
                return list(set(result))

            if dui.startswith("C"):
                if self.RNRBRelData is None:
                    df = self.getRelData(data="RNandRBRel", category="all")
                    self.RNRBRelData = df
                else:
                    df = self.RNRBRelData
                result = df["Category"][df["RNconcept"] == dui]
                if result.empty:
                    sys.stderr.write("your string %s is not in the data\n" % dui)
                    return None
                return list(set(result))

    def getDuiFromTreeCode(self, treeCode=None):
        """Only the main heading concept has tree code.

        **parameter**

        treeCode: string
            MeSH tree code.

        **return**

        string or None.
        """
        if treeCode is None:
            sys.stderr.write("please input the treecode\n")
            exit(1)
        regx = re.compile("^[A-Z][0-9][0-9](\.[0-9][0-9][0-9])*$")
        result = regx.match(treeCode)
        if result:
            if self.MainHeadingDetailData is None:
                df = self.getMainHeadingDetailData()
                self.MainHeadingDetailData = df
            else:
                df = self.MainHeadingDetailData
            result = df["MeSHID"][df["Tree_Code"] == treeCode]
            if result.empty:
                sys.stderr.write("your string %s is not in the data\n" % treeCode)
                return None
            return list(set(result))[0]
        else:
            sys.stderr.write("this is an invalid tree code\n")
            exit(1)

    def getFrequenceByDui(self, dui=None):
        """This function will return the counts of the concept which retrived in a specific text(pubmed article) set

        | Only the main heading concept has this attribute.
        | It is used to calculate the IC(Information Content) Value.

        **parameter**

        dui: string
            MeSH ID.

        **return**

        int
        """
        if dui is None:
            sys.stderr.write("please input the MeSH ID\n")
            exit(1)
        if not self.checkDui(dui=dui):
            sys.stderr.write("this is an invalid MeSH ID\n")
            exit(1)
        if dui.startswith("C"):
            sys.stderr.write("RN concept has no frequence\n")
            return None
        result = self.selectDataByDui(dui=dui, selectCol="Frequence", queryCol="MeSHID")
        if result is None:
            return None
        else:
            return result[0]

    def getAllMHsConceptInOneCategory(self, category=None):
        """Get all MHs in one category."""
        if category not in self.MainHeadingDetailDataInCategory:
            df = self.getMainHeadingDetailData(category=category)
            self.MainHeadingDetailDataInCategory[category] = df
        else:
            df = self.MainHeadingDetailDataInCategory[category]
        conceptList = list(set(list(df["MeSHID"])))
        return conceptList

    def getAllSCRsConceptInOneCategory(self, category=None):
        """Get all SCRs in one category."""
        if category not in self.RNRBRelDataInCategory:
            df = self.getRelData(data="RNandRBRel", category=category)
            self.RNRBRelDataInCategory[category] = df
        else:
            df = self.RNRBRelDataInCategory[category]
        conceptList = list(set(list(df["RNconcept"])))
        return conceptList
