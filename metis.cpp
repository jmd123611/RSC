#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "metis.h"
#include "time.h"
using namespace std;

string name1 = "C:\\dev\\nump15\\skat";
string name2 = ".txt";
string name3 = "C:\\dev\\nump15\\skat_partition";

vector<idx_t> func(vector<idx_t> xadj, vector<idx_t> adjncy, vector<idx_t> vwgt) {
	idx_t nVertices = xadj.size() - 1; // 节点数
	idx_t nEdges = adjncy.size() / 2;    // 边数
	idx_t nWeights = 1;
	idx_t nParts =7;    // 子图个数
	idx_t objval;
	
	std::vector<idx_t> part(nVertices, 0);

	int ret = METIS_PartGraphRecursive(&nVertices, &nWeights, xadj.data(), adjncy.data(),
		vwgt.data(), NULL, NULL, &nParts, NULL,
		NULL, NULL, &objval, part.data());

	//std::cout << ret << std::endl;

	for (unsigned part_i = 0; part_i < part.size(); part_i++) {
		std::cout << part_i << " " << part[part_i] << std::endl;
	}
	return part;
}


int main() {
	for (int ite = 1; ite < 11; ite++) {
		string k = to_string(ite);
		string name = name1 + k + name2;
		cout << name << endl;
		ifstream ingraph(name);
		if (!ingraph) {
			cout << "x打开文件失败！" << endl;
			exit(1);//失败退回操作系统    
		}
		clock_t start_time, end_time;
		start_time = clock();
		int vexnum, edgenum;

		string line;
		getline(ingraph, line);
		istringstream tmp(line);

		tmp >> vexnum >> edgenum;
		vector<idx_t> xadj(0);
		vector<idx_t> adjncy(0); //点的id从0开始
		vector<idx_t> vwgt(0);

		idx_t a, w;
		for (int i = 0; i < vexnum; i++) {
			xadj.push_back(adjncy.size());
			getline(ingraph, line);
			istringstream tmp(line);
			while (tmp >> a >> w) {
				adjncy.push_back(a);
				vwgt.push_back(w);
			}
		}
		xadj.push_back(adjncy.size());
		
		ingraph.close();
		vector<idx_t> part = func(xadj, adjncy, vwgt);
		string nam = name3 + k + name2;
		ofstream outpartition(nam);
		if (!outpartition) {
			cout << "打开文件失败！" << endl;
			exit(1);
		}
		
		for (int i = 0; i < part.size(); i++) {
			outpartition << i << " " << part[i] << endl;
		}
		outpartition.close();
		end_time = clock();     //获取结束时间
		double Times = (double)(end_time - start_time) / CLOCKS_PER_SEC;
		printf("%f seconds\n", Times);
	}
}