import pytest
from cosponsors import (
    NodeData,
    build_graph,
    find_top_sponsors,
    find_top_bills,
    find_most_similar,
)


@pytest.fixture
def graph():
    """Fixture to set up the graph for all tests."""
    return build_graph()


EXPECTED_BILLS = 17817
EXPECTED_LEGISLATORS = 541
EXPECTED_SPONSORSHIPS = 172321


def test_node_data():
    nd = NodeData("legislator", "ocd-person/123456", "Eugene Debs", "I")
    assert nd.kind == "legislator"
    assert nd.identifier == "ocd-person/123456"
    assert nd.name == "Eugene Debs"
    assert nd.party == "I"

    nd2 = NodeData("bill", "HB 1", "Vote Act")
    assert nd2.kind == "bill"
    assert nd2.identifier == "HB 1"
    assert nd2.name == "Vote Act"
    assert nd2.party is None


def test_build_graph_nodes(graph):
    bill_count = 0
    leg_count = 0

    # check that each node has a "data" attribute that is a DataNode
    for _, data in graph.nodes(data="data"):
        if data.kind == "bill":
            assert data.party is None  # Bills should not have a party
            assert data.name is not None  # Bills should have a title
            bill_count += 1
        elif data.kind == "legislator":
            assert data.party is not None  # Legislators should have a party
            assert data.name is not None  # Legislators should have a name
            leg_count += 1

    assert bill_count == EXPECTED_BILLS
    assert leg_count == EXPECTED_LEGISLATORS
    assert len(graph) == EXPECTED_BILLS + EXPECTED_LEGISLATORS


def test_build_graph_edges(graph):
    edge_count = len(graph.edges)
    assert edge_count == EXPECTED_SPONSORSHIPS


def test_find_top_sponsors(graph):
    expected_top_sponsors = [
        ("Eleanor Holmes Norton", 2048),
        ("Brian K. Fitzpatrick", 1360),
        ("Steve Cohen", 1176),
        ("Barbara Lee", 1095),
        ("Janice D. Schakowsky", 1049),
    ]
    top_sponsors = find_top_sponsors(graph, 5)
    assert top_sponsors == expected_top_sponsors


def test_find_top_bills(graph):
    expected_top_bills = [
        ("Republic of Iran", 200),
        ("August 26, 2021", 198),
    ]

    top_bills = find_top_bills(graph, 3)
    assert len(top_bills) == 3
    for idx, exp in enumerate(expected_top_bills):
        # check that string appears in title
        assert exp[0] in top_bills[idx][0]
        # check that count is right
        assert exp[1] == top_bills[idx][1]

    # third bill may vary depend on if aggregation was on title or identifier
    # since underspecified in problem statement, both are acceptable
    assert "Rangers Veterans" in top_bills[2][0] or "Gold Medal" in top_bills[2][0]
    assert top_bills[2][1] in (190, 196)


def test_find_most_similar(graph):
    assert find_most_similar(graph, "Nancy Pelosi") == "Barbara Lee"
    assert find_most_similar(graph, "Mitch McConnell") == "Marsha Blackburn"
    assert find_most_similar(graph, "Ted Cruz") == "Marco Rubio"
    assert (
        find_most_similar(graph, "Alexandria Ocasio-Cortez") == "Eleanor Holmes Norton"
    )


def test_find_most_similar_valueerror(graph):
    with pytest.raises(ValueError):
        assert find_most_similar(graph, "George Washington")
