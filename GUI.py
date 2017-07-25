import sys, random, math, time
from PyQt4 import QtGui, QtCore
from file_IO import File_IO


class GUI(QtGui.QMainWindow):
    def __init__(self, name):
        super(GUI, self).__init__()

        #Sets up the UI
        self.initUI(name)

    def initUI(self, name):
        '''
        Sets global variables and constructs the window
        :param data:
        :param name:
        :return:
        '''
        #read data in file_IO
        self.filename = name
        file_IO = File_IO()
        data = file_IO.load_data(self.filename)
        #creates a color palette
        i = 0
        self.palette = []
        if data.type =="#line":
            while i < len(data.grapharray.graphlist):
                self.palette.append(self.color())
                i+=1
        else:
            i=0
            while i < len(data.grapharray.graphlist[0].pointarray):
                self.palette.append(self.color())
                i+=1
        self.data = data
        self.name = name
        self.gridDesc = 5
        self.x_marg = self.width()/10
        self.y_marg = self.height()/10
        self.grid = True
        self.legend = True
        if self.data.type == "#line" or self.data.type == "#column":
            self.setGeometry(200, 200, 800, 500)
        else:
            self.setGeometry(200, 200, 600, 500)
        self.setWindowTitle(self.filename)
        self.menuBar()
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        '''
        Tahan tulee linechart
        !!! TO DO: Lisaa if-lauseet self.data.typen mukaan!!!
        Ei valttamatta kaikkein kaunein ratkaisu!!
        '''
        if self.data.type == "#line":
            self.drawBackground(qp)
            self.drawLines(qp, e)
            self.lgnd = []
            c = 0
            if self.grid == True:
                self.drawGrid(qp)
            for i in self.data.grapharray.graphlist:
                graph = []
                color = self.palette[c]
                self.lgnd.append([i.name, color])
                for pnt in i.pointarray:
                    graph.append([float(pnt.x), float(pnt.y)])
                GUI.drawGraph(self, qp, graph, color)
                c+=1

            if self.legend == True:
                self.showLegend(qp)

        '''
        piirakkadiagrammin muodostus:
        -laskee jokaisen osuuden kulman ja labelin
        '''

        if self.data.type == "#pie":
            self.lgnd = []
            self.fracs = []
            sumz=0
            c = 0
            start_angle=90 * 16
            for tmp in self.data.grapharray.graphlist[0].pointarray:
                sumz = sumz+float(tmp.y)
            for i in self.data.grapharray.graphlist[0].pointarray:
                color = self.palette[c]
                self.lgnd.append([i.x, color])
                angle = round(float(i.y)/sumz*16*360)
                qp.setPen(QtCore.Qt.white)
                qp.setBrush(color)
                qp.drawPie(self.x_marg,self.y_marg,self.height()-self.y_marg*2,self.height()-self.y_marg*2,start_angle, angle)
                start_angle += angle
                c+=1

            if self.legend == True:
                self.showLegend(qp)


        '''
        Pylvasdiagrammin muodostaminen:
        - laskee pylvaiden lukumaaran ja jakaa silla ikkunan leveyden
        - laskee aariarvot
        '''
        if self.data.type == "#column":
            self.drawBackground(qp)
            self.lgnd = []
            self.countColumns(qp, e)

            c=0
            start_x = self.x_marg + 20
            part = (self.width()-2*self.x_marg)/len(self.data.grapharray.graphlist[0].pointarray)
            for i in self.data.grapharray.graphlist[0].pointarray:
                color = self.palette[c]
                self.lgnd.append([i.x, color])
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(start_x, (self.height() - int(self.y_marg+abs(self.axisArr[0])*((self.height()-self.y_marg*2)/(self.axisArr[1]-self.axisArr[0])))), part/2,\
                            (-1*int(i.y)*((self.height()-self.y_marg*2)/(self.axisArr[1]-self.axisArr[0]))))
                pen = QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
                qp.setFont(QtGui.QFont('Decorative', 10))
                qp.setPen(pen)
                qp.drawText(start_x, self.height()-self.y_marg/2, i.x)
                start_x += part
                c+=1

            if self.legend == True:
                self.showLegend(qp)
        qp.end()

    def countColumns(self, qp, e):
        '''
        Counts the measurements axis
        :param qp:
        :param e:
        :return:
        '''
        lowy = 0
        highy = 0
        graph = []
        for i in self.data.grapharray.graphlist[0].pointarray:
            graph.append(float(i.y))
            '''
            y-akselin arvojen maksimit ja minimit
            '''
        for i in graph:
            if i<lowy:
                lowy = i
            elif i>highy:
                highy = i

        '''
        Nyt maksimit ja minimit laskettu. Pyoristetaan arvot tasalukuun
        '''
        highy = int(math.ceil(highy / 10.0)) * 10
        if lowy<0:
            lowy = int(math.ceil(-1*lowy / 10.0)) * -10

        self.axisArr = [lowy, highy]
        y_crd =[]
        self.xlbl = self.data.grapharray.axX
        self.ylbl = self.data.grapharray.axY
        '''
        TODO:
        - skaalaus oikein high-low välille jos välin suuruus luokkaa 1000 vs. 20
        '''
        i = 0
        scly = highy-lowy
        if lowy<0:
            scly = highy-lowy
        if highy<0:
            scly = highy+lowy
        while i <= self.gridDesc:
            y_crd.insert(0,highy-i*((scly)/self.gridDesc))
            i =i+1
        self.y_crd = y_crd
        #Draws texts for columns
        for i in self.y_crd:
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawText(self.x_marg/self.gridDesc, (self.height() - int(self.y_marg+(i+abs(self.axisArr[0]))*((self.height()-self.y_marg*2)/(highy-lowy)))), "%.1f" % i)
            if self.grid==True:
                pen = QtGui.QPen(QtCore.Qt.lightGray, 1, QtCore.Qt.DotLine)
                qp.setPen(pen)
                qp.drawLine(self.x_marg-2, (self.height() - int(self.y_marg+(i+abs(self.axisArr[0]))*((self.height()-self.y_marg*2)/(highy-lowy)))),\
                            self.width()-self.x_marg, (self.height() - int(self.y_marg+(i+abs(self.axisArr[0]))*((self.height()-self.y_marg*2)/(highy-lowy)))))

        pen = QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.setPen(pen)
        #yaxis
        qp.drawLine(self.x_marg, self.y_marg, self.x_marg, self.height()-self.y_marg)
        qp.drawText(self.x_marg*0.95, self.y_marg*0.9, self.ylbl)

        #xaxis
        qp.drawText(self.width()-self.x_marg*0.9, self.height()-int(self.y_marg*0.95+abs(self.axisArr[0])*((self.height()-self.y_marg*2)/(highy-lowy))), self.xlbl)
        qp.drawLine(self.x_marg, (self.height() - int(self.y_marg+abs(self.axisArr[0])*((self.height()-self.y_marg*2)/(highy-lowy)))), self.width()-self.x_marg, (self.height() - int(self.y_marg+abs(self.axisArr[0])*((self.height()-self.y_marg*2)/(highy-lowy)))))

    def drawLines(self, qp, e):

        pen = QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.setPen(pen)
        #draws axis
        '''
        Viivat skaalautuvat ikkunan mukaan
        laskee nollakohdat!
        '''
        self.countAxis()
        self.xlbl = self.data.grapharray.axX
        self.ylbl = self.data.grapharray.axY
        zero = 0
        while round(self.axisArr[0]-zero, 5) != 0 and zero<self.axisArr[1]:
            zero = zero+0.01


        x_range = self.axisArr[1]-self.axisArr[0]
        y_range = self.axisArr[3]-self.axisArr[2]
        #Draws axis lines and labels
        if x_range != 0 and y_range != 0:
            #yaxis
            qp.drawText(self.x_marg*0.95+abs(self.axisArr[0])*((self.width()-self.x_marg*2-100)/x_range), self.y_marg*0.9, self.ylbl)
            qp.drawLine(int(self.x_marg+abs(self.axisArr[0])*((self.width()-self.x_marg*2-100)/x_range)),\
                        self.y_marg, int(self.x_marg+abs(self.axisArr[0])*((self.width()-self.x_marg*2-100)/x_range)),\
                        self.height()-self.y_marg)
            #x-axis
            qp.drawText(self.width()-self.x_marg*0.9-100, self.height()-int(self.y_marg*0.9+abs(self.axisArr[2])*((self.height()-self.y_marg*2)/y_range)), self.xlbl)
            qp.drawLine(self.x_marg, (self.height() - int(self.y_marg+abs(self.axisArr[2])*((self.height()-self.y_marg*2)/y_range))),\
                        self.width()-self.x_marg-100, (self.height() - int(self.y_marg+abs(self.axisArr[2])*((self.height()-self.y_marg*2)/y_range))))

            #Draws axis numbers
            #x-axis
            c=0
            for i in self.coords[0]:
                qp.drawText(int(self.x_marg+(i+abs(self.axisArr[0]))*((self.width()-self.x_marg*2-100)/x_range)), (self.height()-(self.y_marg/2)), "%.1f" % i)
                c = c+1
            c=0
            #axis nubmers for y-axis
            for i in self.coords[1]:
                qp.drawText(self.x_marg/self.gridDesc, (self.height() - int(self.y_marg+(i+abs(self.axisArr[2]))*((self.height()-self.y_marg*2)/y_range))), "%.1f" % i)
                c = c+1

    def drawGraph(self, qp, arr, color):
        p = 0
        '''
        !!testigraafi arr on random scheise. oikea datajoukko parametrina!!
        TODO:
        akselien skaalaus kohilleen
        eri viivoille eri värit

        '''

        x_range = self.axisArr[1]-self.axisArr[0]
        y_range = self.axisArr[3]-self.axisArr[2]

        p=0
        while p < len(arr)-1:
            pen = QtGui.QPen(color, 4, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(((arr[p][0]+abs(self.axisArr[0]))*((self.width()-self.x_marg*2-100)/x_range))+self.x_marg,\
                        (self.height())-((arr[p][1]+abs(self.axisArr[2]))*(self.height()-self.y_marg*2)/y_range)-self.y_marg,\
                        (arr[p+1][0]+abs(self.axisArr[0]))*((self.width()-self.x_marg*2-100)/x_range)+self.x_marg,\
                        self.height()-self.y_marg-(((arr[p+1][1]+abs(self.axisArr[2]))*(self.height()-self.y_marg*2)/y_range)))
            p +=1

    def drawGrid(self, qp):
        '''
        draws the grid according to axis values
        :param qp:
        :return:
        '''
        pen = QtGui.QPen(QtCore.Qt.lightGray, 1, QtCore.Qt.DotLine)
        qp.setPen(pen)
        self.countAxis()
        x_range = self.axisArr[1]-self.axisArr[0]
        y_range = self.axisArr[3]-self.axisArr[2]
        c=0
        if x_range != 0 and y_range != 0:
            for i in self.coords[0]:
                qp.drawLine(int(self.x_marg+(i+abs(self.axisArr[0]))*((self.width()-self.x_marg*2-100)/x_range)),\
                            (self.height()-self.y_marg-2), int(self.x_marg+(i+abs(self.axisArr[0]))*((self.width()-self.x_marg*2-100)/x_range)), self.y_marg)
                c = c+1
            c = 0
            for i in self.coords[1]:
                qp.drawLine(self.x_marg-2, (self.height() - int(self.y_marg+(i+abs(self.axisArr[2]))*((self.height()-self.y_marg*2)/y_range))),\
                            self.width()-self.x_marg-100, (self.height() - int(self.y_marg+(i+abs(self.axisArr[2]))*((self.height()-self.y_marg*2)/y_range))))
                c = c+1

    def drawBackground(self, qp):
        '''
        Draws a unicolor background
        :param qp:
        :return:
        '''
        if self.data.type == "#line":
            pen = QtGui.QPen(QtCore.Qt.lightGray, 1, QtCore.Qt.DotLine)
            qp.setPen(pen)
            qp.setBrush(QtGui.QColor(255, 255, 255))
            qp.drawRect(self.x_marg, self.y_marg, self.width()-2*self.x_marg-100, self.height()-2*self.y_marg)
        else:
            pen = QtGui.QPen(QtCore.Qt.lightGray, 1, QtCore.Qt.DotLine)
            qp.setPen(pen)
            qp.setBrush(QtGui.QColor(255, 255, 255))
            qp.drawRect(self.x_marg, self.y_marg, self.width()-2*self.x_marg, self.height()-2*self.y_marg)

    def countAxis(self):
        '''
        Counts the labels and lenghts for axis so they scale according to given data
        :return:
        '''
        lowx = 0
        highx = 0
        lowy = 0
        highy = 0
        for i in self.data.grapharray.graphlist:
            graph = []
            for pnt in i.pointarray:
                graph.append([float(pnt.x), float(pnt.y)])
            '''
            x-akselin arvojen maksimit ja minimit.
            !!Oletetaan etta x-akseli on jarjestetty tassa vaiheessa!!
            '''
            if len(graph) != 0:
                tmpxlow = graph[0][0]
                tmpxhigh = graph[len(graph)-1][0]
                if tmpxlow < lowx:
                    lowx = tmpxlow
                if tmpxhigh > highx:
                    highx = tmpxhigh
            '''
            y-akselin arvojen maksimit ja minimit
            '''
            for i in graph:
                if i[0] < lowx:
                    lowx = i[0]
                elif i[0] > highx:
                    highx = i[0]
                if i[1]<lowy:
                    lowy = i[1]
                elif i[1]>highy:
                    highy = i[1]

        '''
        Nyt maksimit ja minimit laskettu. Pyoristetaan arvot tasalukuun
        '''
        highx = int(math.ceil(highx / 10.0)) * 10
        highy = int(math.ceil(highy / 10.0)) * 10
        if lowx<0:
            lowx = int(math.ceil(-1*lowx / 10.0)) * -10
        if lowy<0:
            lowy = int(math.ceil(-1*lowy / 10.0)) * -10

        self.axisArr = [lowx, highx, lowy, highy]
        i = lowx
        coords = []
        x_crd= []
        y_crd =[]

        '''
        TODO:
        - skaalaus oikein high-low välille jos välin suuruus luokkaa 1000 vs. 20
        '''
        sclx = highx -lowx
        scly = highy-lowy
        if lowy<0:
            sclx = highx-lowx
        if highx<0:
            sclx= highx+lowx
        if lowy<0:
            scly = highy-lowy
        if highy<0:
            scly = highy+lowy

        i = 0
        while i <=self.gridDesc:
            x_crd.insert(0,highx-i*((sclx)/self.gridDesc))
            i =i+1
        i = 0
        while i <= self.gridDesc:
            y_crd.insert(0,highy-i*((scly)/self.gridDesc))
            i =i+1
        coords.append(x_crd)
        coords.append(y_crd)
        self.coords = coords


    def color(self):
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        return QtGui.QColor(r, g, b)

    def gridIO(self):
        if self.grid == True:
            self.grid = False
        else: self.grid = True
        self.update()

    def legIO(self):
        if self.legend == True:
            self.legend = False
        else: self.legend = True
        self.update()

    def saveIMG(self):
        p = QtGui.QPixmap.grabWindow(self.winId(),0,25,-1,self.height()-25).save("%s_graph.png" % self.name)

    def showLegend(self, qp):
        '''
        Prints legend and colors in small box
        :return:
        '''
        if self.data.type == "#column":
            return
        pos = 0
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.setPen(pen)
        buf = 1.5
        if self.data.type == "#pie":
            buf = 1
        if self.data.type == "#column":
            buf = 5
        qp.drawText(self.width()-140, 1.5*self.y_marg+(pos*12-5), 'LEGEND:')
        pos = 1
        for i in self.lgnd:
            pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
            qp.setFont(QtGui.QFont('Bold', 10))
            qp.setPen(pen)
            qp.setBrush(i[1])
            qp.drawText(self.width()-130, 1.5*self.y_marg+(pos*12), i[0])
            qp.drawRect(self.width()-140, 1.5*self.y_marg+(pos*12)-8, 8, 8)
            pos +=1

    def fileSwap(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home')

        f = open(fname, 'r')
        with f:
            #file_IO = File_IO()
            #self.data = file_IO.load_data(fname)
            #self.filename = fname
            self.removeToolBar(self.toolbar)
            self.initUI(fname)
        self.update()
        #self.initUI(fname)

    def gridcount(self):
        res, ok = QtGui.QInputDialog.getText(self, 'Grid resolution',
            'Enter new grid resolution as integer:')

        if ok:
            self.gridDesc = int(res)
        self.update()

    def lblSwap(self):
        resx, ok = QtGui.QInputDialog.getText(self, 'X-Axis Label',
            'Enter new x-axis label:')
        if ok:
            self.data.grapharray.axX = resx

        resy, ok = QtGui.QInputDialog.getText(self, 'Y-Axis Label',
            'Enter new y-axis label:')
        if ok:
            self.data.grapharray.axY = resy
        self.update()

    def menuBar(self):
        '''
        Basic stuff that a app needs
        1. File loading
        2. Image saving
        3. Show legend
        4. Grid on/off
        4. Exit
        :return:
        '''
        #FILEACTION
        fileAction = QtGui.QAction('&File', self)
        fileAction.setShortcut('Ctrl+F')
        fileAction.triggered.connect(self.fileSwap)

        #SAVE
        saveAction = QtGui.QAction('&Save Graph', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveIMG)

        #GRID
        gridAction = QtGui.QAction('&Grid', self)
        gridAction.setShortcut('Ctrl+G')
        gridAction.triggered.connect(self.gridIO)

        #GRID_RESO
        gridResAction = QtGui.QAction('&Grid-res', self)
        gridResAction.setShortcut('Ctrl+G')
        gridResAction.triggered.connect(self.gridcount)

        #LEGEND
        legAction = QtGui.QAction('&Legend', self)
        legAction.setShortcut('Ctrl+K')
        legAction.triggered.connect(self.legIO)

        #LABELS
        lblAction = QtGui.QAction('&Labels', self)
        lblAction.setShortcut('Ctrl+L')
        lblAction.triggered.connect(self.lblSwap)

        #EXIT
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        #CREATING TOOLBAR

        self.toolbar = self.addToolBar('MainToolbar')
        '''
        Adding actions to toolbar
        '''
        self.toolbar.addAction(fileAction)
        self.toolbar.addAction(saveAction)
        if self.data.type != "#pie":
            self.toolbar.addAction(gridAction)
            self.toolbar.addAction(gridResAction)
            self.toolbar.addAction(legAction)
            self.toolbar.addAction(lblAction)
        self.toolbar.addAction(exitAction)




