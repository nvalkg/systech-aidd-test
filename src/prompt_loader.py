"""Загрузчик и парсер системных промптов"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptLoader:
    """Загрузчик и парсер системных промптов"""

    def __init__(self, prompt_text: str | None = None, prompt_file: str | None = None) -> None:
        """
        Инициализация загрузчика промптов

        Args:
            prompt_text: Текст промпта (если не используется файл)
            prompt_file: Путь к файлу с промптом (приоритет над prompt_text)
        """
        self.prompt_text = prompt_text or "You are a helpful AI assistant."
        self.prompt_file = prompt_file
        self.full_prompt = self._load_prompt()
        self.role_name = self._parse_role_name()

    def _load_prompt(self) -> str:
        """Загрузить промпт из файла или использовать текст"""
        if self.prompt_file:
            try:
                prompt_path = Path(self.prompt_file)
                content = prompt_path.read_text(encoding="utf-8").strip()
                logger.info(f"Промпт загружен из файла: {self.prompt_file}")
                return content
            except FileNotFoundError:
                logger.warning(f"Файл {self.prompt_file} не найден, используется текст промпта")

        return self.prompt_text

    def _parse_role_name(self) -> str:
        """Извлечь название роли из промпта"""
        # Ищем строку "Роль: <название>"
        match = re.search(r"^Роль:\s*(.+)$", self.full_prompt, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "AI Assistant"

    def get_system_prompt(self) -> str:
        """Получить полный системный промпт для LLM"""
        return self.full_prompt

    def get_role_name(self) -> str:
        """Получить название роли"""
        return self.role_name

    def get_role_description(self) -> str:
        """Получить форматированное описание роли для команды /role"""
        # Извлекаем первые несколько строк после "Роль:"
        lines = self.full_prompt.split("\n")
        description_lines = []

        # Находим индекс строки с ролью
        role_line_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("Роль:"):
                role_line_idx = i
                break

        # Берем до 5 строк после роли
        if role_line_idx >= 0:
            for line in lines[role_line_idx + 1 : role_line_idx + 6]:
                stripped = line.strip()
                if stripped and not stripped.startswith("---"):
                    description_lines.append(stripped)

        description = "\n".join(description_lines) if description_lines else ""

        return f"🤖 Моя роль: {self.role_name}\n\n{description}"
