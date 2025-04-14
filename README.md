# Futbol App

Aplicación para gestionar un equipo de fútbol, incluyendo jugadores, partidos, estadísticas y elementos del equipo.

## Características

- **Gestión de Jugadores**: Registro y seguimiento de jugadores del equipo
- **Gestión de Partidos**: Registro de partidos, resultados y estadísticas
- **Estadísticas**: Seguimiento detallado de estadísticas por jugador (goles, asistencias, tarjetas, minutos jugados)
- **Elementos del Equipo**: Gestión de elementos como pelotas, canchas, arcos, etc.
- **Asignaciones**: Sistema de rotación de elementos entre jugadores

## Tecnologías

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- PostgreSQL
- Alembic (migraciones)

### Frontend
- React
- TypeScript
- Material-UI
- React Query

## Estructura del Proyecto

```
futbol-app/
├── backend/           # API FastAPI
│   ├── app/           # Código de la aplicación
│   ├── alembic/       # Migraciones de base de datos
│   └── requirements.txt
└── frontend/          # Aplicación React
    ├── src/           # Código fuente
    ├── public/        # Archivos estáticos
    └── package.json
```

## Instalación

### Backend

1. Crear un entorno virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos:
```bash
# Crear archivo .env con las credenciales de la base de datos
# Ejecutar migraciones
alembic upgrade head
```

4. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Iniciar la aplicación:
```bash
npm run dev
```

## Uso

- Acceder a la aplicación en `http://localhost:3000`
- La API está disponible en `http://localhost:8000`
- Documentación de la API en `http://localhost:8000/docs`

## Licencia

MIT 