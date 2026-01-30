#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Moltbot ↔ Fizzy Integration
#  Auto-actualiza el tablero cuando el agente trabaja
# ═══════════════════════════════════════════════════════════════

# Cargar funciones de Fizzy
source "$(dirname "$0")/fizzy-tracker.sh"

# ═══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE INTEGRACIÓN CON MOLTBOT
# ═══════════════════════════════════════════════════════════════

# Variables de entorno (configurar en .env)
MOLTBOT_FIZZY_URL="${MOLTBOT_FIZZY_URL:-http://localhost:3000}"
MOLTBOT_FIZZY_TOKEN="${MOLTBOT_FIZZY_TOKEN:-}"
MOLTBOT_FIZZY_BOARD="${MOLTBOT_FIZZY_BOARD:-1}"
MOLTBOT_FIZZY_COLUMN_BACKLOG="${MOLTBOT_FIZZY_COLUMN_BACKLOG:-1}"
MOLTBOT_FIZZY_COLUMN_PROGRESS="${MOLTBOT_FIZZY_COLUMN_PROGRESS:-2}"
MOLTBOT_FIZZY_COLUMN_DONE="${MOLTBOT_FIZZY_COLUMN_DONE:-3}"

# ═══════════════════════════════════════════════════════════════
#  API SIMPLIFICADA PARA INTEGRACIÓN
# ═══════════════════════════════════════════════════════════════

# Crear tarjeta desde Moltbot
moltbot_fizzy_create_card() {
    local title="$1"
    local description="${2:-}"
    local column_id="${3:-$MOLTBOT_FIZZY_COLUMN_BACKLOG}"
    
    local json="{\"card\":{\"title\":\"$title\",\"description\":\"$description\",\"column_id\":$column_id}}"
    
    curl -s -X POST \
        -H "Authorization: Bearer $MOLTBOT_FIZZY_TOKEN" \
        -H "Content-Type: application/json" \
        "$MOLTBOT_FIZZY_URL/api/v1/boards/$MOLTBOT_FIZZY_BOARD/cards" \
        -d "$json" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2
}

# Mover tarjeta
moltbot_fizzy_move_card() {
    local card_id="$1"
    local column_id="$2"
    
    curl -s -X PATCH \
        -H "Authorization: Bearer $MOLTBOT_FIZZY_TOKEN" \
        -H "Content-Type: application/json" \
        "$MOLTBOT_FIZZY_URL/api/v1/cards/$card_id/move" \
        -d "{\"card\":{\"column_id\":$column_id}}" > /dev/null
    
    echo "OK"
}

# Obtener tarjetas de una columna
moltbot_fizzy_get_cards() {
    local column_id="$1"
    
    curl -s -X GET \
        -H "Authorization: Bearer $MOLTBOT_FIZZY_TOKEN" \
        "$MOLTBOT_FIZZY_URL/api/v1/boards/$MOLTBOT_FIZZY_BOARD/columns/$column_id/cards"
}

# ═══════════════════════════════════════════════════════════════
#  INTEGRACIÓN CON EL AGENTE
# ═══════════════════════════════════════════════════════════════

# Registrar inicio de tarea
moltbot_fizzy_on_task_start() {
    local task_title="$1"
    local task_context="${2:-}"
    local card_id
    
    echo "[Fizzy] 🚀 Iniciando: $task_title"
    
    card_id=$(moltbot_fizzy_create_card "$task_title" "$task_context (Iniciado: $(date))" "$MOLTBOT_FIZZY_COLUMN_PROGRESS")
    
    if [ -n "$card_id" ]; then
        echo "[Fizzy] ✅ Tarjeta #$card_id creada en 'En Progreso'"
        echo "$card_id" >> ~/.fizzy/active_tasks.log
    fi
}

# Registrar finalización de tarea
moltbot_fizzy_on_task_complete() {
    local task_title="$1"
    local duration_seconds="${2:-}"
    
    echo "[Fizzy] ✅ Completando: $task_title"
    
    # Buscar tarjeta activa
    if [ -f ~/.fizzy/active_tasks.log ]; then
        local card_id=$(grep "$task_title" ~/.fizzy/active_tasks.log | tail -1 | cut -d' ' -f1)
        
        if [ -n "$card_id" ]; then
            moltbot_fizzy_move_card "$card_id" "$MOLTBOT_FIZZY_COLUMN_DONE"
            
            # Registrar tiempo
            if [ -n "$duration_seconds" ]; then
                local mins=$((duration_seconds / 60))
                echo "[Fizzy] ⏱️  Tiempo registrado: ${mins} minutos"
            fi
            
            # Actualizar log
            sed -i "s/^$card_id.*/$card_id $task_title (done: $(date +%s))/" ~/.fizzy/active_tasks.log
        fi
    fi
}

# ═══════════════════════════════════════════════════════════════
#  CRON: REPORTE AUTOMÁTICO
# ═══════════════════════════════════════════════════════════════

# Generar reporte para el canal de Moltbot
moltbot_fizzy_daily_report() {
    local report_file="/tmp/fizzy_daily_report_$(date +%Y%m%d).txt"
    
    {
        echo "📊 **Reporte Diario de Actividades**"
        echo "==================================="
        echo ""
        
        if [ -f ~/.fizzy/active_tasks.log ]; then
            local today=$(date +%s)
            
            echo "✅ **Completadas hoy:**"
            grep "done:" ~/.fizzy/active_tasks.log | while read line; do
                local done_time=$(echo "$line" | grep -o "done: [0-9]*" | cut -d' ' -f2)
                local task_title=$(echo "$line" | cut -d'(' -f1 | sed 's/^[0-9]* //')
                
                if [ -n "$done_time" ] && [ $done_time -ge $((today - 86400)) ]; then
                    echo "   - $task_title"
                fi
            done
            
            echo ""
            echo "⏳ **En progreso:**"
            grep -v "done:" ~/.fizzy/active_tasks.log | while read line; do
                local task_title=$(echo "$line" | cut -d'(' -f1 | sed 's/^[0-9]* //')
                echo "   - $task_title"
            done
        else
            echo "No hay actividades registradas hoy."
        fi
        
    } > "$report_file"
    
    cat "$report_file"
    return 0
}

# ═══════════════════════════════════════════════════════════════
#  INSTALACIÓN DE CRON
# ═══════════════════════════════════════════════════════════════

moltbot_fizzy_install_cron() {
    local script_path="$(realpath "$0")"
    
    # Reporte diario a las 20:00
    (crontab -l 2>/dev/null | grep -v "fizzy_daily_report"; echo "0 20 * * * $script_path daily-report >> ~/.fizzy/cron.log 2>&1") | crontab -
    
    echo "✅ Cron instalado:"
    echo "   - Reporte diario a las 20:00"
}

# ═══════════════════════════════════════════════════════════════
#  COMANDOS
# ═══════════════════════════════════════════════════════════════

case "${1:-help}" in
    create)
        moltbot_fizzy_create_card "$2" "$3"
        ;;
    move)
        moltbot_fizzy_move_card "$2" "$3"
        ;;
    start)
        moltbot_fizzy_on_task_start "$2" "$3"
        ;;
    complete)
        moltbot_fizzy_on_task_complete "$2" "$3"
        ;;
    report)
        moltbot_fizzy_daily_report
        ;;
    daily-report)
        moltbot_fizzy_daily_report
        ;;
    cron)
        moltbot_fizzy_install_cron
        ;;
    help|*)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║  Moltbot ↔ Fizzy Integration                              ║"
        echo "╠════════════════════════════════════════════════════════════╣"
        echo "║                                                            ║"
        echo "║  COMANDOS:                                                 ║"
        echo "║    $0 create \"título\" [desc]        → Crear tarjeta       ║"
        echo "║    $0 move card_id column_id        → Mover tarjeta       ║"
        echo "║    $0 start \"título\" [contexto]     → Iniciar tarea      ║"
        echo "║    $0 complete \"título\" [segundos]  → Completar tarea    ║"
        echo "║    $0 report                        → Ver reporte diario  ║"
        echo "║    $0 cron                          → Instalar cron       ║"
        echo "║                                                            ║"
        echo "║  INTEGRACIÓN CON AGENTE:                                  ║"
        echo "║    source moltbot-fizzy.sh                                 ║"
        echo "║    moltbot_fizzy_on_task_start \"mi tarea\"                ║"
        echo "║    moltbot_fizzy_on_task_complete \"mi tarea\" 3600         ║"
        echo "║                                                            ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        ;;
esac
