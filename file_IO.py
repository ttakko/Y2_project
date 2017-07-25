#from main import Graph_data, Graph_Set

class ReadError(Exception):
    def __init__(self, arg):
        self.msg = arg
class File_IO(object):
    '''
    The class that read the file and
    '''

    def load_data(self, input):
        '''
        loads data from file
        :param input:
        :return:
        '''
        self.dataset = Graph_Set() #new datalist which contains datasets
        self.graph = Graph()

        try:
            input = open(input, 'r') #reads the file
            read_data = input.readline() #reads the first row
            #Determines and sets dataset type
            read_data = read_data.strip('\n')
            read_parts = read_data.split(':')
            if read_parts[0] == "#line":
                self.dataset.set_type("#line")
            elif read_parts[0] == "#pie":
                self.dataset.set_type("#pie")
            elif read_parts[0] == "#column":
                self.dataset.set_type("#column")
            while read_data != "":
                '''
                determines which type of chart needs to be created
                :functions struct_pie, column, line:
                '''
                current = input.tell()
                if read_parts[0] == "#line":
                    new_data = self.struct_line(input, read_parts[1])
                    self.dataset.add_graph(new_data)
                elif read_parts[0] == "#pie":
                    new_data = self.struct_pie(input, read_parts[1])
                    self.dataset.add_graph(new_data)
                    self.graph.add_set(self.dataset)
                    return self.graph
                elif read_parts[0] == "#column":
                    new_data = self.struct_column(input, read_parts[1])
                    self.dataset.add_graph(new_data)
                    self.graph.add_set(self.dataset)
                    return self.graph
                input.seek(current)
                read_data = input.readline()
                read_data=read_data.strip('\n')
                read_parts = read_data.split(':')
        except:
            raise ReadError("Corrupted of bad file!")

        self.graph.add_set(self.dataset)
        return self.graph



    def struct_line(self, input, name):
        '''
        Structs a linechart graph_data
        :param input:
        :return:
        '''
        data = Graph_data()
        data.name = name
        read_data = input.readline()
        while read_data != "":
            try:
                read_data = read_data.strip('\n')
                if read_data[:2] == '##':
                    read_data = read_data.strip('#')
                    read_data = read_data.split(":")
                    self.dataset.axX = read_data[0]
                    self.dataset.axY = read_data[1]
                    read_data = input.readline()

                read_data = read_data.split(":")
                if read_data[0] == "#line":
                    data.sort_data()
                    return data
                if len(read_data) == 2:
                    x = read_data[0]
                    y = read_data[1]
                    if self.is_number(x) == True and self.is_number(y) == True:
                        data.set_point(x,y)
                read_data = input.readline()
            except:
                raise ReadError("Not working ")

        data.sort_data()

        return data

    def struct_pie(self, input, name):
        '''
        Structs a piechart graph_data
        :param input:
        :return:
        '''
        data = Graph_data()
        data.name = name
        read_data = input.readline()

        while read_data != "":
            read_data = read_data.strip('\n')
            read_data = read_data.split(":")
            if read_data[0] == "#pie":
                print("uusi graafi")
                return data

            '''
            Tahan testi mika testaa etta molemmat numeerisia
            '''
            x = read_data[0]
            y = read_data[1]
            self.is_number(y)
            data.set_point(x,y)
            read_data = input.readline()

        return data

    def struct_column(self, input, name):
        '''
        Structs a columnchart graph_data
        :param input:
        :return:
        '''
        data = Graph_data()
        data.name = name
        read_data = input.readline()
        while read_data != "":
            read_data = read_data.strip('\n')
            if read_data[:2] == '##':
                read_data = read_data.strip('#')
                read_data = read_data.split(":")
                self.dataset.axX = read_data[0]
                self.dataset.axY = read_data[1]
                read_data = input.readline()
            read_data = read_data.split(":")
            if read_data[0] == "#column":
                return data

            '''
            Tahan testi mika testaa etta molemmat numeerisia
            '''
            x = read_data[0]
            y = read_data[1]
            if self.is_number(y) == True:
                data.set_point(x,y)
            read_data = input.readline()

        return data

    def is_number(self,s):
        '''
        tests if the given string is a float number
        :param self:
        :param s:
        :return:
        '''
        try:
            float(s)
            return True
        except ValueError:
            raise ReadError("Wrong kind of data!")
            return False

class Graph(object):
    '''
    Initiates new graph
    '''
    def __init__(self):
        '''
        Initiates a new graph

        '''
        self.grapharray = []
        self.type = "Unknown"
        return

    def get_array(self, i):
        '''
        Returns a array from graphs dataset array
        :return:
        '''
        return self.grapharray[i]
    def get_type(self):
        '''
        returns graphs type
        :return:
        '''
        return self.type
    def add_set(self, set):
        '''

        adds a new dataset
        :return:
        '''
        self.grapharray = set
        self.type = set.type
        return

class Graph_Set(object):
    '''
    Set of all graphs
    Subclass of Graph
    '''
    def __init__(self):
        '''
        initialises new set
        :return:
        '''
        self.graphlist = []
        self.type = "Unknown"
        self.axX = "X"
        self.axY = "Y"
        return
    def add_graph(self, graph):
        '''
        adds new graph into array
        :return:
        '''
        self.graphlist.append(graph)
        return
    def set_type(self, type):
        '''
        Sets graph type
        :return:
        '''
        print("type set to %s" %type)
        self.type = type
        return

class Graph_data(object):
    '''
    Collection of data points
    Subclass of dataset

    '''
    def __init__(self):
        '''
        initialises new data collection
        :return:
        '''
        self.pointarray = []
        self.name = 'Unknown'
        return

    def set_point(self, x, y):
        '''
        Sets a new point object to Graphs point array

        '''
        point = Point()
        point.set_x(x)
        point.set_y(y)
        self.pointarray.append(point)
        return
    def sort_data(self):
        '''
        sorts the data by x axis
        :return:
        '''
        self.pointarray = sorted(self.pointarray, key=Point.get_x, reverse=False)
        return

    def get_data(self):
        '''
        Returns the data array
        :return:
        '''
        return self.pointarray

class Point(object):
    '''
    One datapoint either two float values or one string and one float
    '''
    def __init__(self):
        '''
        Initiates a new datapoint
        :return:
        '''
        self.x = 0
        self.y = 0
    def set_x(self, x):
        '''
        sets a x value for current point
        :return:
        '''
        self.x = x
        return
    def get_x(self):
        '''
        gets a x value for current point
        :return:
        '''
        return float(self.x)
    def set_y(self, y):
        '''
        sets a y value for current point
        :return:
        '''
        self.y = y
        return
    def set_label(self, lbl):
        '''
        if graph is column or pie chart, sets a label for certain y  value
        :return:
        '''
        self.x = lbl
        return