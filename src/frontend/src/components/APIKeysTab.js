import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Paper,
  Button,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
} from "@mui/material";
import axios from "axios";

// Store API keys in localStorage for privacy (not sent to backend)
const LOCAL_KEY = "llm_api_keys";

export default function APIKeysTab() {
  const [providers, setProviders] = useState([]);
  const [selected, setSelected] = useState("");
  const [apiKeys, setApiKeys] = useState({});
  const [input, setInput] = useState("");

  useEffect(() => {
    axios.get("/api/providers").then((res) => {
      setProviders(res.data.providers);
      if (res.data.providers.length > 0) setSelected(res.data.providers[0].id);
    });
    const stored = localStorage.getItem(LOCAL_KEY);
    if (stored) setApiKeys(JSON.parse(stored));
  }, []);

  useEffect(() => {
    setInput(apiKeys[selected] || "");
  }, [selected, apiKeys]);

  const handleSave = () => {
    const newKeys = { ...apiKeys, [selected]: input };
    setApiKeys(newKeys);
    localStorage.setItem(LOCAL_KEY, JSON.stringify(newKeys));
  };

  const selectedProvider = providers.find((p) => p.id === selected);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        API Key Management
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Provider</InputLabel>
          <Select
            value={selected}
            label="Provider"
            onChange={(e) => setSelected(e.target.value)}
          >
            {providers.map((p) => (
              <MenuItem key={p.id} value={p.id}>
                {p.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {selectedProvider && selectedProvider.api_key_label ? (
          <TextField
            label={selectedProvider.api_key_label}
            fullWidth
            type="password"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            sx={{ mb: 2 }}
            helperText={`This key will be used for ${selectedProvider.name} in the AI tab.`}
          />
        ) : (
          <Typography color="text.secondary">
            This provider does not require an API key.
          </Typography>
        )}
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={!selectedProvider || !selectedProvider.api_key_label}
        >
          Save API Key
        </Button>
      </Paper>
      <Typography variant="body2" color="text.secondary">
        API keys are linked to each provider and are used automatically in the
        AI tab. Keys are stored only in your browser (localStorage) for privacy
        and are never sent to the backend.
      </Typography>
    </Box>
  );
}
