from PyQt4 import QtCore, QtGui
import os, sys
from PyQt4.QtGui import QFont

if sys.version_info.major == 2:
    str = unicode    
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        
        self.color_0 = QtGui.QColor(249, 38,  144)
        self.color_1 = QtGui.QColor(102, 217, 239)
        self.color_2 = QtGui.QColor(117, 113, 94 )
        self.color_3 = QtGui.QColor(230, 219, 102)
        self.color_4 = QtGui.QColor(166,226,46)
        self.color_5 = QtGui.QColor(174,129,255)
        self.color_6 = QtGui.QColor(253,151,32)

        group1Format = QtGui.QTextCharFormat()
        group1Format.setForeground(self.color_0)
        group1Patterns = ["\\bimport\\b", '\\bif\\b', '\\belse\\b',
                          "\\bfor\\b", "\\bswitch\\b" , "\\bcase\\b",
                          "\\bbreak\\b", "\\breturn\\b", "\\bwhile\\b",
                          "\\blocal\\b"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), group1Format)
                for pattern in group1Patterns]


        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(self.color_1)
        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]

        self.highlightingRules += [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QtGui.QTextCharFormat()
        classFormat.setForeground(self.color_4)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(self.color_5)
        numberPatterns = ['\\b[+-]?[0-9]+[lL]?\\b', '\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b',
        '\\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b', '\\btrue\\b', '\\bfalse\\b']
        self.highlightingRules += [(QtCore.QRegExp(pattern), numberFormat)
                for pattern in numberPatterns]

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(self.color_2)
        self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(self.color_2)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(self.color_3)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setForeground(self.color_1)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);


class ScriptEditor(QtGui.QDialog):
    def __init__(self, main, name, filename):
        super(ScriptEditor, self).__init__(main)
        self.main = main
        self.filename = filename

        if os.path.exists(os.path.join('..','images')):
        	img_path=os.path.join('..','images')
        else:
        	img_path=os.path.join('images')

        saveAction = QtGui.QAction(QtGui.QIcon(os.path.join(img_path, 'save.png')), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save_file)
        self.toolbar = QtGui.QToolBar('Script Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.addAction(saveAction)

        with open(filename, 'r') as content_file:
            self.content = content_file.read()
        
        self.font = QtGui.QFont()
        self.font.setFamily('ClearSans')
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setFixedPitch(True)
        self.font.setPointSize(int(14))

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)

        self.textedit = QtGui.QTextEdit()
        self.textedit.insertPlainText(self.content)
        self.textedit.moveCursor(QtGui.QTextCursor.Start)
        self.textedit.setLineWrapMode(0)

        self.textedit.setFont(self.font)
        self.ContainerGrid.addWidget(self.toolbar)
        self.ContainerGrid.addWidget(self.textedit)

        self.setLayout(self.ContainerGrid)

        self.highlighter = Highlighter(self.textedit.document())

    def save_file(self):
        with open(self.filename, 'w') as f:
            f.write(self.textedit.toPlainText())
        self.main.statusBar().showMessage(os.path.basename(str(self.filename))+' saved!', 2000)

class Editor(QtGui.QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        target="none"
        pathtofile="scripteditor.py"

        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin(0)

        self.textedit = ScriptEditor(self, target, pathtofile)

        self.showlayout.addWidget(self.textedit)
        self.ShowFrame.setLayout(self.showlayout)

        self.setCentralWidget(self.ShowFrame)
        self.setWindowTitle("Stellar - TextEditor")
        self.resize(640, 480)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f = open('../default.css')
    style = f.read()
    f.close()
    app.setStyleSheet(style)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    mainWin = Editor()
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())