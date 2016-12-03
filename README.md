# About

PHPCLIBrowser is a python3 script that provides a browser window capable to run
php cli (bash php) scripts. As result one may build user interfaces using HTML 
and HTML forms and process them with PHP locally. It does not require any server 
and doesn't run any server. It uses PHP CLI commands only.

## Requirements

To run PHPCLIBrowser you need:
PHP, Python3, pyqt5, pyqt5.webkit
On debian/ubuntu can install them by:

```bash
apt-get insall php python3 pyton3-pyqt5 python3-pyqt5.qtwebkit
```

## Usage

To start provided with the program example run:

```bash
phpclibrowser
```

To start your own PHP script run:

```bash
phpclibrowser -s "path/to/php/script"
```

To run in specific working directory:

```bash
phpclibrowser -s "path/to/php/script" -d "path/to/working/direcory"
```

One may provide a session key to store session variables for particular
programs:

```bash
phpclibrowser -k "mysessionkey"
```

One may change the initial index file (default is index.php):

```bash
phpclibrowser -i "start.php"
```

## PHP Script

`$_SESSION`, `$_POST`, `$_GET` variables are available. 
They may behave slighlty different from standard server based scripts. (we didn't test)

The constants:

`PHP_SCRIPT_PATH` - point to php script directory.
`BROWSER_PATH` - point to browser path directory.

## Known Limitations and Issues

File field in forms does not work as expected. Is impossible to get the selected file path.
Java script and form submission may work different from expected.
