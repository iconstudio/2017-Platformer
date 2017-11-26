
#include <stdio.h>
#include <tchar.h>
#include <cstdlib>

#include <iostream>
#include <random>
#include <vector>
#include <queue>
#include <set>

using namespace std;

class point {
private:
	vector<point*> adjacent;

public:
	int myIndex;
	bool visited = false;

	point(int arg = 0)
		: myIndex(arg) {
	}

	void add_adjacent(point *arg) {
		adjacent.push_back(arg);
}

	auto &get_adjacent() {
		return adjacent;
	}
};

class graph {
public:
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
		for (auto pt : ptlist) {
			cout << "Point <" << pt->myIndex << "> ";
			if (pt->visited)
				cout << "[T]: ";
			else
				cout << "[F]: ";
			for (auto adjp : pt->get_adjacent()) {
				cout << adjp->myIndex << ", ";
			}
			cout << endl;
		}
	}
};

// Depth first search
point *func_dfsatomic(point *arg, int value) {
	arg->visited = true;

	auto &pvec = arg->get_adjacent();
	for (auto pt : pvec) {
		if (pt->myIndex == value)
			return pt;
		if (!pt->visited)
			func_dfsatomic(pt, value);
	}
	return nullptr;
}

void func_dfs(graph arg, int value) {
	auto ptlist = arg.ptlist;
	for (auto &pt : ptlist)
		pt->visited = false;

	for (auto pt : ptlist) {
		if (!pt->visited)
			func_dfsatomic(pt, value);
	}
}

// Breadth first search
point *func_bfs(graph arg, int start) {
	auto ptlist = arg.ptlist;
	queue<point*> Q;

	for (auto &pt : ptlist)
		pt->visited = false;
	ptlist[start]->visited = true;
	Q.push(ptlist[start]);

	while (!Q.empty()) {
		auto current = Q.front();
		Q.pop();
		auto adjlist = current->get_adjacent();
		for (auto &pt : adjlist) {
			if (!pt->visited) {
				pt->visited = true;
				Q.push(pt);
			}
		}
	}
	return nullptr;
}

int main() {
	uniform_int_distribution<int> vdistr(0, 9);
	uniform_int_distribution<int> cdistr(0, 3);
	default_random_engine engine;

	// 그래프 생성
	graph test;
	auto a = test.add_point(0);
	auto b = test.add_point(1);
	auto c = test.add_point(2);
	auto d = test.add_point(3);
	auto e = test.add_point(4);
	auto f = test.add_point(5);
	auto g = test.add_point(6);
	auto h = test.add_point(7);
	auto i = test.add_point(8);

	// 방향 그래프로 구현을 했으나 이 경우는
	// 무방향 그래프이기 때문에 모든 인접 점에 두번씩 서로 추가.
	a->add_adjacent(b);
	a->add_adjacent(c);
	a->add_adjacent(f);
	a->add_adjacent(i);

	b->add_adjacent(a);
	b->add_adjacent(c);
	b->add_adjacent(d);
	b->add_adjacent(f);
	b->add_adjacent(g);
	b->add_adjacent(h);

	c->add_adjacent(a);
	c->add_adjacent(b);
	c->add_adjacent(d);
	c->add_adjacent(e);
	c->add_adjacent(f);

	d->add_adjacent(b);
	d->add_adjacent(c);

	e->add_adjacent(c);
	e->add_adjacent(f);
	e->add_adjacent(g);

	f->add_adjacent(a);
	f->add_adjacent(b);
	f->add_adjacent(c);
	f->add_adjacent(e);
	f->add_adjacent(h);
	f->add_adjacent(i);

	g->add_adjacent(b);
	g->add_adjacent(e);
	g->add_adjacent(i);

	h->add_adjacent(b);
	h->add_adjacent(f);

	i->add_adjacent(a);
	i->add_adjacent(f);
	i->add_adjacent(g);

	test.print();
	
	// 세번째 (0 1 2 ...) 점에서부터 탐색 시작
	func_bfs(test, 2);

	cout << "==========================================" << endl;

	test.print();

	return 0;
}

