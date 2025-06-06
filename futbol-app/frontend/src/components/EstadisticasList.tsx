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
    alpha,
    useMediaQuery,
    Card,
    CardContent,
    Stack,
    Grid
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
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const renderMobileView = () => (
        <Stack spacing={2}>
            {estadisticas.map((stat) => (
                <Card 
                    key={stat.jugador_id}
                    sx={{ 
                        borderRadius: 2,
                        boxShadow: theme.shadows[2],
                        '&:hover': {
                            boxShadow: theme.shadows[4],
                            transform: 'translateY(-2px)',
                            transition: 'all 0.2s ease-in-out'
                        }
                    }}
                >
                    <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                            {`${stat.nombre} ${stat.apellido}`}
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={6}>
                                <Typography variant="subtitle2" color="text.secondary">
                                    Partidos
                                </Typography>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    {stat.total_partidos}
                                </Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="subtitle2" color="text.secondary">
                                    Goles
                                </Typography>
                                <Chip 
                                    label={stat.total_goles}
                                    size="small"
                                    sx={{ 
                                        fontWeight: 'bold',
                                        background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                                        color: 'white'
                                    }}
                                />
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="subtitle2" color="text.secondary">
                                    Asistencias
                                </Typography>
                                <Chip 
                                    label={stat.total_asistencias}
                                    size="small"
                                    sx={{ 
                                        fontWeight: 'bold',
                                        background: `linear-gradient(45deg, ${theme.palette.secondary.main}, ${theme.palette.primary.main})`,
                                        color: 'white'
                                    }}
                                />
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="subtitle2" color="text.secondary">
                                    Tarjetas
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1 }}>
                                    <Chip 
                                        label={stat.total_amarillas}
                                        size="small"
                                        sx={{ 
                                            bgcolor: '#ffd700',
                                            fontWeight: 'bold',
                                            color: '#000'
                                        }}
                                    />
                                    <Chip 
                                        label={stat.total_rojas}
                                        size="small"
                                        sx={{ 
                                            bgcolor: '#ff0000',
                                            color: 'white',
                                            fontWeight: 'bold'
                                        }}
                                    />
                                </Box>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography variant="subtitle2" color="text.secondary">
                                    Promedio Minutos
                                </Typography>
                                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                    {Math.round(stat.promedio_minutos)}
                                </Typography>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>
            ))}
        </Stack>
    );

    const renderDesktopView = () => (
        <TableContainer 
            component={Paper}
            sx={{
                boxShadow: theme.shadows[3],
                borderRadius: 2,
                overflow: 'hidden',
                maxWidth: '100%',
                overflowX: 'auto'
            }}
        >
            <Table>
                <TableHead>
                    <TableRow sx={{ backgroundColor: alpha(theme.palette.primary.main, 0.1) }}>
                        <TableCell sx={{ minWidth: 200 }}>Jugador</TableCell>
                        <TableCell sx={{ minWidth: 100 }}>
                            <TableSortLabel 
                                onClick={() => onSort('partidos')}
                                active={sortField === 'partidos'}
                                direction={sortField === 'partidos' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                            >
                                Partidos
                            </TableSortLabel>
                        </TableCell>
                        <TableCell sx={{ minWidth: 100 }}>
                            <TableSortLabel 
                                onClick={() => onSort('goles')}
                                active={sortField === 'goles'}
                                direction={sortField === 'goles' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                            >
                                Goles
                            </TableSortLabel>
                        </TableCell>
                        <TableCell sx={{ minWidth: 100 }}>
                            <TableSortLabel 
                                onClick={() => onSort('asistencias')}
                                active={sortField === 'asistencias'}
                                direction={sortField === 'asistencias' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                            >
                                Asistencias
                            </TableSortLabel>
                        </TableCell>
                        <TableCell sx={{ minWidth: 100 }}>
                            <TableSortLabel 
                                onClick={() => onSort('amarillas')}
                                active={sortField === 'amarillas'}
                                direction={sortField === 'amarillas' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                            >
                                Amarillas
                            </TableSortLabel>
                        </TableCell>
                        <TableCell sx={{ minWidth: 100 }}>
                            <TableSortLabel 
                                onClick={() => onSort('rojas')}
                                active={sortField === 'rojas'}
                                direction={sortField === 'rojas' ? (sortDesc ? 'desc' : 'asc') : 'asc'}
                            >
                                Rojas
                            </TableSortLabel>
                        </TableCell>
                        <TableCell sx={{ minWidth: 150 }}>
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
                        <TableRow 
                            key={stat.jugador_id}
                            sx={{
                                '&:hover': {
                                    backgroundColor: alpha(theme.palette.primary.main, 0.05)
                                }
                            }}
                        >
                            <TableCell>{`${stat.nombre} ${stat.apellido}`}</TableCell>
                            <TableCell>{stat.total_partidos}</TableCell>
                            <TableCell>
                                <Chip 
                                    label={stat.total_goles}
                                    size="small"
                                    sx={{ 
                                        fontWeight: 'bold',
                                        background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                                        color: 'white'
                                    }}
                                />
                            </TableCell>
                            <TableCell>
                                <Chip 
                                    label={stat.total_asistencias}
                                    size="small"
                                    sx={{ 
                                        fontWeight: 'bold',
                                        background: `linear-gradient(45deg, ${theme.palette.secondary.main}, ${theme.palette.primary.main})`,
                                        color: 'white'
                                    }}
                                />
                            </TableCell>
                            <TableCell>
                                <Chip 
                                    label={stat.total_amarillas}
                                    sx={{ 
                                        bgcolor: '#ffd700',
                                        fontWeight: 'bold',
                                        color: '#000'
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
    );

    return (
        <Box>
            <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                mb: 3,
                flexDirection: { xs: 'column', sm: 'row' },
                gap: { xs: 2, sm: 0 }
            }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Estadísticas de Jugadores
                </Typography>
            </Box>

            {isMobile ? renderMobileView() : renderDesktopView()}
        </Box>
    );
};

export default EstadisticasList; 