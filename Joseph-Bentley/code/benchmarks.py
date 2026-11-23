from problem import load_instance
import time
import statistics
import tracemalloc
import csv

stats = {
    "comparisons": 0,
    "moves": 0
}
results = []


def solve_insertion(inst, stats):

    comps = 0
    mvs = 0
    records = []
    for i in range(inst["n"]):
        records.append(
            (inst["ids"][i], inst["delay"][i])
        )

    n = len(records)
    for i in range(1, n):

        current = records[i]
        j = i - 1

        while j >= 0:
            comps += 1
            if records[j][1] < current[1]:
                comps += 1
                records[j + 1] = records[j]
                mvs += 1
                j -= 1
            else:
                break

        records[j + 1] = current
        mvs += 1

    stats["comparisons"] = comps
    stats["moves"] = mvs
    return [record[0] for record in records]


def solve_merge(inst, stats):

    records = []
    for i in range(inst["n"]):
        records.append((inst["ids"][i], inst["delay"][i]))

    def merge_sort(records, stats):
        if len(records) <= 1:
            return records

        mid = len(records) // 2
        left = merge_sort(records[:mid], stats)
        right = merge_sort(records[mid:], stats)

        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if left[i][1] >= right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            stats["moves"] += 1
            i += 1

        while j < len(right):
            result.append(right[j])
            stats["moves"] += 1
            j += 1

        return result

    sorted_records = merge_sort(records, stats)

    return [record[0] for record in sorted_records]


def solve_heap(inst, stats):

    records = []
    for i in range(inst["n"]):
        records.append(
            (
                inst["ids"][i],
                inst["delay"][i],
                i
            )
        )

    def heapify(arr, n, i, stats):

        def greater(a, b):
            if a[1] > b[1]:
                stats["comparisons"] += 1
                return True
            if a[1] < b[1]:
                stats["comparisons"] += 1
                return False
            stats["comparisons"] += 1
            return a[2] < b[2]

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and greater(arr[left], arr[largest]):
            largest = left
        if right < n and greater(arr[right], arr[largest]):
            largest = right
        if largest != i:
            stats["moves"] += 3
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest, stats)

    n = len(records)

    for i in range(n // 2 - 1, -1, -1):
        heapify(records, n, i, stats)
    for i in range(n - 1, -1, -1):
        stats["moves"] += 3
        records[0], records[i] = records[i], records[0]
        heapify(records, i, 0, stats)

    records.reverse()
    return [record[0] for record in records]


def solve_counting(inst, stats):

    MIN_DELAY = -60
    MAX_DELAY = 900

    buckets = [[] for _ in range(MAX_DELAY - MIN_DELAY + 1)]

    for i in range(inst["n"]):
        record = (
            (inst["ids"][i], inst["delay"][i])
        )
        stats["moves"] += 1
        buckets[record[1] - MIN_DELAY].append(record)

    sorted_records = []

    for idx in range(len(buckets) - 1, - 1, -1):
        stats["moves"] += len(buckets[idx])
        sorted_records.extend(buckets[idx])

    return [record[0] for record in sorted_records]

def benchmark(algorithm, inst, alg, dataset_name, runs=5):

    times = []
    for _ in range(runs):
	    stats["comparisons"] = 0
	    stats["moves"] = 0
	    tracemalloc.start()
	    start = time.perf_counter()
	    result = algorithm(inst, stats)
	    elapsed = time.perf_counter() - start
	    current, peak = tracemalloc.get_traced_memory()
	    tracemalloc.stop()
	    times.append(elapsed)

    results.append({
	"algorithm": alg,
	"dataset": dataset_name,
	"median_time": statistics.median(times),
	"comparisons": stats["comparisons"],
	"moves": stats["moves"],
	"peak_memory": peak
    })

def benchmarking():
    datasets = [
	"../data/flights_n000015_schedule.csv",
	"../data/flights_n001000_schedule.csv",
	"../data/flights_n010000_nearly_sorted.csv",
	"../data/flights_n010000_reversed.csv",
	"../data/flights_n010000_schedule.csv",
	"../data/flights_n100000_nearly_sorted.csv",
	"../data/flights_n100000_schedule.csv"
    ]

    #inst = load_instance(datasets[0])
    #benchmark(solve_insertion, inst, "insertion", "flights_n000015_schedule.csv")
    #inst = load_instance(datasets[1])
    #benchmark(solve_insertion, inst, "insertion", "flights_n001000_schedule.csv")
    #inst = load_instance(datasets[2])
    #benchmark(solve_insertion, inst, "insertion", "flights_n010000_nearly_sorted.csv")
    #inst = load_instance(datasets[3])
    #benchmark(solve_insertion, inst, "insertion", "flights_n010000_reversed.csv")
    #inst = load_instance(datasets[4])
    #benchmark(solve_insertion, inst, "insertion", "flights_n010000_schedule.csv")
    ###LAST SET NOT RECOMMENDED, nearly_sorted WILL TAKE 300 SECONDS PER ATTEMPT
    #inst = load_instance(datasets[5])
    #benchmark(solve_insertion, inst, "insertion", "flights_n100000_nearly_sorted.csv")

    #inst = load_instance(datasets[0])
    #benchmark(solve_merge, inst, "merge", "flights_n000015_schedule.csv")
    #inst = load_instance(datasets[1])
    #benchmark(solve_merge, inst, "merge", "flights_n001000_schedule.csv")
    #inst = load_instance(datasets[2])
    #benchmark(solve_merge, inst, "merge", "flights_n010000_nearly_sorted.csv")
    #inst = load_instance(datasets[3])
    #benchmark(solve_merge, inst, "merge", "flights_n010000_reversed.csv")
    #inst = load_instance(datasets[4])
    #benchmark(solve_merge, inst, "merge", "flights_n010000_schedule.csv")
    #inst = load_instance(datasets[5])
    #benchmark(solve_merge, inst, "merge", "flights_n100000_nearly_sorted.csv")
    #inst = load_instance(datasets[6])
    #benchmark(solve_merge, inst, "merge", "flights_n100000_schedule.csv")

    #inst = load_instance(datasets[0])
    #benchmark(solve_heap, inst, "heap", "flights_n000015_schedule.csv")
    #inst = load_instance(datasets[1])
    #benchmark(solve_heap, inst, "heap", "flights_n001000_schedule.csv")
    #inst = load_instance(datasets[2])
    #benchmark(solve_heap, inst, "heap", "flights_n010000_nearly_sorted.csv")
    #inst = load_instance(datasets[3])
    #benchmark(solve_heap, inst, "heap", "flights_n010000_reversed.csv")
    #inst = load_instance(datasets[4])
    #benchmark(solve_heap, inst, "heap", "flights_n010000_schedule.csv")
    #inst = load_instance(datasets[5])
    #benchmark(solve_heap, inst, "heap", "flights_n100000_nearly_sorted.csv")
    #inst = load_instance(datasets[6])
    #benchmark(solve_heap, inst, "heap", "flights_n100000_schedule.csv")

    inst = load_instance(datasets[0])
    benchmark(solve_counting, inst, "counting", "flights_n000015_schedule.csv")
    inst = load_instance(datasets[1])
    benchmark(solve_counting, inst, "counting", "flights_n001000_schedule.csv")
    inst = load_instance(datasets[2])
    benchmark(solve_counting, inst, "counting", "flights_n010000_nearly_sorted.csv")
    inst = load_instance(datasets[3])
    benchmark(solve_counting, inst, "counting", "flights_n010000_reversed.csv")
    inst = load_instance(datasets[4])
    benchmark(solve_counting, inst, "counting", "flights_n010000_schedule.csv")
    inst = load_instance(datasets[5])
    benchmark(solve_counting, inst, "counting", "flights_n100000_nearly_sorted.csv")
    inst = load_instance(datasets[6])
    benchmark(solve_counting, inst, "counting", "flights_n100000_schedule.csv")

    for res in results:
        print(res)

    with open("benchmark_results.csv", "w", newline="") as outfile:
	    fieldnames = [
	        "algorithm",
	        "dataset",
	        "median_time",
	        "comparisons",
	        "moves",
	        "peak_memory"
	    ]

	    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
	    writer.writeheader()
	    for row in results:
	        writer.writerow(row)

benchmarking()

TECHNIQUES = {
    "insertion": solve_insertion,
    "merge": solve_merge,
    "heap": solve_heap,
    "counting": solve_counting,
}
