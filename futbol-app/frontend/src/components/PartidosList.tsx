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
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    FormControlLabel,
    Switch,
    alpha
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Partido, Estadistica, Jugador } from '../types/index';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { getPartidos, createPartido, deletePartido, getJugadores, registrarEstadisticasMultiple, getEstadisticasPartido } from '../services/api';

// Agregamos el estilo para la fuente musical
const musicalStyle = {
    fontFamily: "'Dancing Script', cursive",
    fontSize: '1.5rem',
    color: '#1565c0',
    textAlign: 'center' as const,
    margin: '20px 0',
    textShadow: '1px 1px 2px rgba(0,0,0,0.1)'
};

const PartidosList: React.FC = () => {
    const theme = useTheme();
    const [openDialog, setOpenDialog] = useState(false);
    const [editDialog, setEditDialog] = useState(false);
    const [selectedPartido, setSelectedPartido] = useState<Partido | null>(null);
    const queryClient = useQueryClient();

    const { data: partidos = [] } = useQuery('partidos', getPartidos);
    const { data: jugadores = [] } = useQuery('jugadores', getJugadores);

    const [partidoData, setPartidoData] = useState<Partial<Partido>>({
        fecha: new Date().toISOString().split('T')[0],
        rival: '',
        resultado_local: null,
        resultado_visitante: null,
        lugar: '',
        tipo: 'PARTIDO'
    });

    const [estadisticasData, setEstadisticasData] = useState<Record<number, Partial<Estadistica>>>({});

    const createPartidoMutation = useMutation(createPartido, {
        onSuccess: () => {
            queryClient.invalidateQueries('partidos');
            setOpenDialog(false);
        }
    });

    const deletePartidoMutation = useMutation(deletePartido, {
        onSuccess: () => {
            queryClient.invalidateQueries('partidos');
        }
    });

    const registrarEstadisticasMutation = useMutation(registrarEstadisticasMultiple, {
        onSuccess: () => {
            queryClient.invalidateQueries('estadisticas');
            queryClient.invalidateQueries('partidos');
            setEditDialog(false);
        }
    });

    const handleOpenDialog = () => {
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setPartidoData({
            fecha: new Date().toISOString().split('T')[0],
            rival: '',
            resultado_local: null,
            resultado_visitante: null,
            lugar: '',
            tipo: 'PARTIDO'
        });
    };

    const handleSubmitPartido = () => {
        if (partidoData.rival) {
            createPartidoMutation.mutate({
                fecha: new Date(partidoData.fecha!).toISOString(),
                rival: partidoData.rival,
                resultado_local: partidoData.resultado_local,
                resultado_visitante: partidoData.resultado_visitante,
                lugar: partidoData.lugar || '',
                tipo: partidoData.tipo || 'PARTIDO'
            } as Omit<Partido, 'id'>);
        }
    };

    const handleDeletePartido = (id: number) => {
        deletePartidoMutation.mutate(id);
    };

    const handleEditPartido = async (partido: Partido) => {
        setSelectedPartido(partido);
        setEditDialog(true);
        
        try {
            const estadisticasPartido = await getEstadisticasPartido(partido.id);
            const estadisticasIniciales: Record<number, Partial<Estadistica>> = {};
            
            estadisticasPartido.jugadores.forEach(est => {
                estadisticasIniciales[est.jugador_id] = {
                    goles: est.goles,
                    asistencias: est.asistencias,
                    tarjetas_amarillas: est.tarjetas_amarillas,
                    tarjetas_rojas: est.tarjetas_rojas,
                    minutos_jugados: est.minutos_jugados,
                    titular: est.titular
                };
            });
            
            setEstadisticasData(estadisticasIniciales);
        } catch (error) {
            console.error('Error al cargar las estadísticas:', error);
            setEstadisticasData({});
        }
    };

    const handleCloseEditDialog = () => {
        setEditDialog(false);
        setSelectedPartido(null);
        setEstadisticasData({});
    };

    const handleSubmitEstadisticas = () => {
        if (selectedPartido) {
            const estadisticas = Object.entries(estadisticasData).map(([jugadorId, data]) => ({
                jugador_id: parseInt(jugadorId),
                partido_id: selectedPartido.id,
                goles: data.goles || 0,
                asistencias: data.asistencias || 0,
                tarjetas_amarillas: data.tarjetas_amarillas || 0,
                tarjetas_rojas: data.tarjetas_rojas || 0,
                minutos_jugados: data.minutos_jugados || 0,
                titular: data.titular || false
            }));

            registrarEstadisticasMutation.mutate(estadisticas);
        }
    };

    return (
        <Box>
            
            
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6" component="h2">
                    Partidos
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={handleOpenDialog}
                    sx={{
                        background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                        color: 'white',
                        '&:hover': {
                            background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`
                        }
                    }}
                >
                    Nuevo Partido
                </Button>
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
                            <TableCell>Fecha</TableCell>
                            <TableCell>Rival</TableCell>
                            <TableCell>Lugar</TableCell>
                            <TableCell>Resultado</TableCell>
                            <TableCell>Acciones</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {partidos.map((partido) => (
                            <TableRow key={partido.id}>
                                <TableCell>{new Date(partido.fecha).toLocaleDateString()}</TableCell>
                                <TableCell>{partido.rival}</TableCell>
                                <TableCell>{partido.lugar}</TableCell>
                                <TableCell>{partido.resultado_local} - {partido.resultado_visitante}</TableCell>
                                <TableCell>
                                    <IconButton 
                                        size="small" 
                                        onClick={() => handleEditPartido(partido)}
                                    >
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton 
                                        size="small" 
                                        onClick={() => handleDeletePartido(partido.id)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Dialog para crear nuevo partido */}
            <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>Nuevo Partido</DialogTitle>
                <DialogContent>
                    <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <TextField
                            label="Fecha"
                            type="date"
                            value={partidoData.fecha}
                            onChange={(e) => setPartidoData({ ...partidoData, fecha: e.target.value })}
                            fullWidth
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                        <TextField
                            label="Rival"
                            value={partidoData.rival}
                            onChange={(e) => setPartidoData({ ...partidoData, rival: e.target.value })}
                            fullWidth
                        />
                        <TextField
                            label="Lugar"
                            value={partidoData.lugar}
                            onChange={(e) => setPartidoData({ ...partidoData, lugar: e.target.value })}
                            fullWidth
                        />
                        <TextField
                            label="Goles Local"
                            type="number"
                            value={partidoData.resultado_local || ''}
                            onChange={(e) => setPartidoData({ ...partidoData, resultado_local: e.target.value ? parseInt(e.target.value) : null })}
                            fullWidth
                        />
                        <TextField
                            label="Goles Visitante"
                            type="number"
                            value={partidoData.resultado_visitante || ''}
                            onChange={(e) => setPartidoData({ ...partidoData, resultado_visitante: e.target.value ? parseInt(e.target.value) : null })}
                            fullWidth
                        />
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancelar</Button>
                    <Button onClick={handleSubmitPartido} variant="contained">Guardar</Button>
                </DialogActions>
            </Dialog>

            {/* Dialog para editar estadísticas del partido */}
            <Dialog 
                open={editDialog} 
                onClose={handleCloseEditDialog}
                maxWidth="md"
                fullWidth
            >
                <DialogTitle>
                    Estadísticas del Partido - {selectedPartido?.rival}
                </DialogTitle>
                <DialogContent>
                    <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
                        {jugadores.map((jugador) => (
                            <Box key={jugador.id} sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                                <Typography sx={{ minWidth: 150 }}>{jugador.nombre}</Typography>
                                <TextField
                                    label="Goles"
                                    type="number"
                                    size="small"
                                    sx={{ width: 100 }}
                                    value={estadisticasData[jugador.id]?.goles || 0}
                                    onChange={(e) => setEstadisticasData({
                                        ...estadisticasData,
                                        [jugador.id]: {
                                            ...estadisticasData[jugador.id],
                                            goles: parseInt(e.target.value) || 0
                                        }
                                    })}
                                />
                                <TextField
                                    label="Asistencias"
                                    type="number"
                                    size="small"
                                    sx={{ width: 100 }}
                                    value={estadisticasData[jugador.id]?.asistencias || 0}
                                    onChange={(e) => setEstadisticasData({
                                        ...estadisticasData,
                                        [jugador.id]: {
                                            ...estadisticasData[jugador.id],
                                            asistencias: parseInt(e.target.value) || 0
                                        }
                                    })}
                                />
                                <TextField
                                    label="Amarillas"
                                    type="number"
                                    size="small"
                                    sx={{ width: 100 }}
                                    value={estadisticasData[jugador.id]?.tarjetas_amarillas || 0}
                                    onChange={(e) => setEstadisticasData({
                                        ...estadisticasData,
                                        [jugador.id]: {
                                            ...estadisticasData[jugador.id],
                                            tarjetas_amarillas: parseInt(e.target.value) || 0
                                        }
                                    })}
                                />
                                <TextField
                                    label="Rojas"
                                    type="number"
                                    size="small"
                                    sx={{ width: 100 }}
                                    value={estadisticasData[jugador.id]?.tarjetas_rojas || 0}
                                    onChange={(e) => setEstadisticasData({
                                        ...estadisticasData,
                                        [jugador.id]: {
                                            ...estadisticasData[jugador.id],
                                            tarjetas_rojas: parseInt(e.target.value) || 0
                                        }
                                    })}
                                />
                                <TextField
                                    label="Minutos"
                                    type="number"
                                    size="small"
                                    sx={{ width: 100 }}
                                    value={estadisticasData[jugador.id]?.minutos_jugados || 0}
                                    onChange={(e) => setEstadisticasData({
                                        ...estadisticasData,
                                        [jugador.id]: {
                                            ...estadisticasData[jugador.id],
                                            minutos_jugados: parseInt(e.target.value) || 0
                                        }
                                    })}
                                />
                                <FormControlLabel
                                    control={
                                        <Switch
                                            checked={estadisticasData[jugador.id]?.titular || false}
                                            onChange={(e) => setEstadisticasData({
                                                ...estadisticasData,
                                                [jugador.id]: {
                                                    ...estadisticasData[jugador.id],
                                                    titular: e.target.checked
                                                }
                                            })}
                                        />
                                    }
                                    label="Titular"
                                />
                            </Box>
                        ))}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseEditDialog}>Cancelar</Button>
                    <Button onClick={handleSubmitEstadisticas} variant="contained">Guardar Estadísticas</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default PartidosList; 