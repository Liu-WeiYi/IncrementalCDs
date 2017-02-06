cmake_minimum_required(VERSION 3.6)
project(Louvain)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES Louvain_Entrance.cpp Graph.cpp GraphReader.cpp Louvain.cpp)
add_executable(Louvain ${SOURCE_FILES})