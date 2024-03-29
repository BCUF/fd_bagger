# fd_bagger

A script to bag(using bagit) multiple directories

## Install

Requires:
* Python >= 3.10
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
* Lauch the gui with cmd (no args required)
```bash
python3 bagger.py
```
* Lauch without the gui
```bash
python3 bagger.py -i "C:\tmp\exemple\input_dir" -o "C:\tmp\exemple\output_dir" -c ARCHNUMFR_6932 -f KEHREN_OBERSON -d "C:\tmp\exemple\metadata\metadata.csv" -m "C:\tmp\exemple\processingMCP.xml" -s 0010 -p 4
```
**Description of arguments:**

- -i the path of input directory which contains all the folder you may package.
- -o the path of output bags
- -c the value of dc.identifier used in the metadata.csv file. This value will be incremented.
- -f the prefix name of the bag. The complete name is composed with the prefix, the dc.identifier and incremented digits. For example, the command above will name the first bag "KEHREN_OBERSON-ARCHNUMFR_6932-0001". By default, 4 digits is used to increment the name of following bags. The complete name of the bag is used to update the dc.title of the metadata.csv file.
- -d the path of the metadata.csv file
- -m the path of the processingMPC.xml file used for Archivematica.
- -s 0010 optionnal argument, if you want to define the first number of bag name incrementation.
- -p 4 defines the number of CPU thread

The first three arguments are mandatory, following arguments are optional.

**Bag structure**

The bag structure should look like :

```
├── bag-info.txt
├── bagit.txt
├── data
│   └── skip-transfer-directory
│       └── BAC A CREME AVEC CUILLIèRE 12-2015
│           ├── BAC A CREME AVEC CUILLIERE TRANS.psd
│           ├── CUILLIERE DETOUREE 9037.jpg
│           ├── DOUBLE CREME DE LA GRUYERE.psd
│           ├── DSC09030.ARW
│           ├── DSC09031.ARW
│           ├── DSC09032.ARW
│           ├── DSC09033.ARW
│           ├── DSC09034.ARW
│           ├── DSC09035.ARW
│           ├── DSC09036.ARW
│           ├── DSC09037_1.PSD
│           ├── DSC09037.ARW
│           ├── DSC09037.JPG
│           ├── DSC09037.PSD
│           ├── DSC09037.xmp
│           ├── DSC09038.ARW
│           ├── DSC09039.ARW
│           ├── DSC09040.ARW
│           ├── DSC09041.ARW
│           ├── DSC09042.ARW
│           ├── DSC09043.ARW
│           ├── DSC09044.ARW
│           └── DSC09045.ARW
├── manifest-md5.txt
├── metadata
│   └── metadata.csv
├── processingMCP.xml
└── tagmanifest-md5.txt
```
# Add content to an existing bag

The utility updatebag let you add some content (file or directories) to an existing bag.

## Run example

```bash
python3 updatebag.py -b "C:\tmp\bag\test_bag_1" -t "C:\tmp\bag\test_bag_1\data" "C:\dev\fd_bagger" ".\updatebag.py" 
```
**Description of arguments:**

- -b the bag to update.
- -t the target directory inside the bag were to put the added content. Should be an absolute path.
- elements [elements ...] the element that will be added to the path. An element can be a directory or a file. 
  If the specified element is a directory the whole content is copied recursively.

## Pyinstaller

# works on windows 
```bash
pyinstaller --noconsole --onefile bagger.py
```
the exe will be in the "./dist" folder

