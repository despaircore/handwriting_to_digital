import tkinter

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QMenu, QMenuBar, QPushButton, QStatusBar, QTextEdit, QWidget

import utility
import pyperclip as pc
from tkinter import filedialog, messagebox
from ultralytics import YOLO

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(570, 350)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(9)
        font.setBold(True)
        font.setKerning(True)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.uploadb = QPushButton(self.centralwidget)

        self.uploadb.setObjectName(u"uploadb")
        self.uploadb.setGeometry(QRect(80, 230, 111, 31))
        self.uploadb.clicked.connect(self.import_and_process)

        self.maintext = QTextEdit(self.centralwidget)
        self.maintext.setObjectName(u"maintext")
        self.maintext.setGeometry(QRect(80, 30, 421, 161))
        self.copyb = QPushButton(self.centralwidget)

        self.copyb.setObjectName(u"copyb")
        self.copyb.setGeometry(QRect(230, 230, 111, 31))
        self.copyb.clicked.connect(self.copy_stuff)

        self.exportb = QPushButton(self.centralwidget)
        self.exportb.setObjectName(u"exportb")
        self.exportb.setGeometry(QRect(390, 230, 111, 31))
        self.exportb.clicked.connect(self.export_stuff)

        self.response = QLabel(self.centralwidget)
        self.response.setObjectName(u"response")
        self.response.setGeometry(QRect(80, 200, 241, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 570, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.uploadb.setText(QCoreApplication.translate("MainWindow", u"upload file", None))
        self.copyb.setText(QCoreApplication.translate("MainWindow", u"copy text", None))
        self.exportb.setText(QCoreApplication.translate("MainWindow", u"export as a txt", None))
        self.response.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Text translator", None))
    # retranslateUi

    def copy_stuff(self):
        copied_text = self.maintext.toPlainText()
        pc.copy(copied_text)
        self.response.setText(QCoreApplication.translate("MainWindow", u"text copied!", None))

    def export_stuff(self):
        written_text = self.maintext.toPlainText()
        types = [("Text files", "*.txt")]
        root = tkinter.Tk()
        root.withdraw()
        fp = filedialog.asksaveasfilename(title = "text_export", filetypes=types, initialdir="/")

        if fp != "":
            file_writer = open(fp, "w", encoding="utf-8")
            file_writer.write(written_text)
            file_writer.close()
            self.response.setText(QCoreApplication.translate("MainWindow", u"text exported!", None))

        else:
            messagebox.showinfo("Something went wrong", "File not exported!")
            raise ErrorClass("File not exported!")

    def import_and_process(self):

        root = tkinter.Tk()
        root.withdraw()
        file_types = [("image files", ".jpg .jpeg .png")]
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=file_types)

        if file_path:
            self.response.setText(QCoreApplication.translate("MainWindow", u"image imported!", None))
            ml = YOLO("my_model.pt")

            results = ml(file_path)

            letters = []
            final = []

            for idx, result in enumerate(results[0].boxes.xyxy):
                letter = [result[0].item(), result[1].item(), result[2].item(), result[3].item(), int(results[0].boxes.cls[idx].item())]
                letters.append(letter)

            letters = sorted(letters, key=lambda b: b[1])

            rows = []
            current_row = [letters[0]]

            for letter in letters[1:]:
                prev_letter = current_row[-1]
                box_height = prev_letter[3] - prev_letter[1]
                y_threshold = box_height * 0.5

                if abs(letter[1] - prev_letter[1]) <= y_threshold:
                    current_row.append(letter)
                else:
                    rows.append(current_row)
                    current_row = [letter]
            rows.append(current_row)

            sorted_letters = []
            for row in rows:
                sorted_row = sorted(row, key=lambda b: b[0])
                sorted_letters.extend(sorted_row)

            space_distance = abs(((sorted_letters[0][0]+sorted_letters[0][2])/2) - ((sorted_letters[1][0]+sorted_letters[1][2])/2))

            for i in range(len(sorted_letters)-1):

                ltr = sorted_letters[i]
                ltr2 = sorted_letters[i+1]
                final.append(str(ltr[4]))

                if abs(((ltr[0]+ltr[2])/2) - ((ltr2[0]+ltr2[2])/2)) >= space_distance*1.5:
                    final.append("55")

                if i == len(sorted_letters)-2:
                    ltr = sorted_letters[i+1]
                    final.append(ltr[4])

            result_og, result2 = utility.text_converter_checker(final)
            self.maintext.setText(f"original text: {result_og}\nspell-checked text: {result2}")

        else:
            messagebox.showinfo("Something went wrong", "File not uploaded!")
            raise ErrorClass("File not found!")


class ErrorClass(Exception):
    pass
