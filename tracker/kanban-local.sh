#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Kanban Tracker Local - Alternativa simple a Fizzy
#  Usa un archivo JSON local para persistencia
# ═══════════════════════════════════════════════════════════════

KANBAN_FILE="${KANBAN_FILE:-$HOME/.fizzy/kanban.json}"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════
#  INICIALIZACIÓN
# ═══════════════════════════════════════════════════════════════

init_kanban() {
    mkdir -p "$(dirname "$KANBAN_FILE")"
    
    if [ ! -f "$KANBAN_FILE" ]; then
        cat > "$KANBAN_FILE" << 'EOF'
{
  "columns": {
    "backlog": {"title": "Backlog", "cards": []},
    "thisweek": {"title": "Esta Semana", "cards": []},
    "progress": {"title": "En Progreso", "cards": []},
    "done": {"title": "Hecho", "cards": []},
    "archived": {"title": "Archivado", "cards": []}
  },
  "last_updated": ""
}
EOF
        echo -e "${GREEN}✅ Kanban inicializado en $KANBAN_FILE${NC}"
    fi
}

# ═══════════════════════════════════════════════════════════════
#  GESTIÓN DE JSON
# ═══════════════════════════════════════════════════════════════

get_json() {
    local field="$1"
    local file="$2"
    python3 -c "import json; d=json.load(open('$file')); print($field)" 2>/dev/null || echo ""
}

set_json() {
    local field="$1"
    local value="$2"
    local file="$3"
    python3 << PYEOF
import json
with open('$file', 'r') as f:
    d = json.load(f)
d$field = $value
with open('$file', 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
PYEOF
}

# ═══════════════════════════════════════════════════════════════
#  TARJETAS
# ═══════════════════════════════════════════════════════════════

kanban_create() {
    init_kanban
    
    local title="$1"
    local description="${2:-}"
    local column="${3:-backlog}"
    
    # Generar ID único
    local id=$(date +%s)$(printf "%04d" $((RANDOM % 10000)))
    
    # Leer JSON
    python3 << PYEOF
import json
with open('$KANBAN_FILE', 'r') as f:
    data = json.load(f)

card = {
    "id": "$id",
    "title": """$title""",
    "description": """$description""",
    "created": "$(date -Iseconds)",
    "started": None,
    "done": None
}

data["columns"]["$column"]["cards"].append(card)
data["last_updated"] = "$(date -Iseconds)"

with open('$KANBAN_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
PYEOF
    
    echo -e "${GREEN}✅ Creada: $title${NC} (ID: $id)"
}

kanban_move() {
    init_kanban
    
    local id="$1"
    local target_column="$2"
    
    python3 << PYEOF
import json
with open('$KANBAN_FILE', 'r') as f:
    data = json.load(f)

card = None
for col_name, col_data in data["columns"].items():
    for c in col_data["cards"]:
        if c["id"] == "$id":
            card = c
            col_data["cards"].remove(c)
            break
    if card:
        break

if card:
    data["columns"]["$target_column"]["cards"].append(card)
    data["last_updated"] = "$(date -Iseconds)"
    with open('$KANBAN_FILE', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("OK")
else:
    print("NOT_FOUND")
PYEOF
    
    echo -e "${YELLOW}🔄 Movida a '$target_column'${NC}"
}

kanban_start() {
    init_kanban
    
    local id="$1"
    
    python3 << PYEOF
import json
from datetime import datetime

with open('$KANBAN_FILE', 'r') as f:
    data = json.load(f)

for col_name, col_data in data["columns"].items():
    for c in col_data["cards"]:
        if c["id"] == "$id":
            c["started"] = datetime.now().isoformat()
            break

with open('$KANBAN_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
PYEOF
    
    echo -e "${CYAN}🚀 Iniciada: $id${NC}"
}

kanban_done() {
    init_kanban
    
    local id="$1"
    
    python3 << PYEOF
import json
from datetime import datetime

with open('$KANBAN_FILE', 'r') as f:
    data = json.load(f)

for col_name, col_data in data["columns"].items():
    for c in col_data["cards"]:
        if c["id"] == "$id":
            c["done"] = datetime.now().isoformat()
            break

with open('$KANBAN_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
PYEOF
    
    echo -e "${GREEN}✅ Completada: $id${NC}"
}

kanban_delete() {
    init_kanban
    
    local id="$1"
    
    python3 << PYEOF
import json
with open('$KANBAN_FILE', 'r') as f:
    data = json.load(f)

for col_name, col_data in data["columns"].items():
    for c in col_data["cards"]:
        if c["id"] == "$id":
            col_data["cards"].remove(c)
            print("OK")
            break
    else:
        continue
    break

with open('$KANBAN_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
PYEOF
    
    echo -e "${RED}🗑️  Eliminada: $id${NC}"
}

# ═══════════════════════════════════════════════════════════════
#  VISUALIZACIÓN
# ═══════════════════════════════════════════════════════════════

kanban_show() {
    init_kanban
    
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                  📋 KANBAN TRACKER                        ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    python3 << 'PYEOF'
import json
import sys

with open('$HOME/.fizzy/kanban.json'.replace('$HOME', __import__('os').environ['HOME']), 'r') as f:
    data = json.load(f)

columns = ['backlog', 'thisweek', 'progress', 'done', 'archived']
titles = {'backlog': '📚 Backlog', 'thisweek': '📅 Esta Semana', 'progress': '🔄 En Progreso', 'done': '✅ Hecho', 'archived': '📦 Archivado'}

# Calcular anchos
for col in columns:
    max_len = len(titles[col])
    for card in data["columns"][col]["cards"]:
        max_len = max(max_len, len(card["title"]))
    data["columns"][col]["_width"] = min(max_len + 4, 40)

# Headers
header = ""
for col in columns:
    col_data = data["columns"][col]
    title = titles[col][:col_data["_width"]-4]
    header += f" {title:<{col_data['_width']-1}} |"
print(f"┌{'─'*(58)}┐")
print(f"│{header}")
print(f"├{'─'*(58)}┤")

# Cards (máximo 5 por columna para mostrar)
max_rows = max(len(data["columns"][c]["cards"]) for c in columns)
max_rows = min(max_rows, 10)

for row in range(max_rows):
    line = "│"
    for col in columns:
        cards = data["columns"][col]["cards"]
        if row < len(cards):
            title = cards[row]["title"]
            if len(title) > col_data["_width"]-5:
                title = title[:col_data["_width"]-8] + "..."
            line += f" {title:<{col_data['_width']-2}} │"
        else:
            line += f" {' '*(col_data['_width']-2)} │"
    print(line)

print(f"└{'─'*(58)}┘")

# Stats
total = sum(len(data["columns"][c]["cards"]) for c in columns)
done = len(data["columns"]["done"]["cards"])
print(f"\n📊 Total: {total} | ✅ Hecho: {done} ({int(done/total*100) if total > 0 else 0}%)")
PYEOF
    
    echo ""
}

kanban_list() {
    init_kanban
    
    local column="${1:-all}"
    
    python3 << 'PYEOF'
import json
import sys

with open('$HOME/.fizzy/kanban.json'.replace('$HOME', __import__('os').environ['HOME']), 'r') as f:
    data = json.load(f)

columns = {'backlog': '📚 Backlog', 'thisweek': '📅 Esta Semana', 'progress': '🔄 En Progreso', 'done': '✅ Hecho', 'archived': '📦 Archivado'}

if "$column" == "all":
    for col_key, col_title in columns.items():
        print(f"\n{col_title}:")
        for card in data["columns"][col_key]["cards"]:
            status = ""
            if card.get("started"):
                status += "🔄"
            if card.get("done"):
                status += "✅"
            print(f"  [{card['id'][-4:]}] {status} {card['title']}")
else:
    col_title = columns.get("$column", "$column")
    print(f"\n{col_title}:")
    for card in data["columns"]["$column"]["cards"]:
        status = ""
        if card.get("started"):
            status += "🔄"
        if card.get("done"):
            status += "✅"
        print(f"  [{card['id'][-4:]}] {status} {card['title']}")
PYEOF
}

# ═══════════════════════════════════════════════════════════════
#  REPORTES
# ═══════════════════════════════════════════════════════════════

kanban_report() {
    init_kanban
    
    python3 << 'PYEOF'
import json
from datetime import datetime, timedelta

with open('$HOME/.fizzy/kanban.json'.replace('$HOME', __import__('os').environ['HOME']), 'r') as f:
    data = json.load(f)

today = datetime.now()
today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)

print("📊 Reporte de Actividades")
print("=" * 40)

# Esta semana (lunes)
week_start = today - timedelta(days=today.weekday())
week_start = week_start.replace(hour=0, minute=0, second=0)

done_today = 0
done_week = 0
in_progress = 0

for card in data["columns"]["done"]["cards"]:
    if card.get("done"):
        done_date = datetime.fromisoformat(card["done"])
        if done_date >= today_start:
            done_today += 1
        if done_date >= week_start:
            done_week += 1

for card in data["columns"]["progress"]["cards"]:
    if card.get("started") and not card.get("done"):
        in_progress += 1

print(f"\n✅ Completadas hoy: {done_today}")
print(f"📅 Completadas esta semana: {done_week}")
print(f"🔄 En progreso: {in_progress}")
print(f"📚 Total en backlog: {len(data['columns']['backlog']['cards'])}")

# Calcular porcentaje de la semana
week_goal = 10  # Meta semanal
print(f"\n🎯 Progreso semanal: {done_week}/{week_goal} ({int(done_week/week_goal*100)}%)")
PYEOF
}

# ═══════════════════════════════════════════════════════════════
#  EXPORTAR PARA REPORTES
# ═══════════════════════════════════════════════════════════════

kanban_export_report() {
    init_kanban
    
    python3 << 'PYEOF'
import json
from datetime import datetime, timedelta

with open('$HOME/.fizzy/kanban.json'.replace('$HOME', __import__('os').environ['HOME']), 'r') as f:
    data = json.load(f)

today = datetime.now()
today_str = today.strftime("%d/%m/%Y")
week_start = today - timedelta(days=today.weekday())

done_today = 0
done_week = 0
in_progress = []
done_titles = []

for card in data["columns"]["done"]["cards"]:
    if card.get("done"):
        done_date = datetime.fromisoformat(card["done"])
        if done_date.date() >= week_start.date():
            done_titles.append(f"  • {card['title']}")

for card in data["columns"]["progress"]["cards"]:
    in_progress.append(f"  🔄 {card['title']}")

print(f"""📊 **Reporte Semanal - {today_str}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **Completadas esta semana:** {len(done_titles)}

{chr(10).join(done_titles) if done_titles else "  (sin tareas completadas)"}

⏳ **En progreso:**
{chr(10).join(in_progress) if in_progress else "  (sin tareas activas)"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_Generado automáticamente por Kanban Tracker_
""")
PYEOF
}

# ═══════════════════════════════════════════════════════════════
#  AYUDA
# ═══════════════════════════════════════════════════════════════

kanban_help() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  Kanban Tracker Local - Comandos                          ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  CONFIGURACIÓN                                             ║"
    echo "║    export KANBAN_FILE=/ruta/kanban.json                   ║"
    echo "║                                                            ║"
    echo "║  GESTIÓN                                                   ║"
    echo "║    kanban_create \"título\" [desc] [columna]                ║"
    echo "║    kanban_move id columna                                 ║"
    echo "║    kanban_start id                                        ║"
    echo "║    kanban_done id                                         ║"
    echo "║    kanban_delete id                                       ║"
    echo "║                                                            ║"
    echo "║  VISUALIZACIÓN                                             ║"
    echo "║    kanban_show                                            ║"
    echo "║    kanban_list [columna]                                  ║"
    echo "║                                                            ║"
    echo "║  REPORTES                                                  ║"
    echo "║    kanban_report                                          ║"
    echo "║    kanban_export_report                                   ║"
    echo "║                                                            ║"
    echo "║  COLUMNAS: backlog, thisweek, progress, done, archived    ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
}

# ═══════════════════════════════════════════════════════════════
#  EJECUCIÓN
# ═══════════════════════════════════════════════════════════════

# Inicializar al cargar
init_kanban

# Ejecutar comando si hay argumentos
if [ $# -gt 0 ]; then
    "$@"
else
    kanban_show
fi
