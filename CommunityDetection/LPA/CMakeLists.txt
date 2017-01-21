cmake_minimum_required(VERSION 3.6)
project(LPA)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    edge_list_parser.h
        edge_list_parser.cpp
    Label_Propagation.h
    Label_Propagation.tpp
    LPA_Entrance.cpp
    networks.h
    networks.tpp)

add_executable(LPA ${SOURCE_FILES})