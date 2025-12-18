import json
import os
from datetime import datetime

class NotesManager:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        """Загрузка заметок из JSON файла"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"notes": [], "last_id": 0}

    def save_notes(self):
        """Сохранение заметок в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def add_note(self, title, content, tags=None):
        """Добавление новой заметки"""
        new_id = self.notes["last_id"] + 1
        note = {
            "id": new_id,
            "title": title,
            "content": content,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "tags": tags or []
        }
        self.notes["notes"].append(note)
        self.notes["last_id"] = new_id
        self.save_notes()
        return new_id

    def get_note(self, note_id):
        """Поиск заметки по ID"""
        for note in self.notes["notes"]:
            if note["id"] == note_id:
                return note
        return None

    def display_note(self, note, width=70):
        """Отображение одной заметки в терминале"""
        print("\n" + "=" * width)
        print(f"ЗАМЕТКА #{note['id']}".center(width))
        print("=" * width)

        title_lines = note['title'].split('\n')
        for line in title_lines:
            print(f"  {line}")

        print("-" * width)

        print("Содержание:")
        content_lines = note['content'].split('\n')
        for i, line in enumerate(content_lines):
            print(f"  {line}")

        print("-" * width)

        if note.get('tags'):
            tags_str = ", ".join([f"#{tag}" for tag in note['tags']])
            print(f"Теги: {tags_str}")

        print(f"Создана: {note['created']}")
        if note.get('updated'):
            print(f"Обновлена: {note['updated']}")

        print("=" * width + "\n")

    def display_all(self):
        """Отображение всех заметок в терминале"""
        for note in self.notes["notes"]:
            self.display_note(note)

    def delete_note(self, note_id):
        """Удаление заметки по ID"""
        self.notes["notes"] = [
            note for note in self.notes["notes"]
            if note["id"] != note_id
        ]
        self.save_notes()

    def search_notes(self, keyword):
        """Поиск заметок по ключевому слову"""
        results = []
        for note in self.notes["notes"]:
            if (keyword.lower() in note["title"].lower() or
                keyword.lower() in note["content"].lower()):
                results.append(note)
        return results

    def console_control(self):
        print("=" * 60)
        print("МЕНЕДЖЕР ЗАМЕТОК")
        print("=" * 60)

        mode = input("\nВыберите режим:\n1. Вывод всех заметок\n2. Вывод одной заметки\n3. Новая заметка\n4. Удалить заметку\n> ").strip()

        try:
            if mode == "1":
                self.display_all()
            elif mode == "2":
                while (True):
                    try:
                        num = int(input("Введите номер заметки: "))
                        break
                    except:
                        print("Ошибка, такой заявки нет, пожалуйста, повторите попытку")
                self.display_note(self.get_note(num))
            elif mode == "3":
                title = input()
                content = input()
                tags = input().split()
                self.add_note(title=title, content=content, tags=tags)
            elif mode == "4":
                while (True):
                    try:
                        num = int(input("Введите номер заметки: "))
                        break
                    except:
                        print("Ошибка, такой заявки нет, пожалуйста, повторите попытку")
                self.delete_note(num)
        except:
            print("Ошибка! Попробуйте снова")
