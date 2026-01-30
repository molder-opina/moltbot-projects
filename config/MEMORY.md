# Configuración de Memoria

## 🎯 Sistema de Memoria Actual

| Provider | Estado | Uso |
|----------|--------|-----|
| **Memoria Local** | ✅ Activo | Búsqueda por palabras clave |
| **Mem0 Cloud** | ✅ Activo | Búsqueda semántica (API key configurada) |

---

## 📋 Memoria Local (Predeterminada)

**Ubicación:** `~/.moltbot/memory/memory.json`

### Uso desde Python:
```python
import sys
sys.path.insert(0, '/Users/molder/moltbot/fizzy-tracker')
from memoria_local import *

# Agregar memoria
add("El usuario prefiere respuestas breves", "preferencia")
add_fact("Ollama corriendo en localhost:11434")
add_preference("El usuario quiere proactividad sin molestar")

# Buscar
results = search("preferencias del usuario")

# Listar
list_memories()
stats()
```

### Comandos CLI:
```bash
# Agregar
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py add "texto" [categoría]
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py pref "preferencia"
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py fact "hecho"

# Buscar
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py search "query"

# Listar
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py list
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py stats
```

### Categorías:
- **general** - Memorias generales
- **preferencia** - Preferencias del usuario
- **hecho** - Facts y datos
- **tarea** - Tareas pendientes
- **contexto** - Contexto de conversación

---

## 📦 Mem0 Cloud (Búsqueda Semántica)

**API Key:** `m0-BaJE0pOCCpJujBbLZCZRFxykr9yzUpylQNj5wQWN`
**User ID:** `moltbot`

Mem0 Cloud proporciona búsqueda semántica avanzada para encontrar contexto relevante.

---

## 🧪 Testing

```bash
# Verificar Memoria Local
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py stats

# Probar búsqueda
python3 /Users/molder/moltbot/fizzy-tracker/memoria-local.py search "preferencias"
```

---

## 📁 Archivos

- `/Users/molder/moltbot/fizzy-tracker/memoria-local.py` - Memoria local simple
- `~/.moltbot/memory/memory.json` - Datos persistentes
