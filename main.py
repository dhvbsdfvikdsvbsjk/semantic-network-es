# main.py - Главный управляющий модуль и интерфейс пользователя

from inference import InferenceEngine

def main():
    print("=== Экспертная система на основе фреймов ===")
    
    # 1. Сбор целочисленных и логических данных (Инициализация и Интерактив)
    budget = int(input("Введите ваш бюджет (целое число): "))
    days = int(input("Введите количество дней отпуска (целое число): "))
    prefer_nature = input("Вы предпочитаете природу? (yes/no): ").strip().lower()
    active_rest = input("Вы хотите активный отдых? (yes/no): ").strip().lower()

    # 2. Передача управления в МЛВ
    engine = InferenceEngine(budget, days, prefer_nature, active_rest)
    result, history = engine.compute()

    print("\n==========================================")
    print(f"РЕКОМЕНДАЦИЯ СИСТЕМЫ: {result}")
    print("==========================================\n")

    # 3. Компонента объяснения вывода
    show_explain = input("Показать трассировку (объяснение) вывода? (yes/no): ").strip().lower()
    if show_explain == "yes":
        print("\n--- Компонента объяснения вывода ---")
        for step in history:
            print(f"[ЛОГ]: {step}")

if __name__ == "__main__":
    main()
