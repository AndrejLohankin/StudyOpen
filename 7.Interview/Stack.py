class Stack:
    def __init__(self):
        """Инициализация пустого стека."""
        self.items = []

    def is_empty(self):
        """Проверка стека на пустоту."""
        return len(self.items) == 0

    def push(self, item):
        """Добавляет новый элемент на вершину стека."""
        self.items.append(item)

    def pop(self):
        """Удаляет верхний элемент стека и возвращает его."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        """Возвращает верхний элемент стека, не удаляя его."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        """Возвращает количество элементов в стеке."""
        return len(self.items)

    def is_balanced_correct(self):
        """Правильная проверка на сбалансированность скобок."""
        brackets_map = {'(': ')', '[': ']', '{': '}'}
        for char in self.items:
            if char in brackets_map:  # Открывающая скобка
                stack.push(char)
            elif char in brackets_map.values():  # Закрывающая скобка
                if stack.is_empty():
                    return False
                if brackets_map[stack.pop()] != char:
                    return False
        return stack.is_empty()


    def __str__(self):
        """Строковое представление стека."""
        return str(self.items)


# Пример использования:
if __name__ == "__main__":
    # Создание стека
    stack = Stack()

    # Проверка на пустоту
    print(f"Стек пустой? {stack.is_empty()}")  # True

    # Добавление элементов
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Стек после добавления элементов: {stack}")  # [1, 2, 3]
    print(f"Размер стека: {stack.size()}")  # 3

    # Просмотр верхнего элемента
    print(f"Верхний элемент: {stack.peek()}")  # 3
    print(f"Стек после peek: {stack}")  # [1, 2, 3] (не изменился)

    # Удаление элементов
    print(f"Удален элемент: {stack.pop()}")  # 3
    print(f"Стек после pop: {stack}")  # [1, 2]
    print(f"Размер стека: {stack.size()}")  # 2

    # Проверка на пустоту
    print(f"Стек пустой? {stack.is_empty()}")  # False

    # Очистка стека
    stack.pop()  # 2
    stack.pop()  # 1
    print(f"Стек пустой? {stack.is_empty()}")  # True

    # Создаем тестовые последовательности
    test_sequences = [
        "(((([{}]))))",  # Сбалансированно
        "[([])((([[[]]])))]{()}",  # Сбалансированно
        "{{[()]}}",  # Сбалансированно
        "}{",  # Несбалансированно
        "{{[(])]}}",  # Несбалансированно
        "[[{())}]",  # Несбалансированно
        "",  # Сбалансированно (пустая строка)
        "(((",  # Несбалансированно
        ")))",  # Несбалансированно
    ]

    # Проверяем каждую последовательность
    for sequence in test_sequences:
        # Создаем стек и заполняем его символами
        stack_2 = Stack()
        stack_2.items = list(sequence)  # Преобразуем строку в список символов

        # Вызываем функцию проверки
        result = stack_2.is_balanced_correct()
        status = "Сбалансированно" if result else "Несбалансированно"
        print(f"'{sequence}' -> {status}")