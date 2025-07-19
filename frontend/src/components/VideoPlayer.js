import React, { useEffect, useRef } from 'react';
import ReactPlayer from 'react-player';
import { Box, Typography } from '@mui/material';

function VideoPlayer({ match }) {
  const playerRef = useRef(null);

  return (
    <Box padding={2}>
      <Typography variant="h4" gutterBottom>Video Player</Typography>
      <ReactPlayer
        ref={playerRef}
        url={`http://localhost/hls/video_${match.params.id}.m3u8`}
        playing
        controls
        width="100%"
        height="auto"
      />
    </Box>
  );
}

export default VideoPlayer;
