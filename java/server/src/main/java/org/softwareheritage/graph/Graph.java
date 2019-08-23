package org.softwareheritage.graph;

import java.io.IOException;

import it.unimi.dsi.big.webgraph.BVGraph;
import it.unimi.dsi.big.webgraph.LazyLongIterator;

import org.softwareheritage.graph.Node;
import org.softwareheritage.graph.SwhPID;
import org.softwareheritage.graph.backend.NodeIdMap;
import org.softwareheritage.graph.backend.NodeTypesMap;

/**
 * Main class storing the compressed graph and node id mappings.
 * <p>
 * The compressed graph is stored using the <a href="http://webgraph.di.unimi.it/">WebGraph</a>
 * ecosystem. Additional mappings are necessary because Software Heritage uses string based <a
 * href="https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html">persistent
 * identifiers</a> (PID) while WebGraph uses integers internally. These two mappings (long id &harr;
 * PID) are used for the input (users refer to the graph using PID) and the output (convert back to
 * PID for users results). However, since graph traversal can be restricted depending on the node
 * type (see {@link AllowedEdges}), a long id &rarr; node type map is stored as well to avoid a full
 * PID lookup.
 *
 * @author Thibault Allançon
 * @see org.softwareheritage.graph.AllowedEdges
 * @see org.softwareheritage.graph.NodeIdMap;
 * @see org.softwareheritage.graph.NodeTypesMap;
 */

public class Graph {
  /** File extension for the SWH PID to long node id map */
  public static final String PID_TO_NODE = ".pid2node.csv";
  /** File extension for the long node id to SWH PID map */
  public static final String NODE_TO_PID = ".node2pid.csv";
  /** File extension for the long node id to node typ map */
  public static final String NODE_TO_TYPE = ".node2type.map";

  /** Compressed graph stored as a {@link it.unimi.dsi.big.webgraph.BVGraph} */
  BVGraph graph;
  /** Transposed compressed graph (used for backward traversals) */
  BVGraph graphTransposed;
  /** Path and basename of the compressed graph */
  String path;
  /** Mapping long id &harr; SWH PIDs */
  NodeIdMap nodeIdMap;
  /** Mapping long id &rarr; node types */
  NodeTypesMap nodeTypesMap;

  /**
   * Constructor.
   *
   * @param path path and basename of the compressed graph to load
   */
  public Graph(String path) throws IOException {
    this.graph = BVGraph.load(path);
    this.graphTransposed = BVGraph.load(path + "-transposed");
    this.path = path;
    this.nodeIdMap = new NodeIdMap(path, getNbNodes());
    this.nodeTypesMap = new NodeTypesMap(path);
  }

  /**
   * Cleans up graph resources after use.
   */
  public void cleanUp() throws IOException {
    nodeIdMap.close();
  }

  /**
   * Returns the graph full path.
   *
   * @return graph full path
   */
  public String getPath() {
    return path;
  }

  /**
   * Converts {@link SwhPID} node to long.
   *
   * @param swhPID node specified as a {@link SwhPID}
   * @return internal long node id
   * @see org.softwareheritage.graph.SwhPID
   */
  public long getNodeId(SwhPID swhPID) {
    return nodeIdMap.getNodeId(swhPID);
  }

  /**
   * Converts long id node to {@link SwhPID}.
   *
   * @param nodeId node specified as a long id
   * @return external SWH PID
   * @see org.softwareheritage.graph.SwhPID
   */
  public SwhPID getSwhPID(long nodeId) {
    return nodeIdMap.getSwhPID(nodeId);
  }

  /**
   * Returns node type.
   *
   * @param nodeId node specified as a long id
   * @return corresponding node type
   * @see org.softwareheritage.graph.Node.Type
   */
  public Node.Type getNodeType(long nodeId) {
    return nodeTypesMap.getType(nodeId);
  }

  /**
   * Returns number of nodes in the graph.
   *
   * @return number of nodes in the graph
   */
  public long getNbNodes() {
    return graph.numNodes();
  }

  /**
   * Returns number of edges in the graph.
   *
   * @return number of edges in the graph
   */
  public long getNbEdges() {
    return graph.numArcs();
  }

  /**
   * Returns lazy iterator of successors of a node.
   *
   * @param nodeId node specified as a long id
   * @return lazy iterator of successors of the node, specified as a <a
   * href="http://webgraph.di.unimi.it/">WebGraph</a> LazyLongIterator
   */
  public LazyLongIterator successors(long nodeId) {
    return graph.successors(nodeId);
  }

  /**
   * Returns the outdegree of a node.
   *
   * @param nodeId node specified as a long id
   * @return outdegree of a node
   */
  public long outdegree(long nodeId) {
    return graph.outdegree(nodeId);
  }

  /**
   * Returns lazy iterator of predecessors of a node.
   *
   * @param nodeId node specified as a long id
   * @return lazy iterator of predecessors of the node, specified as a <a
   * href="http://webgraph.di.unimi.it/">WebGraph</a> LazyLongIterator
   */
  public LazyLongIterator predecessors(long nodeId) {
    return graphTransposed.successors(nodeId);
  }

  /**
   * Returns the indegree of a node.
   *
   * @param nodeId node specified as a long id
   * @return indegree of a node
   */
  public long indegree(long nodeId) {
    return graphTransposed.outdegree(nodeId);
  }

  /**
   * Returns the degree of a node, depending on graph orientation.
   *
   * @param nodeId node specified as a long id
   * @param useTransposed boolean value to use transposed graph
   * @return degree of a node
   */
  public long degree(long nodeId, boolean useTransposed) {
    return (useTransposed) ? indegree(nodeId) : outdegree(nodeId);
  }

  /**
   * Returns the neighbors of a node (as a lazy iterator), depending on graph orientation.
   *
   * @param nodeId node specified as a long id
   * @param useTransposed boolean value to use transposed graph
   * @return lazy iterator of neighbors of the node, specified as a <a
   * href="http://webgraph.di.unimi.it/">WebGraph</a> LazyLongIterator
   */
  public LazyLongIterator neighbors(long nodeId, boolean useTransposed) {
    return (useTransposed) ? predecessors(nodeId) : successors(nodeId);
  }
}
