import sys
from collections import deque, OrderedDict



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

    print("FIFO policy cache misses: ", fifo_res)
    # print("LRU policy cache misses: ", lru_res)

    # Output:
    # FIFO  : <number_of_misses>
    # LRU   : <number_of_misses>
    # OPTFF : <number_of_misses>


if __name__ == '__main__':
    main()
    sys.exit(0)