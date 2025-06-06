import { useState } from 'react';
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
    Stack
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon, Person as PersonIcon } from '@mui/icons-material';
import { useMutation, useQueryClient } from 'react-query';
import { Jugador } from '../types';
import { createJugador, updateJugador, deleteJugador } from '../services/api';

interface JugadoresListProps {
    jugadores: Jugador[];
}

export default function JugadoresList({ jugadores = [] }: JugadoresListProps) {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [open, setOpen] = useState(false);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [jugadorToDelete, setJugadorToDelete] = useState<Jugador | null>(null);
    const [editJugador, setEditJugador] = useState<Jugador | null>(null);
    const [nombre, setNombre] = useState('');
    const queryClient = useQueryClient();

    const createMutation = useMutation(createJugador, {
        onSuccess: () => {
            queryClient.invalidateQueries('jugadores');
            handleClose();
        }
    });

    const updateMutation = useMutation(
        (data: { id: number; jugador: Omit<Jugador, 'id'> }) =>
            updateJugador(data.id, data.jugador),
        {
            onSuccess: () => {
                queryClient.invalidateQueries('jugadores');
                handleClose();
            }
        }
    );

    const deleteMutation = useMutation(deleteJugador, {
        onSuccess: () => {
            queryClient.invalidateQueries('jugadores');
        }
    });

    const handleOpen = (jugador?: Jugador) => {
        if (jugador) {
            setEditJugador(jugador);
            setNombre(jugador.nombre);
        } else {
            setEditJugador(null);
            setNombre('');
        }
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        setEditJugador(null);
        setNombre('');
    };

    const handleSubmit = () => {
        if (editJugador) {
            updateMutation.mutate({
                id: editJugador.id,
                jugador: { 
                    nombre,
                    apellido: editJugador.apellido,
                    fecha_nacimiento: editJugador.fecha_nacimiento,
                    posicion: editJugador.posicion,
                    numero: editJugador.numero,
                    activo: true
                }
            });
        } else {
            createMutation.mutate({ 
                nombre,
                apellido: '',
                fecha_nacimiento: new Date().toISOString().split('T')[0],
                posicion: '',
                numero: 0,
                activo: true
            });
        }
    };

    const handleDeleteClick = (jugador: Jugador) => {
        setJugadorToDelete(jugador);
        setDeleteDialogOpen(true);
    };

    const handleDeleteConfirm = () => {
        if (jugadorToDelete) {
            deleteMutation.mutate(jugadorToDelete.id);
            setDeleteDialogOpen(false);
            setJugadorToDelete(null);
        }
    };

    const handleDeleteCancel = () => {
        setDeleteDialogOpen(false);
        setJugadorToDelete(null);
    };

    const renderMobileView = () => (
        <Stack spacing={2}>
            {jugadores.map((jugador) => (
                <Card 
                    key={jugador.id}
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
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                            <Avatar 
                                sx={{ 
                                    bgcolor: alpha(theme.palette.primary.main, 0.1),
                                    color: theme.palette.primary.main
                                }}
                            >
                                <PersonIcon />
                            </Avatar>
                            <Box sx={{ flexGrow: 1 }}>
                                <Typography sx={{ fontWeight: 500 }}>
                                    {jugador.nombre}
                                </Typography>
                                <Box
                                    sx={{
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        px: 2,
                                        py: 0.5,
                                        borderRadius: 1,
                                        bgcolor: jugador.activo 
                                            ? alpha(theme.palette.success.main, 0.1)
                                            : alpha(theme.palette.error.main, 0.1),
                                        color: jugador.activo 
                                            ? theme.palette.success.main
                                            : theme.palette.error.main,
                                        fontSize: '0.875rem',
                                        fontWeight: 500,
                                        mt: 1
                                    }}
                                >
                                    {jugador.activo ? 'Activo' : 'Inactivo'}
                                </Box>
                            </Box>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                                <IconButton 
                                    onClick={() => handleOpen(jugador)}
                                    sx={{ 
                                        color: theme.palette.primary.main,
                                        '&:hover': { 
                                            bgcolor: alpha(theme.palette.primary.main, 0.1) 
                                        }
                                    }}
                                >
                                    <EditIcon />
                                </IconButton>
                                <IconButton 
                                    onClick={() => handleDeleteClick(jugador)}
                                    sx={{ 
                                        color: theme.palette.error.main,
                                        '&:hover': { 
                                            bgcolor: alpha(theme.palette.error.main, 0.1) 
                                        }
                                    }}
                                >
                                    <DeleteIcon />
                                </IconButton>
                            </Box>
                        </Box>
                    </CardContent>
                </Card>
            ))}
        </Stack>
    );

    const renderDesktopView = () => (
        <TableContainer 
            component={Paper} 
            sx={{ 
                borderRadius: 2,
                overflow: 'hidden',
                boxShadow: theme.shadows[2],
                maxWidth: '100%',
                overflowX: 'auto'
            }}
        >
            <Table>
                <TableHead>
                    <TableRow sx={{ bgcolor: alpha(theme.palette.primary.main, 0.05) }}>
                        <TableCell sx={{ fontWeight: 600, minWidth: 200 }}>Jugador</TableCell>
                        <TableCell sx={{ fontWeight: 600, minWidth: 120 }}>Estado</TableCell>
                        <TableCell sx={{ fontWeight: 600, minWidth: 100 }}>Acciones</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {jugadores.map((jugador) => (
                        <TableRow 
                            key={jugador.id}
                            sx={{ 
                                '&:hover': { 
                                    bgcolor: alpha(theme.palette.primary.main, 0.02) 
                                } 
                            }}
                        >
                            <TableCell>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                    <Avatar 
                                        sx={{ 
                                            bgcolor: alpha(theme.palette.primary.main, 0.1),
                                            color: theme.palette.primary.main
                                        }}
                                    >
                                        <PersonIcon />
                                    </Avatar>
                                    <Typography>{jugador.nombre}</Typography>
                                </Box>
                            </TableCell>
                            <TableCell>
                                <Box
                                    sx={{
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        px: 2,
                                        py: 0.5,
                                        borderRadius: 1,
                                        bgcolor: jugador.activo 
                                            ? alpha(theme.palette.success.main, 0.1)
                                            : alpha(theme.palette.error.main, 0.1),
                                        color: jugador.activo 
                                            ? theme.palette.success.main
                                            : theme.palette.error.main,
                                        fontSize: '0.875rem',
                                        fontWeight: 500
                                    }}
                                >
                                    {jugador.activo ? 'Activo' : 'Inactivo'}
                                </Box>
                            </TableCell>
                            <TableCell>
                                <IconButton 
                                    onClick={() => handleOpen(jugador)}
                                    sx={{ 
                                        color: theme.palette.primary.main,
                                        '&:hover': { 
                                            bgcolor: alpha(theme.palette.primary.main, 0.1) 
                                        }
                                    }}
                                >
                                    <EditIcon />
                                </IconButton>
                                <IconButton 
                                    onClick={() => handleDeleteClick(jugador)}
                                    sx={{ 
                                        color: theme.palette.error.main,
                                        '&:hover': { 
                                            bgcolor: alpha(theme.palette.error.main, 0.1) 
                                        }
                                    }}
                                >
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
        <>
            <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                mb: 3,
                flexDirection: { xs: 'column', sm: 'row' },
                gap: { xs: 2, sm: 0 }
            }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Lista de Jugadores
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpen()}
                    sx={{
                        background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                        color: 'white',
                        '&:hover': {
                            background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`
                        }
                    }}
                >
                    Agregar Jugador
                </Button>
            </Box>

            {isMobile ? renderMobileView() : renderDesktopView()}

            <Dialog 
                open={open} 
                onClose={handleClose}
                PaperProps={{
                    sx: {
                        borderRadius: 2,
                        minWidth: { xs: '90%', sm: 400 },
                        maxWidth: '90%'
                    }
                }}
            >
                <DialogTitle sx={{ pb: 1 }}>
                    {editJugador ? 'Editar Jugador' : 'Nuevo Jugador'}
                </DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="Nombre"
                        type="text"
                        fullWidth
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        sx={{ mt: 2 }}
                    />
                </DialogContent>
                <DialogActions sx={{ px: 3, pb: 3 }}>
                    <Button 
                        onClick={handleClose}
                        sx={{ 
                            color: theme.palette.text.secondary,
                            '&:hover': { 
                                bgcolor: alpha(theme.palette.text.secondary, 0.1) 
                            }
                        }}
                    >
                        Cancelar
                    </Button>
                    <Button 
                        onClick={handleSubmit} 
                        variant="contained"
                        sx={{
                            background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                            color: 'white',
                            '&:hover': {
                                background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.secondary.dark})`
                            }
                        }}
                    >
                        {editJugador ? 'Guardar' : 'Crear'}
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog 
                open={deleteDialogOpen} 
                onClose={handleDeleteCancel}
                PaperProps={{
                    sx: {
                        borderRadius: 2,
                        minWidth: { xs: '90%', sm: 400 },
                        maxWidth: '90%'
                    }
                }}
            >
                <DialogTitle sx={{ pb: 1 }}>
                    Confirmar eliminación
                </DialogTitle>
                <DialogContent>
                    <Typography>
                        ¿Estás seguro que deseas eliminar al jugador {jugadorToDelete?.nombre}? Esta acción no se puede deshacer.
                    </Typography>
                </DialogContent>
                <DialogActions sx={{ px: 3, pb: 3 }}>
                    <Button 
                        onClick={handleDeleteCancel}
                        sx={{ 
                            color: theme.palette.text.secondary,
                            '&:hover': { 
                                bgcolor: alpha(theme.palette.text.secondary, 0.1) 
                            }
                        }}
                    >
                        Cancelar
                    </Button>
                    <Button 
                        onClick={handleDeleteConfirm} 
                        variant="contained"
                        color="error"
                        sx={{
                            textTransform: 'none',
                            px: 3
                        }}
                    >
                        Eliminar
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
} 