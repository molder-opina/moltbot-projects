# 🤖 Moltbot Projects

Repositorio de scripts, documentación y proyectos para el agente Moltbot.

## 📁 Estructura

```
projects/
├── tracker/          # Sistema de tracking de actividades (Kanban)
├── memory/           # Sistema de memoria local
├── scripts/          # Scripts utilitarios
├── config/           # Configuraciones
└── docs/             # Documentación
```

## 🚀 Proyectos

### 📋 Tracker (Kanban Local)
Sistema de tracking de actividades con interfaz Kanban simple.

```bash
cd tracker
./kanban-local.sh show      # Ver tablero
./kanban-local.sh create "Tarea" "Descripción" backlog
./kanban-local.sh move 1234 progress
```

**Características:**
- Sin dependencias externas
- Persistencia en JSON local
- Reportes automáticos

### 🧠 Memory (Memoria Local)
Sistema de memoria persistente para el agente.

```bash
cd memory
python3 memoria-local.py add "texto" [categoría]
python3 memoria-local.py search "query"
python3 memoria-local.py stats
```

**Categorías:**
- `preferencia` - Preferencias del usuario
- `hecho` - Facts y datos
- `tarea` - Tareas pendientes
- `contexto` - Contexto de conversación
- `general` - Memorias generales

## 📦 Instalación

```bash
# Clonar o copiar la carpeta projects
cd /Users/molder/moltbot/projects

# Hacer ejecutables los scripts
find . -name "*.sh" -exec chmod +x {} \;

# Verificar funcionamiento
./tracker/kanban-local.sh show
```

## 🔧 Configuración

Ver `config/MEMORY.md` para detalles sobre el sistema de memoria.

## 📝 Historial

Este repositorio contiene todos los proyectos desarrollados colaborativamente con el usuario para personalizar y mejorar las capacidades del agente Moltbot.

## 🛠️ Tecnologías

- **Bash** - Scripts de automatización
- **Python 3** - Sistema de memoria
- **Docker** - Contenedores (legacy, qdrant eliminado)
- **Git** - Control de versiones

---

*Creado y mantenido por Moltbot 🤖*
