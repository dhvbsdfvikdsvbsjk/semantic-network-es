# kb.py - Модуль Базы Знаний (Фреймовая модель)

class VacationFrame:
    """Базовый фрейм 1-го уровня"""
    def __init__(self, budget, days):
        self.budget = budget
        self.days = days
        self.zone = None

    def run_demons(self):
        """Присоединенная процедура (демон-вычислитель)"""
        if self.budget < 50000 and self.days < 5:
            self.zone = "local"
        elif 50000 <= self.budget < 150000 and 5 <= self.days <= 14:
            self.zone = "domestic"
        else:
            self.zone = "international"


class DomesticVacation(VacationFrame):
    """Фрейм 2-го уровня - Внутренний туризм"""
    def __init__(self, budget, days, prefer_nature):
        super().__init__(budget, days)
        self.run_demons()  # Активация процедуры родителя
        self.prefer_nature = prefer_nature
        self.category = None

    def determine_category(self):
        """Присоединенная процедура для определения категории"""
        if self.prefer_nature == "yes":
            self.category = "Altai_Baikal"
        else:
            self.category = "cultural"


class AltaiFrame(DomesticVacation):
    """Фрейм 3-го уровня - Экземпляр направления"""
    def __init__(self, budget, days, prefer_nature, active_rest):
        super().__init__(budget, days, prefer_nature)
        self.determine_category()
        self.active_rest = active_rest
        self.destination = None

    def get_final_verdict(self):
        """Финальная процедура вывода вердикта"""
        if self.category == "Altai_Baikal" and self.active_rest == "yes":
            self.destination = "Активный экстремальный трекинг на Алтае или конный тур"
            return self.destination
        return None
