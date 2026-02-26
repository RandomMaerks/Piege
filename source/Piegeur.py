import sys
import os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QFontMetricsF, QDesktopServices, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QLabel, QToolBar,
                             QMainWindow, QToolBar, QWidget, QVBoxLayout,
                             QGridLayout, QTextEdit, QPlainTextEdit, QPushButton,
                             QDialog, QFileDialog, QDialogButtonBox, QFontDialog)
import pyqt5_fugueicons as fugue
import interpreter
from time import time
from threading import Thread
from io import StringIO
import contextlib
import decimal


class DialogAbout(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(fugue.icon("information")))

        self.setFixedWidth(400)

        with open("resources/ui_config.txt", "r", encoding="utf8") as file:
            uiConfigFile = file.readlines()
            for line in uiConfigFile:
                exec(line)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.buttonBox.accepted.connect(self.accept)

        self.button_InfoPage = QPushButton("Check out the official GitHub repo!")
        self.button_InfoPage.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.button_InfoPage.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/RandomMaerks/Piege"))
        )

        self.button_License = QPushButton("Check out the official GitHub repo!")
        self.button_License.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.button_License.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/RandomMaerks/Piege/blob/main/LICENSE.txt"))
        )

        self.label_Icon = QLabel(self)
        self.label_Icon.setMaximumHeight(50)
        self.label_Icon.setMaximumWidth(50)
        self.pixmap_Icon = QPixmap("resources/piege.png")
        self.label_Icon.setPixmap(self.pixmap_Icon)
        self.label_Icon.setScaledContents(True)

        self.label_Title = QLabel("Piègeur")
        self.label_Title.setFont(QFont(self.fontNameUI, 20, QFont.Bold))
        
        self.label_Subtitle = QLabel("An IDE for the Piège programming language")
        self.label_Subtitle.setFont(QFont(self.fontNameUI, 12))
        self.label_Subtitle.setWordWrap(True)

        self.label_Description = QLabel("\nIDE version: 0.3.1 (27 February 2026)\n"
                                        "Supports Piège version: 2.1 (25 February 2026)\n\n"
                                        "Free & open-source software, licensed under terms of the MIT license.\n\n"
                                        "Piègeur /pɪ.ˈe.ʒœ/ is the official integrated development "
                                        "environment for the Piège programming language. This IDE "
                                        "includes an interpreter as a backend written in Python, "
                                        "designed to process and run code written specifically in Piège. "
                                        "It also has a custom-made library to store math functions such "
                                        "as arithmetic and trigonometric functions, as well as "
                                        "comparison operators.\n\n"
                                        "Both Piège and Piègeur are developed by RandomMaerks.")
        self.label_Description.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.label_Description.setWordWrap(True)

        self.dialogLayout = QGridLayout()
        self.dialogLayout.addWidget(self.label_Icon, 0, 1, 2, 1)
        self.dialogLayout.addWidget(self.label_Title, 0, 0)
        self.dialogLayout.addWidget(self.label_Subtitle, 1, 0)
        self.dialogLayout.addWidget(self.label_Description, 2, 0, 1, 2)
        self.dialogLayout.addWidget(self.button_InfoPage, 3, 0, 1, 2)
        self.dialogLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.setLayout(self.dialogLayout)

        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)
        
class DialogUnsaved(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save changes")
        self.setWindowIcon(QIcon(fugue.icon("question")))
        
        self.setFixedWidth(300)

        with open("resources/ui_config.txt", "r", encoding="utf8") as file:
            uiConfigFile = file.readlines()
            for line in uiConfigFile:
                exec(line)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save |
                                          QDialogButtonBox.Discard |
                                          QDialogButtonBox.Cancel)
        self.buttonBox.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.buttonBox.clicked.connect(self.returnSignal)

        self.unsavedMessage = QLabel("Do you want to save changes to current file?")
        self.unsavedMessage.setFont(QFont(self.fontNameUI, self.fontSizeUI))
        self.unsavedMessage.setWordWrap(True)
        
        self.dialogLayout = QVBoxLayout()
        self.dialogLayout.addWidget(self.unsavedMessage)
        self.dialogLayout.addWidget(self.buttonBox)
        self.setLayout(self.dialogLayout)

        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)
        
    def returnSignal(self, button):
        role = self.sender().buttonRole(button)
        if role == QDialogButtonBox.AcceptRole: self.accept()    
        elif role == QDialogButtonBox.DestructiveRole: self.done(-1)
        elif role == QDialogButtonBox.RejectRole: self.reject()

class Piegeur(QMainWindow):
    def __init__(self):
        super(Piegeur, self).__init__()
        self.setWindowTitle("Piègeur IDE - None")
        self.setWindowIcon(QIcon("resources/piege.ico"))

        self.currentFile = "None"
        self.savedState = None
        self.dirDisplay = "None"

        # Default window geometry & constraints
        self.width = 1280
        self.height = 720
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setGeometry(200, 200, self.width, self.height)

        # Font config for UI and textboxes

        if not os.path.exists("resources/ui_config.txt"):
            os.makedirs(os.path.dirname("resources/"))
            with open("resources/ui_config.txt", "w", encoding="utf8") as file:
                file.write("self.fontNameUI = \"Segoe UI\"\n"
                           "self.fontSizeUI = 9\n"
                           "self.fontNameTextBox = \"Consolas\"\n"
                           "self.fontSizeTextBox = 10")

        with open("resources/ui_config.txt", "r", encoding="utf8") as file:
            uiConfigFile = file.readlines()
            for line in uiConfigFile:
                exec(line)
                
        self.currentDir = "c://"

        self.initUI()
        
    def initUI(self):
        # Preset action buttons
        self.button_New = QAction(fugue.icon("document--plus"), "&New...", self)
        self.button_New.setShortcut(QKeySequence("Ctrl+n"))
        self.button_New.triggered.connect(self.action_New)
        
        self.button_Open = QAction(fugue.icon("folder-open-document"), "&Open...", self)
        self.button_Open.setShortcut(QKeySequence("Ctrl+o"))
        self.button_Open.triggered.connect(self.action_Open)

        self.button_Save = QAction(fugue.icon("document--arrow"), "&Save", self)
        self.button_Save.setShortcut(QKeySequence("Ctrl+s"))
        self.button_Save.triggered.connect(self.action_Save)

        self.button_SaveAs = QAction(fugue.icon("blue-document--arrow"), "Save &As...", self)
        self.button_SaveAs.setShortcut(QKeySequence("Ctrl+Shift+s"))
        self.button_SaveAs.triggered.connect(self.action_SaveAs)

        self.button_CloseFile = QAction(fugue.icon("document--minus"), "&Close File", self)
        self.button_CloseFile.setShortcut(QKeySequence("Ctrl+w"))
        self.button_CloseFile.setDisabled(True)
        self.button_CloseFile.triggered.connect(self.action_CloseFile)

        self.button_ExitIDE = QAction(fugue.icon("cross"), "&Exit IDE", self)
        self.button_ExitIDE.setShortcut(QKeySequence("Alt+F4"))
        self.button_ExitIDE.triggered.connect(self.action_ExitIDE)

        self.button_Run = QAction(fugue.icon("control"), "&Run", self)
        self.button_Run.setShortcut(QKeySequence("F5"))
        self.button_Run.triggered.connect(self.action_Run)

        self.button_Interrupt = QAction(fugue.icon("control-stop-square"), "&Interrupt (Disabled)", self)
        self.button_Interrupt.setShortcut(QKeySequence("F6"))
        self.button_Interrupt.setDisabled(True)
        #self.button_Interrupt.triggered.connect(self.action_Interrupt)

        self.button_SetFont = QAction(fugue.icon("edit"), "Set &Font...", self)
        self.button_SetFont.setShortcut(QKeySequence("Ctrl+f"))
        self.button_SetFont.triggered.connect(self.action_SetFont)

        self.button_ShowLineNum = QAction("Show &Line Number", self)
        self.button_ShowLineNum.setCheckable(True)
        self.button_ShowLineNum.triggered.connect(self.action_ToggleLineNumber)

        self.button_RelativePath = QAction("&Relative Path", self)
        self.button_RelativePath.setCheckable(True)
        self.button_RelativePath.triggered.connect(self.action_ToggleRelativePath)

        self.button_ShowToolbarText = QAction("Show &Toolbar Text", self)
        self.button_ShowToolbarText.setCheckable(True)
        self.button_ShowToolbarText.setChecked(True)
        self.button_ShowToolbarText.triggered.connect(self.action_ToggleToolbarText)

        self.button_About = QAction(fugue.icon("information"), "&About Piègeur", self)
        self.button_About.setShortcut(QKeySequence("Ctrl+t"))
        self.button_About.triggered.connect(self.action_AboutDialog)

        self.button_PiegeDocs = QAction(fugue.icon("documents-text"), "&Piège Wiki", self)
        self.button_PiegeDocs.setShortcut(QKeySequence("F1"))
        self.button_PiegeDocs.triggered.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/RandomMaerks/Piege/wiki"))
        )

        self.button_Undo = QAction(fugue.icon("arrow-return-180-left"), "&Undo", self)
        self.button_Undo.setShortcut(QKeySequence("Ctrl+z"))

        self.button_Redo = QAction(fugue.icon("arrow-return"), "&Redo", self)
        self.button_Redo.setShortcut(QKeySequence("Ctrl+Shift+z"))

        self.button_SelectAll = QAction(fugue.icon("edit-shade"), "Select &All", self)
        self.button_SelectAll.setShortcut(QKeySequence("Ctrl+a"))

        self.button_Cut = QAction(fugue.icon("scissors"), "Cu&t", self)
        self.button_Cut.setShortcut(QKeySequence("Ctrl+x"))

        self.button_Copy = QAction(fugue.icon("clipboard"), "&Copy", self)
        self.button_Copy.setShortcut(QKeySequence("Ctrl+c"))

        self.button_Paste = QAction(fugue.icon("clipboard-paste"), "&Paste", self)
        self.button_Paste.setShortcut(QKeySequence("Ctrl+v"))

        self.button_QuickSetup = QAction(fugue.icon("wand"), "&Quick Setup", self)
        self.button_QuickSetup.setShortcut(QKeySequence("Ctrl+Shift+q"))
        self.button_QuickSetup.triggered.connect(self.action_QuickSetup)

        # Toolbar

        self.toolbar_File = QToolBar("Files")
        self.addToolBar(self.toolbar_File)
        self.toolbar_File.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar_Edit = QToolBar("Edit")
        self.addToolBar(self.toolbar_Edit)
        self.toolbar_Edit.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar_Run = QToolBar("Run")
        self.addToolBar(self.toolbar_Run)
        self.toolbar_Run.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.toolbar_File.addAction(self.button_New)
        self.toolbar_File.addAction(self.button_Open)
        self.toolbar_File.addAction(self.button_Save)
        self.toolbar_File.addAction(self.button_SaveAs)

        self.toolbar_Edit.addAction(self.button_Undo)
        self.toolbar_Edit.addAction(self.button_Redo)
        self.toolbar_Edit.addAction(self.button_SelectAll)
        self.toolbar_Edit.addAction(self.button_Cut)
        self.toolbar_Edit.addAction(self.button_Copy)
        self.toolbar_Edit.addAction(self.button_Paste)
        self.toolbar_Edit.addAction(self.button_QuickSetup)

        self.toolbar_Run.addAction(self.button_Run)

        # Menu bar
        self.menu = self.menuBar()
        
        self.menu_File = self.menu.addMenu("&File")
        self.menu_File.addAction(self.button_New)
        self.menu_File.addAction(self.button_Open)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.button_Save)
        self.menu_File.addAction(self.button_SaveAs)
        self.menu_File.addAction(self.button_CloseFile)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.button_ExitIDE)

        self.menu_Edit = self.menu.addMenu("&Edit")
        self.menu_Edit.addAction(self.button_Undo)
        self.menu_Edit.addAction(self.button_Redo)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.button_SelectAll)
        self.menu_Edit.addAction(self.button_Cut)
        self.menu_Edit.addAction(self.button_Copy)
        self.menu_Edit.addAction(self.button_Paste)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.button_QuickSetup)

        self.menu_Run = self.menu.addMenu("&Run")
        self.menu_Run.addAction(self.button_Run)
        self.menu_Run.addAction(self.button_Interrupt)

        self.menu_Options = self.menu.addMenu("&Options")
        self.menu_Options.addAction(self.button_SetFont)
        self.menu_Options.addSeparator()
        self.menu_Options.addAction(self.button_ShowLineNum)
        self.menu_Options.addAction(self.button_RelativePath)
        self.menu_Options.addAction(self.button_ShowToolbarText)

        self.menu_Help = self.menu.addMenu("&Help")
        self.menu_Help.addAction(self.button_About)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.button_PiegeDocs)

        # Main editor
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.label_CurrentFile = QLabel(f"Input", self)
        self.label_CurrentFile.setFont(QFont(self.fontNameUI, self.fontSizeUI))

        self.codeEditor = QPlainTextEdit(self)
        self.codeEditor.setFont(QFont(self.fontNameTextBox, self.fontSizeTextBox))
        fontMetrics = QFontMetricsF(self.codeEditor.font())
        spaceWidth = fontMetrics.width(" ")
        self.codeEditor.setTabStopDistance(spaceWidth * 4)
        self.codeEditor.textChanged.connect(self.textChanged)
        self.codeEditor.cursorPositionChanged.connect(self.cursorChanged)

        self.label_Output = QLabel(f"Interpreter output", self)
        self.label_Output.setFont(QFont(self.fontNameUI, self.fontSizeUI))

        self.outputWindow = QTextEdit(self)
        self.outputWindow.setFont(QFont(self.fontNameTextBox, self.fontSizeTextBox))
        self.outputWindow.setReadOnly(True)

        self.label_Runtime = QLabel(f"Runtime", self)
        self.label_Runtime.setFont(QFont(self.fontNameUI, self.fontSizeUI))

        self.runtimeWindow = QTextEdit(self)
        self.runtimeWindow.setFont(QFont(self.fontNameTextBox, self.fontSizeTextBox))
        self.runtimeWindow.setReadOnly(True)
        self.runtimeWindow.setMaximumHeight(50)

        self.label_CursorPos = QLabel(f"Line 1, character 1 index 0 ( )", self)
        self.label_CursorPos.setFont(QFont(self.fontNameUI, self.fontSizeUI))

        self.grid = QGridLayout()
        self.grid.addWidget(self.label_CurrentFile, 0, 0)
        self.grid.addWidget(self.codeEditor, 1, 0, 3, 1)
        self.grid.addWidget(self.label_Output, 0, 1)
        self.grid.addWidget(self.outputWindow, 1, 1)
        self.grid.addWidget(self.label_Runtime, 2, 1)
        self.grid.addWidget(self.runtimeWindow, 3, 1)
        self.grid.addWidget(self.label_CursorPos, 4, 0, 1, 2)
        
        self.centralWidget.setLayout(self.grid)

    def closeEvent(self, event):
        if self.savedState == False and self.currentFile != "None":
            dialog = DialogUnsaved(self)
            returnValue = dialog.exec()
            if returnValue == 1:
                self.action_Save()
                event.accept()
            elif returnValue == 0:
                event.ignore()
            else:
                event.accept()

    def action_ExitIDE(self):
        if self.checkForSaved() == 0: return None
        sys.exit()

    def action_Run(self):
        self.outputWindow.clear()
        self.runtimeWindow.clear()

        t1 = Thread(target = self.executeScript)
        t1.start()

    def action_QuickSetup(self):
        setupString = "# input-output\nOUTPUT interpreter\n\n# math operation\n"
        self.codeEditor.insertPlainText(setupString)

    def action_AboutDialog(self):
        dialog = DialogAbout(self)
        dialog.exec()

    def executeScript(self):
        code = self.codeEditor.toPlainText()
        if len(code) == 0: return None
        
        outputStream = StringIO()

        timeStart = time()
        with contextlib.redirect_stdout(outputStream):
            try:
                interpreter.executeCode(code)
            except Exception as e:
                print(e)
        timeEnd = time()

        output = outputStream.getvalue()
        self.outputWindow.insertPlainText(output)

        runtime = round((timeEnd - timeStart), 5)
        multiple = round(1/runtime, 5)
        self.runtimeWindow.insertPlainText(f"{runtime}s ({runtime} : 1 or 1 : {multiple})")

    def action_Interrupt(self):
        pass

    def textChanged(self):
        self.setWindowTitle(f"*Piègeur IDE - {self.dirDisplay}")
        self.savedState = False

    def cursorChanged(self):
        wholeText = self.codeEditor.toPlainText()
        
        charIndex = self.codeEditor.textCursor().position()
        letterAtCharIndex = "" if charIndex > len(wholeText)-1 else wholeText[charIndex].replace("\n", "\\n")

        lineBreaks = [index for index, char in enumerate(wholeText) if char == "\n"]
        line = 1
        for index, lineBreak in enumerate(lineBreaks):
            if charIndex > lineBreak: line += 1

        self.label_CursorPos.setText(f"Line {line}, character {charIndex+1} index {charIndex} ( {letterAtCharIndex} )")

    def action_ToggleLineNumber(self, s):
        if s == True: print("toggled on")
        else: print("toggled off")

    def action_ToggleRelativePath(self):
        self.checkPathDisplay()

    def action_ToggleToolbarText(self, s):
        if s:
            self.toolbar_File.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.toolbar_Edit.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.toolbar_Run.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        else:
            self.toolbar_File.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.toolbar_Edit.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.toolbar_Run.setToolButtonStyle(Qt.ToolButtonIconOnly)
        
    def checkPathDisplay(self):
        if self.button_RelativePath.isChecked(): self.dirDisplay = os.path.basename(self.currentFile)
        else: self.dirDisplay = self.currentFile
        
        if self.savedState == True: self.setWindowTitle(f"Piègeur IDE - {self.dirDisplay}")
        else: self.setWindowTitle(f"*Piègeur IDE - {self.dirDisplay}")

    def action_New(self):
        if self.checkForSaved() == 0: return None
        fileDir, _ = QFileDialog.getSaveFileName(self, "New", self.currentDir, "Piège files (*.piege)")
        if fileDir:
            self.currentFile = fileDir
            with open(self.currentFile, "w", encoding="utf8") as file:
                file.write("")
            self.currentDir = os.path.dirname(self.currentFile)
            self.codeEditor.setPlainText("")
            self.button_CloseFile.setDisabled(False)
        else: return None
        self.savedState = True
        self.checkPathDisplay()

    def action_Open(self):
        if self.checkForSaved() == 0: return None
        fileDir, _ = QFileDialog.getOpenFileName(self, "Open", self.currentDir, "Piège files (*.piege)")
        if fileDir:
            self.currentFile = fileDir
            with open(self.currentFile, "r", encoding="utf8") as file:
                code = file.read()
            self.currentDir = os.path.dirname(self.currentFile)
            self.codeEditor.setPlainText(code)
            self.button_CloseFile.setDisabled(False)
        else: return None
        self.savedState = True
        self.checkPathDisplay()

    def action_Save(self):
        if self.currentFile == "None":
            fileDir, _ = QFileDialog.getSaveFileName(self, "Save", self.currentDir, "Piège files (*.piege)")
            if fileDir: self.currentFile = fileDir
            else: return None
            self.currentDir = os.path.dirname(self.currentFile)
        code = self.codeEditor.toPlainText()
        with open(self.currentFile, "w", encoding="utf8") as file:
            file.write(code)
        self.button_CloseFile.setDisabled(False)
        self.savedState = True
        self.checkPathDisplay()

    def action_SaveAs(self):
        fileDir, _ = QFileDialog.getSaveFileName(self, "Save", self.currentDir, "Piège files (*.piege)")
        if fileDir: self.currentFile = fileDir
        else: return None
        self.currentDir = os.path.dirname(self.currentFile)
        code = self.codeEditor.toPlainText()
        with open(self.currentFile, "w", encoding="utf8") as file:
            file.write(code)
        self.button_CloseFile.setDisabled(False)      
        self.savedState = True
        self.checkPathDisplay()

    def action_CloseFile(self):
        if self.checkForSaved() == 0: return None
        self.codeEditor.clear()
        self.outputWindow.clear()
        self.runtimeWindow.clear()
        self.currentFile = "None"
        self.button_CloseFile.setDisabled(True)
        self.currentDir = os.path.dirname(self.currentFile)
        self.checkPathDisplay()
        self.savedState = False

    def checkForSaved(self):
        if self.savedState == False and self.currentFile != "None":
            dialog = DialogUnsaved(self)
            returnValue = dialog.exec()
            if returnValue == 1: self.action_Save()
            elif returnValue == 0: return 0

    def action_SetFont(self):
        initialFont = QFont(self.fontNameTextBox, self.fontSizeTextBox)
        fontDialog = QFontDialog()
        font, ok = fontDialog.getFont(initialFont, self, options = QFontDialog.MonospacedFonts)
        if ok:
            self.codeEditor.setFont(font)
            fontMetrics = QFontMetricsF(self.codeEditor.font())
            spaceWidth = fontMetrics.width(" ")
            self.codeEditor.setTabStopDistance(spaceWidth * 4)
            self.outputWindow.setFont(font)
            self.runtimeWindow.setFont(font)
            fontData = font.toString().split(",")
            self.fontNameTextBox = fontData[0]
            self.fontSizeTextBox = int(fontData[1])
            with open("resources/ui_config.txt", "r", encoding="utf8") as file:
                uiConfigFile = file.readlines()
                uiConfigFile[2] = f"self.fontNameTextBox = \"{self.fontNameTextBox}\"\n"
                uiConfigFile[3] = f"self.fontSizeTextBox = {self.fontSizeTextBox}"
            with open("resources/ui_config.txt", "w", encoding="utf8") as file:
                file.writelines(uiConfigFile)

def main():
    app = QApplication(sys.argv)
    ide = Piegeur()
    ide.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
