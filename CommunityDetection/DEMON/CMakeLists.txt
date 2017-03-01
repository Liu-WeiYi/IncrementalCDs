cmake_minimum_required(VERSION 3.6)
project(DEMON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES networks.tpp networks.h Label_Propagation.tpp Label_Propagation.h edge_list_parser.h edge_list_parser.cpp DEMON_Entrance.cpp)
add_executable(DEMON ${SOURCE_FILES} Label_Propagation.tpp DEMON_Entrance.cpp)