#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Fizzy Integration Scripts - Trackeador de Actividades
# ═══════════════════════════════════════════════════════════════

# Configuración
FIZZY_URL="${FIZZY_URL:-http://localhost:3000}"
FIZZY_API_TOKEN="${FIZZY_API_TOKEN:-}"
BOARD_ID="${FIZZY_BOARD_ID:-1}"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════
#  FUNCIONES PRINCIPALES
# ═══════════════════════════════════════════════════════════════

# Verificar configuración
check_config() {
    if [ -z "$FIZZY_API_TOKEN" ]; then
        echo -e "${RED}❌ Error: FIZZY_API_TOKEN no configurado${NC}"
        echo "   Ejecuta: export FIZZY_API_TOKEN='tu-token'"
        echo "   O añade al .env: echo 'FIZZY_API_TOKEN=tu-token' >> .env"
        return 1
    fi
    return 0
}

# Hacer request a la API
fizzy_api() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    curl -s -X "$method" \
        -H "Authorization: Bearer $FIZZY_API_TOKEN" \
        -H "Content-Type: application/json" \
        "$FIZZY_URL/api/v1$endpoint" \
        $data
}

# ═══════════════════════════════════════════════════════════════
#  GESTIÓN DE TARJETAS
# ═══════════════════════════════════════════════════════════════

# Crear nueva tarjeta
# Uso: fizzy_create "Título" "Descripción" [--column id]
fizzy_create() {
    check_config || return 1
    
    local title="$1"
    local description="${2:-}"
    local column_id="${FIZZY_COLUMN_BACKLOG:-1}"
    
    # Parsear argumentos
    while [[ $# -gt 3 ]]; do
        case "$3" in
            --column)
                column_id="$4"
                shift 2
                ;;
        esac
        shift
    done
    
    local json="{\"card\":{\"title\":\"$title\",\"description\":\"$description\",\"column_id\":$column_id}}"
    
    echo -e "${BLUE}📝 Creando tarjeta: $title${NC}"
    
    local response=$(fizzy_api "POST" "/boards/$BOARD_ID/cards" "-d '$json'")
    
    if echo "$response" | grep -q '"id"'; then
        local card_id=$(echo "$response" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
        local column_name=$(echo "$response" | grep -o '"column_name":"[^"]*"' | head -1 | cut -d'"' -f4)
        echo -e "${GREEN}✅ Tarjeta creada (ID: $card_id) en '$column_name'${NC}"
        echo "$card_id"
    else
        echo -e "${RED}❌ Error al crear tarjeta${NC}"
        echo "$response"
    fi
}

# Mover tarjeta a columna
# Uso: fizzy_move card_id "nombre_columna"
fizzy_move() {
    check_config || return 1
    
    local card_id="$1"
    local target_column="$2"
    
    # Buscar ID de la columna destino
    local columns=$(fizzy_api "GET" "/boards/$BOARD_ID/columns")
    local column_id=$(echo "$columns" | grep -o "\"name\":\"[^\"]*$target_column[^\"]*\",\"id\":[0-9]*" | grep -o 'id":[0-9]*' | cut -d':' -f2 | head -1)
    
    if [ -z "$column_id" ]; then
        echo -e "${RED}❌ Columna '$target_column' no encontrada${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}🔄 Moviendo tarjeta $card_id a '$target_column'${NC}"
    
    local response=$(fizzy_api "PATCH" "/cards/$card_id/move" "-d '{\"card\":{\"column_id\":$column_id}}'")
    
    if echo "$response" | grep -q '"id"'; then
        echo -e "${GREEN}✅ Tarjeta movida${NC}"
    else
        echo -e "${RED}❌ Error al mover${NC}"
        echo "$response"
    fi
}

# Completar tarjeta
# Uso: fizzy_done card_id
fizzy_done() {
    local card_id="$1"
    fizzy_move "$card_id" "done" || return 1
    
    # Obtener tiempo registrado si existe
    local card_info=$(fizzy_api "GET" "/cards/$card_id")
    local description=$(echo "$card_info" | grep -o '"description":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    echo -e "${GREEN}✅ Tarjeta $card_id marcada como completada${NC}"
}

# Listar tarjetas de una columna
# Uso: fizzy_list "columna"
fizzy_list() {
    check_config || return 1
    
    local column_name="${1:-backlog}"
    local columns=$(fizzy_api "GET" "/boards/$BOARD_ID/columns")
    
    echo -e "${BLUE}📋 Tarjetas en '$column_name':${NC}"
    echo "$columns" | grep -A 100 "\"name\":\"$column_name\"" | head -50
}

# ═══════════════════════════════════════════════════════════════
#  REGISTRO DE TIEMPO
# ═══════════════════════════════════════════════════════════════

# Iniciar tarea (crear + mover a "en progreso")
# Uso: fizzy_start "Título" [descripción]
fizzy_start() {
    check_config || return 1
    
    local title="$1"
    local description="${2:-}"
    
    # Crear en backlog primero
    local card_id=$(fizzy_create "$title" "$description" --column 1)
    
    if [ -n "$card_id" ]; then
        # Mover a "en progreso"
        fizzy_move "$card_id" "progress" || \
        fizzy_move "$card_id" "doing" || \
        fizzy_move "$card_id" "in-progress"
        
        # Registrar inicio en archivo de tracking
        echo "$(date +%s)|$card_id|$title|started" >> ~/.fizzy/tracking.log
        
        echo -e "${GREEN}🚀 Tarea iniciada: $title${NC}"
    fi
}

# Finalizar tarea
# Uso: fizzy_finish card_id
fizzy_finish() {
    local card_id="$1"
    
    # Buscar inicio en tracking.log
    if [ -f ~/.fizzy/tracking.log ]; then
        local start_line=$(grep "|$card_id|" ~/.fizzy/tracking.log | tail -1)
        if [ -n "$start_line" ]; then
            local start_time=$(echo "$start_line" | cut -d'|' -f1)
            local end_time=$(date +%s)
            local duration=$((end_time - start_time))
            
            # Formatear duración
            local mins=$((duration / 60))
            local hours=$((mins / 60))
            local mins_rem=$((mins % 60))
            
            if [ $hours -gt 0 ]; then
                echo -e "${YELLOW}⏱️  Tiempo: ${hours}h ${mins_rem}m${NC}"
            else
                echo -e "${YELLOW}⏱️  Tiempo: ${mins}m${NC}"
            fi
            
            # Marcar como completada
            fizzy_done "$card_id"
            
            # Actualizar tracking.log
            sed -i "s/$start_line/$start_line|finished|${duration}s/" ~/.fizzy/tracking.log
        else
            fizzy_done "$card_id"
        fi
    else
        fizzy_done "$card_id"
    fi
}

# ═══════════════════════════════════════════════════════════════
#  REPORTES
# ═══════════════════════════════════════════════════════════════

# Reporte diario
fizzy_report_daily() {
    echo -e "${BLUE}📊 Reporte Diario de Actividades${NC}"
    echo "================================"
    
    if [ -f ~/.fizzy/tracking.log ]; then
        local today=$(date +%s | cut -c1-10)
        local yesterday=$(($today - 86400))
        
        echo ""
        echo -e "${GREEN}✅ Completadas hoy:${NC}"
        grep "|$today|finished" ~/.fizzy/tracking.log | while read line; do
            local title=$(echo "$line" | cut -d'|' -f3)
            local duration=$(echo "$line" | cut -d'|' -f5 | tr -d 's')
            local mins=$((duration / 60))
            echo "   - $title ($mins min)"
        done
        
        echo ""
        echo -e "${YELLOW}⏳ En progreso:${NC}"
        grep "|$today|started" ~/.fizzy/tracking.log | grep -v "finished" | while read line; do
            local title=$(echo "$line" | cut -d'|' -f3)
            echo "   - $title"
        done
    else
        echo "No hay datos de tracking aún."
    fi
}

# Reporte semanal
fizzy_report_weekly() {
    echo -e "${BLUE}📊 Reporte Semanal${NC}"
    echo "====================="
    
    if [ -f ~/.fizzy/tracking.log ]; then
        local week_ago=$(($(date +%s) - 604800))
        
        local total_mins=0
        local tasks_done=0
        
        grep "|$week_ago|finished" ~/.fizzy/tracking.log | while read line; do
            local title=$(echo "$line" | cut -d'|' -f3)
            local duration=$(echo "$line" | cut -d'|' -f5 | tr -d 's')
            total_mins=$((total_mins + duration / 60))
            tasks_done=$((tasks_done + 1))
        done
        
        local hours=$((total_mins / 60))
        local mins_rem=$((total_mins % 60))
        
        echo ""
        echo -e "${GREEN}✅ Tareas completadas: $tasks_done${NC}"
        echo -e "${YELLOW}⏱️  Tiempo total: ${hours}h ${mins_rem}m${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════
#  HELP
# ═══════════════════════════════════════════════════════════════

fizzy_help() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  Fizzy Tracker - Comandos Disponibles                     ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  CONFIGURACIÓN                                             ║"
    echo "║    export FIZZY_URL=http://localhost:3000                 ║"
    echo "║    export FIZZY_API_TOKEN=tu-token                        ║"
    echo "║    export FIZZY_BOARD_ID=1                                ║"
    echo "║                                                            ║"
    echo "║  TARJETAS                                                  ║"
    echo "║    fizzy_create \"título\" [descripción]                   ║"
    echo "║    fizzy_move card_id \"columna\"                           ║"
    echo "║    fizzy_done card_id                                     ║"
    echo "║    fizzy_list [columna]                                   ║"
    echo "║                                                            ║"
    echo "║  FLUJO DE TRABAJO                                         ║"
    echo "║    fizzy_start \"título\" [descripción]  → Crea y starts    ║"
    echo "║    fizzy_finish card_id             → Completa y registra ║"
    echo "║                                                            ║"
    echo "║  REPORTES                                                  ║"
    echo "║    fizzy_report_daily                                      ║"
    echo "║    fizzy_report_weekly                                     ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
}

# ═══════════════════════════════════════════════════════════════
#  INICIALIZACIÓN
# ═══════════════════════════════════════════════════════════════

# Crear directorio de tracking
mkdir -p ~/.fizzy

# Exportar funciones
export -f fizzy_create
export -f fizzy_move
export -f fizzy_done
export -f fizzy_list
export -f fizzy_start
export -f fizzy_finish
export -f fizzy_report_daily
export -f fizzy_report_weekly
export -f fizzy_help
export -f check_config
export -f fizzy_api

# Si se ejecuta con argumentos
if [ $# -gt 0 ]; then
    "$@"
else
    fizzy_help
fi
