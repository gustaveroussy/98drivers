# 98drivers
analysis pipeline for cancer whole genom. 

# Description 
This is a snakemake pipeline to analyse variant data from cancer whole genome sequencing of many sample. It takes a bed file as input, containing variant data associated with sample id. Results comes with html page containing counting variant, signature, cluster and peaks detection. 

# Requirements 
## Command line 
* [bedtools](http://bedtools.readthedocs.io/en/latest/)
* [tabix](http://www.htslib.org/doc/tabix.html)
* [snakemake](https://bitbucket.org/snakemake/snakemake/wiki/Home)
* [Python 3.4](https://www.python.org/download/releases/3.0/)
* [R](https://www.r-project.org/)

Those package can be easily installed from your Linux distribution. For exemple, on ubuntu : 

    sudo apt install bedtools
    sudo apt install tabix 
    sudo apt install snakemake
    sudo apt install R-base 


## Python package 
* pytabix 
* entropy
* jinja2 

You can install those packages using pip tools. There is also a file in the repository. Just type the following command to install python requirements. 

    sudo pip install requirements.txt 

## R library  

    * fmsb 
    * RColorBrewer 

You can install R library, by the following commad inside R prompt. 

    install.packages(fmsb)
    install.packages(RColorBrewer)




