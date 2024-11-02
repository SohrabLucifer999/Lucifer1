import threading

class Worker:
    def __init__(self, table1, table2):
        self.table1 = table1
        self.table2 = table2

    def find_on_index(self, on):

        return self.table1[0].index(on)

    def full_join(self, on_index):

        result = []
        i, j = 0, 0
        while i < len(self.table1) and j < len(self.table2):
            if self.table1[i][on_index] == self.table2[j][on_index]:
                result.append(self.table1[i] + self.table2[j])
                i += 1
                j += 1
            elif self.table1[i][on_index] < self.table2[j][on_index]:
                result.append(self.table1[i] + [None] * len(self.table2[0]))
                i += 1
            else:
                result.append([None] * len(self.table1[0]) + self.table2[j])
                j += 1
        while i < len(self.table1):
            result.append(self.table1[i] + [None] * len(self.table2[0]))
            i += 1
        while j < len(self.table2):
            result.append([None] * len(self.table1[0]) + self.table2[j])
            j += 1
        return result

    def left_join(self, on_index):

        result = []
        i, j = 0, 0
        while i < len(self.table1):
            if j < len(self.table2) and self.table1[i][on_index] == self.table2[j][on_index]:
                result.append(self.table1[i] + self.table2[j])
                i += 1
                j += 1
            else:
                result.append(self.table1[i] + [None] * len(self.table2[0]))
                i += 1
        return result

    def right_join(self, on_index):

        result = []
        i, j = 0, 0
        while j < len(self.table2):
            if i < len(self.table1) and self.table1[i][on_index] == self.table2[j][on_index]:
                result.append(self.table1[i] + self.table2[j])
                i += 1
                j += 1
            else:
                result.append([None] * len(self.table1[0]) + self.table2[j])
                j += 1
        return result

    def inner_join(self, on_index):

        result = []
        i, j = 0, 0
        while i < len(self.table1) and j < len(self.table2):
            if self.table1[i][on_index] == self.table2[j][on_index]:
                result.append(self.table1[i] + self.table2[j])
                i += 1
                j += 1
            elif self.table1[i][on_index] < self.table2[j][on_index]:
                i += 1
            else:
                j += 1
        return result

class Master:
    def __init__(self, table1, table2):
        self.table1 = table1
        self.table2 = table2
        self.workers = []

    def split_data(self, num_workers):

        # Remove the header rows
        self.table1 = self.table1[1:]
        self.table2 = self.table2[1:]

        # Split the first table into equal parts
        part_size = len(self.table1) // num_workers
        parts = [self.table1[i:i+part_size] for i in range(0, len(self.table1), part_size)]

        # Create workers and assign parts
        self.workers = [Worker(part, self.table2) for part in parts]

    def find_on_index(self, on):

        return self.workers[0].find_on_index(on)

    def combine_results(self, results):

        combined_result = []
        for result in results:
            combined_result.extend(result)
        return combined_result

    def distribute_tasks(self, join_type, on):

        on_index = self.find_on_index(on)
        results = []
        for worker in self.workers:
            if join_type == "full":
                result = worker.full_join(on_index)
            elif join_type == "left":
                result = worker.left_join(on_index)
            elif join_type == "right":
                result = worker.right_join(on_index)
            elif join_type == "inner":
                result = worker.inner_join(on_index)
            results.append(result)
        return self.combine_results(results)

# Example usage
table1 = [["id", "name", "age"], [1, "Alice", 25], [2, "Bob", 30], [3, "Charlie", 35]]
table2 = [["id", "department", "salary"], [1, "IT", 50000], [2, "HR", 45000], [4, "Finance", 60000]]

master = Master(table1, table2)
master.split_data(num_workers=3)

full_join_result = master.distribute_tasks("full", "id")
left_join_result = master.distribute_tasks("left", "id")
right_join_result = master.distribute_tasks("right", "id")
inner_join_result = master.distribute_tasks("inner", "id")

print("Full Join:")
for row in full_join_result:
    print(row)

print("\nLeft Join:")
for row in left_join_result:
    print(row)

print("\nRight Join:")
for row in right_join_result:
    print(row)

print("\nInner Join:")
for row in inner_join_result:
    print(row)