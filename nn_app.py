# nn_app.py - Нейросетевая система распознавания стрелок (8 сторон света)
import tkinter as tk
from tkinter import messagebox
import math
import random


# ==========================================
# МОДУЛЬ 1: САМОПИСНАЯ НЕЙРОННАЯ СЕТЬ (MLP)
# ==========================================
class NeuralNetwork:
    """Многослойный персептрон 25 -> 10 -> 8 без внешних ИИ-библиотек"""

    def __init__(self):
        # Архитектура сети
        self.input_size = 25
        self.hidden_size = 10
        self.output_size = 8
        self.lr = 0.3  # Скорость обучения

        # Инициализация весов случайными числами
        self.w_input_hidden = [[random.uniform(-0.5, 0.5) for _ in range(self.hidden_size)] for _ in
                               range(self.input_size)]
        self.w_hidden_output = [[random.uniform(-0.5, 0.5) for _ in range(self.output_size)] for _ in
                                range(self.hidden_size)]

    def _sigmoid(self, x):
        return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

    def forward(self, inputs):
        """Прямой проход (вычисление сигналов)"""
        self.inputs = inputs
        # Вычисление скрытого слоя
        self.hidden = [self._sigmoid(sum(inputs[i] * self.w_input_hidden[i][j] for i in range(self.input_size))) for j
                       in range(self.hidden_size)]
        # Вычисление выходного слоя
        self.outputs = [self._sigmoid(sum(self.hidden[j] * self.w_hidden_output[j][k] for j in range(self.hidden_size)))
                        for k in range(self.output_size)]
        return self.outputs

    def backward(self, targets):
        """Обратное распространение ошибки (Backpropagation)"""
        # Ошибка выходного слоя
        out_deltas = [self.outputs[k] * (1.0 - self.outputs[k]) * (targets[k] - self.outputs[k]) for k in
                      range(self.output_size)]

        # Ошибка скрытого слоя
        hidden_deltas = [self.hidden[j] * (1.0 - self.hidden[j]) * sum(
            out_deltas[k] * self.w_hidden_output[j][k] for k in range(self.output_size)) for j in
                         range(self.hidden_size)]

        # Обновление весов скрытый-выходной
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.w_hidden_output[j][k] += self.lr * out_deltas[k] * self.hidden[j]

        # Обновление весов входной-скрытый
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.w_input_hidden[i][j] += self.lr * hidden_deltas[j] * self.inputs[i]


# ==========================================
# МОДУЛЬ 2: ИНТЕРФЕЙС ПРИЛОЖЕНИЯ (GUI)
# ==========================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ЛР №5: Распознавание стрелок (8 направлений)")

        self.nn = NeuralNetwork()
        self.grid_size = 5
        self.pixels = [0] * (self.grid_size * self.grid_size)

        # Направления сторон света
        self.CLASSES = ["Север", "Северо-Восток", "Восток", "Юго-Восток", "Юг", "Юго-Запад", "Запад", "Северо-Запад"]
        self.samples = []  # Обучающая выборка

        # Графическая сетка 5х5 для рисования мымоью
        self.buttons = []
        frame_grid = tk.Frame(root)
        frame_grid.pack(side=tk.LEFT, padx=10, pady=10)

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(frame_grid, width=4, height=2, bg="white")
                # Рисование при зажатии или клике мыши
                btn.bind("<Button-1>", lambda e, idx=i * self.grid_size + j: self._toggle_pixel(idx))
                btn.bind("<B1-Motion>", lambda e, idx=i * self.grid_size + j: self._paint_motion(e, frame_grid))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

        # Панель управления
        frame_controls = tk.Frame(root)
        frame_controls.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(frame_controls, text="Выберите класс для образца:").pack()
        self.class_var = tk.StringVar(value=self.CLASSES[0])
        self.dropdown = tk.OptionMenu(frame_controls, self.class_var, *self.CLASSES)
        self.dropdown.pack(pady=5)

        tk.Button(frame_controls, text="Добавить в выборку", command=self.add_sample, width=20).pack(pady=2)
        tk.Button(frame_controls, text="Очистить сетку", command=self.clear_grid, width=20).pack(pady=2)
        tk.Button(frame_controls, text="Обучить сеть (1000 эпох)", command=self.train_network, width=20,
                  bg="#d4edda").pack(pady=5)
        tk.Button(frame_controls, text="Распознать образ", command=self.recognize, width=20, bg="#cce5ff").pack(pady=5)

        self.lbl_info = tk.Label(frame_controls, text="Выборка: 0 образцов", fg="gray")
        self.lbl_info.pack()

    def _toggle_pixel(self, idx):
        self.pixels[idx] = 1 if self.pixels[idx] == 0 else 0
        self.buttons[idx // self.grid_size][idx % self.grid_size].configure(
            bg="black" if self.pixels[idx] == 1 else "white")

    def _paint_motion(self, event, grid):
        # Вычисление пикселя под курсором при движении мыши
        widget = grid.winfo_containing(event.x_root, event.y_root)
        if widget in grid.winfo_children():
            info = widget.grid_info()
            idx = int(info['row']) * self.grid_size + int(info['column'])
            self.pixels[idx] = 1
            widget.configure(bg="black")

    def clear_grid(self):
        self.pixels = [0] * 25
        for r in self.buttons:
            for b in r:
                b.configure(bg="white")

    def add_sample(self):
        """Требование 1: Добавление элементов в обучающую выборку"""
        target_class = self.class_var.get()
        class_idx = self.CLASSES.index(target_class)
        targets = [0.0] * 8
        targets[class_idx] = 1.0

        self.samples.append((list(self.pixels), targets))
        self.lbl_info.configure(text=f"Выборка: {len(self.samples)} образцов")
        self.clear_grid()
        messagebox.showinfo("Успех", f"Образец для направления '{target_class}' добавлен!")

    def train_network(self):
        """Обучение сети на собранной выборке"""
        if not self.samples:
            messagebox.showwarning("Ошибка", "Сначала добавьте образцы в выборку!")
            return

        for _ in range(1000):  # 1000 эпох обучения
            for inputs, targets in self.samples:
                self.nn.forward(inputs)
                self.nn.backward(targets)
        messagebox.showinfo("Обучение", "Нейросеть успешно обучена!")

    def recognize(self):
        """Распознавание нарисованной стрелки"""
        outputs = self.nn.forward(self.pixels)
        max_idx = outputs.index(max(outputs))
        predicted_class = self.CLASSES[max_idx]
        confidence = outputs[max_idx] * 100

        messagebox.showinfo("Результат", f"Направление стрелки: {predicted_class}\nУверенность: {confidence:.1f}%")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
