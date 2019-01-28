#!/usr/bin/python
# -*- coding: UTF-8 -*- 

from string import Template

class stringAnalysis(object):

    def __init__(self):
        self.status_ = ''
        self.enums_ = {\
                "moudle": 1, \
                "cmake_minimum_required": 2, \
                "project": 3, \
                "CMAKE_BUILD_TYPE": 4,\
                "CMAKE_CXX_FLAGS": 5, \
                "CMAKE_BUILD_BITS" : 6, \
                "CMAKE_CXX_COMPILER":7,\
                "CMAKE_CXX_FLAGS_DEBUG" : 8, \
                "CMAKE_CXX_FLAGS_RELEASE": 9,\
                "EXECUTABLE_OUTPUT_PATH": 10,\
                "LIBRARY_OUTPUT_PATH": 11,\
                "aux_source_directory": 12,\
                }
        self.istream = open("./CMakeLists.txt",'w') 
        self.analysislist = {}
        self.proname_ = ""
        self.renums_ =  {}
        for status in self.enums_ :
            self.renums_[self.enums_[status]] = status
        self.statustofunction_ ={\
                1: self.moudleProcess,\
                2: self.__s2,\
                3: self.__s3,\
                4: self.__s4,\
                5: self.__s5,\
                6: self.__s6,\
                7: self.__s7,\
                8: self.__s8,\
                9: self.__s9,\
                10: self.__s10,\
                11: self.__s11,\
                12: self.__s12,\
                }
    def preProcess(self):
        with open("./compile.txt","r") as f:
            prelist = {}
            for rl in self.stringPreProcess(f.read()):
                if rl == "":
                    continue
                if rl not in self.enums_ and self.status_ == "":
                    print("stringAnalysis fault")
                    break
                if rl in self.enums_ :
                    prelist[rl] = []
                    self.status_ = rl
                    continue
                prelist[self.status_].append(rl)
        self.status_ = ""
        self.cmakeConstruct(prelist)
                
    def stringPreProcess(self, stri):
        return stri.rstrip(" ").split()
    
    def cmakeConstruct(self, premap):
        for value in range(2, 13):
            self.statustofunction_[value](premap[self.renums_[value]])

    def moudleProcess(self):
       pList = self.istream.split('\n')
       for value in pList :
           if self.assertStatus(value):
               self.analysislist[value] = []
               continue
           if self.status_ == '':
               print(" Analysis fault\nPlease write on requestion")
               return
           self.analysislist[self.status_].append(value)

    def assertStatus(self, assertvar):
        if assertvar in self.enums_ :
            self.status_ = assertvar
            return True 
        return False 

    def makedocGenerate(self):
        with open("./CMakeLists.txt","a+") as f :
            f.write("\n# moudle find and assert\n")
            for key in self.analysislist :
                value = self.analysislist[key]
                f.write(self.packImport(value))

    def packImport(self, strlist):
        res =''
        for libstr in strlist:
            temp = Template("""
find_package(${str_})

if(${STR}_FOUND)
    include_directories(${${STR}_INCLUDE_DIR})
    target_link_libraries(${g} ${${STR}_LIBRARY})
    message(STATUS "found ${STR}")
endif(${STR}_FOUND)

            """)
            print(libstr)
            res += temp.safe_substitute(str_=libstr, STR =libstr, g ="muduo")

        return res;

    def __s2(self, value):
        wo = Template("""
cmake_minimum_required(VERSION ${s1_})
                """)
        rs = wo.safe_substitute(s1_ = value[0])
        self.istream.write(rs)

    def __s3(self,value ):
        wo = Template("""
project(${s1_} C CXX)
            """)
        self.proname_ = value[0]
        rs = wo.safe_substitute(s1_ = value[0])
        self.istream.write(rs)

    def __s4(self, value):
        wo = Template("""
# You can respecify how to compile.
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "${s1_}")
endif()

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "Release"))
        self.istream.write(rs)

    def __s5(self, valuearry):
    	head = "set(CXX_FLAGS\n"
    	taril =""
    	for item in valuearry :
    		taril = taril + " "+ item + "\n"
    	rs = head + taril + ")"
    	self.istream.write(rs)

    def __s6(self, value):
    	rs = """
# You can respecify how to compile.
if(CMAKE_BUILD_BITS EQUAL 32)
  list(APPEND CXX_FLAGS "-m32")
endif()

string(REPLACE ";" " " CMAKE_CXX_FLAGS "${CXX_FLAGS}")
"""
        self.istream.write(rs)

    def __s7(self, value):
        wo = Template("""
# g++ is default compiler, if not define the var 
set(CMAKE_CXX_COMPILER "${s1_}")

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "g++"))
        self.istream.write(rs)

    def __s8(self, value):
        wo = Template("""
# "-O0" is default debug, if not define the var 
set(CMAKE_CXX_FLAGS_DEBUG "${s1_}")

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "-O0"))
        self.istream.write(rs)
    def __s9(self, value):
        wo = Template("""
# "-O0" is default release, if not define the var 
set(CMAKE_CXX_FLAGS_RELEASE "${s1_}")

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "-O2 -finline-limit=1000 -DNDEBUG"))
        self.istream.write(rs)

    def __s10(self, value):
        wo = Template("""
# "-O0" is default release, if not define the var 
set(EXECUTABLE_OUTPUT_PATH "${s1_}")

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "${PROJECT_BINARY_DIR}/bin"))
        self.istream.write(rs)
    def __s11(self, value):
        wo = Template("""
# "-O0" is default release, if not define the var 
set(LIBRARY_OUTPUT_PATH "${s1_}")

""")
        rs = wo.safe_substitute(s1_ = self.__sampleReplace(value, "${PROJECT_BINARY_DIR}/lib"))
        self.istream.write(rs)
    def __s12(self, value):
        rs = ""
        gen = []
        for index in range(len(value)):
            print(index)
            wo = Template("""
aux_source_directory(${s1_} ${s2_}_SRCS)

""")
            gen.append(str(index) + "_SRCS")
            rs+=wo.safe_substitute(s1_ = value[index], s2_ = str(index))
        self.istream.write(rs)
        o =""
        for x in gen:
            e = Template("""  ${${_s1}}""")
            o += e.safe_substitute(_s1 = x)
        rs = "add_executable(" + self.proname_ + o + ")"
        self.istream.write(rs)

    def __sampleReplace(self, assertvaluearry, replace) :
        if not assertvaluearry :
            sub = replace
        else:
            sub = assertvaluearry[0]
        return sub

with open("./moudle.t","r") as f:
    mm = stringAnalysis()
    mm.preProcess()

