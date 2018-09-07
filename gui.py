import sys
from PyQt5 import QtWidgets
import IndexCreation
import json

class GUI(QtWidgets.QWidget):

    searches = []

    def __init__(self):
        super().__init__()

        self.initializeInterface()

    def initializeInterface(self):
        self.searchBar = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton('Search')
        self.searchBar.returnPressed.connect(self.searchButton.click)
        self.label = QtWidgets.QLabel('Nothing has been searched...')
        self.index, self.bookkeeping, self.total_docs = IndexCreation.main()

        #creating search labels
        self.search1 = QtWidgets.QLabel()
        self.search2 = QtWidgets.QLabel()
        self.search3 = QtWidgets.QLabel()
        self.search4 = QtWidgets.QLabel()
        self.search5 = QtWidgets.QLabel()
        self.search6 = QtWidgets.QLabel()
        self.search7 = QtWidgets.QLabel()
        self.search8 = QtWidgets.QLabel()
        self.search9 = QtWidgets.QLabel()
        self.search10 = QtWidgets.QLabel()

        GUI.searches.extend((self.search1, self.search2, self.search3, self.search4, self.search5, self.search6, self.search7, self.search8, self.search9, self.search10))

        #creating search bar and search button
        horizontal = QtWidgets.QHBoxLayout()
        horizontal.addWidget(self.searchBar)
        horizontal.addWidget(self.searchButton)

        #adding in search bar, search button, and labels to window
        vertical = QtWidgets.QVBoxLayout()
        vertical.addLayout(horizontal)
        vertical.addWidget(self.label)

        #adding search result labels to window
        for x in range(10):
            vertical.addWidget(GUI.searches[x])
        vertical.addStretch()

        self.setLayout(vertical)
        self.setWindowTitle('Project Group 64 Search')

        #event for search button clicked
        self.searchButton.clicked.connect(self.buttonClicked)

        self.show()

    def buttonClicked(self):
        sender = self.sender()
        query = self.searchBar.text()

        resultTuple = self.generateSearches(query)

        if (resultTuple[1] == resultTuple[2]):
            resultString = 'First 10 results for "' + query + '":'
            self.label.setText(resultString)
        elif ((resultTuple[1] != resultTuple[2]) and len(resultTuple[0]) > 0):
            resultString = "\"" + query + "\" not found; showing results for \"" + resultTuple[2] + "\" instead:"
            self.label.setText(resultString)
        elif (len(resultTuple[0]) == 0):
            resultString = 'No results for "' + query + '"...'
            self.label.setText(resultString)


        #clears old results
        for x in range(10):
            GUI.searches[x].setText("")

        #prints out the first 10 results as hyperlinks
        for x in range(len(resultTuple[0])):
            hyper = str(x+1) + ".  <a href=\"http://" + resultTuple[0][x] + "\">" + str(resultTuple[0][x][:130]) + "</a>"

            if (len(resultTuple[0][x]) > 130): 
                shortenedURL = str(resultTuple[0][x][:130]) + "..."
                hyper = str(x+1) + ".  <a href=\"http://" + resultTuple[0][x] + "\">" + shortenedURL + "</a>"

            GUI.searches[x].setText(hyper)
            GUI.searches[x].setOpenExternalLinks(True)


    def generateSearches(self, query):
        results = []
        temp = IndexCreation.search_phrase(self.index, query)

        for link in temp[0]:
            results.append(self.bookkeeping[link])

        return (results, temp[1],temp[2])


if __name__ == '__main__':

    test = QtWidgets.QApplication(sys.argv)
    test_w = GUI()
    sys.exit(test.exec_())


