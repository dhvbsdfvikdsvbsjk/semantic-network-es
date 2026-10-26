# inference.py - Модуль логического вывода

from kb import AltaiFrame

class InferenceEngine:
    """Компонента МЛВ, управляющая активацией фреймов"""
    def __init__(self, budget, days, prefer_nature, active_rest):
        self.budget = budget
        self.days = days
        self.prefer_nature = prefer_nature
        self.active_rest = active_rest
        self.history = []  # Логирование шагов для компоненты объяснения

    def compute(self):
        self.history.append(f"Инициализация: бюджет={self.budget}, дней={self.days}")
        
        # Создаем целевой фрейм и запускаем его цепочку процедур
        altai = AltaiFrame(self.budget, self.days, self.prefer_nature, self.active_rest)
        
        self.history.append(f"Шаг 1 (Демон родителя): Определена зона -> {altai.zone}")
        self.history.append(f"Шаг 2 (Процедура категории): Определена категория -> {altai.category}")
        
        result = altai.get_final_verdict()
        if result:
            self.history.append(f"Шаг 3 (Финал): Успешно активирован фрейм Алтая. Результат: {result}")
            return result, self.history
        
        self.history.append("Шаг 3: Фрейм не подошел под критерии.")
        return "Направление не найдено", self.history
