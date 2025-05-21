import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Paper,
} from "@mui/material";
import axios from "axios";

export default function SettingsTab() {
  const [settings, setSettings] = useState({
    remove_special_chars: false,
    capitalization_mode: "first",
    history_max_items: 10,
    theme: "light",
    character_limit: 0,
  });
  const [status, setStatus] = useState("");

  useEffect(() => {
    axios.get("/api/settings").then((res) => setSettings(res.data));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings((s) => ({
      ...s,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSave = async () => {
    await axios.post("/api/settings", settings);
    setStatus("Settings saved!");
    setTimeout(() => setStatus(""), 2000);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Settings & About
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <FormControlLabel
          control={
            <Switch
              checked={settings.remove_special_chars}
              onChange={handleChange}
              name="remove_special_chars"
            />
          }
          label="Remove Special Characters"
        />
        <Box sx={{ mt: 2 }}>
          <Typography>Capitalization Mode</Typography>
          <Select
            name="capitalization_mode"
            value={settings.capitalization_mode}
            onChange={handleChange}
            sx={{ minWidth: 120 }}
          >
            <MenuItem value="first">First Letter</MenuItem>
            <MenuItem value="all_caps">ALL CAPS</MenuItem>
            <MenuItem value="lowercase">lowercase</MenuItem>
            <MenuItem value="none">None</MenuItem>
          </Select>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography>History Max Items</Typography>
          <TextField
            name="history_max_items"
            type="number"
            value={settings.history_max_items}
            onChange={handleChange}
            sx={{ width: 100 }}
          />
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography>Theme</Typography>
          <Select
            name="theme"
            value={settings.theme}
            onChange={handleChange}
            sx={{ minWidth: 120 }}
          >
            <MenuItem value="light">Light</MenuItem>
            <MenuItem value="dark">Dark</MenuItem>
          </Select>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography>Character Limit</Typography>
          <TextField
            name="character_limit"
            type="number"
            value={settings.character_limit}
            onChange={handleChange}
            sx={{ width: 100 }}
          />
        </Box>
        <Button variant="contained" sx={{ mt: 3 }} onClick={handleSave}>
          Save Settings
        </Button>
        {status && (
          <Typography color="success.main" sx={{ mt: 1 }}>
            {status}
          </Typography>
        )}
      </Paper>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">About</Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          Hashtag Generator (2025) — Modern web app with AI hashtag support.
          <br />
          Backend: Python Flask | Frontend: React + Material UI
          <br />
          <a
            href="https://github.com/DancikBalancik/Hashtag-Generator"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </Typography>
      </Paper>
    </Box>
  );
}
