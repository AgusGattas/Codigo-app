export enum TipoEvento {
    ENTRENAMIENTO = "ENTRENAMIENTO",
    PARTIDO = "PARTIDO"
}

export enum TipoElemento {
    PELOTA = "PELOTA",
    PECHERA = "PECHERA",
    AGUA = "AGUA",
    CONJUNTO = "CONJUNTO"
}

export interface Jugador {
    id: number;
    nombre: string;
    activo: boolean;
}

export interface Asistencia {
    id: number;
    jugador_id: number;
    fecha: string;
    tipo: TipoEvento;
    presente: boolean;
}

export interface Elemento {
    id: number;
    nombre: string;
    descripcion?: string;
    tipo: TipoElemento;
    cantidad: number;
    activo: boolean;
}

export interface ElementoAsignado {
    id: number;
    jugador_id: number;
    elemento_id: number;
    fecha_asignacion: string;
    fecha_devolucion?: string;
    devuelto: boolean;
}

export interface Partido {
    id: number;
    fecha: string;
    rival: string;
    resultado_local: number | null;
    resultado_visitante: number | null;
    lugar: string;
    tipo: string;
}

export interface Estadistica {
    id: number;
    jugador_id: number;
    partido_id: number;
    goles: number;
    asistencias: number;
    tarjetas_amarillas: number;
    tarjetas_rojas: number;
    minutos_jugados: number;
    titular: boolean;
    fecha_registro: string;
}

export interface EstadisticasJugador {
    jugador_id: number;
    nombre_jugador: string;
    total_partidos: number;
    total_goles: number;
    total_asistencias: number;
    total_amarillas: number;
    total_rojas: number;
    minutos_totales: number;
    promedio_minutos: number;
}

export interface EstadisticasPartido {
    partido_id: number;
    fecha: string;
    rival: string;
    resultado_local: number | null;
    resultado_visitante: number | null;
    lugar: string;
    tipo: string;
    jugadores: Estadistica[];
}

export interface Asignacion {
    id: number;
    jugador_id: number;
    elemento_id: number;
    fecha_asignacion: string;
    activo: boolean;
} 