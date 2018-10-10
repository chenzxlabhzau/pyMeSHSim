------------
Tutorial
------------

Parsing free text
==================

Parsing short sentence
^^^^^^^^^^^^^^^^^^^^^^^^
We can access MetaMap with:

>>> from pyMeSHSim.metamapWrap.MetamapInterface import MetaMap
>>> metamap = MetaMap(path="/home/luozhihui/Project/UMLS/public_mm/bin/metamap16")
>>> concept = metamap.runMetaMap(semantic_types=metamap.semanticTypes, text="Ataxias, Gait")
>>> print(concept)
[{'index': '00000000', 'mm': 'MMI', 'score': '20.95', 'preferred_name': 'Gait Ataxia', 'cui': 'C0751837', 'semtypes': '[sosy]', 'trigger': '["Gait Ataxia"-tx-1-"Ataxias Gait"-noun-0]', 'location': 'TX',
'pos_info': '0/7,9/4', 'tree_codes': 'C10.597.350.090.750;C10.597.404.450;C23.888.592.350.090.600;C23.888.592.413.450', 'MeSHID': 'D020234'}]


Parsing long sentence
^^^^^^^^^^^^^^^^^^^^^^^^
When parsing a long sentence, we should turn off the parameters “conjunction”, “term_processing” as following:


>>> from pyMeSHSim.metamapWrap.MetamapInterface import MetaMap
>>> metamap = MetaMap(path="/home/luozhihui/Project/UMLS/public_mm/bin/metamap16")
>>> concept = metamap.runMetaMap(semantic_types=metamap.semanticTypes , conjunction=False, term_processing=False, text="131-I-TM-601 is investigated in clinical trials for treating brain cancer. 131-I-TM-601 is a solid. Tx binds to and reduces the activity of a matrix metalloproteinase (MMP) that regulates functioning of the chloride channels on cell membranes. TM-601 is a small 36-amino-acid peptide that selectively binds to glioma cells but not normal brain parenchyma. It is a synthetic version of a neurotoxin isolated from the venom of the Giant Yellow Israeli scorpion Leiurus quinquestriatus. The synthetic version of this peptide has been manufactured and covalently linked to iodine 131 ((131)I-TM-601) as a means of targeting radiation to tumor cells in the treatment of brain cancer. The selective effects of TM-601 are regulated by its action on MMP2 receptors.")
>>> for con in concept:
>>>     print(con)
{'index': '00000000', 'mm': 'MMI', 'score': '19.34', 'preferred_name': 'Glioma', 'cui': 'C0017638', 'semtypes': '[neop]', 'trigger': '["Glioma"-tx-4-"glioma"-noun-0]', 'location': 'TX', 'pos_info': '310/6', 'tree_codes': 'C04.557.465.625.600.380;C04.557.470.670.380;C04.557.580.625.600.380', 'MeSHID': 'D005910'}
{'index': '00000000', 'mm': 'MMI', 'score': '16.22', 'preferred_name': 'Brain Neoplasms', 'cui': 'C0006118', 'semtypes': '[neop]', 'trigger': '["Brain Neoplasms"-tx-6-"tumor the of brain"-noun-0]', 'location': 'TX', 'pos_info': '633/5,648/3,662/8', 'tree_codes': 'C04.588.614.250.195;C10.228.140.211;C10.551.240.250', 'MeSHID': 'D001932'}
{'index': '00000000', 'mm': 'MMI', 'score': '13.00', 'preferred_name': 'Gigantism', 'cui': 'C0017547', 'semtypes': '[dsyn]', 'trigger': '["Gigantism"-tx-5-"Giant"-adj-0]', 'location': 'TX', 'pos_info': '429/5', 'tree_codes': 'C05.116.099.492;C05.116.132.479;C19.700.355.528', 'MeSHID': 'D005877'}
{'index': '00000000', 'mm': 'MMI', 'score': '12.89', 'preferred_name': 'Electromagnetic Radiation', 'cui': 'C0034519', 'semtypes': '[npop]', 'trigger': '["Electromagnetic Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.358.500.505;G01.750.250', 'MeSHID': 'D060733'}
{'index': '00000000', 'mm': 'MMI', 'score': '10.06', 'preferred_name': 'Plasma membrane', 'cui': 'C0007603', 'semtypes': '[celc]', 'trigger': '["Plasma Membrane"-tx-3-"cell membranes"-noun-0]', 'location': 'TX', 'pos_info': '228/14', 'tree_codes': 'A11.284.149', 'MeSHID': 'D002462'}
{'index': '00000000', 'mm': 'MMI', 'score': '9.92', 'preferred_name': 'Brain', 'cui': 'C0006104', 'semtypes': '[bpoc]', 'trigger': '["Brain"-tx-4-"brain"-noun-0]', 'location': 'TX', 'pos_info': '338/5', 'tree_codes': 'A08.186.211', 'MeSHID': 'D001921'}
{'index': '00000000', 'mm': 'MMI', 'score': '9.69', 'preferred_name': 'Genetic Selection', 'cui': 'C0036576', 'semtypes': '[genf]', 'trigger': '["Genetic Selection"-tx-7-"selective"-adj-0]', 'location': 'TX', 'pos_info': '683/9', 'tree_codes': 'G05.355.800', 'MeSHID': 'D012641'}
{'index': '00000000', 'mm': 'MMI', 'score': '7.17', 'preferred_name': 'Malignant neoplasm of brain', 'cui': 'C0153633', 'semtypes': '[neop]', 'trigger': '["Brain Neoplasm, Malignant"-tx-6-"the of brain cancer"-noun-0,"Brain Neoplasm, Malignant"-tx-1-"brain cancer"-noun-0]', 'location': 'TX', 'pos_info': '648/3,662/15;61/12', 'tree_codes': '', 'MeSHID': None}
{'index': '00000000', 'mm': 'MMI', 'score': '7.15', 'preferred_name': 'Cells', 'cui': 'C0007634', 'semtypes': '[cell]', 'trigger': '["Cells"-tx-6-"cells"-noun-0,"Cells"-tx-4-"cells"-noun-0]', 'location': 'TX', 'pos_info': '639/5;317/5', 'tree_codes': 'A11', 'MeSHID': 'D002477'}
{'index': '00000000', 'mm': 'MMI', 'score': '6.58', 'preferred_name': 'Radiation', 'cui': 'C0851346', 'semtypes': '[npop]', 'trigger': '["Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.750', 'MeSHID': 'D011827'}
{'index': '00000000', 'mm': 'MMI', 'score': '3.54', 'preferred_name': 'Neoplasms', 'cui': 'C0027651', 'semtypes': '[neop]', 'trigger': '["Neoplasms"-tx-6-"tumor"-noun-0]', 'location': 'TX', 'pos_info': '633/5', 'tree_codes': 'C04', 'MeSHID': 'D009369'}
{'index': '00000000', 'mm': 'MMI', 'score': '3.42', 'preferred_name': 'Malignant Neoplasms', 'cui': 'C0006826', 'semtypes': '[neop]', 'trigger': '["Cancer"-tx-6-"cancer"-noun-0]', 'location': 'TX', 'pos_info': '671/6', 'tree_codes': '', 'MeSHID': None}



Filtering the result
^^^^^^^^^^^^^^^^^^^^^^^^^
While parsing a long sentence, we will get many results. We can discard the ancestor concepts.

>>> from pyMeSHSim.Sim.similarity import metamapFilter
>>> filter = metamapFilter(path="/home/luozhihui/Project/UMLS/public_mm/bin/metamap16")
>>> concepts = filter.runMetaMap(semantic_types=filter.semanticTypes , conjunction=False, term_processing=False, text="131-I-TM-601 is investigated in clinical trials for treating brain cancer. 131-I-TM-601 is a solid. Tx binds to and reduces the activity of a matrix metalloproteinase (MMP) that regulates functioning of the chloride channels on cell membranes. TM-601 is a small 36-amino-acid peptide that selectively binds to glioma cells but not normal brain parenchyma. It is a synthetic version of a neurotoxin isolated from the venom of the Giant Yellow Israeli scorpion Leiurus quinquestriatus. The synthetic version of this peptide has been manufactured and covalently linked to iodine 131 ((131)I-TM-601) as a means of targeting radiation to tumor cells in the treatment of brain cancer. The selective effects of TM-601 are regulated by its action on MMP2 receptors.")
>>> results = filter.discardAncestor(concepts=concepts)
>>> for res in results:
>>>     print (res)
{'index': '00000000', 'mm': 'MMI', 'score': '6.58', 'preferred_name': 'Radiation', 'cui': 'C0851346', 'semtypes': '[npop]', 'trigger': '["Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.750', 'MeSHID': 'D011827'}
{'index': '00000000', 'mm': 'MMI', 'score': '9.69', 'preferred_name': 'Genetic Selection', 'cui': 'C0036576', 'semtypes': '[genf]', 'trigger': '["Genetic Selection"-tx-7-"selective"-adj-0]', 'location': 'TX', 'pos_info': '683/9', 'tree_codes': 'G05.355.800', 'MeSHID': 'D012641'}
{'index': '00000000', 'mm': 'MMI', 'score': '16.22', 'preferred_name': 'Brain Neoplasms', 'cui': 'C0006118', 'semtypes': '[neop]', 'trigger': '["Brain Neoplasms"-tx-6-"tumor the of brain"-noun-0]', 'location': 'TX', 'pos_info': '633/5,648/3,662/8', 'tree_codes': 'C04.588.614.250.195;C10.228.140.211;C10.551.240.250', 'MeSHID': 'D001932'}
{'index': '00000000', 'mm': 'MMI', 'score': '13.00', 'preferred_name': 'Gigantism', 'cui': 'C0017547', 'semtypes': '[dsyn]', 'trigger': '["Gigantism"-tx-5-"Giant"-adj-0]', 'location': 'TX', 'pos_info': '429/5', 'tree_codes': 'C05.116.099.492;C05.116.132.479;C19.700.355.528', 'MeSHID': 'D005877'}
{'index': '00000000', 'mm': 'MMI', 'score': '7.15', 'preferred_name': 'Cells', 'cui': 'C0007634', 'semtypes': '[cell]', 'trigger': '["Cells"-tx-6-"cells"-noun-0,"Cells"-tx-4-"cells"-noun-0]', 'location': 'TX', 'pos_info': '639/5;317/5', 'tree_codes': 'A11', 'MeSHID': 'D002477'}
{'index': '00000000', 'mm': 'MMI', 'score': '9.92', 'preferred_name': 'Brain', 'cui': 'C0006104', 'semtypes': '[bpoc]', 'trigger': '["Brain"-tx-4-"brain"-noun-0]', 'location': 'TX', 'pos_info': '338/5', 'tree_codes': 'A08.186.211', 'MeSHID': 'D001921'}
{'index': '00000000', 'mm': 'MMI', 'score': '12.89', 'preferred_name': 'Electromagnetic Radiation', 'cui': 'C0034519', 'semtypes': '[npop]', 'trigger': '["Electromagnetic Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.358.500.505;G01.750.250', 'MeSHID': 'D060733'}
{'index': '00000000', 'mm': 'MMI', 'score': '19.34', 'preferred_name': 'Glioma', 'cui': 'C0017638', 'semtypes': '[neop]', 'trigger': '["Glioma"-tx-4-"glioma"-noun-0]', 'location': 'TX', 'pos_info': '310/6', 'tree_codes': 'C04.557.465.625.600.380;C04.557.470.670.380;C04.557.580.625.600.380', 'MeSHID': 'D005910'}
{'index': '00000000', 'mm': 'MMI', 'score': '3.54', 'preferred_name': 'Neoplasms', 'cui': 'C0027651', 'semtypes': '[neop]', 'trigger': '["Neoplasms"-tx-6-"tumor"-noun-0]', 'location': 'TX', 'pos_info': '633/5', 'tree_codes': 'C04', 'MeSHID': 'D009369'}
{'index': '00000000', 'mm': 'MMI', 'score': '10.06', 'preferred_name': 'Plasma membrane', 'cui': 'C0007603', 'semtypes': '[celc]', 'trigger': '["Plasma Membrane"-tx-3-"cell membranes"-noun-0]', 'location': 'TX', 'pos_info': '228/14', 'tree_codes': 'A11.284.149', 'MeSHID': 'D002462'}


We can also discard general MeSH terms with too many descendants.

>>> from pyMeSHSim.Sim.similarity import metamapFilter
>>> filter = metamapFilter(path="/home/luozhihui/Project/UMLS/public_mm/bin/metamap16")
>>> concepts = filter.runMetaMap(semantic_types=filter.semanticTypes , conjunction=False, term_processing=False, text="131-I-TM-601 is investigated in clinical trials for treating brain cancer. 131-I-TM-601 is a solid. Tx binds to and reduces the activity of a matrix metalloproteinase (MMP) that regulates functioning of the chloride channels on cell membranes. TM-601 is a small 36-amino-acid peptide that selectively binds to glioma cells but not normal brain parenchyma. It is a synthetic version of a neurotoxin isolated from the venom of the Giant Yellow Israeli scorpion Leiurus quinquestriatus. The synthetic version of this peptide has been manufactured and covalently linked to iodine 131 ((131)I-TM-601) as a means of targeting radiation to tumor cells in the treatment of brain cancer. The selective effects of TM-601 are regulated by its action on MMP2 receptors.")
>>> results = filter.discardNodeHigh(number=50, concepts=concepts)
>>> for res in results:
>>>     print (res)
{'index': '00000000', 'mm': 'MMI', 'score': '19.34', 'preferred_name': 'Glioma', 'cui': 'C0017638', 'semtypes': '[neop]', 'trigger': '["Glioma"-tx-4-"glioma"-noun-0]', 'location': 'TX', 'pos_info': '310/6', 'tree_codes': 'C04.557.465.625.600.380;C04.557.470.670.380;C04.557.580.625.600.380', 'MeSHID': 'D005910'}
{'index': '00000000', 'mm': 'MMI', 'score': '16.22', 'preferred_name': 'Brain Neoplasms', 'cui': 'C0006118', 'semtypes': '[neop]', 'trigger': '["Brain Neoplasms"-tx-6-"tumor the of brain"-noun-0]', 'location': 'TX', 'pos_info': '633/5,648/3,662/8', 'tree_codes': 'C04.588.614.250.195;C10.228.140.211;C10.551.240.250', 'MeSHID': 'D001932'}
{'index': '00000000', 'mm': 'MMI', 'score': '13.00', 'preferred_name': 'Gigantism', 'cui': 'C0017547', 'semtypes': '[dsyn]', 'trigger': '["Gigantism"-tx-5-"Giant"-adj-0]', 'location': 'TX', 'pos_info': '429/5', 'tree_codes': 'C05.116.099.492;C05.116.132.479;C19.700.355.528', 'MeSHID': 'D005877'}
{'index': '00000000', 'mm': 'MMI', 'score': '12.89', 'preferred_name': 'Electromagnetic Radiation', 'cui': 'C0034519', 'semtypes': '[npop]', 'trigger': '["Electromagnetic Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.358.500.505;G01.750.250', 'MeSHID': 'D060733'}
{'index': '00000000', 'mm': 'MMI', 'score': '10.06', 'preferred_name': 'Plasma membrane', 'cui': 'C0007603', 'semtypes': '[celc]', 'trigger': '["Plasma Membrane"-tx-3-"cell membranes"-noun-0]', 'location': 'TX', 'pos_info': '228/14', 'tree_codes': 'A11.284.149', 'MeSHID': 'D002462'}
{'index': '00000000', 'mm': 'MMI', 'score': '9.69', 'preferred_name': 'Genetic Selection', 'cui': 'C0036576', 'semtypes': '[genf]', 'trigger': '["Genetic Selection"-tx-7-"selective"-adj-0]', 'location': 'TX', 'pos_info': '683/9', 'tree_codes': 'G05.355.800', 'MeSHID': 'D012641'}
{'index': '00000000', 'mm': 'MMI', 'score': '7.17', 'preferred_name': 'Malignant neoplasm of brain', 'cui': 'C0153633', 'semtypes': '[neop]', 'trigger': '["Brain Neoplasm, Malignant"-tx-6-"the of brain cancer"-noun-0,"Brain Neoplasm, Malignant"-tx-1-"brain cancer"-noun-0]', 'location': 'TX', 'pos_info': '648/3,662/15;61/12', 'tree_codes': ['C10.551.240.250', 'C10.228.140.211', 'C04.588.614.250.195'], 'MeSHID': 'D001932'}
{'index': '00000000', 'mm': 'MMI', 'score': '6.58', 'preferred_name': 'Radiation', 'cui': 'C0851346', 'semtypes': '[npop]', 'trigger': '["Radiation"-tx-6-"radiation"-noun-0]', 'location': 'TX', 'pos_info': '620/9', 'tree_codes': 'G01.750', 'MeSHID': 'D011827'}



Term library
======================
Apart from metamapWrap, class termComp inherits all the class in pyMeSHSim, and thus many functions can be invoked by termComp.


Obtaining MeSH terms from UMLS concepts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> concept = simCom.getMeSHConcept(cui="C0024116")
>>> print(concept)
{'cui': 'C0024116', 'MeSHID': 'D008172', 'semtypes': 'dsyn', 'tree_code': ['C08.730.435', 'C01.703.534', 'C08.381.472'], 'preferred_name': 'Fungal Lung Disease'}


Obtaining MeSH term detail from MeSH ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| This method will be helpful.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> concept = simCom.getMeSHConcept(dui="D008674")
>>> print(concept)
{'cui': 'C0025556', 'MeSHID': 'D008674', 'semtypes': 'elii', 'tree_code': ['D01.268.558', 'D01.552.550'], 'preferred_name': 'Earth Metals, Rare'}

Obtaining UMLS concept from MeSH ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If one MeSH record corresponds to more than one UMLS concepts, pyMeSHSim only provides the recommended one.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> con = simCom.getUMLSIDbyMeSHID(dui="D008674")
>>> print (con)
C0025556


Obtaining the category of MeSH terms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| A lot of processing should denote the category of terms, it is necessary to get it in the begining.
| getCategory will return the category of a term.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> ty = simCom.getCategory(dui="D008674")
>>> print (ty)
['D']
>>>ty = simCom.getCategory(dui="D008674")
>>>print (ty)
['F']

Obtaining narrow or broad terms of a mesh term
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can obtain the narrow terms of main headings by convertToNarrow and obtain the broad terms of SCRs by convertToBroad.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> NRs = simCom.convertToNarrow(dui="D000544")
>>> print (Nrs)
['C564330', 'C565078', 'C565228', 'C563834', 'C565251', 'C565325', 'C567463', 'C566465', 'C567022', 'C566999', 'C536595', 'C566998', 'C566578', 'C563254', 'C536596', 'C564622', 'C536594', 'C566298', 'C567000', 'C564329', 'C566299', 'C565728', 'C536598', 'C536599']
>>> BRs = simCom.convertToBroad(dui="C565078")
>>> print (BRs)
['D000544']


Obtaining parent or child terms of a MeSH term
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can obtain child and parent terms of main headings by getParentsConceptID and getChildrenConceptID, respectively.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> parents = simCom.getParentsConceptID(dui="D000544", category="C")
>>> print (parents)
['D024801', 'D003704']
>>> children = simCom.getChildrenConceptID(dui="D012559", category="F")
>>> print (children)
['D012753', 'D012562', 'D012563', 'D012560']


Obtaining the top term of a MeSH term
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can obtain the top term of a MeSH term by getTopConceptID.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> topTerm = simCom.getTopConceptID(dui="D000544")
>>> print (topTerm)
{'D001523': 'Disorders, Mental', 'D009422': 'Diseases, Nervous System'}

Obtaining the ancestors or offsprings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can obtain ancestors or offsprings of main headings by getAncestors or getDescendant, respectively.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> ancestors = simCom.getAncestors(dui="D000544", category="C")
>>> print (ancestors)
['D000544', 'D024801', 'D003704', 'D019636', 'D001927', 'D009422', 'D002493']
>>> descendant = simCom.getDescendant(dui="D012559", category="F")
>>> print (descendant)
['D012559', 'D012563', 'D012753', 'D012562', 'D012560']


Retrieving MeSH ID by MeSH tree code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> dui = simCom.getDuiFromTreeCode(treeCode="D01.552.550")
>>> print(dui)
D008674


Obtaining the preffered name by MeSH ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can obtain the preffered name of MeSH terms by getPrefferedName.

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> name = simCom.getPrefferedName(dui="D008674")
>>> print(name)
Earth Metals, Rare


Calculating similarity
===========================

Calculating similarity between MeSH terms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We can calculate semantic similarity between MeSH terms with five algorithms [“lin”, “res”, “jiang”, “rel”, “wang”].

>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> #in different category, the similarity will be different
>>> simCom.termSim(dui1="D000544", dui2="D006816", method="lin", category="F")
D000544	D006816	0.6957847588446384
>>> simCom.termSim(dui1="D000544", dui2="D006816", method="lin", category="C")
D000544	D006816	0.7500806317732097


>>> from pyMeSHSim.Sim.similarity import termComp
>>> simCom = termComp()
>>> #between mainheading and SCR, IC method
>>> simCom.termSim(dui1="C565251", dui2="D012559", method="rel", category="F")
C565251	D012559	0.3314002496646189
>>> #based on path
>>> simCom.termSim(dui1="C565251", dui2="D012559", method="wang", category="F")
C565251	D012559	0.17637095066694894


