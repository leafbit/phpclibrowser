#!/usr/bin/python3

from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMessageBox,
        QWidget, QVBoxLayout)
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWebKit import QWebElement
from shutil import copyfile

import os
import sys
import subprocess
import argparse
import re

class phpCliBrowser(QMainWindow):

    # The browser's python script directory:
    browserDir = os.path.dirname(os.path.abspath(__file__))
    
    # The PHP Script directory:
    scriptDir = browserDir

    # Current working directory - PHP Script and working directories may be different
    # since local programs may be designed to perform tasks on other than php scrip
    # location
    cwd = os.getcwd()

    # Cache directory - where the phpCliBroser stores resulted html from php cli commands:
    cacheDir = os.path.expanduser('~') + os.path.sep + '.phpCliBrowser' + os.path.sep + 'cache'

    def __init__(self):
        super(phpCliBrowser, self).__init__()


        # Make sure cache directory exists. In it we compile and store result html file
        if not os.path.isdir(self.cacheDir):
            os.makedirs(self.cacheDir)

        # Copy globals.php script to cache directory so that it will simplify the inclusion
        # of POST/GET/SESSION variables
        if not os.path.isfile(self.cacheDir + os.path.sep + 'globals.php'):
            copyfile(self.browserDir + os.path.sep + 'globals.php', self.cacheDir + os.path.sep + 'globals.php')

        # Read program's command line arguments
        self.parse_args()

        self.uriCache = 'file://' + self.cacheDir + os.path.sep

        # Start browser window pointing to php program index
        self.wb = QWebView(self)
        self.wb.loadFinished.connect(self.onLoadFinished)
        self.outputPhpScript(self.index)

        # Set initial icon if exists in the php script directory:
        #self.iconPath = self.scriptDir + os.path.sep + 'icon.ico'
        #if os.path.isfile(self.iconPath):
         #   self.setWindowIcon(QIcon(self.iconPath))
            
        self.setCentralWidget(self.wb)

    # Checks if php link is available in the PHP script directory.
    def isPhpAvailable(self, phpFileName):
        src = phpFileName.replace(self.uriCache, '')
        fullPath = self.scriptDir + os.path.sep + src
        if os.path.isfile(fullPath):
            return fullPath
        return False

    def isLocalFile(self, path):
        return path[:len(self.uriCache)] == self.uriCache
        #return path.startswith('file://' + self.cacheDir + os.path.sep, path)

    def getRealLocalPath(self, path):
        if self.isLocalFile(path):
            rezPth = self.scriptDir + os.path.sep
            rezPth += path.replace('file://' + self.cacheDir + os.path.sep, '')
            return rezPth
        return False

    def onLoadFinished(self): 
        self.wb.page().mainFrame().javaScriptWindowObjectCleared.connect(
                self.populateJavaScriptWindowObject)

        # find Icon to display:
        elIcon = self.wb.page().mainFrame().findFirstElement('link[rel=icon]')
        if elIcon:
            iconPath = elIcon.evaluateJavaScript('this.href')
            if iconPath and self.isLocalFile(iconPath):
                realIconPath = self.getRealLocalPath(iconPath)
                if realIconPath:
                    self.setWindowIcon(QIcon(realIconPath))

        elTitle = self.wb.page().mainFrame().findFirstElement('title')
        if elTitle:
            strTitle = elTitle.toPlainText()
        else:
            strTitle = 'Untitled'
        self.setWindowTitle(strTitle)
        
        self.injectJSLinksFormsRewrite()

    # Execute a php script (or load html file) from php script directory
    def outputPhpScript(self, phpFileName):
        fullPath = self.isPhpAvailable(phpFileName)
        globalsPath = self.cacheDir + os.path.sep + 'globals.php';
        tempScript = self.cacheDir + os.path.sep + '/temp.php';
        sessionFile = self.cacheDir + os.path.sep + '' + self.session_file_name;
        if fullPath:
            php = 'define(\'PHP_SCRIPT_PATH\', \\"'+self.scriptDir+'\\"); define(\'BROWSER_PATH\', \\"'+self.browserDir+'\\");'
            php += 'define(\'SESSION_KEY\', \\"'+self.session_file_name+'\\");'
            php += 'require(\'' + globalsPath + '\'); include(\'' + fullPath + '\');'
            php += 'file_put_contents(\'' + sessionFile + '\', serialize(\$_SESSION));';

            php = 'define(\'PHP_SCRIPT_PATH\', "'+self.scriptDir+'"); define(\'BROWSER_PATH\', "'+self.browserDir+'");'
            php += "\n" + 'define(\'SESSION_KEY\', "'+self.session_file_name+'");'
            php += "\n" + 'require(\'' + globalsPath + '\'); include(\'' + fullPath + '\');'
            php += "\n" + 'file_put_contents(\'' + sessionFile + '\', serialize($_SESSION));';
            
            with open(tempScript, 'w') as f:
                f.write('<?php ' + php + ' ?>');
            cmd = 'php -f "' + tempScript + '"' + self.scriptParams
            self.parseBash(cmd)
        else:
            self.parseBash('echo "Cannot find file \'' + phpFileName + '\'"')

        self.wb.setUrl(QUrl('file://' + self.cacheDir + os.path.sep + 'index.html'))

    # Parse arguments
    def parse_args(self):
        p = argparse.ArgumentParser()
        p.add_argument('-s', default='/usr/share/phpclibrowser/example', help="Directory from where php script is served")
        p.add_argument('-d', default=self.cwd, help="Program working directory")
        p.add_argument('-i', default='index.php', help="Index file for php source")
        p.add_argument('-k', default='default.session', help="Session file name")
        p.add_argument('-p', default='', help="Script params")
        args = p.parse_args()
        self.scriptDir = args.s
        self.cwd = args.d
        self.index = args.i
        self.scriptParams = ' -- ' + args.p
        self.session_file_name = args.k

    # Executes a bash command and outputs the result into index.html cache file
    def parseBash(self, bashCommand, fname='index.html'):
        os.system(bashCommand + ' > ' + self.cacheDir + os.path.sep + '' + fname)

    # Injects into browser's window phpCliBrowser class
    def populateJavaScriptWindowObject(self):
        self.wb.page().mainFrame().addToJavaScriptWindowObject(
                'phpCliBrowser', self)
        
    # Injects scripts to forms and links to rewrite behavior and call python functions:
    def injectJSLinksFormsRewrite(self):
        formElements = self.wb.page().mainFrame().findAllElements('form')
        if formElements:
            for f in formElements:
                # Only forms that have action attribute will be altered.
                if not f.hasAttribute('action'):
                    continue
                # Only forms that have their action pointing to local php script will be altered.
                act = f.evaluateJavaScript('this.action')
                if not self.isLocalFile(act):
                    continue
                if not f.hasAttribute('onsubmit'):
                    f.setAttribute('onsubmit', "phpCliBrowser.submit(this);return false;")
                else:
                    print(f.evaluateJavaScript('this.onsubmit'))
                    
        aElements = self.wb.page().mainFrame().findAllElements('a')
        if aElements:
            for a in aElements:
                if a.hasAttribute('href'):
                    href = a.evaluateJavaScript('this.href')
                    localPath = self.getRealLocalPath(href)
                    if localPath:
                        a.setAttribute('href', 'javascript:phpCliBrowser.goto("' + href + '");')
        # fix images:
        images = self.wb.page().mainFrame().findAllElements('img')
        if (images):
            for im in images:
                if im.hasAttribute('src'):
                    src = im.evaluateJavaScript('this.src')
                    localPath = self.getRealLocalPath(src)
                    if localPath:
                        im.setAttribute('src', localPath)

    # Puts raw query string into a file
    def cachePageQuery(self, dest):
        parts = dest.split('?')
        if len(parts) > 1:
            filename = self.cacheDir + os.path.sep + 'query'
            with open(filename, 'w') as f:
                f.write(parts[1].replace('"', '\\"'))

    @pyqtSlot()
    def closeWindow(self):
        self.close()

    # Provides java script function to replace hrefs of A tags.
    @pyqtSlot(str)
    def goto(self, dest):
        parts = dest.split('?')
        if len(parts) > 1:
            fname = 'query'
            dest = self.cacheDir + os.path.sep + '' + fname
            os.system('echo "' + parts[1] + '" > ' + dest);
        self.outputPhpScript(parts[0])

    # Provides java script function to read form fields and translate values to php array.
    @pyqtSlot(QWebElement)
    def submit(self, el):
        nm = 'something'
        i = 0;
        data = ''
        while nm != '':
            strElmt = 'this.elements[' + str(i) + ']'
            tp = el.evaluateJavaScript(strElmt + '.type')
            nm = el.evaluateJavaScript(strElmt + '.name')
            val = el.evaluateJavaScript(strElmt + '.value')
            
            if tp == 'textarea':
                data += '<!CDATA+++ textarea start:' + nm + "\n" + val + "\n >>textarea end]]+++>\n"

            elif tp == 'radio':
                chkd = el.evaluateJavaScript(strElmt + '.checked')
                if (chkd):
                    data += 'FLD:' + nm + '=' + val + "\n"

            elif tp == 'checkbox':
                chkd = el.evaluateJavaScript(strElmt + '.checked')
                if (chkd):
                    if val:
                        data += 'FLD:' + nm + '=' + val + "\n"
                    else:
                        data += 'FLD:' + nm + '=1' + "\n"
                else:
                    data += 'FLD:' + nm + '=0' + "\n"

            else:
                data += 'FLD:' + nm + '=' + val + "\n"
            i = i+1

        formMethod = el.evaluateJavaScript('this.method')
        if not formMethod or formMethod.lower() != 'post':
            formMethod = 'get'
        formMethod = formMethod.lower()
            
        filename = self.cacheDir + os.path.sep + '' + formMethod

        with open(filename, 'w') as f:
            f.write(data)

        act = el.evaluateJavaScript('this.action')
        self.outputPhpScript(act)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    mainWindow = phpCliBrowser()
    # mainWindow.setWindowTitle("PHP Browser")
    mainWindow.show()

    sys.exit(app.exec_())
