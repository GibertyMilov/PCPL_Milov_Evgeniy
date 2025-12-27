# test_programming_tools.py

import unittest
from programming_tools import (
    ProgrammingLanguage,
    DevelopmentTool,
    ToolLanguage,
    ProgrammingToolsService,
    create_sample_data
)


class TestProgrammingToolsService(unittest.TestCase):
    """Тесты для сервиса работы с инструментами разработки"""

    def setUp(self):
        """Настройка тестовых данных перед каждым тестом"""
        self.service = ProgrammingToolsService()
        langs, tools, tool_langs = create_sample_data()
        self.service.set_data(langs, tools, tool_langs)

    def test_get_tools_by_name_ending(self):
        """Тест 1: Поиск инструментов по окончанию названия"""
        # Тестируем окончание 'Studio'
        result = self.service.get_tools_by_name_ending('Studio')

        # Проверяем количество найденных инструментов
        self.assertEqual(len(result), 1)

        # Проверяем содержимое результата
        tool_name, lang_name = result[0]
        self.assertEqual(tool_name, "GNAT Programming Studio")
        self.assertEqual(lang_name, "Ada")

        # Тестируем окончание, которого нет
        result_empty = self.service.get_tools_by_name_ending('XYZ')
        self.assertEqual(len(result_empty), 0)

    def test_get_average_tool_cost_by_language(self):
        """Тест 2: Расчет средней стоимости инструментов по языкам"""
        result = self.service.get_average_tool_cost_by_language()

        # Проверяем, что результат - это список кортежей
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, tuple) for item in result))

        # Проверяем количество языков с инструментами
        # В тестовых данных все 5 языков имеют инструменты
        self.assertEqual(len(result), 5)

        # Проверяем, что результат отсортирован по возрастанию средней стоимости
        costs = [cost for _, cost in result]
        self.assertEqual(costs, sorted(costs))

        # Проверяем конкретные значения
        # JavaScript (VS Code - бесплатный)
        js_avg = next(cost for lang, cost in result if lang == "JavaScript")
        self.assertEqual(js_avg, 0.0)

        # Java (IntelliJ IDEA Ultimate: 249, Eclipse IDE: 0)
        java_avg = next(cost for lang, cost in result if lang == "Java")
        self.assertEqual(java_avg, (249 + 0) / 2)

    def test_get_languages_starting_with_letter(self):
        """Тест 3: Поиск языков по первой букве и их инструментов"""
        # Тестируем поиск языков на 'A'
        result = self.service.get_languages_starting_with_letter('A')

        # Проверяем количество найденных языков
        self.assertEqual(len(result), 1)

        # Проверяем содержимое результата
        lang_name, tool_list = result[0]
        self.assertEqual(lang_name, "Ada")

        # Проверяем инструменты для Ada
        self.assertIn("GNAT Programming Studio", tool_list)
        self.assertIn("AdaCore", tool_list)
        self.assertEqual(len(tool_list), 2)

        # Тестируем поиск языков на букву, которой нет
        result_empty = self.service.get_languages_starting_with_letter('X')
        self.assertEqual(len(result_empty), 0)

        # Тестируем поиск языков на 'J' (Java, JavaScript)
        result_j = self.service.get_languages_starting_with_letter('J')
        self.assertEqual(len(result_j), 2)
        lang_names = [lang for lang, _ in result_j]
        self.assertIn("Java", lang_names)
        self.assertIn("JavaScript", lang_names)

    def test_get_language_by_id(self):
        """Дополнительный тест: Поиск языка по ID"""
        # Тестируем существующий язык
        lang = self.service.get_language_by_id(1)
        self.assertIsNotNone(lang)
        self.assertEqual(lang.name, "Python")

        # Тестируем несуществующий язык
        lang_none = self.service.get_language_by_id(999)
        self.assertIsNone(lang_none)

    def test_get_tool_by_id(self):
        """Дополнительный тест: Поиск инструмента по ID"""
        # Тестируем существующий инструмент
        tool = self.service.get_tool_by_id(4)
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "VS Code")
        self.assertEqual(tool.license_cost, 0)

        # Тестируем несуществующий инструмент
        tool_none = self.service.get_tool_by_id(999)
        self.assertIsNone(tool_none)


class TestDataModels(unittest.TestCase):
    """Тесты для моделей данных"""

    def test_programming_language_creation(self):
        """Тест создания объекта ProgrammingLanguage"""
        lang = ProgrammingLanguage(10, "TestLang")
        self.assertEqual(lang.id, 10)
        self.assertEqual(lang.name, "TestLang")

    def test_development_tool_creation(self):
        """Тест создания объекта DevelopmentTool"""
        tool = DevelopmentTool(20, "TestTool", 100, 10)
        self.assertEqual(tool.id, 20)
        self.assertEqual(tool.name, "TestTool")
        self.assertEqual(tool.license_cost, 100)
        self.assertEqual(tool.lang_id, 10)

    def test_tool_language_creation(self):
        """Тест создания объекта ToolLanguage"""
        tl = ToolLanguage(20, 10)
        self.assertEqual(tl.tool_id, 20)
        self.assertEqual(tl.lang_id, 10)


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2)