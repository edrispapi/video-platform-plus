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
  const [replyTo, setReplyTo] = useState(null);
  const [token, setToken] = useState('');
  const videoId = match.params.id;

  useEffect(() => {
    axios.get(`http://localhost/api/videos/${videoId}/get_token/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => setToken(response.data.token))
      .catch(error => console.error('Error fetching token:', error));

    axios.get(`http://localhost/api/videos/${videoId}/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        setComments(response.data.comments || []);
        setLikes(response.data.likes_count || 0);
      })
      .catch(error => console.error('Error fetching video:', error));
  }, [videoId]);

  const handleCommentSubmit = () => {
    const data = { text: newComment };
    if (replyTo) data.parent_id = replyTo;
    axios.post(`http://localhost/api/videos/${videoId}/add_comment/`, data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(response => {
        setComments([...comments, response.data]);
        setNewComment('');
        setReplyTo(null);
      })
      .catch(error => console.error('Error adding comment:', error));
  };

  const handleLike = () => {
    axios.post(`http://localhost/api/videos/${videoId}/like_video/`, {}, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
      .then(() => setLikes(likes + 1));
  };

  const handleReply = (commentId) => {
    setReplyTo(commentId);
    setNewComment(`@${comments.find(c => c.id === commentId)?.user}: `);
  };

  return (
    <Box padding={2}>
      <Typography variant="h4" gutterBottom>Video Player</Typography>
      <ReactPlayer
        ref={playerRef}
        url={`https://yourdomain.com/hls/video_${videoId}.m3u8`}
        playing
        controls
        width="100%"
        height="auto"
        config={{
          file: {
            hlsOptions: { xhrSetup: (xhr) => xhr.setRequestHeader('X-Token', token) }
          }
        }}
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
          style={{ marginLeft: 10, width: '60%' }}
        />
        <Button variant="contained" onClick={handleCommentSubmit} style={{ marginLeft: 10 }}>
          Submit
        </Button>
      </Box>
      <List>
        {comments.map((comment) => (
          <ListItem key={comment.id}>
            <Typography>
              {comment.user}: {comment.text}
              <IconButton size="small" onClick={() => handleReply(comment.id)}>
                <Chat fontSize="small" />
              </IconButton>
            </Typography>
            {comment.replies && comment.replies.map(reply => (
              <ListItem key={reply.id} style={{ marginLeft: 20 }}>
                <Typography>{reply.user}: {reply.text}</Typography>
              </ListItem>
            ))}
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default VideoPlayer;
