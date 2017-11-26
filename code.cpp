
#include <stdio.h>
#include <cstdlib.h>
#include <memory.h>

#include <iostream>
#include <vector>
#include <queue>
#include <set>
using namespace std;

class point {
private:
	vector<point*> adjacent;

public:
	int value;
	bool visited = false;
	
	point(int arg = 0)
		: value(arg) {
	}
	
	void add_adjacent(point *arg) {
		adjacent.push_back(arg);
	}
	
	auto &get_adjacent() {
		return adjacent;
	}
};

class graph {
	vector<point*> ptlist;

	point *add_point(int value) {
		auto newone = new point(value);
		ptlist.push_back(newone);
		return newone;
	}
	
	point *add_point(point *arg) {
		ptlist.push_back(arg);
		return arg;
	}
	
	point *operator[](size_t index) {
		return ptlist[index];
	}

	void print() {
		for (auto pt : plist) {
			cout << "Point <" << pt << "> - ";
			for (auto adjp : pt->get_adjacent()) {
				cout << adjp->value << "'" << endl;
			}
		}
	}
};

// Depth first search
void func_dfsatomic(point *arg) {
	pt->visited = true;
	
	auto &pvec = pt->get_adjacent();
	for (auto pt : pvec) {
		if (!pt->visited)
			func_dfsatomic(pt);
	}
}

void func_dfs(graph &&arg) {
	auto ptlist = arg.ptlist;
	for (auto pt : ptlist)
		pt->visited = false;

	for (auto pt : ptlist) {
		if (!pt->visited)
			func_dfsatomic(pt);
	}
}

// Breadth first search
void func_bfs(vector<point*> arg) {
	
}

// prim(연결 행렬, 시점);
auto prim(char **matrix, int index) {
	set<int> S, V;
	// 전체 집합
	for (int i = 0; i < 6; ++i) {
		V.push(i);
	}
	
	// 반환용 그래프
	graph _result;
	for (int i = 0; i < 6; ++i) {
		_result.add_point(i)->visited = false;
	}
	
	_result[index]->visited = true;
	S.push(index);
	
	while (S != V) {
		auto diff = V - S; // 현재 집합의 여집합
		
		int temp, min, min_value;
		for (int oindex : S) { // 현재 집합에서 기준 원소 뽑기
			temp = 0;
			min = oindex;
			min_value = 1000;

			for (int nindex : diff) { // 여집합에서 비교 원소 뽑기
				if (matrix[oindex][nindex] < min_value) {
					min_value = matrix[oindex][nindex];
					min = nindex;
				}
			}
			point[nindex]->add_adjacent(_result[nindex]);
			_result[min]->visited = true;
			S.push(min);
		}
	}
	
	return _result;
}

int main() {
	// 연결 관계: 숫자가 0이 아니면 연결된 것임.
	char **matrix = new char*[6];
	for (int i = 0; i < 6; ++i) {
		matrix[i] = new char[6]('0');
	}
	matrix[0][0] = '0';
	matrix[0][1] = '9';
	matrix[0][2] = '7';
	matrix[0][3] = '5';
	matrix[0][5] = '6';
	matrix[1][0] = '9';
	matrix[1][2] = '9';
	matrix[2][0] = '7';
	matrix[2][1] = '8';
	matrix[2][4] = '5';
	matrix[3][0] = '5';
	matrix[3][5] = '5';
	matrix[4][2] = '5';
	matrix[4][5] = '1';
	matrix[5][0] = '6';
	matrix[5][3] = '5';
	matrix[5][4] = '1';
	
	// 2 번째 점이 시작점
	auto result = prim(matrix, 1);
	result.print();
	
	return 0;
}
