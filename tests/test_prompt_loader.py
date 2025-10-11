"""Тесты для PromptLoader - загрузки и парсинга системных промптов"""

from pathlib import Path

from src.prompt_loader import PromptLoader


class TestPromptLoaderInit:
    """Тесты инициализации PromptLoader"""

    def test_prompt_loader_init_default(self) -> None:
        """Тест: инициализация без параметров использует дефолтный промпт"""
        # Arrange & Act
        loader = PromptLoader()

        # Assert
        assert loader.get_system_prompt() == "You are a helpful AI assistant."
        assert loader.get_role_name() == "AI Assistant"

    def test_prompt_loader_init_with_text(self) -> None:
        """Тест: инициализация с текстом промпта"""
        # Arrange
        custom_prompt = "Роль: Custom Assistant\n\nYou are a custom assistant."

        # Act
        loader = PromptLoader(prompt_text=custom_prompt)

        # Assert
        assert loader.get_system_prompt() == custom_prompt
        assert loader.get_role_name() == "Custom Assistant"

    def test_prompt_loader_init_with_file(self, tmp_path: Path) -> None:
        """Тест: загрузка промпта из файла"""
        # Arrange: создаём временный файл с промптом
        prompt_file = tmp_path / "test_prompt.txt"
        prompt_content = "Роль: File Assistant\n\nLoaded from file."
        prompt_file.write_text(prompt_content, encoding="utf-8")

        # Act
        loader = PromptLoader(prompt_file=str(prompt_file))

        # Assert
        assert loader.get_system_prompt() == prompt_content
        assert loader.get_role_name() == "File Assistant"

    def test_prompt_loader_file_not_found(self) -> None:
        """Тест: обработка отсутствующего файла - fallback на текст"""
        # Arrange
        non_existent_file = "non_existent_prompt.txt"
        fallback_text = "Роль: Fallback Assistant\n\nFallback prompt."

        # Act
        loader = PromptLoader(prompt_text=fallback_text, prompt_file=non_existent_file)

        # Assert: должен использовать fallback текст
        assert loader.get_system_prompt() == fallback_text
        assert loader.get_role_name() == "Fallback Assistant"


class TestPromptLoaderParsing:
    """Тесты парсинга информации из промпта"""

    def test_prompt_loader_parse_role_name(self) -> None:
        """Тест: парсинг названия роли из строки 'Роль: ...'"""
        # Arrange
        prompt_with_role = "Роль: Python Expert\n\nYou are a Python expert."

        # Act
        loader = PromptLoader(prompt_text=prompt_with_role)

        # Assert
        assert loader.get_role_name() == "Python Expert"

    def test_prompt_loader_parse_role_missing(self) -> None:
        """Тест: промпт без строки 'Роль:' возвращает дефолтное название"""
        # Arrange
        prompt_without_role = "You are a helpful assistant without explicit role."

        # Act
        loader = PromptLoader(prompt_text=prompt_without_role)

        # Assert
        assert loader.get_role_name() == "AI Assistant"

    def test_prompt_loader_get_system_prompt(self) -> None:
        """Тест: получение полного системного промпта для LLM"""
        # Arrange
        full_prompt = """Роль: Test Assistant

You are a test assistant with multiple lines.

Key features:
- Feature 1
- Feature 2

End of prompt."""

        # Act
        loader = PromptLoader(prompt_text=full_prompt)

        # Assert
        assert loader.get_system_prompt() == full_prompt

    def test_prompt_loader_get_role_description(self) -> None:
        """Тест: форматирование описания роли для команды /role"""
        # Arrange
        prompt = """Роль: Code Reviewer

Ты - опытный разработчик, специализирующийся на code review.

Твои принципы:
- SOLID, DRY, KISS
- Type hints обязательны"""

        # Act
        loader = PromptLoader(prompt_text=prompt)
        description = loader.get_role_description()

        # Assert
        assert "🤖 Моя роль: Code Reviewer" in description
        assert "опытный разработчик" in description

    def test_prompt_loader_priority_file_over_text(self, tmp_path: Path) -> None:
        """Тест: приоритет файла над текстом при наличии обоих"""
        # Arrange
        prompt_file = tmp_path / "priority_test.txt"
        file_content = "Роль: File Priority\n\nFile has priority."
        prompt_file.write_text(file_content, encoding="utf-8")

        text_content = "Роль: Text Priority\n\nText should be ignored."

        # Act
        loader = PromptLoader(prompt_text=text_content, prompt_file=str(prompt_file))

        # Assert: должен использовать файл, а не текст
        assert loader.get_system_prompt() == file_content
        assert loader.get_role_name() == "File Priority"
