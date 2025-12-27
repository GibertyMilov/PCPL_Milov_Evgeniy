import json
import os
from datetime import datetime


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, description):
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'completed': False,
            'completed_at': None
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Задача добавлена (ID: {task['id']})")

    def show_tasks(self, show_all=True):
        if not self.tasks:
            print("📭 Список задач пуст")
            return

        print("\n" + "=" * 50)
        print("📋 СПИСОК ЗАДАЧ")
        print("=" * 50)

        for task in self.tasks:
            if not show_all and task['completed']:
                continue

            status = "✅" if task['completed'] else "⏳"
            print(f"{task['id']}. {status} {task['description']}")
            print(f"   📅 Создана: {task['created']}")
            if task['completed']:
                print(f"   🏁 Завершена: {task['completed_at']}")
            print("-" * 50)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                if task['completed']:
                    print(f"⚠️ Задача {task_id} уже выполнена")
                    return
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                print(f"✅ Задача {task_id} отмечена как выполненная")
                return
        print(f"❌ Задача с ID {task_id} не найдена")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                for j, t in enumerate(self.tasks[i:], start=i):
                    t['id'] = j + 1
                self.save_tasks()
                print(f"🗑️ Задача удалена: {deleted_task['description']}")
                return
        print(f"❌ Задача с ID {task_id} не найдена")

    def get_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed

        print("\n" + "=" * 50)
        print("📊 СТАТИСТИКА")
        print("=" * 50)
        print(f"📋 Всего задач: {total}")
        print(f"✅ Выполнено: {completed} ({completed / total * 100:.1f}%)" if total > 0 else "✅ Выполнено: 0")
        print(f"⏳ Осталось: {pending} ({pending / total * 100:.1f}%)" if total > 0 else "⏳ Осталось: 0")
        print("=" * 50)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    print("\n" + "=" * 50)
    print("🎯 МЕНЕДЖЕР ЗАДАЧ")
    print("=" * 50)
    print("1. 📝 Показать все задачи")
    print("2. 🔍 Показать активные задачи")
    print("3. ➕ Добавить задачу")
    print("4. ✅ Отметить задачу как выполненную")
    print("5. 🗑️ Удалить задачу")
    print("6. 📊 Показать статистику")
    print("7. 💾 Сохранить и выйти")
    print("=" * 50)


def main():
    manager = TaskManager()

    while True:
        clear_screen()
        show_menu()

        try:
            choice = input("\nВыберите действие (1-7): ").strip()

            if choice == '1':
                clear_screen()
                manager.show_tasks(show_all=True)
                input("\nНажмите Enter для продолжения...")

            elif choice == '2':
                clear_screen()
                manager.show_tasks(show_all=False)
                input("\nНажмите Enter для продолжения...")

            elif choice == '3':
                clear_screen()
                description = input("Введите описание задачи: ").strip()
                if description:
                    manager.add_task(description)
                else:
                    print("❌ Описание задачи не может быть пустым")
                input("\nНажмите Enter для продолжения...")

            elif choice == '4':
                clear_screen()
                manager.show_tasks(show_all=False)
                try:
                    task_id = int(input("\nВведите ID задачи для завершения: ").strip())
                    manager.complete_task(task_id)
                except ValueError:
                    print("❌ Введите корректный номер задачи")
                input("\nНажмите Enter для продолжения...")

            elif choice == '5':
                clear_screen()
                manager.show_tasks(show_all=True)
                try:
                    task_id = int(input("\nВведите ID задачи для удаления: ").strip())
                    confirm = input(f"Вы уверены, что хотите удалить задачу {task_id}? (да/нет): ").strip().lower()
                    if confirm == 'да':
                        manager.delete_task(task_id)
                except ValueError:
                    print("❌ Введите корректный номер задачи")
                input("\nНажмите Enter для продолжения...")

            elif choice == '6':
                clear_screen()
                manager.get_statistics()
                input("\nНажмите Enter для продолжения...")

            elif choice == '7':
                print("\n💾 Данные сохранены. До свидания!")
                break

            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                input("\nНажмите Enter для продолжения...")

        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем")
            break
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()