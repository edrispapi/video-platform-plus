import React, { useEffect, useRef, useState } from 'react';
import ReactPlayer from 'react-player';
import { Box, Typography, TextField, Button, List, ListItem, IconButton } from '@mui/material';
import { ThumbUp, Chat } from '@mui/icons-material';
import axios from 'axios';

function VideoPlayer({ match }) {
  const playerRef = useRef(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [likes, setLikes] = useState(0);
  const videoId = match.params.id;

  useEffect(() => {
    axios.get(`http://localhost/api/videos/${videoId}/comments/`)
      .then(response => setComments(response.data));
    axios.get(`http://localhost/api/videos/${videoId}/likes/`)
      .then(response => setLikes(response.data.count));
  }, [videoId]);

  const handleCommentSubmit = () => {
    axios.post(`http://localhost/api/videos/${videoId}/add_comment/`, { comment: newComment })
      .then(() => {
        setComments([...comments, { text: newComment, user: 'You' }]);
        setNewComment('');
      });
  };

  const handleLike = () => {
    axios.post(`http://localhost/api/videos/${videoId}/like_video/`)
      .then(() => setLikes(likes + 1));
  };

  return (
    <Box padding={2}>
      <Typography variant="h4" gutterBottom>Video Player</Typography>
      <ReactPlayer
        ref={playerRef}
        url={`http://localhost/hls/video_${videoId}.m3u8`}
        playing
        controls
        width="100%"
        height="auto"
      />
      <Box mt={2}>
        <IconButton color="primary" onClick={handleLike}>
          <ThumbUp /> {likes}
        </IconButton>
        <TextField
          label="Add Comment"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          variant="outlined"
          size="small"
          style={{ marginLeft: 10 }}
        />
        <Button variant="contained" onClick={handleCommentSubmit} style={{ marginLeft: 10 }}>
          Submit
        </Button>
      </Box>
      <List>
        {comments.map((comment, index) => (
          <ListItem key={index}>
            <Typography>{comment.user}: {comment.text}</Typography>
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default VideoPlayer;
