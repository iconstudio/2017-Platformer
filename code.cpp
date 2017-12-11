// CodeStudy.cpp: 콘솔 응용 프로그램의 진입점을 정의합니다.
//

#include "stdafx.h"


#include <stdio.h>
#include <tchar.h>
#include <cstdlib>

#include <iostream>
#include <random>
#include <vector>
#include <queue>
#include <set>

using namespace std;

static const int nsize = 5;
static bool *visited = new bool[5]{ false, false, false, false, false };
static const auto V = initializer_list<int>{ 0, 1, 2, 3, 4 };

int graph[nsize][nsize] = {
	{ 0, 0, 0, 0, 0 },
	{ 0, 0, 0, 0, 0 },
	{ 0, 0, 0, 0, 0 },
	{ 0, 0, 0, 0, 0 },
	{ 0, 0, 0, 0, 0 }
};

// 인접 리스트
initializer_list<int> adjList(int vertex) {

}

// 깊이 우선 탐색
void DFS() {
	for (const auto vertex : V)
		visited[vertex] = false;

	for (const auto vertex : V)
		if (!visited[vertex])
			aDFS(vertex);
}

void aDFS(int vertex) {
	visited[vertex] = true;
	for (const auto x : adjList(vertex)) { // L(v) : 정점 v의 인접 리스트
		if (!visited[x])
			aDFS(x);
	}
}

// 너비 우선 탐색
auto BFS(int vertex) {
	queue<int> Q;
	for (const auto v : V)
		visited[v] = false;

	visited[vertex] = true;
	Q.push(vertex);
	while (!Q.empty()) {
		int u = Q.front();
		Q.pop();
		for (const auto v : adjList(u)) {
			if (!visited[v]) {
				visited[u] = true;
				Q.push(v);
			}
		}
	}

	return Q;
}

set<int> Prim(int r) {
	set<int> S, Vset(V);

	// 정점 r을 방문되었다고 표시하고, 집합 S에 포함시킨다;
	while (S != Vset) {
		// S에서 V - S를 연결하는 간선들 중 최소길이의 간선(x, y) 를 찾는다; // (x∈S, y∈V-S)
		// 정점 y를 방문되었다고 표시하고, 집합 S에 포함시킨다;
	}

	return S;
}

int *Dijkstra(int r)
// G = (V, E): 주어진 그래프 
// r: 시작으로 삼을 정점 
{
	set<int> S, Vset(V);

	// 간선 길이
	int *distance = new int[nsize];
	for (const auto u : V) {
		distance[u] = INT_MAX;
	}

	distance[r] = 0;
	while (S != Vset) { // n회 순환된다
		int u = extractMin(Vset - S, distance);
		S = S + u;
		for (const auto v : adjList(u)) { // L(u): u로부터 연결된 정점들의 집합
			if (v ∈ Vset - S && distance[v] < distance[u] + graph[u][v])
				distance[v] = distance[u] + graph[u][v];
		}
	}

	return distance;
}


int extractMin(set<int> &&Q, int *distance) {
	// 집합 Q에서 d값이 가장 작은 정점 u를 리턴한다;
}

int *BallmanFord(int s) {
	// 간선 길이
	int *distance = new int[nsize];
	distance[s] = 0;

	for (const auto u : V) {
		if (u != s)
			distance[u] = INT_MAX;
	}

	for (int k = 0; k < nsize - 1; ++k) {
		for (const auto b : V) {
			if (distance[k] + graph[k][b] < distance[b])
				distance[b] = distance[k] + graph[k][b];
		}
	}

	return distance;
}

#define RED 1
#define BLACK 0

struct Node {
	int data, color;
	Node *parent = NULL, *left = NULL, *right = NULL;
};

class xTree {
public:
	Node *root;

	xTree() {
		root = NULL;
	}

	void print(Node *p, int i) {
		if (p != NULL) {
			print(p->left, i + 1);

			cout << "[" << i << "] ";
			if (p->color == RED)
				cout << "RED, ";
			else cout << "BLACK, ";
			cout << p->data << ", ";
			if (p->parent != NULL)
				cout << p->parent->data << endl;
			else
				cout << "NULL" << endl;

			print(p->right, i + 1);
		}
	}

	void insert_case1(Node *p) {
		if (p->parent == NULL)
			p->color = BLACK;
		else
			insert_case2(p);
	}

	void insert_case2(Node *p) {
		if (p->parent->color == BLACK)
			return;
		else
			insert_case3(p);
	}

	void insert_case3(Node *p) {
		Node *u;

		if (p->parent->parent->right == p->parent)
			u = p->parent->parent->left;
		else
			u = p->parent->parent->right;

		if ((u != NULL && u->color == RED) || u == NULL) {
			p->parent->color = BLACK;
			if (u != NULL)
				u->color = BLACK;
			p->parent->parent->color = RED;
			insert_case1(p->parent->parent); //재귀적 호출
		} else
			insert_case4(p);
	}

	void insert_case4(Node *p) //case 2-1
	{
		if (p == p->parent->right) {
			rotate_left(p->parent);
			insert_case5(p);
		} else
			insert_case5(p);
	}

	void insert_case5(Node *p) //case 2-2
	{
		rotate_right(p->parent);
	}

	void rotate_left(Node *p) {
		Node *x = p->right;

		if (x->left != NULL) //1
			x->left->parent = p;

		p->right = x->left; //1
		x->parent = p->parent;
		p->parent = x;
		x->left = p;

		if (x->parent != NULL) //root경우 제외
			if (x->parent->left == p)
				x->parent->left = x;
			else x->parent->right = x;
	}

	void rotate_right(Node *p) {
		Node *x = p->left;

		if (x->right != NULL) //1
			x->right->parent = p;

		p->left = x->right; //1
		x->parent = p->parent;
		p->parent = x;
		x->right = p;

		if (x->parent != NULL) //root경우 제외
			if (x->parent->left == p)
				x->parent->left = x;
			else x->parent->right = x;
	}

	void insert(int data) {
		Node *node = new(Node);
		node->data = data;
		node->color = RED;
		node->left = NULL;
		node->right = NULL;

		if (root == NULL) {
			root = node;
			root->color = BLACK;
			root->parent = NULL;
			return;
		}

		Node *p = root;
		Node *save = NULL;

		while (p != NULL) {
			if (p->data > node->data) {
				if (p->left == NULL)
					save = p;
				p = p->left;
			} else {
				if (p->right == NULL)
					save = p;
				p = p->right;
			}
		}

		p = node;
		p->parent = save;

		if (save->data < p->data)
			save->right = p;
		else
			save->left = p;

		insert_case1(p);
	}
};

class Tree {
public:
	Node *root;

	Tree() {
		root = NULL;
	}

	void print(Node *p, int i) {
		if (p != NULL) {
			print(p->left, i + 1);

			cout << "[" << i << "] ";
			if (p->color == RED)
				cout << "RED, ";
			else cout << "BLACK, ";
			cout << p->data << ", ";
			if (p->parent != NULL)
				cout << p->parent->data << endl;
			else
				cout << "NULL" << endl;

			print(p->right, i + 1);
		}
	}

	void rotate_left(Node *p) {
		Node *x = p->right;

		if (x->left != NULL) //1
			x->left->parent = p;

		p->right = x->left; //1
		x->parent = p->parent;
		p->parent = x;
		x->left = p;

		if (x->parent != NULL) //root경우 제외
			if (x->parent->left == p)
				x->parent->left = x;
			else x->parent->right = x;
	}

	void rotate_right(Node *p) {
		Node *x = p->left;

		if (x->right != NULL) //1
			x->right->parent = p;

		p->left = x->right; //1
		x->parent = p->parent;
		p->parent = x;
		x->right = p;

		if (x->parent != NULL) //root경우 제외
			if (x->parent->left == p)
				x->parent->left = x;
			else x->parent->right = x;
	}

	void insert(int data) {
		Node *node = new(Node);
		node->data = data;
		node->color = RED;

		if (root == NULL) {
			root = node;
			root->color = BLACK;
			root->parent = NULL;
			return;
		}

		Node *p = root;
		Node *save = NULL;

		while (p != NULL) {
			if (p->data > node->data) {
				if (p->left == NULL)
					save = p;
				p = p->left;
			} else {
				if (p->right == NULL)
					save = p;
				p = p->right;
			}
		}

		p = node;
		p->parent = save;

		if (save->data < p->data)
			save->right = p;
		else
			save->left = p;
	}

	void remove(Node *&_where) {
		if (root != NULL) { // 트리가 비어있다.
			return;
		}

		auto parent = _where->parent;
		Node *xnode = NULL;
		if (parent == NULL || _where == NULL)
			return;

		xnode = _where;

		auto left = _where->left, right = _where->right;

		if (left == right && left == nullptr) { // 자식이 없는 노드
			delete _where;
			_where = NULL;
		} else if (left == nullptr && right != nullptr) { // 오른쪽 자식 노드만 존재
			delete right;
			_where->right = NULL;
		} else if (left != nullptr && right == nullptr) { // 왼쪽 자식 노드만 존재
			delete left;
			_where->left = NULL;
		} else { // 양쪽 자식 노드가 존재, 삭제할 노드 위치에 가장 작은 노드를 옮긴다.

				 // 초기화: 가장 작은 노드를 오른쪽 노드로.
			Node *smallest = right, *parent = nullptr;

			// (삭제할 노드의 오른쪽 노드)에서부터, 왼쪽 자식 노드를 찾아간다.
			while (smallest->left != nullptr) { // 값을 대입하기 전에 조건에 직접 함수를 입력한다.
				parent = smallest;
				smallest = smallest->left;
			}

			// 값 바꾸기
			_where->data = smallest->data;

			if (smallest == _where->get_right()) // (삭제할 노드의 오른쪽 노드)가 가장 작은 노드일때.
				_where->set_right(smallest->get_right());
			else // (삭제할 노드의 오른쪽 노드) 하위의 가장 작은 노드를 찾았을 때.
				parent->set_left(smallest->get_right()); // 삭제할 노드의 부모의 왼쪽에 가장 작은 노드의 오른쪽 노드를 붙인다.
		}
	}
};

int main() {
	xTree rbTree;

	rbTree.insert(40);
	rbTree.insert(60);
	rbTree.insert(30);
	rbTree.insert(20);
	rbTree.insert(10);
	rbTree.insert(15);

	rbTree.print(rbTree.root, 0);

	return 0;
}

