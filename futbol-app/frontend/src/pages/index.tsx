import React, { useState } from 'react';
import { 
    Container, 
    Typography, 
    Box, 
    Tabs, 
    Tab, 
    Paper,
    AppBar,
    Toolbar,
    useTheme,
    alpha,
    useMediaQuery
} from '@mui/material';
import Image from 'next/image';
import { useQuery } from 'react-query';
import { getJugadores, getResumenEstadisticas } from '../services/api';
import JugadoresList from '../components/JugadoresList';
import PartidosList from '../components/PartidosList';
import EstadisticasList from '../components/EstadisticasList';
import { Jugador, EstadisticasJugador } from '../types';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}

export default function Home() {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [tabValue, setTabValue] = useState(0);
    const [sortField, setSortField] = useState('goles');
    const [sortDesc, setSortDesc] = useState(true);

    const { data: estadisticas = [] } = useQuery<EstadisticasJugador[]>('estadisticas', () => getResumenEstadisticas(sortField, sortDesc));
    const { data: jugadores = [] } = useQuery<Jugador[]>('jugadores', getJugadores);

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
    };

    const handleSort = (field: string) => {
        if (field === sortField) {
            setSortDesc(!sortDesc);
        } else {
            setSortField(field);
            setSortDesc(true);
        }
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" sx={{ 
                background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                boxShadow: theme.shadows[3]
            }}>
                <Toolbar sx={{ justifyContent: 'center' }}>
                    <Box sx={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: 3,
                        py: 1
                    }}>
                        <Image
                            src="/images/logo.png"
                            alt="Logo Fútbol App"
                            width={60}
                            height={60}
                            style={{ borderRadius: '50%' }}
                        />
                        <Typography 
                            variant="h4" 
                            component="div" 
                            sx={{ 
                                color: 'white',
                                fontWeight: 600,
                                letterSpacing: '0.5px'
                            }}
                        >
                            Fútbol App
                        </Typography>
                    </Box>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4 }}>
                <Paper sx={{ width: '100%', mb: 2 }}>
                    <Tabs
                        value={tabValue}
                        onChange={handleTabChange}
                        variant={isMobile ? "fullWidth" : "standard"}
                        sx={{
                            borderBottom: 1,
                            borderColor: 'divider',
                            '& .MuiTab-root': {
                                color: theme.palette.text.secondary,
                                '&.Mui-selected': {
                                    color: theme.palette.primary.main,
                                },
                            },
                        }}
                    >
                        <Tab label="Jugadores" />
                        <Tab label="Partidos" />
                        <Tab label="Estadísticas" />
                    </Tabs>

                    <TabPanel value={tabValue} index={0}>
                        <JugadoresList jugadores={jugadores} />
                    </TabPanel>

                    <TabPanel value={tabValue} index={1}>
                        <PartidosList />
                    </TabPanel>

                    <TabPanel value={tabValue} index={2}>
                        <EstadisticasList
                            estadisticas={estadisticas}
                            onSort={handleSort}
                            sortField={sortField}
                            sortDesc={sortDesc}
                        />
                    </TabPanel>
                </Paper>
            </Container>
        </Box>
    );
} 