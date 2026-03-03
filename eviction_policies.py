import sys
from collections import deque, OrderedDict


def fifo(capacity: int, requests: list[int]) -> int:
    """Returns the number of cache misses under First-In, First-Out policy"""

    cache_misses = 0
    fifo_queue = deque()
    cache_set = set()
    for request in requests:
        if request in cache_set:
            continue

        if len(fifo_queue) == capacity:
            evicted = fifo_queue.popleft()
            cache_set.remove(evicted)

        fifo_queue.append(request)
        cache_set.add(request)
        cache_misses += 1
    return cache_misses

def lru(capacity: int, requests: list[int]) -> int:
    """Returns the number of cache misses under LRU policy"""

    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0

    for request in requests:
        if request in cache:
            cache.move_to_end(request)
        else:
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[request] = None
            misses += 1

    return misses

def fif(capacity: int, requests: list[int]) -> int:
    """Returns the number of cache misses under Farthest-In-Future policy"""

    if capacity == 0:
        return len(requests)

    cache: set[int] = set()
    misses = 0

    for i, request in enumerate(requests):
        if request in cache:    # cache hit
            continue

        misses += 1             # o.w. cache miss

        if len(cache) < capacity:
            cache.add(request)
            continue

        farthest_req = None
        farthest_dist = -1

        for item in cache:
            try:
                use_next = requests.index(item, i + 1)
            except ValueError:
                farthest_req = item
                break

            if use_next > farthest_dist:
                farthest_dist = use_next
                farthest_req = item

        cache.remove(farthest_req)
        cache.add(request)

    return misses

def main():
    """Usage: python eviction_policies.py <input_file>"""

    # Ex. Input:
    # 3 12
    # 1 2 3 4 1 3 2 1 2 3 4 1
    if len(sys.argv) < 2:
        print("Usage: python eviction_policies.py <file_input>")

    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        header = file.readline().split()
        if not header:
            print("Error: input file must be non-empty")
            return

        k, _ = map(int, header)

        line = file.readline()
        data = (list(map(int, line.split())))

    fifo_res = fifo(k, data)
    lru_res = lru(k, data)
    fif_res = fif(k, data)

    print("First-In, First-Out policy cache misses: ", fifo_res)
    print("Least-Recently-Used policy cache misses: ", lru_res)
    print("Farthest-In-Future policy cache misses: ", fif_res)

    # Output:
    # FIFO  : <number_of_misses>
    # LRU   : <number_of_misses>
    # OPTFF : <number_of_misses>


if __name__ == '__main__':
    main()
    sys.exit(0)