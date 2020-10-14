package org.softwareheritage.graph.experiments.topology;

import com.martiansoftware.jsap.*;
import it.unimi.dsi.Util;
import it.unimi.dsi.big.webgraph.ImmutableGraph;
import it.unimi.dsi.big.webgraph.LazyLongIterator;
import it.unimi.dsi.fastutil.BigArrays;
import it.unimi.dsi.fastutil.longs.LongBigArrays;
import it.unimi.dsi.logging.ProgressLogger;
import it.unimi.dsi.util.XoRoShiRo128PlusRandom;
import org.softwareheritage.graph.AllowedNodes;
import org.softwareheritage.graph.Graph;
import org.softwareheritage.graph.Node;
import org.softwareheritage.graph.Subgraph;

import java.io.*;
import java.util.*;
import java.util.concurrent.*;

public class ClusteringCoefficient {
    private final Graph graph;
    private final Subgraph subgraph;
    private final String outdirPath;
    private final ConcurrentHashMap<Long, Long> result_full;
    private final ConcurrentHashMap<Long, Long> result_dircnt;
    private final ConcurrentHashMap<Long, Long> result_rev;
    private final ConcurrentHashMap<Long, Long> result_revrel;
    private final ConcurrentHashMap<Long, Long> result_orisnp;

    public ClusteringCoefficient(String graphBasename, String allowedNodes, String outdirPath) throws IOException {
        this.outdirPath = outdirPath;
        System.err.println("Loading graph " + graphBasename + " ...");
        this.graph = new Graph(graphBasename);
        this.subgraph = new Subgraph(this.graph, new AllowedNodes(allowedNodes));
        System.err.println("Graph loaded.");

        result_full = new ConcurrentHashMap<>();
        result_dircnt = new ConcurrentHashMap<>();
        result_rev = new ConcurrentHashMap<>();
        result_revrel = new ConcurrentHashMap<>();
        result_orisnp = new ConcurrentHashMap<>();
    }

    private static JSAPResult parse_args(String[] args) {
        JSAPResult config = null;
        try {
            SimpleJSAP jsap = new SimpleJSAP(AveragePaths.class.getName(), "",
                    new Parameter[]{
                            new FlaggedOption("graphPath", JSAP.STRING_PARSER, JSAP.NO_DEFAULT, JSAP.REQUIRED, 'g',
                                    "graph", "Basename of the compressed graph"),
                            new FlaggedOption("nodeTypes", JSAP.STRING_PARSER, JSAP.NO_DEFAULT, JSAP.REQUIRED, 's',
                                    "nodetypes", "Node type constraints"),
                            new FlaggedOption("outdir", JSAP.STRING_PARSER, JSAP.NO_DEFAULT, JSAP.REQUIRED, 'o',
                                    "outdir", "Directory where to put the results"),
                            new FlaggedOption("numThreads", JSAP.INTEGER_PARSER, "32", JSAP.NOT_REQUIRED, 't',
                                    "numthreads", "Number of threads"),});

            config = jsap.parse(args);
            if (jsap.messagePrinted()) {
                System.exit(1);
            }
        } catch (JSAPException e) {
            e.printStackTrace();
        }
        return config;
    }

    private void run(int numThreads) throws InterruptedException {
        final long END_OF_QUEUE = -1L;

        ArrayBlockingQueue<Long> queue = new ArrayBlockingQueue<>(numThreads);
        ExecutorService service = Executors.newFixedThreadPool(numThreads + 1);

        service.submit(() -> {
            try {
                Graph thread_graph = graph.copy();
                Subgraph thread_subgraph = subgraph.copy();

                long[][] randomPerm = Util.identity(thread_graph.numNodes());
                LongBigArrays.shuffle(randomPerm, new XoRoShiRo128PlusRandom());
                long n = thread_graph.numNodes();

                ProgressLogger pl = new ProgressLogger();
                pl.expectedUpdates = n;
                pl.itemsName = "nodes";
                pl.start("Filling processor queue...");

                for (long j = 0; j < n; ++j) {
                    long node = BigArrays.get(randomPerm, j);
                    if (thread_subgraph.nodeExists(node) && thread_subgraph.outdegree(node) == 0) {
                        queue.put(node);
                    }
                    if (j % 10000 == 0) {
                        printResult();
                    }
                    pl.update();
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                for (int i = 0; i < numThreads; ++i) {
                    try {
                        queue.put(END_OF_QUEUE);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        for (int i = 0; i < numThreads; ++i) {
            service.submit(() -> {
                try {
                    Subgraph thread_subgraph = subgraph.copy();
                    while (true) {
                        Long node = null;
                        try {
                            node = queue.take();
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        if (node == null || node == END_OF_QUEUE) {
                            return;
                        }

                        computeAt(thread_subgraph, node);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        }

        service.shutdown();
        service.awaitTermination(365, TimeUnit.DAYS);
    }

    private void computeAt(Subgraph graph, long node) {
        long d = graph.outdegree(node);
        if (d < 2) {
            return;
        }
        Node.Type nodeType = graph.getNodeType(node);

        HashSet<Long> neighborhood = new HashSet<>();
        long succ;
        final LazyLongIterator iterator = graph.successors(node);
        while ((succ = iterator.nextLong()) != -1) {
            neighborhood.add(succ);
        }

        long triangles_full = 0;
        long triangles_dircnt = 0;
        long triangles_rev = 0;
        long triangles_revrel = 0;
        long triangles_orisnp = 0;

        for (Long neighbor : neighborhood) {
            Node.Type neighborNodeType = graph.getNodeType(neighbor);
            final LazyLongIterator it = graph.successors(neighbor);
            while ((succ = it.nextLong()) != -1) {
                if (neighborhood.contains(succ)) {
                    Node.Type succNodeType = graph.getNodeType(succ);
                    triangles_full++;
                    if ((nodeType == Node.Type.DIR || nodeType == Node.Type.CNT)
                            && (neighborNodeType == Node.Type.DIR || neighborNodeType == Node.Type.CNT)
                            && (succNodeType == Node.Type.DIR || succNodeType == Node.Type.CNT)) {
                        triangles_dircnt++;
                    } else if ((nodeType == Node.Type.REV || nodeType == Node.Type.REL)
                            && (neighborNodeType == Node.Type.REV || neighborNodeType == Node.Type.REL)
                            && (succNodeType == Node.Type.REV || succNodeType == Node.Type.REL)) {
                        triangles_revrel++;
                        if (nodeType == Node.Type.REV && neighborNodeType == Node.Type.REV
                                && succNodeType == Node.Type.REV)
                            triangles_rev++;
                    } else if ((nodeType == Node.Type.ORI || nodeType == Node.Type.SNP)
                            && (neighborNodeType == Node.Type.ORI || neighborNodeType == Node.Type.SNP)
                            && (succNodeType == Node.Type.ORI || succNodeType == Node.Type.SNP)) {
                        triangles_orisnp++;
                    }
                }
            }
        }

        result_full.merge(triangles_full, 1L, Long::sum);
        result_dircnt.merge(triangles_dircnt, 1L, Long::sum);
        result_rev.merge(triangles_rev, 1L, Long::sum);
        result_revrel.merge(triangles_revrel, 1L, Long::sum);
        result_orisnp.merge(triangles_orisnp, 1L, Long::sum);
    }

    public void printSortedDistribution(String distribPath, Map<Long, Long> distrib) throws IOException {
        PrintWriter f = new PrintWriter(new FileWriter(distribPath));
        TreeMap<Long, Long> sortedDistribution = new TreeMap<>(distrib);
        for (Map.Entry<Long, Long> entry : sortedDistribution.entrySet()) {
            f.println(entry.getKey() + " " + entry.getValue());
        }
        f.close();
    }

    public void printResult() throws IOException {
        new File(outdirPath).mkdirs();

        printSortedDistribution(outdirPath + "/distribution-full.txt", result_full);
        printSortedDistribution(outdirPath + "/distribution-dircnt.txt", result_dircnt);
        printSortedDistribution(outdirPath + "/distribution-rev.txt", result_rev);
        printSortedDistribution(outdirPath + "/distribution-revrel.txt", result_revrel);
        printSortedDistribution(outdirPath + "/distribution-orisnp.txt", result_orisnp);
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        JSAPResult config = parse_args(args);

        String graphPath = config.getString("graphPath");
        String outdir = config.getString("outdir");
        String allowedNodes = config.getString("nodeTypes");
        int numThreads = config.getInt("numThreads");

        ClusteringCoefficient cc = new ClusteringCoefficient(graphPath, allowedNodes, outdir);
        cc.run(numThreads);
        cc.printResult();
    }

    // Old unused functions

    private long oppositeEdges(ImmutableGraph graph, long node) {
        HashSet<Long> neighborhood = new HashSet<>();
        long succ;
        final LazyLongIterator iterator = graph.successors(node);
        while ((succ = iterator.nextLong()) != -1) {
            neighborhood.add(succ);
        }

        long closed_triplets = 0;
        for (Long neighbor : neighborhood) {
            final LazyLongIterator it = graph.successors(neighbor);
            while ((succ = it.nextLong()) != -1) {
                if (neighborhood.contains(succ)) {
                    closed_triplets++;
                }
            }
        }
        return closed_triplets;
    }

    public void compute(ProgressLogger pl, Formatter out_local, Formatter out_global) {
        final long n = this.graph.numNodes();

        pl.expectedUpdates = n;
        pl.itemsName = "nodes";

        long nodes_d2 = 0;
        double cum_lcc = 0;
        double cum_lcc_c0 = 0;
        double cum_lcc_c1 = 0;
        HashMap<Double, Long> distribution = new HashMap<>();

        for (long node = 0; node < n; node++) {
            long d = graph.outdegree(node);
            if (d >= 2) {
                double t = (d * (d - 1));
                double m = oppositeEdges(graph, node);
                double lcc = m / t;

                distribution.merge(lcc, 1L, Long::sum);

                cum_lcc += lcc;
                nodes_d2++;
            } else {
                cum_lcc_c1++;
            }
            pl.update();
        }
        pl.done();

        for (Map.Entry<Double, Long> entry : distribution.entrySet()) {
            out_local.format("%f %d\n", entry.getKey(), entry.getValue());
        }

        double gC = cum_lcc / nodes_d2;
        double gC0 = cum_lcc_c0 / n;
        double gC1 = cum_lcc_c1 / n;

        out_global.format("C: %f\n", gC);
        out_global.format("C0: %f\n", gC0);
        out_global.format("C1: %f\n", gC1);
    }

    public void compute_approx(Formatter out_global) {
        final long n = this.graph.numNodes();

        long trials = 0;
        long triangles = 0;

        while (true) {
            long node = ThreadLocalRandom.current().nextLong(0, n);
            long d = graph.outdegree(node);
            if (d >= 2) {
                Long u = null;
                Long v = null;

                long u_idx = ThreadLocalRandom.current().nextLong(0, d);
                long v_idx = ThreadLocalRandom.current().nextLong(0, d - 1);
                if (v_idx >= u_idx) {
                    v_idx++;
                }

                long succ;
                final LazyLongIterator node_iterator = graph.successors(node);
                for (long succ_idx = 0; (succ = node_iterator.nextLong()) != -1; succ_idx++) {
                    if (succ_idx == u_idx) {
                        u = succ;
                    }
                    if (succ_idx == v_idx) {
                        v = succ;
                    }
                }

                final LazyLongIterator u_iterator = graph.successors(u);
                while ((succ = u_iterator.nextLong()) != -1) {
                    if (succ == v)
                        triangles++;
                }
            }
            trials++;

            if (trials % 100 == 0 || true) {
                double gC = (double) triangles / (double) trials;
                out_global.format("C: %f (triangles: %d, trials: %d)\n", gC, triangles, trials);
                System.out.format("C: %f (triangles: %d, trials: %d)\n", gC, triangles, trials);
            }
        }
    }
}
