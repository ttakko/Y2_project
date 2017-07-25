import unittest
import coverage
from file_IO import *
from io import StringIO

class Test(unittest.TestCase):
    '''
    Tests for different methods in file reading and data constructing
    '''
    def setUp(self):
        self.file_io = File_IO()


    def test_line(self):
        #Tests a normal linegraph
        data = self.file_io.load_data('testiline.txt')
        self.assertEqual("#line", data.get_type(), "First Graph type is wrong!")
        self.assertEqual("#line", data.get_type(), "Second Graph type is wrong!")
        self.assertEqual("hinta", data.grapharray.axX, "X-axis name is wrong!")
        self.assertEqual("voima", data.grapharray.axY, "Y-axis name is wrong!")
        self.assertEqual('11', data.grapharray.graphlist[0].pointarray[1].x, "Point not found!")
        self.assertEqual('toka', data.grapharray.graphlist[1].name, "Wrong name!")

    def test_pie(self):
        #Tests a normal piegraph
        data = self.file_io.load_data('testipie.txt')
        self.assertEqual("#pie", data.get_type(), "First Graph type is wrong!")
        self.assertEqual("testi", data.grapharray.graphlist[0].name, "Piechart name is wrong!")
        self.assertEqual('30', data.grapharray.graphlist[0].pointarray[1].y, "Point not found!")
        self.assertEqual('toka', data.grapharray.graphlist[0].pointarray[1].x, "Wrong name!")

    def test_column(self):
        #Tests a normal columngraph
        data = self.file_io.load_data('testicolumn.txt')
        self.assertEqual("#column", data.get_type(), "First Graph type is wrong!")
        self.assertEqual("testi", data.grapharray.graphlist[0].name, "Piechart name is wrong!")
        self.assertEqual(30, int(data.grapharray.graphlist[0].pointarray[1].y), "Point not found!")
        self.assertEqual('toka', data.grapharray.graphlist[0].pointarray[1].x, "Wrong name!")

    def test_sortbadlinechart(self):
        #Tests a linechart that has x-values in wrong order
        data = self.file_io.load_data('testbadline.txt')
        self.assertEqual("#line", data.get_type(), "First Graph type is wrong!")
        self.assertEqual("eka", data.grapharray.graphlist[0].name, "Piechart name is wrong!")
        self.assertEqual(30, int(data.grapharray.graphlist[0].pointarray[1].y), "Point not found!")
        self.assertEqual('11', data.grapharray.graphlist[0].pointarray[1].x, "Wrong name!")

    def test_badvalueslinechart(self):
        #Tests a normal columngraph, tests that fileIO raises correct errors
        try:
            data = self.file_io.load_data('testbadlinevalues.txt')
        except ReadError:
            pass



