import { useState, useEffect } from 'react';
import {
    Box,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    IconButton,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    useTheme,
    alpha,
    Chip,
    Tooltip
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Refresh as RefreshIcon } from '@mui/icons-material';
import { useMutation, useQueryClient } from 'react-query';
import { Asignacion, Elemento, Jugador, TipoElemento } from '../types';
import { createAsignacion, deleteAsignacion, getAsignaciones, rotateElementos } from '../services/api';

interface AsignacionesListProps {
    jugadores: Jugador[];
    elementos: Elemento[];
    asignaciones: Asignacion[];
}

export default function AsignacionesList({ jugadores, elementos, asignaciones }: AsignacionesListProps) {
    const theme = useTheme();
    const [openDialog, setOpenDialog] = useState(false);
    const [formData, setFormData] = useState({
        jugador_id: 0,
        elemento_id: 0,
        fecha_asignacion: new Date().toISOString().split('T')[0]
    });

    const queryClient = useQueryClient();

    const createMutation = useMutation(createAsignacion, {
        onSuccess: () => {
            queryClient.invalidateQueries('asignaciones');
            handleCloseDialog();
        }
    });

    const deleteMutation = useMutation(deleteAsignacion, {
        onSuccess: () => {
            queryClient.invalidateQueries('asignaciones');
        }
    });

    const rotateMutation = useMutation(rotateElementos, {
        onSuccess: () => {
            queryClient.invalidateQueries('asignaciones');
        }
    });

    const handleOpenDialog = () => {
        setFormData({
            jugador_id: 0,
            elemento_id: 0,
            fecha_asignacion: new Date().toISOString().split('T')[0]
        });
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setFormData({
            jugador_id: 0,
            elemento_id: 0,
            fecha_asignacion: new Date().toISOString().split('T')[0]
        });
    };

    const handleSubmit = () => {
        createMutation.mutate({
            jugador_id: Number(formData.jugador_id),
            elemento_id: Number(formData.elemento_id),
            fecha_asignacion: formData.fecha_asignacion
        });
    };

    const handleDelete = (id: number) => {
        if (window.confirm('¿Estás seguro de que deseas eliminar esta asignación?')) {
            deleteMutation.mutate(id);
        }
    };

    const handleRotate = () => {
        if (window.confirm('¿Estás seguro de que deseas rotar los elementos entre los jugadores?')) {
            rotateMutation.mutate();
        }
    };

    const getElementoColor = (tipo: TipoElemento) => {
        switch (tipo) {
            case TipoElemento.PELOTA:
                return theme.palette.primary.main;
            case TipoElemento.PECHERA:
                return theme.palette.secondary.main;
            case TipoElemento.AGUA:
                return theme.palette.info.main;
            case TipoElemento.CONJUNTO:
                return theme.palette.success.main;
            default:
                return theme.palette.grey[500];
        }
    };

    const renderDesktopView = () => (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Jugador</TableCell>
                        <TableCell>Elemento</TableCell>
                        <TableCell>Fecha de Asignación</TableCell>
                        <TableCell>Estado</TableCell>
                        <TableCell>Acciones</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {asignaciones.map((asignacion) => {
                        const jugador = jugadores.find(j => j.id === asignacion.jugador_id);
                        const elemento = elementos.find(e => e.id === asignacion.elemento_id);
                        return (
                            <TableRow key={asignacion.id}>
                                <TableCell>{jugador?.nombre}</TableCell>
                                <TableCell>
                                    <Chip
                                        label={elemento?.nombre}
                                        size="small"
                                        sx={{
                                            bgcolor: alpha(getElementoColor(elemento?.tipo || TipoElemento.PELOTA), 0.1),
                                            color: getElementoColor(elemento?.tipo || TipoElemento.PELOTA),
                                            fontWeight: 'bold'
                                        }}
                                    />
                                </TableCell>
                                <TableCell>{new Date(asignacion.fecha_asignacion).toLocaleDateString()}</TableCell>
                                <TableCell>
                                    <Chip
                                        label={asignacion.activo ? 'Activo' : 'Inactivo'}
                                        size="small"
                                        color={asignacion.activo ? 'success' : 'default'}
                                    />
                                </TableCell>
                                <TableCell>
                                    <IconButton onClick={() => handleDelete(asignacion.id)}>
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );

    return (
        <Box sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h5">Asignaciones</Typography>
                <Box>
                    <Tooltip title="Rotar elementos entre jugadores">
                        <IconButton
                            onClick={handleRotate}
                            sx={{ mr: 1 }}
                            color="primary"
                        >
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                    <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={handleOpenDialog}
                    >
                        Nueva Asignación
                    </Button>
                </Box>
            </Box>

            {renderDesktopView()}

            <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>Nueva Asignación</DialogTitle>
                <DialogContent>
                    <FormControl fullWidth margin="dense">
                        <InputLabel>Jugador</InputLabel>
                        <Select
                            value={formData.jugador_id}
                            label="Jugador"
                            onChange={(e) => setFormData({ ...formData, jugador_id: Number(e.target.value) })}
                        >
                            {jugadores.map((jugador) => (
                                <MenuItem key={jugador.id} value={jugador.id}>
                                    {jugador.nombre}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="dense">
                        <InputLabel>Elemento</InputLabel>
                        <Select
                            value={formData.elemento_id}
                            label="Elemento"
                            onChange={(e) => setFormData({ ...formData, elemento_id: Number(e.target.value) })}
                        >
                            {elementos
                                .filter(e => e.activo)
                                .map((elemento) => (
                                    <MenuItem key={elemento.id} value={elemento.id}>
                                        {elemento.nombre}
                                    </MenuItem>
                                ))}
                        </Select>
                    </FormControl>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancelar</Button>
                    <Button onClick={handleSubmit} variant="contained">
                        Crear
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
} 