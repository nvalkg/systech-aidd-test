# DevOps Documentation

Документация по DevOps процессам проекта AIDD Bot.

## 📋 Общая информация

- **[DevOps Roadmap](devops-roadmap.md)** - роадмап развития DevOps процессов

## 📖 Руководства (Guides)

### Docker

- **[Docker Quickstart](guides/docker-quickstart.md)** - быстрый старт с Docker
  - Локальная сборка и запуск
  - Использование образов из GitHub Container Registry
  - Troubleshooting

### GitHub Actions & CI/CD

- **[GitHub Actions Intro](guides/github-actions-intro.md)** - введение в GitHub Actions
  - Workflows, jobs, steps
  - Триггеры и события
  - Matrix strategy
  - GitHub Container Registry
  - Best practices

- **[Make Images Public](guides/make-images-public.md)** - как сделать образы публичными
  - Пошаговая инструкция с скриншотами
  - Проверка публичного доступа
  - FAQ

## 📝 Планы спринтов (Plans)

Детальные планы реализации для каждого спринта:

- **[D0: Basic Docker Setup](plans/d0-basic-docker-setup.md)** ✅ Completed
  - Dockerfile для bot, api, frontend
  - docker-compose.yml для локального запуска
  - Миграции и entrypoint

- **[D1: Build & Publish](plans/d1-build-publish.md)** 🚧 In Progress
  - GitHub Actions workflow
  - Автоматическая сборка и публикация
  - docker-compose.registry.yml

- **D2: Развертывание на сервер** 📋 Planned
  - Ручное развертывание
  - SSH доступ
  - Production конфигурация

- **D3: Auto Deploy** 📋 Planned
  - Автоматическое развертывание
  - workflow_dispatch триггер
  - Уведомления

## 📊 Отчеты (Reports)

### Спринт D0

- **[D0 Summary](reports/d0-summary.md)** - краткий итоговый отчет
- **[D0 Testing Report](reports/d0-testing-report.md)** - результаты тестирования

### Спринт D1

- **[D1 Summary](reports/d1-summary.md)** - краткий итоговый отчет (в процессе)
- **[D1 Testing Report](reports/d1-testing-report.md)** - чеклист для тестирования (шаблон)

## 🗂️ Структура документации

```
devops/doc/
├── README.md                    # Этот файл
├── devops-roadmap.md           # Общий роадмап
├── guides/                     # Руководства
│   ├── docker-quickstart.md
│   ├── github-actions-intro.md
│   └── make-images-public.md
├── plans/                      # Детальные планы спринтов
│   ├── d0-basic-docker-setup.md
│   └── d1-build-publish.md
└── reports/                    # Отчеты о выполнении
    ├── d0-summary.md
    ├── d0-testing-report.md
    ├── d1-summary.md
    └── d1-testing-report.md
```

## 🚀 Быстрая навигация

### Я хочу...

| Задача | Документ |
|--------|----------|
| Запустить проект локально через Docker | [Docker Quickstart](guides/docker-quickstart.md) |
| Использовать готовые образы из registry | [Docker Quickstart → Registry](guides/docker-quickstart.md#использование-образов-из-github-container-registry) |
| Понять как работает CI/CD | [GitHub Actions Intro](guides/github-actions-intro.md) |
| Сделать образы публичными | [Make Images Public](guides/make-images-public.md) |
| Узнать план развития DevOps | [DevOps Roadmap](devops-roadmap.md) |
| Посмотреть план текущего спринта | [Plans](plans/) |
| Узнать результаты тестирования | [Reports](reports/) |

### По типу задачи

#### Разработка
- Локальная разработка → [Docker Quickstart](guides/docker-quickstart.md)
- Изменение Dockerfile → [D0 Plan](plans/d0-basic-docker-setup.md)

#### DevOps
- Настройка CI/CD → [GitHub Actions Intro](guides/github-actions-intro.md)
- Автоматическая сборка → [D1 Plan](plans/d1-build-publish.md)
- Публикация образов → [Make Images Public](guides/make-images-public.md)

#### Production
- Ручной deploy → [D2 Plan](plans/) (скоро)
- Автоматический deploy → [D3 Plan](plans/) (скоро)

## 📚 Внешние ресурсы

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

### GitHub Container Registry
- [Working with Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Publishing Docker images](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

## 🤝 Вклад в документацию

При добавлении новой документации:

1. **Руководства** (guides/) - практические how-to инструкции
2. **Планы** (plans/) - детальные планы реализации спринтов
3. **Отчеты** (reports/) - результаты и выводы после завершения

Обновите этот README при добавлении новых документов.

## 📞 Поддержка

Если у вас есть вопросы по DevOps процессам:

1. Проверьте [DevOps Roadmap](devops-roadmap.md) - возможно, это запланировано
2. Посмотрите соответствующее руководство в [guides/](guides/)
3. Создайте issue в репозитории

---

**Последнее обновление:** 18.10.2025
**Версия:** 1.1
