import React, { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Button,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    IconButton,
    Box,
    Typography,
    useTheme,
    alpha,
    Avatar,
    useMediaQuery,
    Card,
    CardContent,
    CardActions,
    Stack,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Chip
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon, SportsSoccer as SportsSoccerIcon } from '@mui/icons-material';
import { useMutation, useQueryClient } from 'react-query';
import { Elemento, TipoElemento } from '../types/index';
import { createElemento, updateElemento, deleteElemento, getElementos } from '../services/api';

const ELEMENTOS_PREDEFINIDOS = [
    { nombre: 'Pelota 1', tipo: TipoElemento.PELOTA, cantidad: 1, descripcion: 'Pelota oficial del equipo' },
    { nombre: 'Pelota 2', tipo: TipoElemento.PELOTA, cantidad: 1, descripcion: 'Pelota de respaldo' },
    { nombre: 'Pecheras', tipo: TipoElemento.PECHERA, cantidad: 15, descripcion: 'Set de pecheras para entrenamiento' },
    { nombre: 'Agua', tipo: TipoElemento.AGUA, cantidad: 24, descripcion: 'Botellas de agua para el equipo' },
    { nombre: 'Conjunto Local', tipo: TipoElemento.CONJUNTO, cantidad: 15, descripcion: 'Uniforme local completo' },
    { nombre: 'Conjunto Visitante', tipo: TipoElemento.CONJUNTO, cantidad: 15, descripcion: 'Uniforme visitante completo' }
];

interface ElementosListProps {
    elementos: Elemento[];
}

const ElementosList: React.FC<ElementosListProps> = ({ elementos }) => {
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedElemento, setSelectedElemento] = useState<Elemento | null>(null);
    const [formData, setFormData] = useState<Omit<Elemento, 'id'>>({
        nombre: '',
        descripcion: '',
        tipo: TipoElemento.PELOTA,
        cantidad: 0,
        activo: true
    });
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const queryClient = useQueryClient();

    const createMutation = useMutation(createElemento, {
        onSuccess: () => {
            queryClient.invalidateQueries('elementos');
            handleCloseDialog();
        }
    });

    const updateMutation = useMutation(
        (data: { id: number; elemento: Omit<Elemento, 'id'> }) =>
            updateElemento(data.id, data.elemento),
        {
            onSuccess: () => {
                queryClient.invalidateQueries('elementos');
                handleCloseDialog();
            }
        }
    );

    const deleteMutation = useMutation(deleteElemento, {
        onSuccess: () => {
            queryClient.invalidateQueries('elementos');
        }
    });

    useEffect(() => {
        // Verificar si los elementos predefinidos ya existen
        const elementosExistentes = elementos.map(e => e.nombre);
        const elementosFaltantes = ELEMENTOS_PREDEFINIDOS.filter(
            e => !elementosExistentes.includes(e.nombre)
        );

        // Crear elementos predefinidos faltantes
        elementosFaltantes.forEach(elemento => {
            createMutation.mutate({
                ...elemento,
                activo: true
            });
        });
    }, [elementos]);

    const handleOpenDialog = (elemento?: Elemento) => {
        if (elemento) {
            setSelectedElemento(elemento);
            setFormData({
                nombre: elemento.nombre,
                descripcion: elemento.descripcion || '',
                tipo: elemento.tipo,
                cantidad: elemento.cantidad,
                activo: elemento.activo
            });
        } else {
            setSelectedElemento(null);
            setFormData({
                nombre: '',
                descripcion: '',
                tipo: TipoElemento.PELOTA,
                cantidad: 0,
                activo: true
            });
        }
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setSelectedElemento(null);
    };

    const handleSubmit = () => {
        if (selectedElemento) {
            updateMutation.mutate({
                id: selectedElemento.id,
                elemento: formData
            });
        } else {
            createMutation.mutate(formData);
        }
    };

    const handleDelete = (id: number) => {
        if (window.confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
            deleteMutation.mutate(id);
        }
    };

    const getTipoColor = (tipo: TipoElemento) => {
        switch (tipo) {
            case TipoElemento.PELOTA:
                return theme.palette.primary.main;
            case TipoElemento.PECHERA:
                return theme.palette.success.main;
            case TipoElemento.AGUA:
                return theme.palette.warning.main;
            case TipoElemento.CONJUNTO:
                return theme.palette.info.main;
            default:
                return theme.palette.grey[500];
        }
    };

    const renderMobileView = () => (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {elementos.map((elemento) => (
                <Card key={elemento.id}>
                    <CardContent>
                        <Typography variant="h6">{elemento.nombre}</Typography>
                        <Chip
                            label={elemento.tipo}
                            sx={{
                                backgroundColor: getTipoColor(elemento.tipo),
                                color: 'white',
                                mt: 1,
                            }}
                        />
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                            Estado: {elemento.activo ? 'Activo' : 'Inactivo'}
                        </Typography>
                    </CardContent>
                    <CardActions>
                        <IconButton onClick={() => handleOpenDialog(elemento)}>
                            <EditIcon />
                        </IconButton>
                        <IconButton onClick={() => handleDelete(elemento.id)}>
                            <DeleteIcon />
                        </IconButton>
                    </CardActions>
                </Card>
            ))}
        </Box>
    );

    const renderDesktopView = () => (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Nombre</TableCell>
                        <TableCell>Descripción</TableCell>
                        <TableCell>Tipo</TableCell>
                        <TableCell>Cantidad</TableCell>
                        <TableCell>Estado</TableCell>
                        <TableCell>Acciones</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {elementos.map((elemento) => (
                        <TableRow key={elemento.id}>
                            <TableCell>{elemento.nombre}</TableCell>
                            <TableCell>{elemento.descripcion}</TableCell>
                            <TableCell>
                                <Chip
                                    label={elemento.tipo}
                                    size="small"
                                    sx={{
                                        bgcolor: alpha(getTipoColor(elemento.tipo), 0.1),
                                        color: getTipoColor(elemento.tipo),
                                        fontWeight: 'bold'
                                    }}
                                />
                            </TableCell>
                            <TableCell>{elemento.cantidad}</TableCell>
                            <TableCell>
                                <Chip
                                    label={elemento.activo ? 'Activo' : 'Inactivo'}
                                    size="small"
                                    color={elemento.activo ? 'success' : 'default'}
                                />
                            </TableCell>
                            <TableCell>
                                <IconButton onClick={() => handleOpenDialog(elemento)}>
                                    <EditIcon />
                                </IconButton>
                                <IconButton onClick={() => handleDelete(elemento.id)}>
                                    <DeleteIcon />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );

    return (
        <Box sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h5">Elementos</Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpenDialog()}
                >
                    Agregar Elemento
                </Button>
            </Box>

            {isMobile ? renderMobileView() : renderDesktopView()}

            <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>
                    {selectedElemento ? 'Editar Elemento' : 'Nuevo Elemento'}
                </DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="Nombre"
                        fullWidth
                        value={formData.nombre}
                        onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                    />
                    <TextField
                        margin="dense"
                        label="Descripción"
                        fullWidth
                        multiline
                        rows={2}
                        value={formData.descripcion}
                        onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                    />
                    <TextField
                        margin="dense"
                        label="Cantidad"
                        type="number"
                        fullWidth
                        value={formData.cantidad}
                        onChange={(e) => setFormData({ ...formData, cantidad: parseInt(e.target.value) })}
                    />
                    <FormControl fullWidth margin="dense">
                        <InputLabel>Tipo</InputLabel>
                        <Select
                            value={formData.tipo}
                            label="Tipo"
                            onChange={(e) => setFormData({ ...formData, tipo: e.target.value as TipoElemento })}
                        >
                            {Object.values(TipoElemento).map((tipo) => (
                                <MenuItem key={tipo} value={tipo}>
                                    {tipo}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl fullWidth margin="dense">
                        <InputLabel>Estado</InputLabel>
                        <Select
                            value={formData.activo}
                            label="Estado"
                            onChange={(e) => setFormData({ ...formData, activo: e.target.value === 'true' })}
                        >
                            <MenuItem value="true">Activo</MenuItem>
                            <MenuItem value="false">Inactivo</MenuItem>
                        </Select>
                    </FormControl>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancelar</Button>
                    <Button onClick={handleSubmit} variant="contained">
                        {selectedElemento ? 'Guardar' : 'Crear'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default ElementosList; 