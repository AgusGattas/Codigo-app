import axios from 'axios';
import { Jugador, Asistencia, Elemento, ElementoAsignado, Partido, Estadistica, EstadisticasJugador, EstadisticasPartido, Asignacion } from '../types/index';

const api = axios.create({
    baseURL: 'http://localhost:8000'
});

// Jugadores
export const getJugadores = () => api.get<Jugador[]>('/jugadores').then(res => res.data);
export const createJugador = (jugador: Omit<Jugador, 'id'>) => 
    api.post<Jugador>('/jugadores', jugador).then(res => res.data);
export const updateJugador = (id: number, jugador: Omit<Jugador, 'id'>) =>
    api.put<Jugador>(`/jugadores/${id}`, jugador).then(res => res.data);
export const deleteJugador = (id: number) =>
    api.delete(`/jugadores/${id}`).then(res => res.data);

// Asistencias
export const getAsistencias = (fecha?: string, tipo?: string) =>
    api.get<Asistencia[]>('/asistencias', { params: { fecha, tipo } }).then(res => res.data);
export const createAsistencia = (asistencia: Omit<Asistencia, 'id'>) =>
    api.post<Asistencia>('/asistencias', asistencia).then(res => res.data);
export const getAsistenciasJugador = (jugadorId: number) =>
    api.get<Asistencia[]>(`/asistencias/jugador/${jugadorId}`).then(res => res.data);

// Elementos
export const getElementos = () =>
    api.get<Elemento[]>('/elementos').then(res => res.data);
export const createElemento = (elemento: Omit<Elemento, 'id'>) =>
    api.post<Elemento>('/elementos', elemento).then(res => res.data);
export const updateElemento = async (id: number, elemento: Omit<Elemento, 'id'>): Promise<Elemento> => {
    const response = await api.put(`/elementos/${id}`, elemento);
    return response.data;
};
export const deleteElemento = async (id: number): Promise<void> => {
    await api.delete(`/elementos/${id}`);
};

// Asignaciones
export const asignarElemento = (asignacion: Omit<ElementoAsignado, 'id'>) =>
    api.post<ElementoAsignado>('/asignaciones', asignacion).then(res => res.data);
export const devolverElemento = (asignacionId: number) =>
    api.put(`/asignaciones/devolver/${asignacionId}`).then(res => res.data);
export const getAsignacionesPendientes = () =>
    api.get<ElementoAsignado[]>('/asignaciones/pendientes').then(res => res.data);

// Servicios para Partidos
export const getPartidos = async (): Promise<Partido[]> => {
    const response = await api.get('/partidos/');
    return response.data;
};

export const getPartido = async (id: number): Promise<Partido> => {
    const response = await api.get(`/partidos/${id}`);
    return response.data;
};

export const createPartido = async (partido: Omit<Partido, 'id'>): Promise<Partido> => {
    const response = await api.post('/partidos/', partido);
    return response.data;
};

export const updatePartido = async (id: number, partido: Omit<Partido, 'id'>): Promise<Partido> => {
    const response = await api.put(`/partidos/${id}`, partido);
    return response.data;
};

export const deletePartido = async (id: number): Promise<void> => {
    await api.delete(`/partidos/${id}`);
};

// Servicios para Estadísticas
export const registrarEstadistica = async (estadistica: Omit<Estadistica, 'id' | 'fecha_registro'>): Promise<Estadistica> => {
    const response = await api.post('/estadisticas/registro/', estadistica);
    return response.data;
};

export const getEstadisticasJugador = async (jugadorId: number): Promise<EstadisticasJugador> => {
    const response = await api.get(`/estadisticas/jugadores/${jugadorId}`);
    return response.data;
};

export const getResumenEstadisticas = async (
    ordenarPor: string = 'goles',
    descendente: boolean = true
): Promise<EstadisticasJugador[]> => {
    const response = await api.get('/estadisticas/resumen/', {
        params: {
            ordenar_por: ordenarPor,
            orden: descendente ? 'desc' : 'asc'
        }
    });
    return response.data;
};

export const registrarEstadisticasMultiple = async (estadisticas: Omit<Estadistica, 'id' | 'fecha_registro'>[]): Promise<Estadistica[]> => {
    const response = await api.post('/estadisticas/registro-multiple/', estadisticas);
    return response.data;
};

export const getEstadisticasPartido = async (partidoId: number): Promise<EstadisticasPartido> => {
    const response = await api.get(`/estadisticas/partidos/${partidoId}`);
    return response.data;
};

export const createAsignacion = async (asignacion: Omit<Asignacion, 'id' | 'activo'>): Promise<Asignacion> => {
    const response = await api.post('/asignaciones', asignacion);
    return response.data;
};

export const deleteAsignacion = async (jugadorId: number, elementoId: number): Promise<void> => {
    await api.delete(`/asignaciones/desasignar/${jugadorId}/${elementoId}`);
};

export const getAsignaciones = async (jugadorId: number): Promise<Elemento[]> => {
    const response = await api.get(`/asignaciones/jugador/${jugadorId}`);
    return response.data;
};

export const rotateElementos = async (): Promise<void> => {
    await api.post('/asignaciones/rotar');
}; 