# ASII
Analysis of the Spread of Information and Infection

## INFORMATION (AGENT) PROPERTIES
	Information is more abstract, it docent necessarily have features like an infection instead it more about what the agents in the simulation have access to. How many infected agents can they identify? How connected are they?
		AGENTS
		- Nodes
		- Sub-graphs
		- Infections
		
		
		

## INFECTION PROPERTIES
	- Probability of transmission 
	- Incubation period


## OTHER IDEAS
### GRAPH GENERATION
	Below is an algorithm for generating a graph with similarities to the geographical layout of real cities. The graph could also be viewed as a community or family with highly connected central members, and lesser socially connected members at the edge of the group. The construction of the graph also provides a convenient way for plotting the graph using networkX.
	
	1) *Group Initialization*: Scatter $N_g$ points across a 2d plane. Each of these points will represent a sub-graph in the full network. These can be though of as central community hubs.
	
	2) *Member Initialization*: Around each point $n_g$ scatter $N_i$ points with a Gaussian distribution (or other distribution). Each node assigned at this point should be assigned a group index indicating the group belongs too.
	
	3) *Intra-Group Connections*: Then all nodes should be connected with a weight equal to the euclidean distance separating them. Signifying either geographical or social connection of the nodes. 
		- There could also be a Threshold to limit number of connections. However this could result in isolated and completely un-connected nodes. 
		
	4) *Inter-Group Connections*: There are multiple ways to connect individual groups. I'll outline a few below, no one of them at this point stands out as the obvious way to proceed.
		4a) Euclidean distance with threshold: Again connect all nodes waited by their euclidean distances, with the option of not adding a note if its greater than some value. In this case groups would be connected by their peripheral members.
		4b) Central Node Connections: All central nodes could be connected with some modified weight. This could signify air travel as airports and other transportation systems as they are typically located in dense areas and are more efficient ways to connect to other geographically distant locations.



## DATA
	- Accessed google mobility data at link below.
		https://www.google.com/covid19/mobility/
