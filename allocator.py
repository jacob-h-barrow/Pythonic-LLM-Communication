class Allocator:
    def __init__(self, n: int):
        self.slots_available = {0: n}
        self.alo = {}

    def allocate(self, size: int, mID: int) -> int:
        found = None
        for key, val in sorted(self.slots_available.items(), key=lambda x: x[0]):
            if val >= size:
                try:
                    self.alo[mID].append((key, size))
                except:
                    self.alo[mID] = [(key, size)]

                found = [key, size]
                break

        if found:
            key, size = found
            val = self.slots_available[key]
            del self.slots_available[key]
            if val - size > 0:
                self.slots_available[key + size] = val - size

            self.merge_consecutive()
            return key
        return -1        

    def merge_consecutive(self):
        # left_most_idx: count
        if not self.slots_available:
            return 
        items = list(sorted(self.slots_available.items(), key=lambda x: x[0]))
        ptr = 1
        length = len(items)
        curr_key, curr_size = items[0]

        while ptr < length:
            key, size = items[ptr]
            
            if (curr_key + curr_size) == key:
                self.slots_available[curr_key] += size
                del self.slots_available[key]
            else:
                curr_key, curr_size = key, size
            ptr += 1

    def free(self, mID: int) -> int:
        total = 0
        
        if mID in self.alo.keys():
            for key, size in self.alo[mID]:
                self.slots_available[key] = size
                total += size
            del self.alo[mID]

        self.merge_consecutive()

        return total
        
if __name__ == "__main__":
    testcases_calls = [["Allocator","allocate","allocate","allocate","free","allocate","allocate","allocate","free","allocate","free"]]
    testcases_numbers = [[[10],[1,1],[1,2],[1,3],[2],[3,4],[1,1],[1,1],[1],[10,2],[7]]]

    for idx, items in enumerate(zip(testcases_calls, testcases_numbers)):
        print(f'Running testcase {idx}')
        calls, numbers = items
        obj = None
        length = len(calls)
        
        # Output is a lot, get the first min(length, 20) calls
        for idx in range(min(length, 20)):
            nums_tuple = numbers[idx]
            match calls[idx]:
                case "Allocator":
                    obj = Allocator(*nums_tuple)
                case "allocate":
                    print(f'Allocating a block size of {nums_tuple[0]} using the following id {nums_tuple[1]}')
                    res = obj.allocate(*nums_tuple)
                    if res == -1:
                        print('\tFailed to allocate')
                    else:
                        print('\tBlock idx: {res}')
                case _:
                    # free
                    print(f'Releasing nodes with the following id: {nums_tuple}\t\nFreed up {obj.free(*nums_tuple)} blocks')
            
