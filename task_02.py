from dataclasses import dataclass, field
from typing import Set, List, Optional

@dataclass
class Teacher:
    """
    Клас, що представляє викладача.
    """
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)


def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Optional[List[Teacher]]:
    """
    Створює розклад занять, призначаючи викладачів таким чином,
    щоб мінімізувати їх кількість і покрити всі предмети.
    """
    schedule = []  # Остаточний список викладачів із призначеними предметами
    uncovered_subjects = subjects.copy()  # Множина непокритих предметів

    while uncovered_subjects:
        # Знайти викладача, що покриває найбільше непокритих предметів, 
        # а у разі рівності - наймолодшого
        best_teacher: Optional[Teacher] = None
        best_cover: Set[str] = set()

        for teacher in teachers:
            cover = teacher.can_teach_subjects & uncovered_subjects
            if len(cover) > len(best_cover) or (
                    len(cover) == len(best_cover) and teacher.age < (best_teacher.age if best_teacher else float('inf'))):
                best_teacher = teacher
                best_cover = cover

        if not best_cover:  # Якщо більше неможливо покрити предмети
            return None

        # Призначити предмети викладачеві
        best_teacher.assigned_subjects = best_cover
        schedule.append(best_teacher)
        uncovered_subjects -= best_cover

    return schedule


if __name__ == '__main__':
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"})
    ]

    schedule = create_schedule(subjects, teachers)

    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")