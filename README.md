# UI_odrivetool

Forked from [ui_odrivetool](https://gitlab.com/p87942130/ui_odrivetool) on GitLab

Tested on Ubuntu 18.04 - Python 3.7.7 - ODrive python 0.5.2 (later version won't work)

```shell
pip install odrive=0.5.2
```

Make sure you can run odrivetool and it can find odrive board connected.

## Repo setup

### Python env setup

#### 1. Setup python environment
```
python3 -m venv env
```
#### 2. Activate python source
```
source env/bin/activate
```

#### 3. Upgrade PIP installer
```
pip install --upgrade pip
```

#### 4. Install requirements

```
pip install odrive
pip install pyqtgraph
pip install pyqt5
```

#### 5. Run Python from terminal

**Run Python file**
```
python3 odrivetool_UI.py
```
