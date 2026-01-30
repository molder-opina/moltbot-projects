#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Fizzy Daily Report - Envía reporte automático al canal
# ═══════════════════════════════════════════════════════════════

# Cargar configuración
source "$(dirname "$0")/.env"
source "$(dirname "$0")/fizzy-tracker.sh"

# ═══════════════════════════════════════════════════════════════
#  GENERAR REPORTE
# ═══════════════════════════════════════════════════════════════

generate_report() {
    local report=""
    local date_formatted=$(date "+%d/%m/%Y")
    
    report="📊 **Reporte Diario de Actividades - $date_formatted**"
    report="$report"$'\n'"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    report="$report"$'\n\n'
    
    # Contar tareas completadas hoy
    local today=$(date +%s)
    local today_start=$((today - $(date +%H) * 3600 - $(date +%M) * 60 - $(date +%S)))
    
    local completed_count=0
    local in_progress_count=0
    local total_time=0
    
    if [ -f ~/.fizzy/active_tasks.log ]; then
        # Tareas completadas hoy
        while IFS= read -r line; do
            if echo "$line" | grep -q "done:"; then
                local done_time=$(echo "$line" | grep -oE "done: [0-9]+" | grep -oE "[0-9]+")
                if [ -n "$done_time" ] && [ $done_time -ge $today_start ]; then
                    completed_count=$((completed_count + 1))
                    
                    # Calcular tiempo (si hay started time)
                    local started_time=$(echo "$line" | grep -oE "started [0-9]+" | grep -oE "[0-9]+" | head -1)
                    if [ -n "$started_time" ]; then
                        local duration=$((done_time - started_time))
                        total_time=$((total_time + duration))
                    fi
                fi
            fi
        done < ~/.fizzy/active_tasks.log
        
        # Tareas en progreso
        while IFS= read -r line; do
            if ! echo "$line" | grep -q "done:"; then
                local task_title=$(echo "$line" | sed 's/^[0-9]* //' | sed 's/ (.*//')
                in_progress_count=$((in_progress_count + 1))
            fi
        done < ~/.fizzy/active_tasks.log
    fi
    
    # Formatear tiempo total
    local total_mins=$((total_time / 60))
    local hours=$((total_mins / 60))
    local mins=$((total_mins % 60))
    
    # Construir reporte
    report="$report✅ **Completadas hoy:** $completed_count"
    
    if [ $hours -gt 0 ] || [ $mins -gt 0 ]; then
        report="$report ($hours h $mins m)"
    fi
    report="$report"$'\n'
    report="$report"$'\n'
    report="$report"⏳ **En progreso:** $in_progress_count"$'\n'
    report="$report"$'\n'
    report="$report"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"$'\n'
    
    # Lista de tareas completadas
    report="$report"$'\n'**Últimas completadas:**'$'\n'
    
    if [ -f ~/.fizzy/active_tasks.log ]; then
        local found=false
        while IFS= read -r line; do
            if echo "$line" | grep -q "done:"; then
                local done_time=$(echo "$line" | grep -oE "done: [0-9]+" | grep -oE "[0-9]+")
                if [ -n "$done_time" ] && [ $done_time -ge $today_start ]; then
                    local task_title=$(echo "$line" | sed 's/^[0-9]* //' | sed 's/ (.*//')
                    report="$report"• "$task_title"$'\n'
                    found=true
                fi
            fi
        done < ~/.fizzy/active_tasks.log
        
        if [ "$found" = false ]; then
            report="$report"_(sin tareas completadas)_$'\n'
        fi
    else
        report="$report"_(sin datos de tracking)_$'\n'
    fi
    
    # Tareas en progreso
    report="$report"$'\n'**Ahora:**'$'\n'
    
    if [ -f ~/.fizzy/active_tasks.log ]; then
        local found=false
        while IFS= read -r line; do
            if ! echo "$line" | grep -q "done:"; then
                local task_title=$(echo "$line" | sed 's/^[0-9]* //' | sed 's/ (.*//')
                report="$report"• 🔄 "$task_title"$'\n'
                found=true
            fi
        done < ~/.fizzy/active_tasks.log
        
        if [ "$found" = false ]; then
            report="$report"_(sin tareas activas)_$'\n'
        fi
    else
        report="$report"_(sin datos de tracking)_$'\n'
    fi
    
    # Footer
    report="$report"$'\n'
    report="$report"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"$'\n'
    report="$report"_Generado automáticamente por Fizzy Tracker_$'\n'
    
    echo "$report"
}

# ═══════════════════════════════════════════════════════════════
#  ENVIAR AL CANAL
# ═══════════════════════════════════════════════════════════════

send_report() {
    local report=$(generate_report)
    local channel="${1:-telegram}"
    local target="${2:-main}"
    
    echo "Enviando reporte a $channel / $target..."
    echo "$report"
    echo ""
    
    # Usar message tool de Moltbot
    # El message tool se invoca directamente
    moltbot message send "$channel" "$target" "$report"
}

# ═══════════════════════════════════════════════════════════════
#  MODO CRON (salida simple sin formatting)
# ═══════════════════════════════════════════════════════════════

cron_mode() {
    local today=$(date +%s)
    local today_start=$((today - $(date +%H) * 3600 - $(date +%M) * 60 - $(date +%S)))
    
    local completed_count=0
    local in_progress_count=0
    
    if [ -f ~/.fizzy/active_tasks.log ]; then
        while IFS= read -r line; do
            if echo "$line" | grep -q "done:"; then
                local done_time=$(echo "$line" | grep -oE "done: [0-9]+" | grep -oE "[0-9]+")
                if [ -n "$done_time" ] && [ $done_time -ge $today_start ]; then
                    completed_count=$((completed_count + 1))
                fi
            else
                in_progress_count=$((in_progress_count + 1))
            fi
        done < ~/.fizzy/active_tasks.log
    fi
    
    echo "REPORT COMPLETED=$completed_count IN_PROGRESS=$in_progress_count"
}

# ═══════════════════════════════════════════════════════════════
#  EJECUCIÓN
# ═══════════════════════════════════════════════════════════════

case "${1:-report}" in
    report)
        send_report "${2:-telegram}" "${3:-main}"
        ;;
    cron)
        cron_mode
        ;;
    generate)
        generate_report
        ;;
    help|*)
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║  Fizzy Daily Report - Envío Automático                    ║"
        echo "╠════════════════════════════════════════════════════════════╣"
        echo "║                                                            ║"
        echo "║  USO:                                                      ║"
        echo "║    $0 report [canal] [target]  → Enviar reporte           ║"
        echo "║    $0 generate                 → Generar sin enviar       ║"
        echo "║    $0 cron                     → Modo cron (texto plano)  ║"
        echo "║                                                            ║"
        echo "║  EJEMPLOS:                                                 ║"
        echo "║    $0 report telegram main                              ║"
        echo "║    $0 report discord general                             ║"
        echo "║    $0 report webchat main                                ║"
        echo "║                                                            ║"
        echo "║  CANALES: telegram, discord, webchat, signal, etc.        ║"
        echo "║                                                            ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        ;;
esac
