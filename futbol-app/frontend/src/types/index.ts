export enum TipoEvento {
    ENTRENAMIENTO = "ENTRENAMIENTO",
    PARTIDO = "PARTIDO"
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