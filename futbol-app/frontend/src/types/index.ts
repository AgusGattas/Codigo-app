export enum TipoEvento {
    PARTIDO = 'PARTIDO',
    ENTRENAMIENTO = 'ENTRENAMIENTO',
    TORNEO = 'TORNEO'
}

export interface Jugador {
    id: number;
    nombre: string;
    apellido: string;
    fecha_nacimiento: string;
    posicion: string;
    numero: number;
    activo: boolean;
    created_at?: string;
    updated_at?: string | null;
}

export interface Asistencia {
    id: number;
    jugador_id: number;
    partido_id: number;
    presente: boolean;
    justificacion: string | null;
    created_at: string;
    updated_at: string | null;
    jugador: Jugador;
}

export interface Partido {
    id: number;
    fecha: string;
    rival: string;
    resultado_local: number | null;
    resultado_visitante: number | null;
    lugar: string;
    tipo: TipoEvento;
    created_at: string;
    updated_at: string | null;
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
    created_at: string;
    updated_at: string | null;
}

export interface EstadisticasJugador {
    jugador_id: number;
    nombre: string;
    apellido: string;
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