# fd_bagger

A script to bag(using bagit) multiple directories

## Install

Requires:
* Python >= 3.6
* Check the version running python --version or python3 --version

```bash
git clone https://github.com/BCUF/fd_bagger.git
cd fd_bagger
python3 -m pip install --upgrade pip
pip3 install virtualenv
python3 -m venv env
env/Scripts/activate (on windows)
source env/bin/activate (on unix)
pip3 install -r require.txt
```

## Run example

```bash
python3 bagger.py -i "C:\tmp\exemple\input_dir" -o "C:\tmp\exemple\output_dir" -c ARCHNUMFR_6932 -f KEHREN_OBERSON -d "C:\tmp\exemple\metadata\metadata.csv" -m "C:\tmp\exemple\processingMCP.xml" -p 4
```
**Description of arguments:**

- -i the path of input directory which contains all the folder you may package.

-o the path of output bags

-c the value of dc.identifier used in the metadata.csv file

-f the prefix name of the bag. The complete name is composed with the prefix and the dc.identifier. For example, the command above will name the first bag "KEHREN_OBERSON-ARCHNUMFR_6932-0001". By default, 4 digits is used to increment the name of following bags.
-d the path of the metadata.csv file
-m the path of the processingMPC.xml file used for Archivematica.
-s 0010 optionnal argument, if you want to define the first number of bag name incrementation.

