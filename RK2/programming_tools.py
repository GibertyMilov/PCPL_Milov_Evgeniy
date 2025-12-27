# programming_tools.py

class ProgrammingLanguage:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class DevelopmentTool:
    def __init__(self, id, name, license_cost, lang_id=None):
        self.id = id
        self.name = name
        self.license_cost = license_cost
        self.lang_id = lang_id


class ToolLanguage:
    def __init__(self, tool_id, lang_id):
        self.tool_id = tool_id
        self.lang_id = lang_id


class ProgrammingToolsService:
    def __init__(self, langs=None, tools=None, tool_langs=None):
        """Инициализация сервиса с данными"""
        self.langs = langs or []
        self.tools = tools or []
        self.tool_langs = tool_langs or []

    def set_data(self, langs, tools, tool_langs):
        """Установка данных"""
        self.langs = langs
        self.tools = tools
        self.tool_langs = tool_langs

    def get_tools_by_name_ending(self, ending):
        """Получить инструменты с названиями, оканчивающимися на заданное окончание"""
        result = []
        for tool in self.tools:
            if tool.name.endswith(ending):
                # Находим язык программирования для инструмента
                lang = next((l for l in self.langs if l.id == tool.lang_id), None)
                lang_name = lang.name if lang else "Unknown"
                result.append((tool.name, lang_name))
        return result

    def get_average_tool_cost_by_language(self):
        """Получить среднюю стоимость инструментов по языкам программирования"""
        lang_tool_stats = {}

        for lang in self.langs:
            # Находим инструменты для этого языка (один-ко-многим)
            lang_tools = [tool for tool in self.tools if tool.lang_id == lang.id]

            if lang_tools:
                total_cost = sum(tool.license_cost for tool in lang_tools)
                count = len(lang_tools)
                avg_cost = total_cost / count
                lang_tool_stats[lang.name] = avg_cost

        # Сортируем по средней стоимости
        return sorted(lang_tool_stats.items(), key=lambda x: x[1])

    def get_languages_starting_with_letter(self, letter):
        """Получить языки программирования, начинающиеся с заданной буквы, и их инструменты (многие-ко-многим)"""
        result = []

        for lang in self.langs:
            if lang.name.startswith(letter):
                supporting_tools = []

                # Находим связи многие-ко-многим через tool_langs
                for tl in self.tool_langs:
                    if tl.lang_id == lang.id:
                        tool = next((t for t in self.tools if t.id == tl.tool_id), None)
                        if tool:
                            supporting_tools.append(tool.name)

                result.append((lang.name, supporting_tools))

        return result

    def get_language_by_id(self, lang_id):
        """Получить язык программирования по ID"""
        return next((lang for lang in self.langs if lang.id == lang_id), None)

    def get_tool_by_id(self, tool_id):
        """Получить инструмент по ID"""
        return next((tool for tool in self.tools if tool.id == tool_id), None)


# Функции для работы с данными по умолчанию
def create_sample_data():
    """Создание тестовых данных"""
    langs = [
        ProgrammingLanguage(1, "Python"),
        ProgrammingLanguage(2, "Java"),
        ProgrammingLanguage(3, "C++"),
        ProgrammingLanguage(4, "JavaScript"),
        ProgrammingLanguage(5, "Ada"),
    ]

    tools = [
        DevelopmentTool(1, "PyCharm Professional", 199, 1),
        DevelopmentTool(2, "IntelliJ IDEA Ultimate", 249, 2),
        DevelopmentTool(3, "Visual Studio Enterprise", 299, 3),
        DevelopmentTool(4, "VS Code", 0, 4),
        DevelopmentTool(5, "Eclipse IDE", 0, 2),
        DevelopmentTool(6, "GNAT Programming Studio", 150, 5),
        DevelopmentTool(7, "AdaCore", 199, 5),
    ]

    tool_langs = [
        ToolLanguage(1, 1),
        ToolLanguage(2, 2),
        ToolLanguage(3, 3),
        ToolLanguage(4, 4),
        ToolLanguage(4, 1),
        ToolLanguage(4, 2),
        ToolLanguage(5, 2),
        ToolLanguage(5, 3),
        ToolLanguage(6, 5),
        ToolLanguage(7, 5),
    ]

    return langs, tools, tool_langs


def main():
    """Основная функция для демонстрации работы"""
    service = ProgrammingToolsService()
    langs, tools, tool_langs = create_sample_data()
    service.set_data(langs, tools, tool_langs)

    print("Запрос 1: Средства разработки с названиями на 'ov' или 'OV'")
    query1 = service.get_tools_by_name_ending('ov')
    if not query1:
        query1 = service.get_tools_by_name_ending('OV')
    print("Результат:", query1)

    print("\nЗапрос 1 (альтернатива - окончание 'Studio'):")
    query1_alt = service.get_tools_by_name_ending('Studio')
    print(query1_alt)

    print("\nЗапрос 2: Языки программирования со средней стоимостью инструментов:")
    query2 = service.get_average_tool_cost_by_language()
    for lang, avg_cost in query2:
        print(f"{lang}: {avg_cost:.2f}")

    print("\nЗапрос 3: Языки на 'A' и их инструменты (многие-ко-многим):")
    query3 = service.get_languages_starting_with_letter('A')
    for lang_name, tool_list in query3:
        print(f"{lang_name}: {', '.join(tool_list)}")


if __name__ == "__main__":
    main()