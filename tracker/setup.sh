#!/bin/bash
# Script de setup para Fizzy Tracker

set -e

echo "🔧 Setup de Fizzy Tracker para Agente"

cd "$(dirname "$0\")"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Verificar docker compose
if ! docker compose version &> /dev/null; then
    echo "❌ docker compose no está disponible"
    exit 1
fi

# Generar SECRET_KEY_BASE si no existe
if [ ! -f .env ]; then
    echo "📝 Generando configuración..."
    cp .env.example .env
    SECRET_KEY=$(openssl rand -base64 32 2>/dev/null || head -c 32 /dev/urandom | base64)
    sed -i "s/your-secret-key-min-32-chars-here/$SECRET_KEY/" .env
    echo "✅ .env creado"
else
    echo "ℹ️  .env ya existe"
fi

echo ""
echo "🚀 Iniciando contenedores..."
docker compose up -d

echo ""
echo "⏳ Esperando que Fizzy esté listo..."
sleep 10

echo ""
echo "✅ Fizzy debería estar corriendo en: http://localhost:3000"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Crear cuenta en http://localhost:3000"
echo "   2. Configurar tableros según README.md"
echo "   3. Empezar a trackear actividades!"
