# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import sys
from ..data.duiFunc import duiFunc

class Concept(object):
    """This is base class of MetaMap in metamapWrap."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        return str(self.__dict__)


    @classmethod
    def MMIConcept(cls, mmi_array=None):
        """This method used to create a concept object

        | mmi output format still will create AA and UA result, but abbreviation recognition always mistake.
        | We drop these result.

        **Attribute of mmi concept**

        | "index" : text serial number
        | "mm": result type
        | score: result score, higher means more accurate
        | preffered_name: freferred name
        | cui: UMLS ID
        | semtypes: semantic type
        | trigger: Comma separated sextuple showing what triggered MMI to identify this UMLS concept
        | location: Summarizes where UMLS concept was found
        | pos_info: Semicolon-separated list of positional-information terns
        | tree_codes: Semicolon-separated list of any MeSH treecode

        **parameter**

        mmi_array: list
            The MetaMap result with option -N.

        **return**

        Concept object.
        """
        mmi_name = ('index', 'mm', 'score', 'preferred_name', 'cui', 'semtypes',
                    'trigger', 'location', 'pos_info', 'tree_codes')
        d = dict(zip(mmi_name, mmi_array))
        if d["cui"] is not None:
            duiFunction = duiFunc()
            MeSHID = duiFunction.getMeSHIDbyUMLSID(cui=d["cui"])
            d["MeSHID"] = MeSHID
        if d["tree_codes"] == "" and d["MeSHID"] is not None and d["MeSHID"].startswith("D"):
            treeCode = duiFunction.getMeSHTreecode(dui=d["MeSHID"])
            d["tree_codes"] = treeCode

        return cls(**d)

    @classmethod
    def MeSHConcept(cls, cui=None, dui=None, tree_code=None):
        """This method create a concept object.

        Only can select one paremeter.

        **parameter**

        cui: String
            UMLS ID.

        dui: String
            MeSH ID.

        tree_code: String
            MeSH tree number.

        **return**

        Concept object
        """
        d = {}
        duiFunction = duiFunc()
        flag = 0
        if dui is not None:
            flag = flag + 1

        if cui is not None:
            flag = flag + 1

        if tree_code is not None:
            flag = flag + 1

        if flag >=2:
            sys.stderr.write("Please input only one parameter in [dui, cui, tree_code] \n")
            exit(1)

        if flag ==0:
            sys.stderr.write("None parameter has been set\n")
            exit(1)

        if tree_code is not None:
            dui = duiFunction.getDuiFromTreeCode(treeCode=tree_code)

        if dui is not None:
            if not duiFunction.checkDui(dui=dui):
                sys.stderr.write("this is an invalid MeSH ID\n")
                exit(1)

            semanticType = duiFunction.getSemanticType(dui=dui)
            treeCode = duiFunction.getMeSHTreecode(dui=dui)
            UMLSID = duiFunction.getUMLSIDbyMeSHID(dui=dui)
            prefferredName = duiFunction.getPrefferedName(dui=dui)
            d["cui"] = UMLSID
            d["MeSHID"] = dui
            d["semtypes"] = semanticType
            d["tree_code"] = treeCode
            d['preferred_name'] = prefferredName




        if cui is not None:
            if not duiFunction.checkCui(cui=cui):
                sys.stderr.write("this is an invalid UMLS ID\n")
                exit(1)
            semanticType = duiFunction.getSemanticType(cui=cui)
            treeCode = duiFunction.getMeSHTreecode(cui=cui)
            MeSHID = duiFunction.getMeSHIDbyUMLSID(cui=cui)
            prefferredName = duiFunction.getPrefferedName(cui=cui)
            d["cui"] = cui
            d["MeSHID"] = MeSHID
            d["semtypes"] = semanticType
            d["tree_code"] = treeCode
            d['preferred_name'] = prefferredName
        return cls(**d)

