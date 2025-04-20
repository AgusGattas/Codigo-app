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
    const [sortField, setSortField] = useState<string>('goles');
    const [sortDesc, setSortDesc] = useState<boolean>(true);

    const { data: jugadores = [] } = useQuery('jugadores', getJugadores);
    const { data: estadisticas = [] } = useQuery(
        ['estadisticas', sortField, sortDesc],
        () => getResumenEstadisticas(sortField, sortDesc)
    );

    const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
    };

    const handleSort = (campo: string) => {
        if (campo === sortField) {
            setSortDesc(!sortDesc);
        } else {
            setSortField(campo);
            setSortDesc(true);
        }
    };

    return (
        <Box sx={{ 
            flexGrow: 1, 
            minHeight: '100vh', 
            bgcolor: 'background.default',
            background: `
                linear-gradient(135deg, 
                    ${alpha(theme.palette.primary.main, 0.05)} 0%, 
                    ${alpha(theme.palette.background.default, 0.8)} 30%,
                    ${alpha(theme.palette.background.default, 0.95)} 50%,
                    ${alpha(theme.palette.background.default, 0.8)} 70%,
                    ${alpha(theme.palette.secondary.main, 0.05)} 100%
                )
            `,
            position: 'relative',
            '&::before': {
                content: '""',
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                opacity: 0.4,
                zIndex: -1,
                background: `
                    radial-gradient(circle at 0% 0%, ${alpha(theme.palette.primary.main, 0.1)} 0%, transparent 50%),
                    radial-gradient(circle at 100% 0%, ${alpha(theme.palette.secondary.main, 0.1)} 0%, transparent 50%),
                    radial-gradient(circle at 50% 100%, ${alpha(theme.palette.primary.main, 0.1)} 0%, transparent 50%)
                `
            }
        }}>
            <AppBar 
                position="static" 
                elevation={0}
                sx={{
                    background: `linear-gradient(90deg, ${alpha(theme.palette.primary.main, 0.95)} 0%, ${alpha(theme.palette.secondary.main, 0.95)} 100%)`,
                    backdropFilter: 'blur(8px)',
                    borderBottom: `1px solid ${alpha(theme.palette.common.white, 0.1)}`
                }}
            >
                <Toolbar sx={{ py: { xs: 1, md: 2 } }}>
                    <Box 
                        sx={{ 
                            position: 'relative', 
                            width: { xs: 50, sm: 60 }, 
                            height: { xs: 50, sm: 60 }, 
                            mr: 2,
                            filter: 'drop-shadow(0px 2px 4px rgba(0,0,0,0.2))',
                            transition: 'transform 0.2s ease-in-out',
                            '&:hover': {
                                transform: 'scale(1.05)'
                            }
                        }}
                    >
                        <Image
                            src="/images/logo.png"
                            alt="Logo del equipo"
                            fill
                            sizes="(max-width: 600px) 50px, 60px"
                            style={{ 
                                objectFit: 'contain',
                                filter: 'brightness(1.1)'
                            }}
                            priority
                        />
                    </Box>
                    <Box sx={{ flexGrow: 1 }}>
                        <Typography 
                            variant="h5" 
                            component="div" 
                            sx={{ 
                                fontWeight: 700,
                                fontSize: { xs: '1.25rem', sm: '1.5rem' },
                                background: `linear-gradient(90deg, ${theme.palette.common.white} 0%, ${alpha(theme.palette.common.white, 0.9)} 100%)`,
                                backgroundClip: 'text',
                                WebkitBackgroundClip: 'text',
                                color: 'transparent',
                                letterSpacing: '0.5px',
                                textShadow: '0px 2px 4px rgba(0,0,0,0.1)'
                            }}
                        >
                            Codigo App
                        </Typography>
                        <Typography 
                            variant="subtitle2" 
                            sx={{ 
                                color: alpha(theme.palette.common.white, 0.7),
                                fontSize: { xs: '0.75rem', sm: '0.875rem' },
                                mt: 0.5,
                                display: { xs: 'none', sm: 'block' }
                            }}
                        >
                            Gestión de Equipo
                        </Typography>
                    </Box>
                </Toolbar>
            </AppBar>

            <Container 
                maxWidth="lg" 
                sx={{ 
                    px: { xs: 2, sm: 3, md: 4 },
                    py: { xs: 3, sm: 4, md: 5 }
                }}
            >
                <Box sx={{ 
                    position: 'relative',
                    '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: -20,
                        left: -20,
                        right: -20,
                        bottom: -20,
                        background: `linear-gradient(135deg, 
                            ${alpha(theme.palette.background.paper, 0.8)} 0%,
                            ${alpha(theme.palette.background.paper, 0.95)} 100%
                        )`,
                        borderRadius: 4,
                        boxShadow: `0 0 40px ${alpha(theme.palette.common.black, 0.1)}`,
                        backdropFilter: 'blur(12px)',
                        zIndex: -1
                    }
                }}>
                    <Typography 
                        variant="h4" 
                        component="h1" 
                        gutterBottom 
                        sx={{ 
                            fontWeight: 700,
                            background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                            backgroundClip: 'text',
                            WebkitBackgroundClip: 'text',
                            color: 'transparent',
                            mb: { xs: 2, sm: 3, md: 4 },
                            textAlign: { xs: 'center', sm: 'left' },
                            textShadow: `0 2px 4px ${alpha(theme.palette.common.black, 0.1)}`
                        }}
                    >
                        Panel 2025
                    </Typography>
                    
                    <Paper 
                        sx={{ 
                            width: '100%', 
                            mb: 2,
                            borderRadius: 2,
                            overflow: 'hidden',
                            boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.1)}`,
                            background: alpha(theme.palette.background.paper, 0.8),
                            backdropFilter: 'blur(8px)',
                            border: `1px solid ${alpha(theme.palette.common.white, 0.1)}`
                        }}
                    >
                        <Tabs
                            value={tabValue}
                            onChange={handleTabChange}
                            aria-label="basic tabs example"
                            variant={isMobile ? "fullWidth" : "standard"}
                            sx={{
                                borderBottom: `1px solid ${theme.palette.divider}`,
                                '& .MuiTab-root': {
                                    fontWeight: 600,
                                    textTransform: 'none',
                                    fontSize: { xs: '0.875rem', sm: '1rem' },
                                    minHeight: { xs: 40, sm: 48 },
                                    px: { xs: 1, sm: 3 }
                                }
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
                </Box>
            </Container>
        </Box>
    );
} 