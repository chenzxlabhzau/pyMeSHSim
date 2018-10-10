------------
Install
------------

Dependences
==============
- software

   + MetaMap 2016v2

- python packages

   + python 3.6

   + pandas

   + bcolz>=1.2.1

MetaMap install
================
| MetaMap is the base implement of the subpackage metamapWrap.
| You need to activate a UMLS Terminology Services (UTS) account to fetch MetaMap. Please see `MetaMap <https://metamap.nlm.nih.gov/>`_ for more information.
| The 2016 version has some important featrue, it will be helpful when parsing the text.

    MetaMap depends on Java. To install openJDK::

        $ sudo apt install default-jdk


    After downloading MetaMap and Extracting it, you can install it by::

        $ cd ./public_mm/
        $ bash ./bin/install.sh


At this point, you have successfully installed MetaMap.

    Please add the bin directory to the environment variable PATH in bashrc for convenience::

        $ export PATH=$PATH:/home/luozhihui/Project/UMLS/public_mm/bin

    Then, launch MetaMap server before running pyMeSHSim::

        $ skrmedpostctl start
        $ wsdserverctl start


Install pandas and bcolz
========================
    To install python package pandas and bcolz::

        $ pip3 install pandas
        $ pip3 install bcolz

Install pyMeSHSim
===================
    To install pyMeSHSim from source code::

        $ tar -zxvf pyMeSHSim-0.0.1.tar.gz
        $ python3 ./setup.py install


