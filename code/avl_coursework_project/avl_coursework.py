import random
import time
import csv
import math
import matplotlib.pyplot as plt

# Узел дерева
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


#  АВЛ-дерево
class AVLTree:
    def __init__(self):
        self.root = None
        self.steps = 0

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def right_rotate(self, y):
        self.steps += 1
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        self.steps += 1
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        self.update_height(x)
        self.update_height(y)
        return y

    # Вставка
    def insert(self, key):
        self.steps = 0
        self.root = self._insert(self.root, key)
        return self.steps

    def _insert(self, node, key):
        self.steps += 1

        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # одинаковые ключи не добавляем

        self.update_height(node)
        balance = self.get_balance(node)

        # Левый левый случай
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Правый правый случай
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Левый правый случай
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Правый левый случай
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Поиск
    def search(self, key):
        self.steps = 0
        current = self.root

        while current is not None:
            self.steps += 1
            if key == current.key:
                return True, self.steps
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return False, self.steps

    # Удаление
    def delete(self, key):
        self.steps = 0
        self.root = self._delete(self.root, key)
        return self.steps

    def _delete(self, node, key):
        self.steps += 1

        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # узел найден
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # если есть два потомка, берем минимальный элемент справа
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        if node is None:
            return node

        self.update_height(node)
        balance = self.get_balance(node)

        # Балансировка после удаления
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            self.steps += 1
            current = current.left
        return current


#  Измерение времени
def measure(func, value):
    start = time.perf_counter()
    steps = func(value)
    end = time.perf_counter()
    return end - start, steps


def average(values):
    return sum(values) / len(values)


#  Графики
def make_graph(values, title, x_label, y_label, file_name):
    plt.figure()
    plt.plot(range(1, len(values) + 1), values)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig(file_name)
    plt.close()


# Основная программа
def main():
    random.seed(42)

    # Генерация 10 000 уникальных целых чисел
    data = random.sample(range(1, 1_000_000), 10_000)

    with open("input_data.txt", "w", encoding="utf-8") as file:
        for number in data:
            file.write(str(number) + "\n")

    tree = AVLTree()
    rows = []

    insert_times = []
    insert_steps = []

    # Вставка 10 000 элементов
    for i, number in enumerate(data, start=1):
        work_time, steps = measure(tree.insert, number)
        insert_times.append(work_time)
        insert_steps.append(steps)
        rows.append(["insert", i, number, work_time, steps, math.log2(i + 1)])

    # Поиск 100 случайных элементов
    search_values = random.sample(data, 100)
    search_times = []
    search_steps = []

    for i, number in enumerate(search_values, start=1):
        start = time.perf_counter()
        found, steps = tree.search(number)
        end = time.perf_counter()
        search_times.append(end - start)
        search_steps.append(steps)
        rows.append(["search", i, number, end - start, steps, math.log2(len(data) + 1)])

    # Удаление 1000 случайных элементов
    delete_values = random.sample(data, 1000)
    delete_times = []
    delete_steps = []

    current_size = len(data)
    for i, number in enumerate(delete_values, start=1):
        work_time, steps = measure(tree.delete, number)
        delete_times.append(work_time)
        delete_steps.append(steps)
        rows.append(["delete", i, number, work_time, steps, math.log2(current_size + 1)])
        current_size -= 1

    # Построение графиков
    make_graph(insert_steps, "Вставка: шаги", "Номер вставки", "Количество шагов", "insert_steps.png")
    make_graph(search_steps, "Поиск: шаги", "Номер поиска", "Количество шагов", "search_steps.png")
    make_graph(delete_steps, "Удаление: шаги", "Номер удаления", "Количество шагов", "delete_steps.png")

    make_graph(insert_times, "Вставка: время", "Номер вставки", "Время, сек", "insert_time.png")
    make_graph(search_times, "Поиск: время", "Номер поиска", "Время, сек", "search_time.png")
    make_graph(delete_times, "Удаление: время", "Номер удаления", "Время, сек", "delete_time.png")

    # Сохранение всех результатов
    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["operation", "number", "value", "time_seconds", "steps", "log2_n"])
        writer.writerows(rows)

    # Сохранение средних значений
    summary = [
        ["Операция", "Среднее время, сек", "Среднее количество шагов"],
        ["Вставка", average(insert_times), average(insert_steps)],
        ["Поиск", average(search_times), average(search_steps)],
        ["Удаление", average(delete_times), average(delete_steps)],
    ]

    with open("summary.txt", "w", encoding="utf-8") as file:
        for row in summary:
            file.write(f"{row[0]}: {row[1]} | {row[2]}\n")

    print("Работа программы завершена.")
    print("Файлы созданы: input_data.txt, results.csv, summary.txt и PNG-графики")
    print()
    print("Средние значения:")
    for row in summary[1:]:
        print(f"{row[0]}: время = {row[1]:.10f} сек, шаги = {row[2]:.2f}")


if __name__ == "__main__":
    main()
