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

langs = [
    ProgrammingLanguage(1, "Python"),
    ProgrammingLanguage(2, "Java"),
    ProgrammingLanguage(3, "C++"),
    ProgrammingLanguage(4, "JavaScript"),
    ProgrammingLanguage(5, "Ada"),  # Добавим язык на "А"
]

tools = [
    DevelopmentTool(1, "PyCharm Professional", 199, 1),
    DevelopmentTool(2, "IntelliJ IDEA Ultimate", 249, 2),
    DevelopmentTool(3, "Visual Studio Enterprise", 299, 3),
    DevelopmentTool(4, "VS Code", 0, 4),
    DevelopmentTool(5, "Eclipse IDE", 0, 2),
    DevelopmentTool(6, "GNAT Programming Studio", 150, 5),  # Для языка Ada
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


def main():
    print("Запрос 1:")
    query1 = [(tool.name, next(lang.name for lang in langs if lang.id == tool.lang_id))
              for tool in tools if tool.name.endswith('ov') or tool.name.endswith('OV')]
    print("Средства разработки с названиями на 'ov':", query1)

    print("\nЗапрос 1 (альтернатива - окончание 'Studio'):")
    query1_alt = [(tool.name, next(lang.name for lang in langs if lang.id == tool.lang_id))
                  for tool in tools if tool.name.endswith('Studio')]
    print(query1_alt)

    print("\nЗапрос 2:")
    lang_tool_stats = {}
    for lang in langs:
        lang_tools = [tool for tool in tools if tool.lang_id == lang.id]
        if lang_tools:
            total_cost = sum(tool.license_cost for tool in lang_tools)
            count = len(lang_tools)
            avg_cost = total_cost / count
            lang_tool_stats[lang.name] = avg_cost

    query2 = sorted(lang_tool_stats.items(), key=lambda x: x[1])
    print("Языки программирования со средней стоимостью инструментов:")
    for lang, avg_cost in query2:
        print(f"{lang}: {avg_cost:.2f}")

    print("\nЗапрос 3:")
    query3 = []
    for lang in langs:
        if lang.name.startswith('A'):
            supporting_tools = []
            for tl in tool_langs:
                if tl.lang_id == lang.id:
                    tool = next((t for t in tools if t.id == tl.tool_id), None)
                    if tool:
                        supporting_tools.append(tool.name)
            query3.append((lang.name, supporting_tools))

    print("Языки на 'A' и их инструменты (многие-ко-многим):")
    for lang_name, tool_list in query3:
        print(f"{lang_name}: {', '.join(tool_list)}")


if __name__ == "__main__":
    main()