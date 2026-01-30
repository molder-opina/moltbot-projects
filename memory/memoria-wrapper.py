#!/usr/bin/env python3
"""
Wrapper de Memoria para Moltbot
Combina: Memoria Local Simple + Mem0 Cloud (si hay API key)
"""

import os
import sys
import json
from typing import List, Dict, Optional

# ═══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

MEMORY_DIR = os.path.expanduser("~/.moltbot/memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "memory.json")

# Mem0 Cloud
MEM0_API_KEY = os.environ.get("MEM0_API_KEY", "m0-BaJE0pOCCpJujBbLZCZRFxykr9yzUpylQNj5wQWN")

# ═══════════════════════════════════════════════════════════════
#  MEMORIA LOCAL (PRIMARIA)
# ═══════════════════════════════════════════════════════════════

def load_local_memory() -> Dict:
    """Cargar memoria local"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"memories": [], "last_updated": None}, f, indent=2)
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_local_memory(data: Dict):
    """Guardar memoria local"""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def local_search(query: str, limit: int = 5) -> List[str]:
    """Búsqueda local simple"""
    data = load_local_memory()
    query_words = set(query.lower().split())
    results = []
    
    for m in data.get("memories", []):
        text_words = set(m.get("text", "").lower().split())
        if query_words & text_words:
            results.append(m.get("text", ""))
    
    return results[:limit]

def local_add(text: str, category: str = "general"):
    """Agregar a memoria local"""
    data = load_local_memory()
    data["memories"].append({
        "id": str(int(__import__('time').time() * 1000)),
        "text": text,
        "category": category,
        "created": __import__('datetime').datetime.now().isoformat()
    })
    save_local_memory(data)

# ═══════════════════════════════════════════════════════════════
#  MEM0 CLOUD (BÚSQUEDA SEMÁNTICA)
# ═══════════════════════════════════════════════════════════════

_mem0_available = False
_memory_instance = None

def init_mem0() -> bool:
    """Inicializar Mem0 Cloud"""
    global _mem0_available, _memory_instance
    
    try:
        from mem0 import Memory
        
        _memory_instance = Memory.from_config({
            "version": "v1",
            "user_id": "moltbot"
        })
        _mem0_available = True
        return True
    except Exception as e:
        print(f"⚠️ Mem0 Cloud no disponible: {e}")
        _mem0_available = False
        return False

def mem0_search(query: str, limit: int = 5) -> List[str]:
    """Buscar con Mem0 Cloud"""
    if not _mem0_available:
        return []
    
    try:
        results = _memory_instance.search(query, user_id="moltbot", limit=limit)
        return [r.get("text", "") for r in results]
    except Exception as e:
        print(f"⚠️ Error en Mem0 search: {e}")
        return []

def mem0_add(text: str):
    """Agregar con Mem0 Cloud"""
    if not _mem0_available:
        return False
    
    try:
        _memory_instance.add(text, user_id="moltbot")
        return True
    except Exception as e:
        print(f"⚠️ Error en Mem0 add: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
#  API UNIFICADA
# ═══════════════════════════════════════════════════════════════

class Memoria:
    """API unificada de memoria"""
    
    def __init__(self):
        self.mem0_enabled = init_mem0()
        print(f"🧠 Memoria: Local={'✅'} Mem0 Cloud={'✅' if self.mem0_enabled else '❌'}")
    
    def add(self, text: str, category: str = "general") -> str:
        """Agregar memoria (Mem0 Cloud + local)"""
        # Mem0 Cloud
        if self.mem0_enabled:
            try:
                mem0_add(text)
            except:
                pass
        
        # Memoria local
        local_add(text, category)
        return f"✅ Guardado: {text[:40]}..."
    
    def search(self, query: str, limit: int = 5) -> List[str]:
        """Buscar memorias"""
        results = []
        
        # Mem0 Cloud (semántica)
        if self.mem0_enabled:
            mem0_results = mem0_search(query, limit)
            results.extend(mem0_results)
        
        # Local (palabras clave)
        if len(results) < limit:
            local_results = local_search(query, limit - len(results))
            results.extend(local_results)
        
        # Deduplicar
        seen = set()
        unique = []
        for r in results:
            if r and r not in seen:
                seen.add(r)
                unique.append(r)
        
        return unique[:limit]
    
    def get_all(self, category: Optional[str] = None) -> List[Dict]:
        """Obtener todas las memorias"""
        data = load_local_memory()
        memories = data.get("memories", [])
        
        if category:
            memories = [m for m in memories if m.get("category") == category]
        
        return memories
    
    def stats(self) -> Dict:
        """Estadísticas"""
        data = load_local_memory()
        memories = data.get("memories", [])
        
        categories = {}
        for m in memories:
            cat = m.get("category", "sin categoría")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total": len(memories),
            "categories": categories,
            "mem0_enabled": self.mem0_enabled
        }

# ═══════════════════════════════════════════════════════════════
#  CLI / MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("🧠 Memoria Wrapper - Moltbot")
        print("=" * 40)
        print("\nUso:")
        print("  memoria.py add \"texto\" [categoría]")
        print("  memoria.py search \"query\"")
        print("  memoria.py list")
        print("  memoria.py stats")
        print()
        
        mem = Memoria()
        s = mem.stats()
        print(f"📊 Total: {s['total']} memorias")
        return
    
    command = sys.argv[1]
    text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    mem = Memoria()
    
    if command == "add":
        if text:
            print(mem.add(text))
        else:
            print("❌ Falta texto")
    
    elif command == "search":
        if text:
            results = mem.search(text)
            print(f"\n🔍 Resultados para '{text}':")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r[:70]}...")
            print()
        else:
            print("❌ Falta query")
    
    elif command == "list":
        memories = mem.get_all()
        print(f"\n📋 Todas las memorias ({len(memories)}):")
        for m in memories:
            cat = m.get("category", "gen")
            print(f"  [{cat.upper():4}] {m['text'][:60]}...")
        print()
    
    elif command == "stats":
        s = mem.stats()
        print(f"\n📊 Estadísticas")
        print(f"   Total: {s['total']} memorias")
        print(f"   Mem0 Cloud: {'✅' if s['mem0_enabled'] else '❌'}")
        for cat, count in s.get("categories", {}).items():
            print(f"   • {cat}: {count}")
        print()

if __name__ == "__main__":
    main()
