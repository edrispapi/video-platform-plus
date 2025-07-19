import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Grid, Card, CardMedia, CardContent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function VideoList() {
  const [videos, setVideos] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('http://localhost/api/videos/?q=')
      .then(response => setVideos(response.data))
      .catch(error => console.error('Error fetching videos:', error));
  }, []);

  return (
    <Grid container spacing={3} padding={2}>
      {videos.map(video => (
        <Grid item xs={12} sm={6} md={4} key={video.id}>
          <Card onClick={() => navigate(`/video/${video.id}`)} style={{ cursor: 'pointer' }}>
            <CardMedia
              component="img"
              height="140"
              image={`https://via.placeholder.com/300x140?text=${video.title}`}
              alt={video.title}
            />
            <CardContent>
              <Typography variant="h6">{video.title}</Typography>
              <Typography variant="body2" color="text.secondary">
                {video.description || 'No description'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

export default VideoList;
