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
    const [sortField, setSortField] = useState('goles');
    const [sortDesc, setSortDesc] = useState(true);

    const { data: estadisticas = [] } = useQuery('estadisticas', getResumenEstadisticas);

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
            <AppBar position="static" sx={{ backgroundColor: theme.palette.primary.main }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Fútbol App
                    </Typography>
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
                        <JugadoresList />
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