# Author: ZhiHui Luo
# Organization: HuaZhong Agricultural University

#!/usr/bin/python3
import os
import re
import sys
import time
from subprocess import *
import tempfile

from .Concept import Concept
from ..data.dataInterface import dataHandle


class Basic(object):
    def __init__(self):
        pass

    @staticmethod
    def run(cmd=None, wkdir=None):
        sys.stderr.write("Running %s ...\n" % cmd)
        p = Popen(cmd, shell=True, cwd=wkdir, stdout=PIPE)
        p.wait()
        return p


class MetaMap(object):
    """This class wraps the natural-language processing software "MetaMap".

    | Which can map biomedical text to the UMLS Metathesaurus.
    | As base of this work, MetaMap should has been installed.

    **parameter**

    path : str
        | metamap path.
        | eg. path="/home/Project/UMLS/public_mm/bin/metamap16".
        | please avoid to use this "/home/Project/UMLS/public_mm/bin/metamap" execute file path.
        | this module will select the parameters according your metamap version.

    **attributes**

    metamap: String
        | metamap path.

    metamapBinDir: String
        | metamap bin directory.

    skrmedpostctl: String
        | skrmedpostctl path, it is component of metamap.
        | start skrmedpostctl to start metamap.

    wsdserverctl: String
        | wsdserverctl path, it is component of metamap.
        | strat wsdserverctl to start metamap.

    semanticTypes: List
        | it contains the semantic type abbreviation in UMLS Metathesaurus.
        | like ["dsyn", "anab", "inpo", ....].
        | this value comes from table "parent".

    mmiName: Tuple
        | The SKR program is an extension of MetaMap, it formats the metamap's output.
        | such as
        | \'00000000 | MM | 4 | Complication | C0009566 | [patf] | ["Complications"-tx-1-"complications"] \|AB\'
        | columns seperated by "|", this attribute store the corresponding column's name.


    this class will create metamap object.

    **see also**

    pyMeSHSim.metamapWrap.Concept
    """

    def __init__(self, path=None):
        # p = Basic.run(cmd="which metamap")
        # self.metamap = p.stdout.read().decode().strip("\n")
        if path is None or path == "":
            sys.stderr.write("metamap path can't be None\n")
            exit(1)
        self.metamap = path
        self.metamapBinDir = os.path.dirname(self.metamap)
        self.skrmedpostctl = os.path.join(self.metamapBinDir, "skrmedpostctl")
        self.wsdserverctl = os.path.join(self.metamapBinDir, "wsdserverctl")
        self.datahandle = dataHandle()
        # self.semanticTypes = ["acab", "anab", "comd", "cgab", "dsyn", "emod", "inpo", "mobd", "neop", "patf"]
        self.semanticTypes = self.datahandle.getParentTableSemantiTypes()
        self.mminName = ('index', 'mm', 'score', 'preferred_name', 'cui', 'semtypes',
                         'trigger', 'location', 'pos_info', 'tree_codes')

    def startMetaMap(self):
        """Start metamap service"""

        cmd = self.skrmedpostctl + "\t" + "start"
        Basic.run(cmd)
        time.sleep(5)
        cmd = self.wsdserverctl + "\t" + "start"
        Basic.run(cmd)
        time.sleep(10)

    def runMetaMap(self, text=None, source=["MSH"], semantic_types=None, ignore_word_order=True, \
                   conjunction=True, composite_phrases=4, silent=True, sldi=True, sldiID=False, \
                   term_processing=True, input_file_path=None, text_convert=False
                   ):
        """The main method run the MetaMap.

        **parameters**

        text : String
            The free text will  be processed.

        source : List
            | A list of string, the source of UMLS Metathesaurus.
            | MSH (MeSH).
            | MTH (Metathesaurus Names).
            | SNOMEDCT_US (US Edition of SNOMED CT).
            | OMIM (Online Mendelian Inheritance in Man).
            | ICD10CM (International Classification of Diseases, Tenth Revision, Clinical Modification).
            | ...
            | eg. ["MSH", "MTH"].
            | default: ["MSH"].

        semantic_types: List
            | A list of string, containing the abbr. of different semantic type.
            | default: None.
            | It is all semantic types occur in MeSH "Disease" category, get from table "parents".

        ignore_word_order: True or False
            | Allows MetaMap to ignore the order of words in the input text.
            | default: True.

        conjunction: True or False
            | Causes MetaMap's phrase chunker to recombine smaller phrases separated by a conjunction.
            | This argument exists only in version 2016.
            | default: False.

        composite_phrases: int
            | Causes MetaMap to construct longer, composite phrases from the smaller phrases produced by the parser.
            | default: 4.

        silent: True or False
            | Suppresses the display of header information.
            | default: True.

        sldi: True or False
            | MetaMap by default expects input records to be separated by a blank line.
            | To process such a list of terms without inserting a blank line between each term, call MetaMap with the
            | --sldi (Single-Line Delimited Input) option.
            | the input File example:
            | ---------------------------------
            | Written informed consent.
            | Age 18 years or older.
            | informed consent.
            | Male or female.
            | At least 18 years of age.
            | Able to give informed consent.
            | Signed informed consent.
            | Healthy.
            | Male.
            | ---------------------------------
            | default: True.

        slidID: True or False
            | This parameter can be use only in the situation that input_file_path is not None, and text is None.
            | The input file format should be like below.
            | This input format is very similar to that described in List of Terms. To associate a specific term ID (similar to a MEDLINE PMID) with each term in a list, simply prefix each term with an ID followed by a pipe symbol \|".
            | eg.

            | Txt001|Written informed consent.
            | Txt002|Age 18 years or older.
            | Txt003|informed consent.
            | Txt004|Male or female.
            | Txt005|At least 18 years of age.
            | Txt006|Able to give informed consent.
            | Txt007|Signed informed consent.
            | Txt008|Healthy.
            | Txt009|Male.


        term_processing: True or False
            | Each term will be analyzed as a single phrase, and not chunked into separate components.
            | default: True

        input_file_path: String or None
            | MetaMap input file.
            | default: None

        text_convert: True or False
            | this parameter will be set only when set the "sldiID" option.
            | "|" is the seperate character in sldiID format, if its in you free text.
            | The software will mistake.
            | default False.

        **return**

        list of concept object or None.

        **see also**

        | pyMeSHSim.data.dataInterface
        | pyMeSHSim.metamapWrap.Concept
        """

        if text is not None and input_file_path is not None:
            sys.stderr.write("please only chose one parameter in text and input_file_Path\n")
            exit(1)

        if text is not None and not isinstance(text, str):
            sys.stderr.write("text must be string\n")
            exit(1)

        if input_file_path is not None:
            if not isinstance(input_file_path, str):
                sys.stderr.write("input_file_path must be string\n")
                exit(1)

            if not os.path.exists(input_file_path):
                sys.stderr.write("file doesn't exits\n")
                exit(1)

        initCMD = [self.metamap, "-N"]

        #set ST, if None skip this parameter
        if semantic_types is not None:
            if isinstance(semantic_types, list) and len(semantic_types) > 0:
                restrictST = ",".join(semantic_types)
            else:
                sys.stderr.write("semantic_types is invalid type, need a list\n")
                exit(1)
            initCMD.append("-J %s" % restrictST)

        #set source
        if isinstance(source, list) and len(source) >0:
            sourceUMLS = ",".join(source)
            sourceUMLS = "-R " + sourceUMLS
            initCMD.append(sourceUMLS)

        #set i
        if ignore_word_order is True:
            initCMD.append("-i")

        #set z
        if term_processing is True:
            initCMD.append("-z")

        #get metamap version, set conj
        exe = os.path.basename(self.metamap)
        result = re.match("metamap(\d*)", exe)
        if result:
            version = int(result.groups()[0])
        else:
            version = 0
        if conjunction is True and version >= 16:
            initCMD.append("--conj")
        #set Q
        if isinstance(composite_phrases, int):
            initCMD.append("-Q %s" % composite_phrases)
        #set silent
        if silent is True:
            initCMD.append("--silent")
        #set sldi and sldiID
        if sldi is True and sldiID is True:
            sys.stderr.write("sldi and sldiID can't be simultaneously turned On")
        if sldi is True:
            initCMD.append("--sldi")
        if sldiID is True:
            initCMD.append("--sldiID")
        #input file
        if text is not None:
            inputFile = tempfile.NamedTemporaryFile(mode="w", delete=True)
            inputFile.write("%s\n" % text)
            inputFile.flush()
        else:
            inputFile = input_file_path
        #output file
        outputFile = tempfile.NamedTemporaryFile(mode="r", delete=True)

        initCMD.append(inputFile.name)
        initCMD.append(outputFile.name)
        cmdString = "\t".join(initCMD)
        #run
        try:
            p = Basic.run(cmd=cmdString)
        except:
            sys.stderr.write(p.stdout.read())
            exit(1)
        concepts = self._parseMMI(outputFile)
        return concepts

    def _parseMMI(self, text_handle=None):
        """Parse the output of MetaMap.

        **parameter**

        text_handle: file handle
            Produced in runMetaMap method.

        **return**

        list of dict
        """
        concepts = []
        if text_handle is None:
            sys.stderr("No MetaMap result")
            exit(1)
        for line in text_handle:
            if line is "\n" or line is None:
                continue
            mmi_array = line.strip("\n").split("|")
            #select the only mmi output
            #except from mmi, there are "ua" and "aa", more
            if mmi_array[1] == "MMI":
                concept = Concept.MMIConcept(mmi_array=mmi_array)
                concepts.append(concept.__dict__)
        text_handle.close()
        return concepts


