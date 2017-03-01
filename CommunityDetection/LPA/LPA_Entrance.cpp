#include <iostream>
#include <fstream>
#include "networks.h"
#include "edge_list_parser.h"
#include "Label_Propagation.h"

using namespace std;


network<std::string,double> createLayer(std::map<int, vector<string> > edge_file, std::string name){
    network<std::string,double> network;
    network.setName(name);
    set<string> node_list_tmp;
    for (auto iter : edge_file){
        vector<string> edge = iter.second;
        string src = edge[0];
        string dst = edge[1];
        node_list_tmp.insert(src);
        node_list_tmp.insert(dst);
        // 构建网络的边
        network.add_edge(src, dst, 1.0, false);
    }

    // 将set 转换成 vector
    std::vector<std::string> node_list;
    for (auto node:node_list_tmp){
        if (node_list_tmp.find(node)!= node_list_tmp.end()){
            node_list.push_back(node);
        }
    }

    // 构建 网络 的点
    network.add_nodes_from(node_list);

    return  network;
};

void showCommunities(std::vector<std::set<std::string> > community){
    std::cout << "\n ------ ------ ------ ------ ------\n";
    std::cout << "\nCommunity Output:\n";

    for (int i = 0; i < community.size(); ++i) {
        std::set<std::string> currentCom = community[i];
        std::cout << "com_"<< i << ":\t";
        for (std::string node : currentCom){std::cout << node << " ";}
        std::cout << std::endl;
    }
}

int main(int argc, char *argv[]){

    if (argc < 1 | argc > 2){
        cout << "Usage: edge.list [-w]"
                "\n\tedge.list ---> Edge_List File"
                "\n\t-w ---> optional: weight flag" << endl;
        exit(EXIT_FAILURE);
    }
    else {
        // 获取需要读入的文件名
        string filename = argv[1];
        // 指定当前读入的网络是否有权重
        bool weightedFlag = false;
        if (argv[2] == "-w") {
            weightedFlag = true;
        }
        cout << "\nprocessing file: " << filename << "\tweighted: " << weightedFlag << endl;

        /// 1. 生成edge文件
        std::map<int, vector<string> > edge_file = edge_list_parser(filename,filename);
        /// 2. 构成网络
        network<std::string,double> layer = createLayer(edge_file, filename);
        /// 3. 调用LPA算法
        LPA<std::string,double> lpa1(layer, weightedFlag);
        std::vector<std::set<std::string> > communities = lpa1.community();
        /// 4. 输出社团结果
        showCommunities(communities);
        // 5.  输出社团结果于文件中
        string output_filename = filename+".com";
        ofstream fout(output_filename);
        for (int i=0; i<communities.size(); i++){
            for (auto node: communities[i]){
                fout << node << " ";
            }
            fout << "\n";
        }
        fout.close();
    }

    return 0;



}
