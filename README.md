# fd_bagger

A script to bag(using bagit) multiple directory

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
python3 bagger.py -i "C:\tmp\exemple\input_dir" -o "C:\tmp\exemple\output_dir" -c ARCHNUMFR_6932 -f KEHREN_OBERSON -d "C:\tmp\exemple\metadata\metadata.json" -m "C:\tmp\exemple\processingMCP.xml" -p 4
```


