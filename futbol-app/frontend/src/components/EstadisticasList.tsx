import React, { useState } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    IconButton,
    Box,
    Typography,
    useTheme,
    Chip,
    TableSortLabel,
    alpha
} from '@mui/material';
import { EstadisticasJugador } from '../types/index';

interface EstadisticasListProps {
    estadisticas: EstadisticasJugador[];
    onSort: (campo: string) => void;
    sortField: string;
    sortDesc: boolean;
}

const EstadisticasList: React.FC<EstadisticasListProps> = ({ estadisticas, onSort, sortField, sortDesc }) => {
    const theme = useTheme();

    return (
        <Box>
            <Box sx={{ mb: 3 }}>
                <Typography variant="h6" component="h2">
                    Estadísticas de Jugadores
                </Typography>
            </Box>

            <TableContainer 
                component={Paper}
                sx={{
                    boxShadow: theme.shadows[3],
                    borderRadius: 2,
                    overflow: 'hidden'
                }}
            >
                <Table>
                    <TableHead>
                        <TableRow sx={{ backgroundColor: alpha(theme.palette.primary.main, 0.1) }}>
                            <TableCell>Jugador</TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('partidos')}
                                    active={sortField === 'partidos'}
                                    direction={sortField === 'partidos' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Partidos
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('goles')}
                                    active={sortField === 'goles'}
                                    direction={sortField === 'goles' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Goles
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('asistencias')}
                                    active={sortField === 'asistencias'}
                                    direction={sortField === 'asistencias' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Asistencias
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('amarillas')}
                                    active={sortField === 'amarillas'}
                                    direction={sortField === 'amarillas' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Amarillas
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('rojas')}
                                    active={sortField === 'rojas'}
                                    direction={sortField === 'rojas' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Rojas
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel 
                                    onClick={() => onSort('minutos')}
                                    active={sortField === 'minutos'}
                                    direction={sortField === 'minutos' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                                >
                                    Promedio Minutos
                                </TableSortLabel>
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {estadisticas.map((stat) => (
                            <TableRow key={stat.jugador_id}>
                                <TableCell>{stat.nombre_jugador}</TableCell>
                                <TableCell>{stat.total_partidos}</TableCell>
                                <TableCell>
                                    <Chip 
                                        label={stat.total_goles}
                                        color="primary"
                                        size="small"
                                        sx={{ fontWeight: 'bold' }}
                                    />
                                </TableCell>
                                <TableCell>
                                    <Chip 
                                        label={stat.total_asistencias}
                                        color="secondary"
                                        size="small"
                                        sx={{ fontWeight: 'bold' }}
                                    />
                                </TableCell>
                                <TableCell>
                                    <Chip 
                                        label={stat.total_amarillas}
                                        sx={{ 
                                            bgcolor: '#ffd700',
                                            fontWeight: 'bold'
                                        }}
                                        size="small"
                                    />
                                </TableCell>
                                <TableCell>
                                    <Chip 
                                        label={stat.total_rojas}
                                        sx={{ 
                                            bgcolor: '#ff0000',
                                            color: 'white',
                                            fontWeight: 'bold'
                                        }}
                                        size="small"
                                    />
                                </TableCell>
                                <TableCell>{Math.round(stat.promedio_minutos)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default EstadisticasList; 