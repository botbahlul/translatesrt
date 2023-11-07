# translatesrt <a href="https://pypi.python.org/pypi/translatesrt"><img src="https://img.shields.io/pypi/v/translatesrt.svg"></img></a>

### Translate subtitle files into another language
translatesrt is a simple command line tool made with python to translate subtitle files to another language.

### Installation
If you don't have python on your Windows system you can get compiled version from this git release assets
https://github.com/botbahlul/translatesrt/releases

Just extract that translatesrt.exe into a folder that has been added to PATH ENVIRONTMET for example in C:\Windows\system32

In Linux you have to install this script with python (version minimal 3.8 ) 

To install this translatesrt, just type :
```
pip install translatesrt
```

You can try to compile that translatesrt.py script in win or linux folder to a single executable file with pyinstaller by typing these :
```
pip install pyinstaller
pyinstaller --onefile translatesrt.py
```

The executable compiled file will be placed by pyinstaller into dist subfolder of your current working folder, so you can just rename and put that compiled file into a folder that has been added to your PATH ENVIRONTMENT so you can execute it from anywhere

I was succesfuly compiled it in Windows 10 with pyinstaller-5.1 and Pyhton-3.10.4, and python-3.8.12 in Debian 9

Another alternative way to install this script with python is by cloning this git (or downloading this git as zip then extract it into a folder), and then just type :

```
pip install wheel
python setup.py build
python setup.py bdist_wheel
```

Then check the name of the whl file created in dist folder. In case the filename is translatesrt-0.0.1-py2.py3-none-any.whl then you can install that whl file with pip :
```
cd dist
pip install translatesrt-0.0.1-py2.py3-none-any.whl
```

You can also install this script (or any pip package) in ANDROID DEVICES via PYTHON package in TERMUX APP

https://github.com/termux/termux-app/releases/tag/v0.118.0

Choose the right apk for your device, install it, then open it

Type these commands to get python, pip, this translatesrt, (and any other pip packages) :

```
termux-setup-storage
pkg update -y
pkg install -y python
pkg install -y ffmpeg
pip install translatesrt
```

### Simple usage example 

```
translatesrt --help
translatesrt "Episode 1.srt" -S en -D id
```

### Usage

```
usage: translatesrt.py [-h] [-S SRC_LANGUAGE] [-D DST_LANGUAGE] [-ll] [-F FORMAT] [-lf] [-C CONCURRENCY] [-v]
                       [subtitle_file_path ...]

positional arguments:
  subtitle_file_path    Subtitle file path you want to translate (use wildcard for multiple files or separate them with a space
                        character e.g. "file 1.srt" "file 2.srt")

options:
  -h, --help            show this help message and exit
  -S SRC_LANGUAGE, --src-language SRC_LANGUAGE
                        Language code of subtitle file you want to translate
  -D DST_LANGUAGE, --dst-language DST_LANGUAGE
                        Desired translation language code for the subtitles
  -ll, --list-languages
                        List all supported languages
  -F FORMAT, --format FORMAT
                        Desired subtitles file format
  -lf, --list-formats   List all supported subtitles file formats
  -C CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent API requests to make
  -v, --version         show program's version number and exit
```

### License

MIT

Check my other SPEECH RECOGNITIION + TRANSLATE PROJECTS in https://botbahlul.github.io
