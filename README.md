# Programming Assignment 2: Greedy Algorithms

**COP4533 - Spring 2026**

**Students:**
- Pablo Pupo (UFID: 96796601)
- Preston Hemmy (UFID: 31020809)

## Description

Implementation and comparison of three cache eviction policies:
1. **FIFO** (First-In, First-Out)
2. **LRU** (Least Recently Used)
3. **OPTFF** (Belady's Farthest-in-Future, optimal offline)

## How to Run

**Requirements:** Python 3.10+. No external dependencies.

```bash
python3 src/eviction_policies.py <input_file>
```

**Example:**

```bash
python3 src/eviction_policies.py data/example.in
```

**Expected output:**

```
FIFO  : 9
LRU   : 8
OPTFF : 6
```

## Input Format

The input file has two lines:
- Line 1: `k m` where `k` is the cache capacity (k >= 1) and `m` is the number of requests.
- Line 2: `r1 r2 r3 ... rm`, a space-separated sequence of integer request IDs.

## Output Format

```
FIFO  : <number_of_misses>
LRU   : <number_of_misses>
OPTFF : <number_of_misses>
```

## Assumptions

- Input is well-formed (integers, correct counts).
- Python 3.10+ is available.
- No external libraries required; only standard library modules (`sys`, `collections`) are used.

---

## Written Component

### Question 1: Empirical Comparison

Results from three nontrivial input files:

| Input File | k | m  | FIFO | LRU | OPTFF |
|------------|---|----|------|-----|-------|
| input1.txt | 3 | 54 | 36   | 20  | 20    |
| input2.txt | 3 | 60 | 60   | 60  | 22    |
| input3.txt | 5 | 60 | 27   | 21  | 13    |

**Does OPTFF have the fewest misses?**

Yes. In all three test cases, OPTFF produced fewer or equal misses compared to both FIFO and LRU. This is expected, since OPTFF has complete knowledge of the future request sequence and can always make the optimal eviction choice. No online algorithm can outperform it.

**How does FIFO compare to LRU?**

FIFO performs equal to or worse than LRU across all test cases. In input1, where frequently accessed items (1 and 2) are repeatedly requested between new items, LRU retains them because they are always "recently used," while FIFO evicts them simply because they were loaded earliest. This results in FIFO incurring 36 misses versus LRU's 20. In input2, both perform identically (60 misses on 60 requests) because the cyclic scan pattern `1 2 3 4` with k=3 is a worst case for both policies: every access is a miss regardless of the eviction strategy. In input3, LRU again outperforms FIFO (21 vs. 27) due to the workload's temporal locality. In general, LRU tends to outperform FIFO on workloads with temporal locality, since it adapts to which items are actively in use. FIFO ignores usage patterns entirely and evicts based solely on insertion order.

### Question 2: Bad Sequence for LRU or FIFO

**Claim:** For k = 3, there exists a sequence where OPTFF incurs strictly fewer misses than both LRU and FIFO.

**Sequence:** `1 2 3 4 1 2 3 4 1 2 3 4` (k = 3, m = 12)

**FIFO trace (k = 3):**

| Request | Cache (after)  | Miss? |
|---------|---------------|-------|
| 1       | {1}           | Miss  |
| 2       | {1, 2}        | Miss  |
| 3       | {1, 2, 3}     | Miss  |
| 4       | {2, 3, 4}     | Miss (evict 1) |
| 1       | {3, 4, 1}     | Miss (evict 2) |
| 2       | {4, 1, 2}     | Miss (evict 3) |
| 3       | {1, 2, 3}     | Miss (evict 4) |
| 4       | {2, 3, 4}     | Miss (evict 1) |
| 1       | {3, 4, 1}     | Miss (evict 2) |
| 2       | {4, 1, 2}     | Miss (evict 3) |
| 3       | {1, 2, 3}     | Miss (evict 4) |
| 4       | {2, 3, 4}     | Miss (evict 1) |

**FIFO misses: 12** (every request is a miss).

**LRU trace (k = 3):**

| Request | Cache (after)  | Miss? |
|---------|---------------|-------|
| 1       | {1}           | Miss  |
| 2       | {1, 2}        | Miss  |
| 3       | {1, 2, 3}     | Miss  |
| 4       | {2, 3, 4}     | Miss (evict 1, LRU) |
| 1       | {3, 4, 1}     | Miss (evict 2, LRU) |
| 2       | {4, 1, 2}     | Miss (evict 3, LRU) |
| 3       | {1, 2, 3}     | Miss (evict 4, LRU) |
| 4       | {2, 3, 4}     | Miss (evict 1, LRU) |
| 1       | {3, 4, 1}     | Miss (evict 2, LRU) |
| 2       | {4, 1, 2}     | Miss (evict 3, LRU) |
| 3       | {1, 2, 3}     | Miss (evict 4, LRU) |
| 4       | {2, 3, 4}     | Miss (evict 1, LRU) |

**LRU misses: 12** (every request is a miss).

**OPTFF trace (k = 3):**

| Step | Request | Cache (after)  | Miss? |
|------|---------|---------------|-------|
| 0    | 1       | {1}           | Miss  |
| 1    | 2       | {1, 2}        | Miss  |
| 2    | 3       | {1, 2, 3}     | Miss  |
| 3    | 4       | {1, 2, 4}     | Miss (evict 3: farthest next use at index 6) |
| 4    | 1       | {1, 2, 4}     | Hit   |
| 5    | 2       | {1, 2, 4}     | Hit   |
| 6    | 3       | {1, 3, 4}     | Miss (evict 2: farthest next use at index 9) |
| 7    | 4       | {1, 3, 4}     | Hit   |
| 8    | 1       | {1, 3, 4}     | Hit   |
| 9    | 2       | {3, 4, 2}     | Miss (evict 1: never used again) |
| 10   | 3       | {3, 4, 2}     | Hit   |
| 11   | 4       | {3, 4, 2}     | Hit   |

**OPTFF misses: 6**

Verified programmatically: running this input produces FIFO: 12, LRU: 12, OPTFF: 6.

**Explanation:** With k = 3 and 4 distinct items cycling, both LRU and FIFO miss on every single request (12/12) because each eviction removes an item that is needed in the very next cycle. OPTFF avoids this by always evicting the item whose next use is farthest away, achieving 6 hits out of 12 requests. For example, at step 3 OPTFF evicts item 3 (not needed until step 6) instead of item 1 (needed at step 4), securing hits at steps 4 and 5.

### Question 3: Prove OPTFF is Optimal

**Theorem.** Let OPTFF be Belady's Farthest-in-Future algorithm and let A be any offline algorithm that knows the full request sequence. For any fixed request sequence and cache of capacity k, the number of misses incurred by OPTFF is no larger than that of A.

**Proof (by exchange argument).**

Let the request sequence be r_1, r_2, ..., r_m. We show that any offline algorithm A can be transformed into OPTFF step by step without increasing the total number of misses.

Suppose A and OPTFF process the same request sequence with the same cache capacity k. We will show that at every step where A and OPTFF make a different eviction decision, we can modify A to match OPTFF's decision without increasing A's total miss count.

Consider the first time step j at which A and OPTFF make different eviction decisions. Both experience a cache miss at step j (otherwise there is no eviction). Let OPTFF evict item f (the one whose next request is farthest in the future) and let A evict some other item a, where a != f.

After step j, A's cache contains f but not a, while OPTFF's cache contains a but not f.

We construct a new algorithm A' that evicts f instead of a at step j (matching OPTFF), and otherwise follows A. The only difference between their caches after step j is that A' holds a while A holds f.

Since OPTFF chose to evict f — the item with the farthest (or nonexistent) next use — we know that a's next request comes no later than f's. So a will be requested before f (or at the same time).

When a is next requested, A does not have it (A evicted a at step j) and misses. Meanwhile, A' still has a and gets a hit. At this point, A loads a and evicts some item b. A' can evict f (still not needed yet) so that both caches now hold exactly the same items. From here on A' mimics A exactly.

Between step j and this synchronization point, f is never requested — because a comes first — so A' never misses on f in that window. The net effect is that A' gets one hit where A got a miss, so A' incurs no more total misses than A.

By repeating this exchange at every step where A' and OPTFF differ, we eventually transform A into OPTFF without ever increasing the miss count. Therefore:

**misses(OPTFF) <= misses(A)**

for any offline algorithm A on any fixed request sequence. This completes the proof that OPTFF is optimal.
