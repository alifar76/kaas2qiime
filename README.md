#kaas2qiime

Background
------

This is a simple script to generate QIIME-based taxa plots using output of KAAS - KEGG Automatic Annotation Server. 

Required Packages
------

**Python:**

- [PICRUSt 1.0.0](http://picrust.github.io/picrust/install.html#install)
- [BIOM 1.3.1](http://biom-format.org/)
- [QIIME 1.8.0 (stable public release)](https://github.com/qiime/qiime-deploy)

The script has been tested on Ubuntu 12.04.3 LTS.

How to use
------

There is a single script in the src folder. It's called:

- ```annotate_kos.py```

In addition to this, a [QIIME parameter file](http://qiime.org/documentation/qiime_parameters_files.html) is also required, which provided in the src directory. It's called ```qiime_params.txt```.
