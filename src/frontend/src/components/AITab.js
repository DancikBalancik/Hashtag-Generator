import React, { useState, useEffect, useRef } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  CircularProgress,
  Paper,
  Stack,
  InputAdornment,
} from "@mui/material";
import axios from "axios";

const PROMPT_PREFIX = "Suggest a hashtag for the word: ";

const getApiKey = (provider) => {
  try {
    const keys = JSON.parse(localStorage.getItem("llm_api_keys") || "{}");
    return keys[provider] || "";
  } catch {
    return "";
  }
};

export default function AITab() {
  const [providers, setProviders] = useState([]);
  const [provider, setProvider] = useState("");
  const [models, setModels] = useState([]);
  const [model, setModel] = useState("");
  const [userPrompt, setUserPrompt] = useState("");
  const [endpoint, setEndpoint] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [modelsLoading, setModelsLoading] = useState(false);
  const promptInputRef = useRef();

  useEffect(() => {
    axios.get("/api/providers").then((res) => {
      setProviders(res.data.providers);
      if (res.data.providers.length > 0) {
        setProvider(res.data.providers[0].id);
      }
    });
  }, []);

  useEffect(() => {
    if (!provider) return;
    setModels([]);
    setModel("");
    setModelsLoading(true);
    const selectedProvider = providers.find((p) => p.id === provider);
    const key = getApiKey(provider); // Always get the latest key
    let params = { provider };
    if (key) params.api_key = key;
    if (selectedProvider && selectedProvider.extra_fields.includes("endpoint"))
      params.endpoint = endpoint;
    if (selectedProvider && selectedProvider.extra_fields.includes("base_url"))
      params.base_url = baseUrl;
    // Debug: log params
    // console.log('Fetching models with params:', params);
    axios
      .get("/api/models", { params })
      .then((res) => {
        setModels(res.data.models);
        setModel(res.data.models[0] || "");
      })
      .catch(() => setModels([]))
      .finally(() => setModelsLoading(false));
  }, [provider, endpoint, baseUrl, providers, userPrompt]);

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResult("");
    try {
      const key = getApiKey(provider);
      const payload = {
        provider,
        prompt: PROMPT_PREFIX + userPrompt,
        api_key: key,
        model,
      };
      if (endpoint) payload.endpoint = endpoint;
      if (baseUrl) payload.base_url = baseUrl;
      const res = await axios.post("/api/ai", payload);
      setResult(res.data.result);
    } catch (e) {
      setError(e.response?.data?.error || "Error contacting AI API");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResult("");
    setError("");
    setUserPrompt("");
    if (promptInputRef.current) promptInputRef.current.focus();
  };

  const selectedProvider = providers.find((p) => p.id === provider);

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        AI Hashtag Generator
      </Typography>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Provider</InputLabel>
        <Select
          value={provider}
          label="Provider"
          onChange={(e) => setProvider(e.target.value)}
        >
          {providers.map((p) => (
            <MenuItem key={p.id} value={p.id}>
              {p.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {selectedProvider &&
        selectedProvider.extra_fields.includes("endpoint") && (
          <TextField
            label="Endpoint"
            fullWidth
            value={endpoint}
            onChange={(e) => setEndpoint(e.target.value)}
            sx={{ mb: 2 }}
          />
        )}
      {selectedProvider &&
        selectedProvider.extra_fields.includes("base_url") && (
          <TextField
            label="Base URL"
            fullWidth
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            sx={{ mb: 2 }}
          />
        )}
      {modelsLoading ? (
        <Box sx={{ mb: 2 }}>
          <CircularProgress size={24} />
        </Box>
      ) : models.length > 0 ? (
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Model</InputLabel>
          <Select
            value={model}
            label="Model"
            onChange={(e) => setModel(e.target.value)}
          >
            {models.map((m) => (
              <MenuItem key={m} value={m}>
                {m}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      ) : (
        <Typography color="text.secondary" sx={{ mb: 2 }}>
          No models found for this provider/API key.
        </Typography>
      )}
      <TextField
        inputRef={promptInputRef}
        value={userPrompt}
        onChange={(e) => setUserPrompt(e.target.value)}
        placeholder="What should the hashtag be about?"
        variant="outlined"
        fullWidth
        sx={{ mb: 2 }}
        InputProps={{
          style: { background: "#fff" },
          "aria-label": "Prompt",
        }}
      />
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading || !model || !userPrompt}
        >
          {loading ? <CircularProgress size={24} /> : "Generate with AI"}
        </Button>
        <Button
          variant="outlined"
          onClick={handleClear}
          disabled={loading && !result && !error}
        >
          Clear
        </Button>
      </Stack>
      {result && (
        <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6">AI Result:</Typography>
          <Typography
            variant="body1"
            sx={{ fontWeight: "bold", fontSize: 20, whiteSpace: "pre-line" }}
          >
            {result
              .replace(/[`*_#>\-\[\]!\(\)]/g, "") // Remove markdown symbols
              .replace(/\n{2,}/g, "\n") // Collapse multiple newlines
              .replace(/^\s*\.|\s*\?|\s*\!|\s*\,|\s*\:/g, "") // Remove leading punctuation
              .replace(/\s+$/, "") // Remove trailing whitespace
              .trim()}
          </Typography>
        </Paper>
      )}
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
}
