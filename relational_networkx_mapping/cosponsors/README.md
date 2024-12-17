# Cosponsors

In this problem you will be analyzing data on Congressional bills.

In many legislative bodies a legislator can signal their support for a bill by signing on as a "cosponsor."
Being a cosponsor has no bearing on the bill's passage, but places political pressure on leaders to hold hearings or votes.

We will be looking at sponsorship data from the US Senate and writing code to analyze the data.

## NetworkX

This problem will have you using the [NetworkX](https://networkx.org) library, which provides classes & functions for dealing with graph data structures.

Part of the challenge of this problem will be in reading & interpreting the library's documentation. Now that you know the fundamentals, a lot of your growth as a programmer will come through learning new third-party libraries.

I recommend starting the assignment by reading the [NetworkX Tutorial](https://networkx.org/documentation/latest/tutorial.html). **Stop when you get to "Multigraphs"**, the content after that point is not relevant to this assignment.

You may also need to consult additional documentation to learn to use this new library, but that tutorial should give a foundation that you can build upon.

## Data

You are provided with three data files in `sponsorships/data`:

**bills.csv** contains 'identifier' and 'title' pairs, one per bill. This links a given bill ID to a name.  There will be one entry per 'identifier'.

**legislators.csv** contains 'person_id', 'name', and 'current_party' fields, one per legislator.

**sponsorships.csv** contains 'identifier' and 'person_id' pairs. Each pair represents a sponsors of a bill.  Bills can have multiple sponsors, and sponsors can sponsor multiple bills, so neither column is guaranteed to be unique.

 **Note** There are some sponsorships in the data set that refer to a person_id that does not appear anywhere in `legislators.csv`. You should ignore these records!

## Assignment

You will need to implement the following functions.

**You should write helper functions as needed to keep your code well organized and free of duplication. A significant portion of your grade will be based on your approach avoiding unnecessary code duplication.**

### `NodeData`

To help out, write a `NodeData` class that has the following:

- Constructor: `NodeData(kind, identifier, name, party=None)`
- `self.kind` - either 'legislator' or 'bill' depending on the kind of node
- `self.identifier` - the identifier of the given object (HB 1234 or ocd-person/123456..)
- `self.name` - the name of the legislator or title of the bill
- `self.party` - the party of the legislator, `None` if `kind` is 'bill'

You may use a `dataclass` for this as introduced in lecture, or a traditional class.

### `build_graph() -> networkx.Graph`

The `build_graph` function should return a `networkx.Graph` with:

- a node for each bill with the key set to the bill identifier (e.g. "HB 1234")
- a node for each legislator with the key set to the person_id (e.g. "ocd-person/123456...")
- every node (both kinds) should have a 'data' property (as shown in the tutorial) that should be set to the a `NodeData` instance for the given bill or legislator
- an edge connecting bills to people per `sponsorships.csv`.  **Note** There are some sponsorships in the data set that do not have a corresponding legislator record. Your code should avoid adding these edges!

NetworkX requires a scalar for the identifier of each node. You may set the identifier for the node to whatever you find most helpful in your implementation, for example:

```
g = nx.Graph()

# identifier may be whatever you find useful -- our tests will not check it
# node_data_instance must be a `NodeData`!
g.add_node(identifier, data=node_data_instance)
```


### `find_top_sponsors(graph, n) -> list[tuple[str, int]]`

Return an ordered list of the names of the **n** sponsors with the most bills sponsored.

Each element in the list is a 2-element tuple like `("Frank", 13)` where "Frank" is the name of the sponsor and 13 is the number of bills sponsored.

**n** will never exceed the number of sponsors in the graph.

### `find_top_bills(graph, n) -> list[tuple[str, int]]`

Return an ordered list of the names of the **n** bills with the most sponsors.

Each element in the list is a 2-element tuple like `("Affordable Care Act", 20)` where "Affordable Care Act" is the name of the bill and 20 is the number of sponsors.

**n** will never exceed the number of bills in the graph.

## `find_most_similar(graph, to_legislator: str) -> str`

Find the legislator with the most sponsorships in common with the given legislator.

`to_legislator` will be a name, and the return value should be a name as well.

If there is a tie, the legislator with the name earlier in the alphabet should win.

e.g. if 'Adam Smith' and 'Jane Adams' both sponsored 100 bills that 'Mary Ng' had sponsored:

```
>>> find_most_similar(g, "Mary Ng")
"Adam Smith"   # because "Adam Smith" < "Jane Adams"
```

(Do not worry about splitting the names/sorting by last name.)

If the `to_legislator` is not found in the graph, raise a `ValueError.`
