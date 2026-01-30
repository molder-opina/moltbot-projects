#!/usr/bin/env python3
"""
Memoria Local Simple para Moltbot
Sin dependencias externas - usa archivo JSON local
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

MEMORY_DIR = os.path.expanduser("~/.moltbot/memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "memory.json")

# ═══════════════════════════════════════════════════════════════
#  GESTIÓN DE MEMORIA
# ═══════════════════════════════════════════════════════════════

def init_memory():
    """Inicializar archivo de memoria si no existe"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"memories": [], "last_updated": None}, f, indent=2, ensure_ascii=False)

def load_memory() -> Dict:
    """Cargar memoria desde archivo"""
    init_memory()
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(data: Dict):
    """Guardar memoria a archivo"""
    data["last_updated"] = datetime.now().isoformat()
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════
#  OPERACIONES BÁSICAS
# ═══════════════════════════════════════════════════════════════

def add(text: str, category: str = "general") -> str:
    """Agregar memoria"""
    data = load_memory()
    
    memory = {
        "id": f"{int(datetime.now().timestamp() * 1000)}",
        "text": text,
        "category": category,
        "created": datetime.now().isoformat(),
        "usage_count": 0
    }
    
    data["memories"].append(memory)
    save_memory(data)
    
    return f"✅ Memoria guardada: {text[:50]}..."

def get(category: Optional[str] = None) -> List[Dict]:
    """Obtener memorias"""
    data = load_memory()
    
    if category:
        return [m for m in data["memories"] if m.get("category") == category]
    return data["memories"]

def delete(memory_id: str) -> bool:
    """Eliminar memoria"""
    data = load_memory()
    original_len = len(data["memories"])
    data["memories"] = [m for m in data["memories"] if m["id"] != memory_id]
    
    if len(data["memories"]) < original_len:
        save_memory(data)
        return True
    return False

def update_usage(memory_id: str):
    """Actualizar contador de uso"""
    data = load_memory()
    for m in data["memories"]:
        if m["id"] == memory_id:
            m["usage_count"] = m.get("usage_count", 0) + 1
            break
    save_memory(data)

# ═══════════════════════════════════════════════════════════════
#  BÚSQUEDA SEMÁNTICA SIMPLE
# ═══════════════════════════════════════════════════════════════

def search(query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
    """Buscar memorias - coincidencia simple de palabras"""
    data = load_memory()
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    results = []
    
    for memory in data["memories"]:
        # Filtrar por categoría
        if category and memory.get("category") != category:
            continue
        
        text_lower = memory["text"].lower()
        
        # Contar palabras coincidentes
        text_words = set(text_lower.split())
        matches = len(query_words & text_words)
        
        if matches > 0:
            # Añadir score de relevancia
            memory["_score"] = matches / max(len(query_words), 1)
            results.append(memory)
    
    # Ordenar por score y uso
    results.sort(key=lambda x: (-x.get("_score", 0), -x.get("usage_count", 0)))
    
    # Actualizar contadores de uso
    for m in results[:limit]:
        update_usage(m["id"])
    
    return results[:limit]

def search_by_text(search_text: str, limit: int = 10) -> List[str]:
    """Búsqueda simple por texto - retorna solo textos"""
    results = search(search_text, limit=limit)
    return [r["text"] for r in results]

# ═══════════════════════════════════════════════════════════════
#  CATEGORÍAS
# ═══════════════════════════════════════════════════════════════

def add_preference(text: str):
    """Agregar preferencia del usuario"""
    return add(text, category="preferencia")

def add_fact(text: str):
    """Agregar hecho/fact"""
    return add(text, category="hecho")

def add_task(text: str):
    """Agregar tarea"""
    return add(text, category="tarea")

def add_context(text: str):
    """Agregar contexto"""
    return add(text, category="contexto")

# ═══════════════════════════════════════════════════════════════
#  UTILIDADES
# ═══════════════════════════════════════════════════════════════

def stats():
    """Mostrar estadísticas de memoria"""
    data = load_memory()
    memories = data["memories"]
    
    categories = {}
    for m in memories:
        cat = m.get("category", "sin categoría")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Estadísticas de Memoria")
    print(f"   Total: {len(memories)} memorias")
    for cat, count in categories.items():
        print(f"   • {cat}: {count}")
    print()

def list_memories(category: Optional[str] = None):
    """Listar todas las memorias"""
    memories = get(category)
    
    print(f"\n📋 Memorias" + (f" [{category}]" if category else ""))
    print("-" * 50)
    
    for m in memories:
        cat = m.get("category", "gen")
        print(f"  [{cat.upper():4}] {m['text'][:60]}...")
    
    print()

def clear_all():
    """Limpiar todas las memorias (peligroso)"""
    confirm = input("⚠️ ¿Eliminar todas las memorias? (escribe 'sí'): ")
    if confirm.lower() == "sí":
        save_memory({"memories": [], "last_updated": None})
        print("✅ Memoria limpiada")
    else:
        print("❌ Cancelado")

# ═══════════════════════════════════════════════════════════════
#  MAIN / CLI
# ═══════════════════════════════════════════════════════════════

def main():
    import sys
    
    init_memory()
    
    if len(sys.argv) < 2:
        print("🧠 Memoria Local - Moltbot")
        print("=" * 40)
        print("\nUso:")
        print("  memoria.py add \"texto\"           → Agregar")
        print("  memoria.py search \"query\"        → Buscar")
        print("  memoria.py list                  → Listar todas")
        print("  memoria.py stats                 → Estadísticas")
        print("  memoria.py pref \"texto\"          → Preferencia")
        print("  memoria.py fact \"texto\"          → Hecho")
        print("  memoria.py context \"texto\"       → Contexto")
        print()
        stats()
        return
    
    command = sys.argv[1]
    text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    if command == "add":
        if text:
            add(text)
        else:
            print("❌ Falta texto")
    
    elif command == "search":
        if text:
            results = search(text)
            print(f"\n🔍 Resultados para '{text}':")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['text'][:70]}")
            print()
        else:
            print("❌ Falta query")
    
    elif command == "list":
        list_memories()
    
    elif command == "stats":
        stats()
    
    elif command == "pref":
        if text:
            add_preference(text)
        else:
            print("❌ Falta texto")
    
    elif command == "fact":
        if text:
            add_fact(text)
        else:
            print("❌ Falta texto")
    
    elif command == "context":
        if text:
            add_context(text)
        else:
            print("❌ Falta texto")
    
    elif command == "clear":
        clear_all()
    
    else:
        print(f"❌ Comando desconocido: {command}")

if __name__ == "__main__":
    main()
