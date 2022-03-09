package org.softwareheritage.graph.utils;

import it.unimi.dsi.fastutil.longs.LongArrays;
import org.junit.jupiter.api.Test;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class ForkJoinQuickSort3Test {
    private static long[] identity(final int n) {
        final long[] perm = new long[n];
        for (int i = perm.length; i-- != 0;)
            perm[i] = i;
        return perm;
    }

    private static void checkArraySorted(long[] x, long[] y, long[] z) {
        checkArraySorted(x, y, z, 0, x.length);
    }

    private static void checkArraySorted(long[] x, long[] y, long[] z, int from, int to) {
        for (int i = to - 1; i-- != from;)
            assertTrue(x[i] < x[i + 1] || x[i] == x[i + 1] && (y[i] < y[i + 1] || y[i] == y[i + 1] && z[i] <= z[i + 1]),
                    String.format("%d: <%d, %d, %d>, <%d, %d, %d>", i, x[i], y[i], z[i], x[i + 1], y[i + 1], z[i + 1]));
    }

    @Test
    public void testParallelQuickSort3() {
        final long[][] d = new long[3][];

        d[0] = new long[10];
        for (int i = d[0].length; i-- != 0;)
            d[0][i] = 3 - i % 3;
        d[1] = LongArrays.shuffle(identity(10), new Random(0));
        d[2] = LongArrays.shuffle(identity(10), new Random(1));
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);

        d[0] = new long[100000];
        for (int i = d[0].length; i-- != 0;)
            d[0][i] = 100 - i % 100;
        d[1] = LongArrays.shuffle(identity(100000), new Random(6));
        d[2] = LongArrays.shuffle(identity(100000), new Random(7));
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);

        d[0] = new long[10];
        for (int i = d[0].length; i-- != 0;)
            d[0][i] = i % 3 - 2;
        Random random = new Random(0);
        d[1] = new long[d[0].length];
        for (int i = d[1].length; i-- != 0;)
            d[1][i] = random.nextInt();
        d[2] = new long[d[0].length];
        for (int i = d[2].length; i-- != 0;)
            d[2][i] = random.nextInt();
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);

        d[0] = new long[100000];
        d[1] = new long[100000];
        d[2] = new long[100000];
        for (int i = d[0].length; i-- != 0;)
            d[2][i] = random.nextInt();
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);

        d[0] = new long[100000];
        random = new Random(0);
        for (int i = d[0].length; i-- != 0;)
            d[0][i] = random.nextInt();
        d[1] = new long[d[0].length];
        for (int i = d[1].length; i-- != 0;)
            d[1][i] = random.nextInt();
        d[2] = new long[d[0].length];
        for (int i = d[2].length; i-- != 0;)
            d[2][i] = random.nextInt();
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);
        for (int i = 100; i-- != 10;)
            d[0][i] = random.nextInt();
        for (int i = 100; i-- != 10;)
            d[1][i] = random.nextInt();
        for (int i = 100; i-- != 10;)
            d[2][i] = random.nextInt();
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2], 10, 100);
        checkArraySorted(d[0], d[1], d[2], 10, 100);

        d[0] = new long[10000000];
        random = new Random(0);
        for (int i = d[0].length; i-- != 0;)
            d[0][i] = random.nextInt();
        d[1] = new long[d[0].length];
        for (int i = d[1].length; i-- != 0;)
            d[1][i] = random.nextInt();
        d[2] = new long[d[0].length];
        for (int i = d[2].length; i-- != 0;)
            d[2][i] = random.nextInt();
        ForkJoinQuickSort3.parallelQuickSort(d[0], d[1], d[2]);
        checkArraySorted(d[0], d[1], d[2]);
    }
}
