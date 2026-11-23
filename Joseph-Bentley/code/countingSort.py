def countingSort(arr, min, max):
    n = len(arr)
    count = []
    for i in range(max - min + 1):
        count.append(0)

    for num in arr:
        count[num - min] += 1

    z = 0
    for i in range(min, max + 1, 1):
        while count[i - min] > 0:
            arr[z] = i
            z += 1
            count[i - min] -= 1
