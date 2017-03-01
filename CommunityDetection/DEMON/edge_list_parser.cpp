//
// Created by weiyiliu on 1/17/17.
//

#include "edge_list_parser.h"
#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;

/**
 * @brief 读取edge_list文件
 * @param filename  --- 读取文件的文件名
 * @param name      --- 指定返回网络的名称, 默认不指定, 为""
 * @return
 */
map<int, vector<string>> edge_list_parser(string filename, string network_name){

    map<int, vector<string>> edge_file;

    ifstream inFile;
    inFile.open(filename);
    // 首先判断 文件是否能够打开。。。不能直接退出！
    if (!inFile.is_open()){
        cout << "Could NOT open the file: " << filename << endl;
        cout << "Program terminating...\n";
        exit(EXIT_FAILURE);
    }
    else{
        cout << "load file: " << filename << "...";
    }
    // 读文件操作开始
    int lineNumber = 0;
    while (inFile.good()){
        ++lineNumber;
        string src,dst;
        inFile >> src;
        inFile >> dst;

        edge_file[lineNumber].push_back(src);
        edge_file[lineNumber].push_back(dst);

//        cout << src << "\t" << dst << endl;
    }
    cout << "down" << "\tcurrent Edges number: " << lineNumber << endl;
    inFile.close();

    return edge_file;
}


