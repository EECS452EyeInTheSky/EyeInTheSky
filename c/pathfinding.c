#include <stdio.h>
#include <math.h>
#include <float.h>
#include <stdlib.h>

#define NUM_COL 80
#define NUM_ROW 70

#define MAP_INVALID_VAL 1
#define TRUE 1
#define FALSE 0

#define NUM_NODES (NUM_COL * NUM_ROW)

typedef struct Point
{
	unsigned x;
	unsigned y;
} Point;

float point_distance(Point a, Point b)
{
	float xd = a.x - b.x;
	float yd = a.y - b.y;
	float result = sqrt ( (xd*xd) + (yd*yd) );
	return result;
}
	
typedef struct Node
{
	Point position;
	struct Node * prev;
	float cost;
	float heur;
	unsigned passable; // True if the robot can pass through this point, False otherwise
	unsigned visited;
	struct Node  * neighbors[8];
	size_t num_neighbors;
} Node;


#define NODE_TOTAL_COST(n) ( (n).cost + (n).heur )
#define POINT_TO_INDEX(p) ( (p).x * NUM_ROW + (p).y )
#define PAIR_TO_INDEX(x, y) ( (x) * NUM_ROW + (y) )

typedef struct NodeSearchList
{
	Node nodes[NUM_NODES];
	size_t size;
} NodeSearchList;

void add_node_to_search_list(NodeSearchList * searchList, Node node)
{
	searchList->nodes[searchList->size++] = node;
}

Node get_min_node_from_search_list(NodeSearchList * searchList)
{
	Node result = searchList->nodes[0];
	size_t i;
	for (i = 0; i < searchList->size; i++)
	{
		if ( NODE_TOTAL_COST(result) > NODE_TOTAL_COST(searchList->nodes[i]))
			result = searchList->nodes[i];
	}
	return result;
}

typedef struct Graph
{
	Node nodes[NUM_NODES];
	//NodeSearchList searchList;
	Point start;
	Point goal;
} Graph;

void node_find_neighbors(Graph * graph, Node  * node)
{
	/* Upper Left Corner */
	if (node->position.x > 0 && node->position.y > 0)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x - 1, node->position.y - 1)];
//		printf("Found upper left neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Left */
	if (node->position.x > 0)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x - 1, node->position.y)];
////		printf("Found left neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Bottom Left Corner */
	if (node->position.x > 0 && node->position.y < NUM_ROW-1)
	{
		node->neighbors[node->num_neighbors++] =  & graph->nodes[PAIR_TO_INDEX(node->position.x - 1, node->position.y + 1)];
////		printf("Found bottom left neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Down */
	if (node->position.y < NUM_ROW-1)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x, node->position.y + 1)];
//		printf("Neighbor index: %d\n", PAIR_TO_INDEX(node->position.x, node->position.y + 1));
//		printf("Found down neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Bottom Right Corner */
	if (node->position.x < NUM_COL-1 && node->position.y < NUM_ROW-1)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x + 1, node->position.y + 1)];
//		printf("Found bottom right neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Right */
	if (node->position.x < NUM_COL-1)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x + 1, node->position.y)];
//		printf("Found right neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* Upper Right Corner */
	if (node->position.x < NUM_COL-1 && node->position.y > 0)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x + 1, node->position.y - 1)];
//		printf("Found upper right neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

	/* upper */
	if (node->position.y > 0)
	{
		node->neighbors[node->num_neighbors++] = & graph->nodes[PAIR_TO_INDEX(node->position.x, node->position.y - 1)];
//		printf("Found upper neigh (%d, %d)\n", node->neighbors[node->num_neighbors-1]->position.x, node->neighbors[node->num_neighbors-1]->position.y);
	}

}

Node * graph_find_min_node(Graph * graph)
{
	size_t i = 0;
	while ((graph->nodes[i].visited || ! graph->nodes[i].passable) && i < NUM_NODES)
		i++;
	Node * result;
	if (i < NUM_NODES)
	{
		result = &graph->nodes[i];
	}
	else
	{
		return NULL;
	}
//	printf("Starting search at node %2d, %2d\n (visisted: %s, passable: %s)\n", result->position.x, result->position.y, result->visited ? "TRUE" : "FALSE", result->passable ? "TRUE" : "FALSE");
	for (; i < NUM_NODES; i++)
	{
		if (graph->nodes[i].visited || ! graph->nodes[i].passable)
		{
			continue;
		}
		else if (NODE_TOTAL_COST(graph->nodes[i]) < NODE_TOTAL_COST(*result))
		{
			result = &graph->nodes[i];
		}
	}
	return result;
}


Point index_to_point(size_t index)
{
	Point res;
	res.x = index / (NUM_ROW);
	res.y = index % (NUM_ROW);
	return res;
}

void * find_path(unsigned * map, Point start, Point finish)
{
	Graph * graph = (Graph *) calloc(sizeof(struct Graph), 1);
//	printf("Graph allocated at %p\n", graph);
	graph->start = start;
	graph->goal = finish;
	
	size_t i;

	// Initialize the nodes
//	printf("Initializing the nodes...\n");
	for (i = 0; i < NUM_NODES; i++)
	{
		Node node;
		node.position = index_to_point(i);
//		printf("Initializing node at (%d, %d)\n", node.position.x, node.position.y);
		node.cost = FLT_MAX;
		node.heur = point_distance(node.position, graph->goal);
		node.passable = map[i] == 1 ? FALSE : TRUE;
		if ( ! node.passable )
		{
			printf("Node at (%d, %d) is not passable\n", node.position.x, node.position.y);
		}
		//printf("Node at %2d, %2d is %s\n", node.position.x, node.position.y, node.passable ? "PASSABLE" : "NOT PASSABLE");
		node.visited = FALSE;
		node.prev = NULL;
		graph->nodes[i] = node;
	}
	graph->nodes[POINT_TO_INDEX(start)].cost = 0;
//	printf("DONE\n");

//	printf("Finding neighbors...\n");
	for (i = 0; i < NUM_NODES; i++)
	{
		node_find_neighbors(graph, &graph->nodes[i]);
	}
//	printf("Finding the min node...\n");
	Node * cur = graph_find_min_node(graph);
	if (cur == NULL)
	{
		printf("Failed to find a path!\n");
		graph->nodes[POINT_TO_INDEX(graph->goal)].prev = NULL;
		return graph;
	}
//	printf("DONE\n");

	while ( ! cur->visited )
	{
//		printf("Visiting node at (%2d, %2d) (%s) Has %ld neighbors\n", cur->position.x, cur->position.y, cur->visited ? "HAS BEEN VISITED" : "HAS NOT BEEN VISITED", cur->num_neighbors);
		for (i = 0; i < cur->num_neighbors; i++)
		{
			Node * neigh = cur->neighbors[i];
			if ( ! neigh->passable )
				continue;
//			printf("Node (%d, %d) has neighbor (%d, %d)\n", cur->position.x, cur->position.y, neigh->position.x, neigh->position.y);
			if (cur->cost + point_distance(cur->position, neigh->position) < neigh->cost)
			{
//				printf("Setting node (%d, %d) previous to (%d, %d)\n", neigh->position.x, neigh->position.y, cur->position.x, cur->position.y);
				neigh->cost = cur->cost + point_distance(cur->position, neigh->position);
				neigh->prev = cur;
			}
		}
		if (	cur->position.x == graph->goal.x &&
				cur->position.y == graph->goal.y 
		   )
		{
			break;
		}
		cur->visited = TRUE;
		cur = graph_find_min_node(graph);
	}
	return (void *) graph;
}

int find_path_length(void * raw_graph)
{
//	printf("Graph allocated at %p\n", raw_graph);
	Graph * graph = (Graph *) raw_graph;
	Node * cur = &graph->nodes[POINT_TO_INDEX(graph->goal)];
	if (cur->prev == NULL)
		return 0;
	int length = 0;
	while (cur != NULL)
	{
//		printf("Found point at %2d, %2d\n", cur->position.x, cur->position.y);
		length++;
		cur = cur->prev; 
	}
	return length;
}

Point * get_path(void * raw_graph)
{
	Graph * graph = (Graph *) raw_graph;
	int length = find_path_length(graph);
	size_t i = 0;
	if (length == 0)
		return NULL;
	Point * path = malloc(length * sizeof(Point));
	Node * cur = &graph->nodes[POINT_TO_INDEX(graph->goal)];
	while (cur != NULL)
	{
		path[i] = cur->position;
		i++;
		cur = cur->prev;
	}
	return path;
}
