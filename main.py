import sys
from PyQt4 import QtGui
from GUI import *

def main():
    file = input("Give filename:")
    #file = "testbadlinevalues.txt"

    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.processEvents()
    ex = GUI(file)
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

    '''
    DOGEEEE
    ─────────▄──────────────▄
    ────────▌▒█───────────▄▀▒▌
    ────────▌▒▒▀▄───────▄▀▒▒▒▐
    ───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
    ─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
    ───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌
    ──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌
    ──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
    ─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌
    ─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
    ─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐
    ▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌
    ▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐
    ─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌
    ─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
    ──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌
    ────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
    ───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
    ──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀
    '''
