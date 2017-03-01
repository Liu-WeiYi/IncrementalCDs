//
// Created by weiyiliu on 1/17/17.
//

#ifndef INCREMENTALMUTIPLEXDEMON_EDGE_LIST_PARSER_H
#define INCREMENTALMUTIPLEXDEMON_EDGE_LIST_PARSER_H

#include <string> // 用来存储名称
#include <vector> // 用来存储当前行中的所有字段
#include <map>
using namespace std;

map<int, vector<string>>
edge_list_parser(string filename, string network_name="");




#endif //INCREMENTALMUTIPLEXDEMON_EDGE_LIST_PARSER_H
