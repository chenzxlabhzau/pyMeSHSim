# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University


#!/usr/bin/python3
from .PathScore import pathMethod
from ..metamapWrap.MetamapInterface import MetaMap
import sys, copy

class termComp(pathMethod):

    def __init__(self):
        pathMethod.__init__(self)

    def termSim(self, dui1=None, dui2=None, category=None, method=None):
        """This function used to measure the distance between two MeSH terms. including MHs and SCRs.

        **parameter**

        dui1: String
            MeSH ID.

        dui1: String
            MeSH ID.

        category: String
            A MeSH category.
            One of the value in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'V', 'Z').
            It can't be None.

        method: String
            One value in ["lin", "res", "jiang", "rel", "wang"].

        **return**

        list of float
        """

        if not self.checkDui(dui=dui1):
            sys.stderr.write("invalid MeSH ID in dui1\n")
            exit(1)

        if not self.checkDui(dui=dui2):
            sys.stderr.write("invalid MeSH ID in dui2\n")
            exit(1)

        term_list_1 = []
        if dui1.startswith("C"):
            BRs1 = self.convertToBroad(dui=dui1)
            if len(BRs1) == 0:
                sys.stderr.write("MeSH concept %s has no broad terms\n" % dui1)
                exit(1)
            else:
                term_list_1 = copy.deepcopy(BRs1)
        else:
            term_list_1 = [dui1]

        term_list_2 = []
        if dui2.startswith("C"):
            BRs2 = self.convertToBroad(dui=dui2)
            if len(BRs2) == 0:
                sys.stderr.write("MeSH concept %s has no broad terms\n" % dui2)
                exit(1)
            else:
                term_list_2 = copy.deepcopy(BRs2)
        else:
            term_list_2 = [dui2]


        score_list = []
        for con1 in term_list_1:
            for con2 in term_list_2:
                if method in ["lin", "res", "jiang", "rel"]:
                    score = self.calICSimilarity(dui1=con1, dui2=con2, category=category, method=method)
                elif method == "wang":
                    score = self.calPathSimilarity(dui1=con1, dui2=con2, category=category)
                score_list.append(score)
                print("%s\t%s\t%s\n" % (dui1, dui2, score))

        return score_list

class metamapFilter(MetaMap, pathMethod):
    """This class inherits from MetaMap and pathMethod."""

    def __init__(self, path=None):
        MetaMap.__init__(self, path=path)
        pathMethod.__init__(self)

    def discardAncestor(self, concepts=None):
        """Discard the ancestor concept in one parse result.

        **parameter**

        concepts: list
            A list of dict, result of runmetamap.

        **return**

        a list of concept
        """
        if len(concepts) <=0 or concepts is None:
            sys.stderr.write("no items in concepts\n")
            exit(1)

        mesh_dict = {}
        for con in concepts:
            if con["MeSHID"] is None:
                continue
            dui = con["MeSHID"]
            if dui not in mesh_dict:
                mesh_dict[dui] = con

        if len(mesh_dict) == 0:
            return concepts

        all_meshid = mesh_dict.keys()
        for key in all_meshid:
            cates = self.getCategory(dui=key)
            ances_list = []
            for cate in cates:
                ancestors = self.getAncestors(dui="D000544", category=cate)
                ances_list = ances_list + ancestors
            if key in ances_list:
                ances_list.remove(key)
            #tmp = [val for val in ances_list if val in all_meshid]
            all_meshid = list(set(all_meshid).difference(set(ances_list)))

        new_concept = []
        for id in all_meshid:
            new_concept.append(mesh_dict[id])

        return new_concept


    def discardNodeHigh(self, number=None, concepts=None):
        """This method will discard the concept which is in a high leve, has many offsprings.


        **parameter**

        number: int
            Threshold value, above this value will be discarded.

        concepts: list
            A list of dict, result of runmetamap.

        **return**

        list of concept
        """

        if len(concepts) <=0 or concepts is None:
            sys.stderr.write("no items in concepts\n")
            exit(1)

        new_concept = []
        for con in concepts:

            if con["MeSHID"] is None:
                continue
            dui = con["MeSHID"]
            cates = self.getCategory(dui=dui)
            descen_list = []
            for cate in cates:
                offsp = self.getDescendant(dui=dui, category=cate)
                descen_list = descen_list + offsp
            if dui in descen_list:
                descen_list.remove(dui)
            if len(descen_list) > number:
                continue
            else:
                new_concept.append(con)

        return new_concept


