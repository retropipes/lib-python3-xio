'''
Created on Feb 8, 2015

@author: ericahnell
'''

XML_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
XML_DOUBLE_TAG = "double"
XML_INT_TAG = "integer"
XML_LONG_TAG = "long"
XML_BYTE_TAG = "byte"
XML_BOOLEAN_TAG = "boolean"
XML_STRING_TAG = "string"
XML_OPENING_TAG_START = "<"
XML_CLOSING_TAG_START = "</"
XML_TAG_END = ">"
NEW_LINE = "\n"

class XDataReader(object):
    '''
    classdocs
    '''

    def __init__(self, xfile, xdoctype):
        '''
        Constructor
        '''
        self.file = xfile
        self.doctype = xdoctype
        
    def __enter__(self):
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
        
    def close(self):
        self.file.close()
        
    def read_double(self):
        pass
    
    def read_byte(self):
        pass
    
    def read_int(self):
        pass
    
    def read_long(self):
        pass
    
    def read_boolean(self):
        pass
    
    def read_string(self):
        pass

class XDataWriter(object):
    '''
    classdocs
    '''

    def __init__(self, xfile, xdoctype):
        '''
        Constructor
        '''
        self.file = xfile
        self.doctype = xdoctype
        
    def __enter__(self):
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
        
    def close(self):
        self.file.close()
        
    def write_double(self, value):
        pass
    
    def write_byte(self, value):
        pass
    
    def write_int(self, value):
        pass
    
    def write_long(self, value):
        pass
    
    def write_boolean(self, value):
        pass
    
    def write_string(self, value):
        pass
    
class XMLDataReader(XDataReader):
    '''
    classdocs
    '''

    def __init__(self, xfile, xdoctype):
        '''
        Constructor
        '''
        XDataReader.__init__(self, xfile, xdoctype)
        self.__read_header()
        
    def close(self):
        self.__read_footer()
        self.file.close()
        
    def read_double(self):
        line = self.file.readline()
        return float(self.__split_line(line, XML_DOUBLE_TAG))
    
    def read_byte(self):
        line = self.file.readline()
        return int(self.__split_line(line, XML_BYTE_TAG))
    
    def read_int(self):
        line = self.file.readline()
        return int(self.__split_line(line, XML_INT_TAG))
    
    def read_long(self):
        line = self.file.readline()
        return int(self.__split_line(line, XML_LONG_TAG))
    
    def read_boolean(self):
        line = self.file.readline()
        value = self.__split_line(line, XML_BOOLEAN_TAG)
        return value == "true"
    
    def read_string(self):
        line = self.file.readline()
        return self.__split_line(line, XML_STRING_TAG)
    
    def __split_line(self, line, tag):
        pos1 = len(XML_OPENING_TAG_START + tag + XML_TAG_END) + 1
        pos2 = line.find(XML_CLOSING_TAG_START + tag + XML_TAG_END)
        if pos2 == -1:
            raise UnexpectedTagError("Tag does not match: expected open/close " + tag + ", found " + line + "!")
        return line[pos1:pos2]
    
    def __read_header(self):
        fileheader = self.file.readline()
        filedoctype = self.file.readline()
        if fileheader != XML_HEADER:
            raise UnexpectedTagError("Corrupt or invalid header!")
        if filedoctype != XML_OPENING_TAG_START + self.doctype + XML_TAG_END:
            raise UnexpectedTagError("Opening doc tag does not match: expected " + self.doctype + ", found " + filedoctype + "!")
        
    def __read_footer(self):
        filefooter = self.file.readline()
        if filefooter != XML_CLOSING_TAG_START + self.doctype + XML_TAG_END:
            raise UnexpectedTagError("Closing doc tag does not match: expected " + self.doctype + ", found " + filefooter + "!")

class XMLDataWriter(XDataWriter):
    '''
    classdocs
    '''

    def __init__(self, xfile, xdoctype):
        '''
        Constructor
        '''
        XDataWriter.__init__(self, xfile, xdoctype)
        self.__write_header()
        
    def close(self):
        self.__write_footer()
        self.file.close()
        
    def write_double(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_DOUBLE_TAG + XML_TAG_END + value + XML_CLOSING_TAG_START + XML_DOUBLE_TAG + XML_TAG_END + NEW_LINE)
    
    def write_byte(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_BYTE_TAG + XML_TAG_END + value + XML_CLOSING_TAG_START + XML_BYTE_TAG + XML_TAG_END + NEW_LINE)
    
    def write_int(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_INT_TAG + XML_TAG_END + value + XML_CLOSING_TAG_START + XML_INT_TAG + XML_TAG_END + NEW_LINE)
    
    def write_long(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_LONG_TAG + XML_TAG_END + value + XML_CLOSING_TAG_START + XML_LONG_TAG + XML_TAG_END + NEW_LINE)
    
    def write_boolean(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_BOOLEAN_TAG + XML_TAG_END + str(value).lower() + XML_CLOSING_TAG_START + XML_BOOLEAN_TAG + XML_TAG_END + NEW_LINE)
    
    def write_string(self, value):
        self.file.write(XML_OPENING_TAG_START + XML_STRING_TAG + XML_TAG_END + value + XML_CLOSING_TAG_START + XML_STRING_TAG + XML_TAG_END + NEW_LINE)
    
    def __write_header(self):
        self.file.write(XML_HEADER + NEW_LINE)
        self.file.write(XML_OPENING_TAG_START + self.doctype + XML_TAG_END + NEW_LINE)
    
    def __write_footer(self):
        self.file.write(XML_CLOSING_TAG_START + self.doctype + XML_TAG_END + NEW_LINE)
        
class UnexpectedTagError(IOError):
    pass