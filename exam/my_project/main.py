from notes_manager import NotesManager

if __name__ == "__main__":
    manager = NotesManager()

    results = manager.search_notes("демо")
    print(f"Найдено заметок: {len(results)}")

    # manager.display_all()
    manager.console_control()