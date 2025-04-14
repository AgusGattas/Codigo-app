# Aplicación de Gestión de Equipo de Fútbol

Esta aplicación permite gestionar los elementos del equipo de fútbol, incluyendo jugadores, elementos (pelotas, pecheras, aguas, conjuntos) y sus asignaciones.

## Estructura del Proyecto

```
futbol-app/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── models/   # Modelos de la base de datos
│   │   ├── schemas/  # Esquemas Pydantic
│   │   ├── routes/   # Rutas de la API
│   │   └── services/ # Servicios de la aplicación
│   └── requirements.txt
└── frontend/         # Aplicación Next.js
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── types/
    └── package.json
```

## Requisitos

- Python 3.8+
- Node.js 14+
- npm o yarn

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
# Crear un archivo .env en la carpeta backend con:
DATABASE_URL=sqlite:///./futbol_app.db
```

4. Ejecutar el servidor:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Ejecutar el servidor de desarrollo:
```bash
npm run dev
```

## Uso

1. Acceder a la aplicación web en `http://localhost:3000`
2. La documentación de la API está disponible en `http://localhost:8000/docs`

## Funcionalidades

- Gestión de jugadores (agregar, editar, eliminar)
- Gestión de elementos (agregar, ver lista)
- Asignación de elementos a jugadores
- Registro de devoluciones
- Seguimiento de asistencias

## Tecnologías Utilizadas

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

### Frontend
- Next.js
- TypeScript
- Material-UI
- React Query
- Axios 