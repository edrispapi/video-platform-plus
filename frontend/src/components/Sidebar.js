import React from 'react';
import { Drawer, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import { Home, VideoLibrary, Dashboard as DashboardIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

function Sidebar() {
  const navigate = useNavigate();

  return (
    <Drawer variant="permanent" anchor="left">
      <List>
        <ListItem button onClick={() => navigate('/')}>
          <ListItemIcon><Home /></ListItemIcon>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button onClick={() => navigate('/video/1')}>
          <ListItemIcon><VideoLibrary /></ListItemIcon>
          <ListItemText primary="Videos" />
        </ListItem>
        <ListItem button onClick={() => navigate('/dashboard')}>
          <ListItemIcon><DashboardIcon /></ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
      </List>
    </Drawer>
  );
}

export default Sidebar;
