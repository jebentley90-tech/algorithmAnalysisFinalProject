def solve_insertion(inst):
    
    records = []
    for i in range(inst["n"]):
        records.append(
            (inst["ids"][i], inst["delay"][i])
        )

    n = len(records)
    for i in range(1, n):
        
        current = records[i]
        j = i - 1

        while j >= 0 and records[j][1] < current[1]:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = current

    return [record[0] for record in records]


def solve_merge(inst):
    
    records = []
    comparisons = 0
    for i in range(inst["n"]):
        records.append((inst["ids"][i], inst["delay"][i]))

    def merge_sort(records, comparisons):
        if len(records) <= 1:
            return records

        mid = len(records) // 2
        left = merge_sort(records[:mid], comparisons)
        right = merge_sort(records[mid:], comparisons)

        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i][1] >= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    sorted_records = merge_sort(records, comparisons)

    return [record[0] for record in sorted_records]


def solve_heap(inst):
    
    records = []
    for i in range(inst["n"]):
        records.append(
            (
                inst["ids"][i],
                inst["delay"][i],
                i
            )
        )
        
    def heapify(arr, n, i):

        def greater(a, b):
            if a[1] > b[1]: return True
            if a[1] < b[1]: return False
            return a[2] < b[2]

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and greater(arr[left], arr[largest]):
            largest = left
        if right < n and greater(arr[right], arr[largest]):
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(records)

    for i in range(n // 2 - 1, -1, -1):
        heapify(records, n, i)
    for i in range(n - 1, -1, -1):
        records[0], records[i] = records[i], records[0]
        heapify(records, i, 0)

    records.reverse()
    return [record[0] for record in records]


def solve_counting(inst):
    
    MIN_DELAY = -60
    MAX_DELAY = 900

    buckets = [[] for _ in range(MAX_DELAY - MIN_DELAY + 1)]

    for i in range(inst["n"]):
        record = (
            (inst["ids"][i], inst["delay"][i])
        )
        buckets[record[1] - MIN_DELAY].append(record)

    sorted_records = []

    for idx in range(len(buckets) - 1, - 1, -1):
        sorted_records.extend(buckets[idx])

    return [record[0] for record in sorted_records]


TECHNIQUES = {
    "insertion": solve_insertion,
    "merge": solve_merge,
    "heap": solve_heap,
    "counting": solve_counting,
}
