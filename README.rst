please use the latest version in： https://github.com/luozhhub/pyMeSHSim
I always fix some bugs in my personal project.



------------
Introduction
------------

More details can be seen in the newest `reference <https://pymeshsim.readthedocs.io/en/latest/>`_.

cite：Luo, Z., Shi, M., Yang, Z. et al. pyMeSHSim: an integrative python package for biomedical named entity recognition, normalization, and comparison of MeSH terms. BMC Bioinformatics 21, 252 (2020). https://doi.org/10.1186/s12859-020-03583-6

pyMeSHSim at glance
===================

Biomedical named entity (Bio-NE) recognition, normalization, and comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The recognition and normalization of bio-NE, especially for diseases, play an important
role in clinical and biomedical research, such as clinical decision support, cohort
identification, pharmacovigilance, and drug repositioning. For example, bio-NE recognition
and normalization are prerequisites for semantic analysis, including semantic comparison
of bio-NEs in drug repositioning. However, there are multiple synonyms, abbreviations and
variations for bio-NEs, making it challenging to curate bio-NEs from free biomedical text or
clinical narrative text.

MeSH
^^^^^^^^^^^^^^
We extracted bio-NEs from free biomedical text and measured semantic similarity between
the bio-NEs based on the `Medical Subject Headings(MeSH) <https://www.nlm.nih.gov/mesh/>`_.

MeSH is a medical vocabulary resource curated by the National Library of Medicine (NLM).
It provides a hierarchically-organized terminology for indexing and cataloging of biomedical
information in MEDLINE/PubMed and other NLM databases. Moreover, MeSH is organized as a
directed acyclic graph, laying the foundation for computing semantic similarities between
two concepts.

Although MeSH has potential for bio-NE recognition, normalization, and comparison , there is
still a lack of MeSH tools to automatically recognize bio-NEs from free text and measure the
semantic similarity between bio-NEs after normalization.

pyMeSHSim
^^^^^^^^^^^^^^^^^
Here, we developed an integrative, lightweight and data-rich python package
named pyMeSHSim to curate MeSH terms from free text and measure the semantic similarity
between the MeSH terms.





Currently, pyMeSHSim consists of three subpackages:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- data subpackage
    + The data subpackage has reorganized the MeSH information in bcolz format.
    + It is lightweight and data-rich.
    + It contained the main heading concepts, unique DescriptorUI, MeSH Tree code, and correspond UMLS ID.
    + It contained all narrow concepts of the main heading concepts. It reserved the parent-child relationships and RN/RB relationships for all concepts.

- metamapWrap subpackage
    + It provided some filter rules for parsing the free text.
    + It provided a unified interface to create the MeSH concept objects.

- Sim subpackage
    + It provided useful APIs to retrieve the MeSH dataset.
    + It implemented four methods of semantic similarity measures based on information content.It implemented one method of semantic similarity measures based on path.






-------------------
Installation
-------------------

Requirements
==============
- Software

   + MetaMap 2016v2

- Python packages

   + python 3.6

   + pandas

   + bcolz>=1.2.1

MetaMap installation
=======================
| MetaMap is the base implement of the subpackage metamapWrap.
| You need to activate a UMLS Terminology Services (UTS) account to fetch MetaMap. Please see `MetaMap <https://metamap.nlm.nih.gov/>`_ for more information.


    MetaMap depends on Java. To install openJDK::

        $ sudo apt install default-jdk


    After downloading MetaMap and Extracting it, you can install it by::

        $ cd ./public_mm/
        $ bash ./bin/install.sh


At this point, you have successfully installed MetaMap.

    Please add the bin directory to the environment variable PATH in bashrc for convenience::

        $ export PATH=$PATH:/path_to_MetaMap/bin

    Then, launch MetaMap server before running pyMeSHSim::

        $ skrmedpostctl start
        $ wsdserverctl start


Installation of pandas and bcolz
==================================
    To install python package pandas and bcolz::

        $ pip3 install pandas
        $ pip3 install bcolz

Installation of pyMeSHSim
===============================
    To install pyMeSHSim from source code::

        $ git clone https://github.com/luozhhub/pyMeSHSim.git
        $ cd pyMeSHSim
        $ python3 ./setup.py install


