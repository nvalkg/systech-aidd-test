#!/bin/bash
# ============================================================================
# Скрипт проверки работоспособности развертывания AIDD Bot
# ============================================================================
#
# Использование:
#   bash deploy-check.sh
#
# Или на сервере:
#   chmod +x deploy-check.sh
#   ./deploy-check.sh
#

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Параметры
COMPOSE_FILE="docker-compose.prod.yml"
API_URL="http://localhost:8005"
FRONTEND_URL="http://localhost:3005"

# Счетчики
PASSED=0
FAILED=0

# ============================================================================
# Функции
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "$1 установлен ($(command -v $1))"
        return 0
    else
        print_error "$1 не установлен"
        return 1
    fi
}

# ============================================================================
# Проверки
# ============================================================================

print_header "Проверка системных требований"

# Проверка Docker
check_command docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_info "Версия: $DOCKER_VERSION"
fi

# Проверка Docker Compose
check_command docker-compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    print_info "Версия: $COMPOSE_VERSION"
fi

# Проверка curl
check_command curl

# ============================================================================

print_header "Проверка файлов"

# Проверка docker-compose.prod.yml
if [ -f "$COMPOSE_FILE" ]; then
    print_success "Файл $COMPOSE_FILE существует"
else
    print_error "Файл $COMPOSE_FILE не найден"
fi

# Проверка .env
if [ -f ".env" ]; then
    print_success "Файл .env существует"

    # Проверка обязательных переменных
    if grep -q "TELEGRAM_BOT_TOKEN=" .env && ! grep -q "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" .env; then
        print_success "TELEGRAM_BOT_TOKEN настроен"
    else
        print_error "TELEGRAM_BOT_TOKEN не настроен или использует значение по умолчанию"
    fi

    if grep -q "OPENROUTER_API_KEY=" .env && ! grep -q "OPENROUTER_API_KEY=your_openrouter_api_key_here" .env; then
        print_success "OPENROUTER_API_KEY настроен"
    else
        print_error "OPENROUTER_API_KEY не настроен или использует значение по умолчанию"
    fi

    if grep -q "POSTGRES_PASSWORD=" .env && ! grep -q "POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD" .env; then
        print_success "POSTGRES_PASSWORD настроен"
    else
        print_warning "POSTGRES_PASSWORD использует значение по умолчанию (небезопасно для production)"
    fi
else
    print_error "Файл .env не найден"
fi

# ============================================================================

print_header "Проверка Docker контейнеров"

# Проверка, что Docker Compose файл существует
if [ ! -f "$COMPOSE_FILE" ]; then
    print_error "Невозможно проверить контейнеры: $COMPOSE_FILE не найден"
else
    # Проверка статуса контейнеров
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        print_success "Docker Compose проект запущен"

        # Проверка каждого сервиса
        SERVICES=("postgres" "bot" "api" "frontend")
        for service in "${SERVICES[@]}"; do
            if docker-compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up"; then
                print_success "Сервис $service запущен"
            else
                print_error "Сервис $service не запущен"
            fi
        done
    else
        print_error "Docker Compose проект не запущен"
        print_info "Запустите: docker-compose -f $COMPOSE_FILE up -d"
    fi
fi

# ============================================================================

print_header "Проверка PostgreSQL"

# Проверка healthcheck
POSTGRES_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q postgres 2>/dev/null || echo "")
if [ -n "$POSTGRES_CONTAINER" ]; then
    HEALTH_STATUS=$(docker inspect "$POSTGRES_CONTAINER" --format='{{.State.Health.Status}}' 2>/dev/null || echo "unknown")

    if [ "$HEALTH_STATUS" == "healthy" ]; then
        print_success "PostgreSQL healthcheck: healthy"
    elif [ "$HEALTH_STATUS" == "starting" ]; then
        print_warning "PostgreSQL healthcheck: starting (подождите немного)"
    else
        print_error "PostgreSQL healthcheck: $HEALTH_STATUS"
    fi

    # Проверка логов на ошибки
    if docker-compose -f "$COMPOSE_FILE" logs postgres | grep -i error | grep -v "ERROR:  database \"aidd\" does not exist" > /dev/null; then
        print_warning "В логах PostgreSQL есть ошибки (проверьте: docker-compose logs postgres)"
    else
        print_success "В логах PostgreSQL нет критических ошибок"
    fi
else
    print_error "Контейнер PostgreSQL не найден"
fi

# ============================================================================

print_header "Проверка миграций базы данных"

# Проверка логов bot на наличие сообщения о миграциях
if docker-compose -f "$COMPOSE_FILE" logs bot | grep -q "Миграции выполнены"; then
    print_success "Миграции базы данных выполнены"
elif docker-compose -f "$COMPOSE_FILE" logs bot | grep -q "Запуск миграций"; then
    if docker-compose -f "$COMPOSE_FILE" logs bot | grep -i "error" > /dev/null; then
        print_error "Миграции выполнены с ошибками (проверьте: docker-compose logs bot)"
    else
        print_success "Миграции выполнены успешно"
    fi
else
    print_warning "Не удалось определить статус миграций (проверьте: docker-compose logs bot)"
fi

# ============================================================================

print_header "Проверка Bot"

BOT_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q bot 2>/dev/null || echo "")
if [ -n "$BOT_CONTAINER" ]; then
    if docker-compose -f "$COMPOSE_FILE" logs bot | grep -q "Telegram bot started"; then
        print_success "Telegram bot запущен"
    elif docker-compose -f "$COMPOSE_FILE" logs bot | grep -i "error" > /dev/null; then
        print_error "Bot запущен с ошибками (проверьте: docker-compose logs bot)"
    else
        print_warning "Статус bot неопределен (проверьте: docker-compose logs bot)"
    fi
else
    print_error "Контейнер bot не найден"
fi

# ============================================================================

print_header "Проверка API"

API_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q api 2>/dev/null || echo "")
if [ -n "$API_CONTAINER" ]; then
    # Проверка доступности API
    if curl -s -f "$API_URL/health" > /dev/null 2>&1; then
        print_success "API доступен ($API_URL/health)"

        # Проверка ответа
        HEALTH_RESPONSE=$(curl -s "$API_URL/health")
        if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
            print_success "API health check: OK"
        else
            print_warning "API health check: неожиданный ответ ($HEALTH_RESPONSE)"
        fi
    else
        print_error "API недоступен ($API_URL/health)"
        print_info "Проверьте логи: docker-compose logs api"
    fi

    # Проверка логов на ошибки
    if docker-compose -f "$COMPOSE_FILE" logs api | grep -i "error" > /dev/null; then
        print_warning "В логах API есть ошибки (проверьте: docker-compose logs api)"
    else
        print_success "В логах API нет ошибок"
    fi
else
    print_error "Контейнер API не найден"
fi

# ============================================================================

print_header "Проверка Frontend"

FRONTEND_CONTAINER=$(docker-compose -f "$COMPOSE_FILE" ps -q frontend 2>/dev/null || echo "")
if [ -n "$FRONTEND_CONTAINER" ]; then
    # Проверка доступности Frontend
    if curl -s -f "$FRONTEND_URL" > /dev/null 2>&1; then
        print_success "Frontend доступен ($FRONTEND_URL)"
    else
        print_error "Frontend недоступен ($FRONTEND_URL)"
        print_info "Проверьте логи: docker-compose logs frontend"
    fi

    # Проверка логов
    if docker-compose -f "$COMPOSE_FILE" logs frontend | grep -q "ready"; then
        print_success "Frontend готов к работе"
    else
        print_warning "Frontend еще не готов (проверьте: docker-compose logs frontend)"
    fi

    # Проверка на ошибки
    if docker-compose -f "$COMPOSE_FILE" logs frontend | grep -i "error" > /dev/null; then
        print_warning "В логах Frontend есть ошибки (проверьте: docker-compose logs frontend)"
    else
        print_success "В логах Frontend нет ошибок"
    fi
else
    print_error "Контейнер Frontend не найден"
fi

# ============================================================================

print_header "Проверка портов"

# Проверка, что порты открыты
check_port() {
    local port=$1
    local service=$2

    if netstat -tuln 2>/dev/null | grep -q ":$port " || ss -tuln 2>/dev/null | grep -q ":$port "; then
        print_success "Порт $port ($service) открыт"
    else
        print_error "Порт $port ($service) не открыт"
    fi
}

check_port 8005 "API"
check_port 3005 "Frontend"

# ============================================================================

print_header "Проверка использования ресурсов"

# Docker stats (быстрый снимок)
print_info "Использование ресурсов контейнерами:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || print_warning "Не удалось получить статистику"

# Проверка места на диске
print_info "Использование дискового пространства Docker:"
docker system df 2>/dev/null || print_warning "Не удалось получить информацию о дисковом пространстве"

# ============================================================================

print_header "Итоги проверки"

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo ""
echo -e "Пройдено проверок: ${GREEN}$PASSED${NC} / $TOTAL (${PERCENTAGE}%)"
if [ $FAILED -gt 0 ]; then
    echo -e "Провалено проверок: ${RED}$FAILED${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Все проверки пройдены успешно!${NC}"
    echo -e "${GREEN}  Развертывание работает корректно.${NC}"
    exit 0
elif [ $FAILED -le 3 ]; then
    echo -e "${YELLOW}⚠ Развертывание работает с предупреждениями${NC}"
    echo -e "${YELLOW}  Проверьте отмеченные проблемы выше.${NC}"
    exit 0
else
    echo -e "${RED}✗ Обнаружены критические проблемы${NC}"
    echo -e "${RED}  Развертывание требует исправлений.${NC}"
    exit 1
fi

