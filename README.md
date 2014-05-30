#kaas2qiime

Background
------

This is a simple script to generate QIIME-based taxa plots using the output of KAAS - KEGG Automatic Annotation Server. 

Required Packages
------

**Python:**

- [PICRUSt 1.0.0](http://picrust.github.io/picrust/install.html#install)
- [BIOM 1.3.1](http://biom-format.org/)
- [QIIME 1.8.0 (stable public release)](https://github.com/qiime/qiime-deploy)

The script has been tested on Ubuntu 12.04.3 LTS.

Input files
------

The main input files for this script are output files generated via the [KEGG Automatic Annotation Server](http://www.genome.jp/kegg/kaas/). Multiple KAAS output files can be provided. To ensure uniformity, all KAAS output files require a standard naming convention for this script. All files must be named by their sample ID followed by a ```_kaas.txt``` extension.

For example, if KAAS was used to annotate 2 genomes called "GenomeA" and "GenomeB", the KAAS output files for these must be named as following:

1) **GenomeA_kaas.txt**

2) **GenomeA_kaas.txt**

In addition to KAAS output files, a [QIIME parameter file](http://qiime.org/documentation/qiime_parameters_files.html) is also required, which is provided in the src directory. It's called ```qiime_params.txt```. Another file needed to specifically annotate the KAAS output is a KEGG database flat file that can be downloaded from [here](https://raw.githubusercontent.com/ivan-kryukov/Kegg-Htext-Parser/master/ko00001.keg).

Please save this file in same folder as ```kaas_to_qiime.py``` and name this KEGG database file as **ko00001.keg**. Please note that without the ko00001.keg file, the script will crash.

How to use
------

There is a single script in the src folder. It's called:

- ```kaas_to_qiime.py```

To run the script, simply type ```python kaas_to_qiime.py``` in the terminal and make sure all the input files are present in the working directory. 
