#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

"""
Stellar
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil

from PyQt4 import QtCore, QtGui

import cfg
from splashscreen import Start
from newprojectdialog import NewProjectDialog
from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from scriptgui import ScriptGUI
from objectgui import ObjectGUI


class QMdiAreaW(QtGui.QMdiArea):
    def __init__(self, main):
        super(QMdiAreaW, self).__init__(main)
        self.setBackground (QtGui.QBrush(QtGui.QPixmap(os.path.join("Data", "background.png"))))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, main):
        super(TreeWidget, self).__init__(main)
        self.header().setHidden(True)
        self.setWindowTitle('Resources')
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.main = main
        self.dirname = ''
        self.connect(self, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),self.DoEvent)

        self.PathSprite = ''
        self.PathSound = ''
        self.PathFonts = ''
        self.PathScripts = ''
        self.PathObjects = ''
        self.PathRooms = ''

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        insertAction = menu.addAction("Insert")
        insertAction.triggered.connect(self.AddSprChild)
        
        duplicateAction = menu.addAction("Duplicate")
        duplicateAction.setShortcut('Alt+Ins')
        duplicateAction.setDisabled (True)
        menu.addSeparator()
        insertgroupAction = menu.addAction("Insert Group")
        insertgroupAction.setShortcut('Shift+Ins')
        insertgroupAction.setDisabled (True)
        menu.addSeparator()
        deleteAction = menu.addAction("Delete")
        deleteAction.setShortcut('Shift+Del')
        deleteAction.setDisabled (True)
        menu.addSeparator()
        renameAction = menu.addAction("Rename")
        renameAction.setShortcut('F2')
        renameAction.setDisabled (True)
        menu.addSeparator()
        propertiesAction = menu.addAction("Properties...")
        propertiesAction.setShortcut('Alt+Enter')
        propertiesAction.triggered.connect(self.DoEvent)
        action = menu.exec_(self.mapToGlobal(event.pos()))

    def DoEvent(self):
        item = self.currentItem()
        bln = True
        if not item.parent() == None:
            if item.parent().text(0) == "Sprites":

                for index, sprite in enumerate(self.main.Sprites):
                    if sprite[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_sprites.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(0)
                        break

                if bln==True:
                    self.main.window = QtGui.QWidget()
                    self.main.sprite = SpriteGUI(self.main.window,item.text(0), self.main.dirname)
                    self.main.qmdiarea.addSubWindow(self.main.window)
                    self.main.window.setVisible(True)
                    self.main.window.setWindowTitle("Sprite Properties: "+ item.text(0))

            elif item.parent().text(0) == "Sound":

                for index, sound in enumerate(self.main.Sound):
                    if sound[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_sound.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(1)
                        break

                if bln==True:
                    self.main.window = QtGui.QWidget()
                    self.main.sound = SoundGUI(self.main.window,item.text(0), self.main.dirname)
                    self.main.qmdiarea.addSubWindow(self.main.window)
                    self.main.window.setVisible(True)
                    self.main.window.setWindowTitle("Sound Properties: "+ item.text(0))

            elif item.parent().text(0) == "Fonts":

                for index, font in enumerate(self.main.Fonts):
                    if font[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_font.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(2)
                        break

                if bln==True:
                    self.main.window = QtGui.QWidget()
                    self.main.font = FontGUI(self.main.window,item.text(0))
                    self.main.qmdiarea.addSubWindow(self.main.window)
                    self.main.window.setVisible(True)
                    self.main.window.setWindowTitle("Font Properties: "+ item.text(0))

            elif item.parent().text(0) == "Scripts":

                for index, script in enumerate(self.main.Scripts):
                    if script[1] == item.text(0):
                        bln = False
                        self.main.qmdiarea.setActiveSubWindow(index)
                        break

                if bln==True:
                    self.main.window = QtGui.QWidget()
                    self.main.script = ScriptGUI(self.main.window,item.text(0), self.main.dirname, self.main)
                    self.main.qmdiarea.addSubWindow(self.main.window)
                    self.main.window.setVisible(True)
                    
                    #self.main.window.setWindowTitle("Script Properties: "+ item.text(0))
                    
            elif item.parent().text(0) == "Objects":

                for index, object in enumerate(self.main.Objects):
                    if object[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_objects.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(4)
                        break

                if bln==True:
                    self.main.window = QtGui.QWidget()
                    self.main.object = ObjectGUI(self.main.window,item.text(0), self.main.dirname)
                    self.main.qmdiarea.addSubWindow(self.main.window)
                    self.main.window.setVisible(True)
                    self.main.window.setWindowTitle("Object Properties: "+ item.text(0))

    def InitParent(self):

        #Sprites------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSprite = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sprites'))
        self.ParentSprite.setIcon(0,icon)

        #sound--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSound = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sound'))
        self.ParentSound.setIcon(0,icon)
        
        #Fonts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentFonts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Fonts'))
        self.ParentFonts.setIcon(0,icon)

        #Scripts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentScripts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Scripts'))
        self.ParentScripts.setIcon(0,icon)

        #Objects------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentObjects = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Objects'))
        self.ParentObjects.setIcon(0,icon)

        #Rooms--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentRooms = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Rooms'))
        self.ParentRooms.setIcon(0,icon)

        #Included Files-----------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentIncluded = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Included Files'))
        self.ParentIncluded.setIcon(0,icon)

        #Extensions---------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentExtensions = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Extensions'))
        self.ParentExtensions.setIcon(0,icon)

    def InitChild(self):
        self.dirname = self.main.dirname
        self.PathSprite = os.path.join(self.dirname, "Sprites")
        self.PathSound = os.path.join(self.dirname, "Sound")
        self.PathFonts = os.path.join(self.dirname, "Fonts")
        self.PathScripts = os.path.join(self.dirname, "Scripts")
        self.PathObjects = os.path.join(self.dirname, "Objects")
        self.PathRooms = os.path.join(self.dirname, "Rooms") 

        #Sprites----------------------------------
        for ChildSprite in os.listdir(self.PathSprite):
            self.main.Sprites.append(ChildSprite)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.PathSprite, ChildSprite)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(ChildSprite[:-4])).setIcon(0,icon)      

        #Sound------------------------------------
        for ChildSound in os.listdir(self.PathSound):
            self.main.Sound.append(ChildSound)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(ChildSound[:-4])).setIcon(0,icon)

        #Fonts------------------------------------
        for ChildFont in os.listdir(self.PathFonts):
            self.main.Fonts.append(ChildFont)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(ChildFont[:-4])).setIcon(0,icon)

        #Scripts------------------------------------
        for ChildScript in os.listdir(self.PathScripts):
            self.main.Scripts.append(ChildScript)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "addscript.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(ChildScript[:-3])).setIcon(0,icon)

        #Objects----------------------------------
        for ChildObject in os.listdir(self.PathObjects):
            self.main.Objects.append(ChildObject)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentObjects, QtCore.QStringList(ChildObject[:-3])).setIcon(0,icon)

        #Rooms------------------------------------
        for ChildRoom in os.listdir(self.PathRooms):
            self.main.Rooms.append(ChildRoom)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "game.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentRooms, QtCore.QStringList(ChildRoom[:-4])).setIcon(0,icon)

    def AddSprChild(self,name):
        #Sprites----------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.PathSprite, name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(name[:-4])).setIcon(0,icon)    

    def AddSndChild(self,name):
        #Sound------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(name[:-4])).setIcon(0,icon)

    def AddScriptChild(self,name):
        #Script------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(name)).setIcon(0,icon)
        
    def AddObjectChild(self,name):
        #Object------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentObjects, QtCore.QStringList(name)).setIcon(0,icon)

    def AddFontChild(self,name):
        #Font------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(name[:-4])).setIcon(0,icon)        


class Stellar(QtGui.QMainWindow,QtGui.QTextEdit,QtGui.QTreeWidget, QtGui.QMdiArea):
    
    def __init__(self):
        super(Stellar, self).__init__()
        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.Objects=[]
        self.Rooms=[]
        self.initUI()
        
    def initUI(self):
        
        #Saving where you opened the program for opening a new window in the future
        self.stellardir = inspect.getfile(inspect.currentframe())
        dirname, filename = os.path.split(os.path.abspath(self.stellardir))
        self.pref = "preferences.pyw"
        self.stellarnew = "Stellar.pyw"
        
        #ACTIONS -------------------------------
        
        def newAction(name, image, trigger, statusTip, shortcut='', enabled=True):
            action = QtGui.QAction(QtGui.QIcon(os.path.join('Data', image)), name, self)
            action.setShortcut(shortcut)
            action.setStatusTip(statusTip)
            action.triggered.connect(trigger)
            action.setEnabled(enabled)
            return action
        
        projectAction = newAction('New Project', 'new.png', self.newproject, 'New Project', 'Ctrl+N')
        
        loadAction = newAction('Open...', 'folder.png', self.openfile, 'Open Game.', 'Ctrl+O')
        saveAction = newAction('Save Game As...', 'save.png', self.savefile, 'Save Game As...', 'Ctrl+Shift+S')
        fsaveAction = newAction('Save', 'save.png', self.fsavefile, 'Save Game', 'Ctrl+S', False)
        
        shareAction = newAction('Share', 'publish.png', self.sharegame, 'Share your creations with the community!')
        buildAction = newAction('Build', 'build.png', self.Build, 'Build game.', '', False)
        playAction = newAction('Run', 'play.png', self.playgame, 'Test your game.', 'F5')
        playDebugAction = newAction('Run in debug mode', 'playdebug.png', self.playgame, 'Test your game on debug mode.', 'F6', False)
        
        spriteAction = newAction('Add Sprite', 'sprite.png', self.addsprite, 'Add a sprite to the game.')
        animatedspriteAction = newAction('Add Animated Sprite', 'gif.png', self.addAnimatedSprite, 'Add an animated sprite to the game.')
        soundAction = newAction('Add Sound', 'sound.png', self.addsound, 'Add a sound to the game.')
        fontAction = newAction('Add Font', 'font.png', self.addfont, 'Add a font to the game.')
        objectAction = newAction('Add Object', 'object.png', self.addobject, 'Add an object to the game.')
        roomAction = newAction('Add Room', 'room.png', self.addroom, 'Add an room to the game.')
        scriptAction = newAction('Add Script', 'addscript.png', self.addscript, 'Add A Script To The Game.')
        
        zoominAction = newAction('Zoom In', 'plus.png', self.onZoomInClicked, 'Zoom in the font of the editor.')
        zoomoutAction = newAction('Zoom Out', 'minus.png', self.onZoomOutClicked, 'Zoom out the font of the editor.')
        sfontAction = newAction('Set Font', 'font.png', self.fontdialog, 'Change the font of the text editor.')

        exitAction = newAction('Exit', 'exit.png', self.close, 'Exit application.', 'Ctrl+Q')
        aboutAction = newAction('About', 'info.png', self.aboutStellar, 'About Stellar.')
        preferencesAction = newAction('Preferences...', 'preferences.png', self.preferencesopen, 'Change Stellar preferences.', '', False)

        self.statusBar()

        #MENU BAR --------------------------------------
        menubar = self.menuBar()
        
        def addBar(bar, action):
            if bar == 'menubar':
                self.fileMenu = menubar.addMenu(action[0])
            
            for i in range(1, len(action)):
                if action[i] == '|':
                    if bar == 'menubar':
                        self.fileMenu.addSeparator()
                    elif bar == 'toolbar':
                        self.toolbar.addSeparator()
                else:
                    if bar == 'menubar':
                        self.fileMenu.addAction(action[i])
                    elif bar == 'toolbar': 
                        self.toolbar.addAction(action[i])

        addBar('menubar', ['&File', projectAction, loadAction, '|', fsaveAction, saveAction, '|',\
                                buildAction, shareAction, '|', preferencesAction, '|', exitAction])

        addBar('menubar', ['&Resources', spriteAction, animatedspriteAction, soundAction, objectAction,\
                                fontAction, roomAction])
        
        addBar('menubar', ['&Scripts', scriptAction])
        addBar('menubar', ['&Run', playAction, playDebugAction])
        addBar('menubar', ['&Text Editor', zoominAction, zoomoutAction, sfontAction])
        addBar('menubar', ['&Help', aboutAction])

        #TOOL BAR --------------------------------------
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (True)
        
        addBar('toolbar', [ None, projectAction, fsaveAction, loadAction, '|', buildAction, shareAction, '|',\
                                playAction, '|', spriteAction, animatedspriteAction, soundAction, fontAction,\
                                scriptAction, objectAction, roomAction, '|', aboutAction, zoominAction, zoomoutAction ] )

        #Qtree----------------------------------------
        self.tree = TreeWidget(self)

        #QMdiArea--------------------------------------
        self.qmdiarea= QMdiAreaW(self)
        #self.addScriptsubWindow("hola")

        #WINDOW----------------------------------------
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.subfolders = ['Sprites', 'Sound', 'Fonts', 'Scripts', 'Objects', 'Rooms', 'Build']
        self.fname = "<New game>"
        self.dirname = ''
        self.setWindowTitle('{0} - Stellar {1}'.format(self.fname, cfg.__version__))
        self.center()
        self.start = Start(self)
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter1.addWidget(self.tree)
        self.splitter1.addWidget(self.qmdiarea)
        self.splitter1.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter1)

    def updatetree(self):
        self.Scripts = []
        self.tree.clear()
        self.tree.InitParent()
        self.tree.InitChild()

    def preferencesopen(self):
        print(self.pref)
        execfile(self.pref, {})

    def newproject(self):
        self.window = QtGui.QWidget()
        projectdirname = NewProjectDialog(self.window)

    def Build(self):
        print("To do")

    def aboutStellar(self):
        about = QtGui.QMessageBox.information(self, 'About Stellar',
            "<center><b>Stellar</b> is an open-source program inspired in 'Game Maker' for <b>Pygame/Python</b> development.<br/><br/>    The goal is to have a program to design your own games using easy-to-learn drag-and-drop actions and different easy tools for begginers.<br/>    When you become more experienced, you will have the possibilitie of writing and editing your game with the full flexibility given by <b>Python/Pygame</b>.<br/><br/>    This is an uncomplete version, it has almost nothing, but I would love to be helped by anyone interested in the project.<br/><br/>    You are free to distribute the games you create with <b>Stellar</b> in any way you like. You can even sell them.<br/>     This of course assumes that the sprites, images, and sounds you use can be distributed or sold as well.<br/><HR><br/>  You can contribute to the project on our Github:<br/><a href=\'https://github.com/Coppolaemilio/stellar'>Stellar on Git</a></center>", QtGui.QMessageBox.Ok)
            
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, "Exit Stellar", "Save Python File before Exit?",
                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            p = str(self.fname)
            d = os.path.basename(p)
            fname = os.path.join(self.dirname, d)
            self.setWindowTitle('{0} - Stellar {1}'.format(d, cfg.__version__))

            with open(fname, 'w') as f:
                data = self.textEdit.toPlainText()
                f.write(data)
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.accept()
        else:
            event.ignore()
            
    def openfile(self):
        project = str(QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Game', 
                            '', self.tr("Python files (*.py *.pyw)")))

        if project == '':
            return
        if not os.path.isfile(project):
            QtGui.QMessageBox.question(self, "Project doesn't exist",
                "This project doesn't exist or has been removed",
                QtGui.QMessageBox.Ok)
            return
            

        for subfolder in self.subfolders:

            if not os.path.exists(os.path.join(os.path.dirname(project), subfolder)):

                QtGui.QMessageBox.question(self, "Project is broken",
                    "Project is broken or doesn't contain important folders",
                    QtGui.QMessageBox.Ok)
                return

        self.dirname = os.path.dirname(project)

        self.fname = os.path.basename(project)



        cfg.config.set('stellar', 'recentproject', project)

        with open('config.ini', 'wb') as configfile:

            cfg.config.write(configfile)
            
        self.setWindowTitle('%s - Stellar %s'% (self.fname, cfg.__version__))


        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.Objects=[]
        self.Rooms=[]

        self.tree.clear()
        self.tree.InitParent()

        self.tree.InitChild()
        self.show()

    def sharegame(self):
        webbrowser.open("http://www.pygame.org/news.html")
            
    def savefile(self):
        project = str(QtGui.QFileDialog.getSaveFileName(self, 'Save project as...', 

                            self.dirname, self.tr("Python files (*.py *.pyw)")))

        if project == "":
            return
        else:
            fromDir = self.dirname
            self.fname = os.path.basename(project)
            self.dirname = os.path.dirname(project)

            if not os.path.exists(self.dirname):
                os.mkdir(self.dirname)
                
            for subfolder in self.subfolders:
                if not os.path.exists(os.path.join(self.dirname, subfolder)):

                    os.mkdir(os.path.join(self.dirname, subfolder))

            f = open(os.path.join(self.dirname, self.fname), 'w+')

            f.write('# This file was created with Stellar')

            f.close()

            cfg.config.set('stellar', 'recentproject', project)

            with open('config.ini', 'wb') as configfile:

                cfg.config.write(configfile)

            self.setWindowTitle('%s - Stellar %s'% (os.path.basename(project), cfg.__version__))

            self.addsprite(self.Sprites, fromDir)
            self.addsound(self.Sound, fromDir)
            self.addfont(self.Fonts, fromDir)
            self.addscript(self.Scripts, fromDir)
            self.addobject(self.Objects, fromDir)
            self.addroom(self.Rooms, fromDir)
            
    def fsavefile(self):
        print("To do")

    def onZoomInClicked(self):
        self.textEdit.zoomIn(+1)

    def onZoomOutClicked(self):
        self.textEdit.zoomOut(+1)       
        
    def playgame(self):
        execfile(os.path.join(self.dirname, self.fname), {})

    def fontdialog(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def addsprite(self, asprite = None, fromDir = None):
        if asprite is None:
            self.asprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
            if self.asprite !='':
                for sprite in self.asprite:
                    d = os.path.basename(str(sprite))
                    if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                        if d[:4]=='spr_':
                            shutil.copy(sprite, os.path.join('Sprites', d))
                            self.tree.AddSprChild(d)
                            self.Sprites.append(d)
                        else:
                            shutil.copy(sprite, os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                            self.tree.AddSprChild('spr_' + d)
                            self.Sprites.append('spr_' + d)
 
        else:
            for sprite in asprite:
                if not os.path.isfile(os.path.join(self.dirname, 'Sprites', sprite)):
                    shutil.copy(os.path.join(fromDir, 'Sprites', sprite), os.path.join(self.dirname, 'Sprites', sprite))

    def addAnimatedSprite(self, aGIFsprite = None, fromDir = None):
        if aGIFsprite is None:
            self.aGIFsprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Animated Sprite(s)', 
                    '', self.tr("Image file (*.png *.gif *.jpg)"))
            
            if self.aGIFsprite !='':
                for sprite in self.aGIFsprite:
                    d = os.path.basename(str(sprite))
                    if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                        if d[:4]=='spr_':
                            shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', d))
                            self.tree.AddSprChild(d)
                            self.Sprites.append(d)
                        else:
                            shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                            self.tree.AddSprChild('spr_' + d)
                            self.Sprites.append('spr_' + d)

        else:
            for sprite in aGIFsprite:
                if not os.path.isfile(os.path.join(self.dirname, 'Sprites', sprite)):
                    shutil.copy(os.path.join(fromDir, 'Sprites', sprite), os.path.join(self.dirname, 'Sprites', sprite))

    def addsound(self, asound = None, fromDir = None):
        if asound is None:
            self.asound = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sound(s)', 
                    '', self.tr("Sound file (*.ogg *.wav)"))
            
            if self.asound !='':
                for sound in self.asound:
                    d = os.path.basename(str(sound))
                    if not os.path.exists(os.path.join(self.dirname, 'Sound', d)):
                        if d[:4]=='snd_':
                            shutil.copy(sound,os.path.join(self.dirname, 'Sound', d))
                            self.tree.AddSndChild(d)
                            self.Sound.append(d)
                        else:
                            shutil.copy(sound,os.path.join(self.dirname, 'Sound', 'snd_{0}'.format(d)))
                            self.tree.AddSndChild('snd_'+d)
                            self.Sound.append('snd_' + d)

        else:
            for sound in asound:
                if not os.path.isfile(os.path.join(self.dirname, 'Sound', sound)):
                    shutil.copy(os.path.join(fromDir, 'Sound', sound), os.path.join(self.dirname, 'Sound', sound))

    def addfont(self, afont = None, fromDir = None):
        if afont is None:
            self.afont = QtGui.QFileDialog.getOpenFileNames(self, 'Open Font(s)', 
                    '', self.tr("Font file (*.ttf *.ttc *.fon)"))
            
            if self.afont !='':
                for font in self.afont:
                    d = os.path.basename(str(font))
                    f = os.path.splitext(d)[0]
                    if not os.path.exists(os.path.join(self.dirname, 'Fonts', d)):
                        if d[:5]=='font_':
                            shutil.copy(font,os.path.join(self.dirname, 'Fonts', d))
                            self.tree.AddFontChild(d)
                            self.Fonts.append(d)
                        else:
                            shutil.copy(font,os.path.join(self.dirname, 'Fonts', 'font_{0}'.format(d)))
                            self.tree.AddFontChild('font_'+d)
                            self.Fonts.append('font_' + d)

        else:
            for font in afont:
                if not os.path.isfile(os.path.join(self.dirname, 'Fonts', font)):
                    shutil.copy(os.path.join(fromDir, 'Fonts', font), os.path.join(self.dirname, 'Fonts', font))

    def addscript(self, ascript = None, fromDir = None):
        if ascript is None:
            script = "script_"
            scriptnumber = 0
            TmpScript = script + str(scriptnumber)
            while os.path.exists(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript))):
                scriptnumber += 1 
                TmpScript = script + str(scriptnumber)
            f = open(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript)),'w')
            f.close()
            self.tree.AddScriptChild(TmpScript)
            self.Scripts.append(TmpScript)
        else:
            for script in ascript:
                if not os.path.isfile(os.path.join(self.dirname, 'Scripts', script)):
                    shutil.copy(os.path.join(fromDir, 'Scripts', script), os.path.join(self.dirname, 'Scripts', script))

    def addobject(self, aobject = None, fromDir = None):
        if aobject is None:
            object = "obj_"
            objectnumber = 0
            TmpObject= object + str(objectnumber)
            while os.path.exists(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject))):
                objectnumber += 1 
                TmpObject = object + str(objectnumber)
            f = open(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject)),'w')
            f.close()
            self.tree.AddObjectChild(TmpObject)
            self.Objects.append(TmpObject)
        else:
            for object in aobject:
                if not os.path.isfile(os.path.join(self.dirname, 'Objects', object)):
                    shutil.copy(os.path.join(fromDir, 'Objects', object), os.path.join(self.dirname, 'Objects', object))

    def addroom(self, aroom = None, fromDir = None):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

      
def main():
    app = QtGui.QApplication(sys.argv)
    st = Stellar()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
