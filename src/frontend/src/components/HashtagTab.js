import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  ListItemText,
  Paper,
} from "@mui/material";
import axios from "axios";

export default function HashtagTab() {
  const [text, setText] = useState("");
  const [hashtag, setHashtag] = useState("");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get("/api/history").then((res) => setHistory(res.data.history));
  }, [hashtag]);

  const handleGenerate = async () => {
    const res = await axios.post("/api/hashtag", { text });
    setHashtag(res.data.hashtag);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Hashtag Generator
      </Typography>
      <TextField
        label="Enter your text"
        multiline
        minRows={2}
        fullWidth
        value={text}
        onChange={(e) => setText(e.target.value)}
        sx={{ mb: 2 }}
      />
      <Button variant="contained" onClick={handleGenerate} sx={{ mb: 2 }}>
        Generate
      </Button>
      {hashtag && (
        <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6">Generated Hashtag:</Typography>
          <Typography variant="body1" sx={{ fontWeight: "bold", fontSize: 20 }}>
            {hashtag}
          </Typography>
        </Paper>
      )}
      <Typography variant="subtitle1">History</Typography>
      <List>
        {history.map((h, i) => (
          <ListItem key={i}>
            <ListItemText primary={h} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
