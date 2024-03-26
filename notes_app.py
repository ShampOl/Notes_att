import csv
import os
from datetime import datetime


class Note:
    def __init__(self, note_id, title, body, created_at=None, updated_at=None):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at if updated_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"ID: {self.note_id}\nЗаголовок: {self.title}\nТекст: {self.body}\nСоздано: {self.created_at}\nОбновлено: {self.updated_at}"


class NotesApp:
    def __init__(self):
        self.notes = []

    def load_notes(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.notes.append(Note(int(row['ID']), row['Заголовок'], row['Текст'], row['Создано'], row['Обновлено']))

    def save_notes(self, file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Заголовок', 'Текст', 'Создано', 'Обновлено']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    'ID': note.note_id,
                    'Заголовок': note.title,
                    'Текст': note.body,
                    'Создано': note.created_at,
                    'Обновлено': note.updated_at
                })

    def create_note(self, title, body):
        note_id = len(self.notes) + 1
        new_note = Note(note_id, title, body)
        self.notes.append(new_note)
        self.save_notes('notes.csv')  # Сохранение заметки сразу после создания
        return new_note

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes('notes.csv')  # Сохранение заметки сразу после редактирования
                return note
        return None

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes('notes.csv')  # Сохранение заметки сразу после удаления
                return True
        return False

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def get_all_notes(self):
        return self.notes

    def filter_notes_by_date(self, date, mode='created'):
        filtered_notes = []
        for note in self.notes:
            if mode == 'created':
                if note.created_at.startswith(date):
                    filtered_notes.append(note)
            elif mode == 'updated':
                if note.updated_at.startswith(date):
                    filtered_notes.append(note)
        return filtered_notes


def main():
    notes_app = NotesApp()
    notes_app.load_notes('notes.csv')

    while True:
        print("\n🙋Меню приложения Заметки🙋")
        print("📝1. Создать заметку")
        print("📑2. Редактировать заметку")
        print("❌3. Удалить заметку")
        print("👀4. Просмотреть заметку")
        print("📅5. Просмотреть все заметки")
        print("⏳6. Фильтр заметок по дате")
        print("👋7. Выйти")

        choice = input("Введите Ваш выбор👉: ")

        if choice == '1':
            title = input("Введите заголовок заметки: ")
            body = input("Введите текст заметки: ")
            note = notes_app.create_note(title, body)
            print(f"Заметка успешно создана с ID: {note.note_id}✅")

        elif choice == '2':
            note_id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок: ")
            body = input("Введите новый текст: ")
            if notes_app.edit_note(note_id, title, body):
                print("Заметка успешно отредактирована✅")
            else:
                print("Заметка не найдена❌")

        elif choice == '3':
            note_id = int(input("Введите ID заметки для удаления: "))
            if notes_app.delete_note(note_id):
                print("Заметка успешно удалена✅")
            else:
                print("Заметка не найдена❌")
        elif choice == '4':
            note_id = int(input("Введите ID заметки для просмотра: "))
            note = notes_app.get_note_by_id(note_id)
            if note:
                print(note)
            else:
                print("Заметка не найдена❌")

        elif choice == '5':
            all_notes = notes_app.get_all_notes()
            if all_notes:
                for note in all_notes:
                    print(note)
            else:
                print("Заметок нет❌")
        
        elif choice == '6':
            date = input("Введите дату (ГГГГ-ММ-ДД): ")
            filtered_notes = notes_app.filter_notes_by_date(date)
            if filtered_notes:
                print("Отфильтрованные заметки✅:")
                for note in filtered_notes:
                    print(note)
            else:
                print("Заметки не найдены для указанной даты❌")

        elif choice == '7':
            notes_app.save_notes('notes.csv')
            print("🌞Выход из приложения Заметки. До свидания!🌞")
            break
        else:
                print("❌Неверный выбор. Пожалуйста, введите число от 1 до 7❌")
        

if __name__ == "__main__":
    main()
