# Следующие шаги для завершения Спринта D1

Этот документ описывает оставшиеся шаги для завершения Спринта D1 - Build & Publish.

## ✅ Что уже сделано

- [x] Создан GitHub Actions workflow (`.github/workflows/build.yml`)
- [x] Настроена matrix strategy для параллельной сборки 3 образов
- [x] Добавлено кэширование Docker слоев
- [x] Создан `docker-compose.registry.yml` для работы с образами из GHCR
- [x] Написана документация (GitHub Actions intro, обновлен Docker Quickstart)
- [x] Добавлены badges в README
- [x] Созданы шаблоны отчетов для тестирования

## 🔄 Что нужно сделать

### Шаг 1: Создать тестовую ветку и закоммитить изменения

```bash
# Создать ветку для тестирования
git checkout -b devops/d1-ci

# Добавить все новые файлы
git add .

# Закоммитить
git commit -m "feat(devops): Add GitHub Actions workflow for Docker images build & publish

- Add .github/workflows/build.yml with matrix strategy
- Add docker-compose.registry.yml for registry images
- Add comprehensive documentation (GitHub Actions intro, make-images-public guide)
- Update Docker Quickstart with registry usage
- Add badges and update README files
- Create testing report templates

Part of Sprint D1: Build & Publish
"

# Push в ветку
git push origin devops/d1-ci
```

### Шаг 2: Проверить первую сборку

1. **Откройте GitHub:**
   - Перейдите в репозиторий
   - Вкладка **Actions**

2. **Проверьте workflow:**
   - Должен запуститься workflow "Build & Publish Docker Images"
   - Проверьте, что все 3 job (bot, api, frontend) запустились
   - Дождитесь завершения сборки

3. **Проверьте логи:**
   - Откройте каждый job
   - Убедитесь что образы собрались без ошибок
   - Проверьте что образы опубликованы в GHCR

**Ожидаемый результат:**
- ✅ Все jobs completed successfully
- ✅ Образы опубликованы в ghcr.io
- ✅ Доступны теги `latest` и `devops/d1-ci-<sha>`

### Шаг 3: Сделать образы публичными

После первой публикации образы будут приватными. Нужно сделать их публичными:

1. **Перейдите на GitHub Packages:**
   ```
   https://github.com/nvalkg?tab=packages
   ```

2. **Для каждого образа (aidd-bot, aidd-api, aidd-frontend):**
   - Откройте пакет
   - **Package settings** → **Danger Zone** → **Change visibility**
   - Выберите **Public**
   - Введите имя пакета для подтверждения
   - Нажмите **I understand the consequences, change package visibility**

3. **Проверьте результат:**
   - Каждый пакет должен показывать badge **Public**

📖 **Детальная инструкция:** [devops/doc/guides/make-images-public.md](doc/guides/make-images-public.md)

### Шаг 4: Проверить публичный доступ

Убедитесь, что образы доступны без авторизации:

```bash
# Выйдите из registry (если авторизованы)
docker logout ghcr.io

# Попробуйте скачать образы
docker pull ghcr.io/nvalkg/aidd-bot:latest
docker pull ghcr.io/nvalkg/aidd-api:latest
docker pull ghcr.io/nvalkg/aidd-frontend:latest
```

**Ожидаемый результат:**
- ✅ Все образы скачались успешно
- ✅ Не требовалась авторизация

### Шаг 5: Локальное тестирование с образами из registry

```bash
# Перейдите в devops директорию
cd devops

# Укажите GitHub username (или создайте .env файл)
export GITHUB_USERNAME=nvalkg

# Скачайте образы
docker-compose -f docker-compose.registry.yml pull

# Запустите сервисы
docker-compose -f docker-compose.registry.yml up
```

**Что проверить:**
- [ ] PostgreSQL запустился (healthcheck passed)
- [ ] Bot запустился и миграции выполнены
- [ ] API доступен на http://localhost:8000
- [ ] API health: `curl http://localhost:8000/api/health`
- [ ] Frontend доступен на http://localhost:3000
- [ ] Telegram бот отвечает на `/start`

### Шаг 6: Заполнить отчет о тестировании

Откройте `devops/doc/reports/d1-testing-report.md` и заполните:

- [ ] Результаты проверки workflow
- [ ] Время сборки (первая и повторная)
- [ ] Результаты smoke tests
- [ ] Обнаруженные проблемы (если есть)
- [ ] Скриншоты или логи

**Критерии успеха:**
- ✅ Все тесты пройдены
- ✅ Образы публичные и доступны
- ✅ docker-compose.registry.yml работает
- ✅ Все сервисы функционируют корректно

### Шаг 7: Создать Pull Request в main

После успешного тестирования:

```bash
# Убедитесь что все изменения закоммичены
git status

# Создайте PR через GitHub CLI
gh pr create --title "feat(devops): Sprint D1 - Build & Publish" \
  --body "## Спринт D1: Build & Publish

### Реализовано:
- GitHub Actions workflow для автоматической сборки и публикации
- Matrix strategy для параллельной сборки 3 образов
- docker-compose.registry.yml для использования образов из GHCR
- Кэширование Docker слоев
- Подробная документация и руководства

### Тестирование:
- [x] Workflow успешно собирает все образы
- [x] Образы опубликованы в ghcr.io
- [x] Образы сделаны публичными
- [x] Smoke tests пройдены
- [x] Все сервисы работают корректно

Closes #[номер issue если есть]

Документация: devops/doc/plans/d1-build-publish.md
"

# Или создайте PR через web UI
```

**В PR должны быть:**
- ✅ Описание изменений
- ✅ Ссылка на план спринта
- ✅ Результаты тестирования
- ✅ Скриншоты (опционально)

### Шаг 8: Проверить сборку на PR

После создания PR:

1. **Проверьте автоматические проверки:**
   - Должен запуститься workflow
   - Образы должны собраться (но **не публиковаться**)
   - Все проверки должны пройти

2. **Review и merge:**
   - Код ревью (если применимо)
   - Merge в main

### Шаг 9: Проверить сборку после merge

После merge в main:

1. **Проверьте workflow:**
   - Должен запуститься автоматически
   - Образы должны собраться и опубликоваться
   - Теги: `latest` и `main-<sha>`

2. **Проверьте образы:**
   ```bash
   docker pull ghcr.io/nvalkg/aidd-bot:latest
   docker pull ghcr.io/nvalkg/aidd-api:latest
   docker pull ghcr.io/nvalkg/aidd-frontend:latest
   ```

3. **Проверьте badge:**
   - Откройте README.md на GitHub
   - Badge "Build Status" должен показывать "passing"

### Шаг 10: Удалить временный триггер

После успешного merge и проверки:

```bash
# Откройте .github/workflows/build.yml
# Удалите строку: - devops/d1-ci

# Было:
on:
  push:
    branches:
      - main
      - devops/d1-ci  # <-- удалить эту строку

# Стало:
on:
  push:
    branches:
      - main

# Закоммитить и запушить
git add .github/workflows/build.yml
git commit -m "chore(ci): Remove temporary devops/d1-ci trigger"
git push origin main
```

### Шаг 11: Финализация документации

1. **Заполнить итоговый отчет:**
   - Откройте `devops/doc/reports/d1-summary.md`
   - Заполните секции:
     - Дата завершения
     - Извлеченные уроки
     - Метрики (время выполнения)
     - Заключение

2. **Обновить roadmap:**
   - Откройте `devops/doc/devops-roadmap.md`
   - Измените статус D1 на "✅ Completed"
   - Укажите дату завершения

```markdown
| D1 | Build & Publish | ✅ Completed | [План спринта](plans/d1-build-publish.md) | 18.10.2025 |
```

3. **Закоммитить финальные изменения:**
   ```bash
   git add devops/doc/
   git commit -m "docs(devops): Complete Sprint D1 documentation"
   git push origin main
   ```

### Шаг 12: Удалить тестовую ветку (опционально)

```bash
# Локально
git branch -d devops/d1-ci

# На GitHub
git push origin --delete devops/d1-ci
```

## ✅ Критерии завершения спринта

Спринт D1 считается завершенным когда:

- [x] GitHub Actions workflow работает и образы собираются
- [x] Образы публикуются в ghcr.io при push в main
- [x] Образы публичные (доступны без авторизации)
- [x] docker-compose.registry.yml работает корректно
- [x] Все сервисы запускаются из образов registry
- [x] Документация полная и актуальная
- [x] Тестирование завершено, отчеты заполнены
- [x] Badge статуса сборки показывает "passing"
- [x] PR смержен в main
- [x] Roadmap обновлен

## 🎯 Готовность к следующему спринту

После завершения D1 будет готово для D2 (Развертывание на сервер):

- ✅ Образы в публичном registry
- ✅ Автоматическая сборка при изменениях
- ✅ Возможность pull образов на любой сервер
- ✅ docker-compose.registry.yml для деплоя

## 📚 Полезные ссылки

- **План спринта:** [devops/doc/plans/d1-build-publish.md](doc/plans/d1-build-publish.md)
- **Отчет о тестировании:** [devops/doc/reports/d1-testing-report.md](doc/reports/d1-testing-report.md)
- **GitHub Actions Intro:** [devops/doc/guides/github-actions-intro.md](doc/guides/github-actions-intro.md)
- **Make Images Public:** [devops/doc/guides/make-images-public.md](doc/guides/make-images-public.md)
- **Quick Reference:** [devops/QUICK-REFERENCE.md](QUICK-REFERENCE.md)

## 🆘 Проблемы?

Если что-то пошло не так:

1. **Workflow failed:**
   - Проверьте логи в GitHub Actions
   - Убедитесь что Dockerfile корректны
   - Проверьте permissions в workflow

2. **Образы не публикуются:**
   - Проверьте что push в правильную ветку (main или devops/d1-ci)
   - Убедитесь что условие `github.event_name == 'push'` выполнено

3. **Не могу скачать образы:**
   - Проверьте что образы публичные на GitHub
   - Убедитесь что username правильный

4. **docker-compose.registry.yml не работает:**
   - Проверьте переменную GITHUB_USERNAME
   - Убедитесь что образы существуют в registry

**Дополнительная помощь:** См. [devops/doc/guides/docker-quickstart.md](doc/guides/docker-quickstart.md) секция Troubleshooting

---

**Создано:** 18.10.2025
**Обновлено:** 18.10.2025
**Версия:** 1.0
