import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper } from '@mui/material';
import axios from 'axios';

function Dashboard() {
  const [heatmap, setHeatmap] = useState({});

  useEffect(() => {
    axios.get('http://localhost/api/heatmap/1') // فرض API برای هیت‌مپ
      .then(response => setHeatmap(response.data))
      .catch(error => console.error('Error fetching heatmap:', error));
  }, []);

  return (
    <Box padding={2}>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Paper elevation={3} style={{ padding: '20px' }}>
        <Typography variant="h6">Heatmap Data</Typography>
        <pre>{JSON.stringify(heatmap, null, 2)}</pre>
        {/* بعداً Chart.js برای نمودار اضافه می‌شه */}
      </Paper>
    </Box>
  );
}

export default Dashboard;
