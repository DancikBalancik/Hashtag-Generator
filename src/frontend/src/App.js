import React, { useState } from "react";
import { AppBar, Tabs, Tab, Box, Typography, Container } from "@mui/material";
import HashtagTab from "./components/HashtagTab";
import AITab from "./components/AITab";
import SettingsTab from "./components/SettingsTab";
import APIKeysTab from "./components/APIKeysTab";

function App() {
  const [tab, setTab] = useState(0);
  const handleTabChange = (event, newValue) => setTab(newValue);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <AppBar position="static" color="default" sx={{ borderRadius: 2, mb: 2 }}>
        <Tabs value={tab} onChange={handleTabChange} variant="fullWidth">
          <Tab label="Hashtag Generator" />
          <Tab label="AI Hashtag" />
          <Tab label="API Keys" />
          <Tab label="Settings / About" />
        </Tabs>
      </AppBar>
      <Box hidden={tab !== 0}>
        <HashtagTab />
      </Box>
      <Box hidden={tab !== 1}>
        <AITab />
      </Box>
      <Box hidden={tab !== 2}>
        <APIKeysTab />
      </Box>
      <Box hidden={tab !== 3}>
        <SettingsTab />
      </Box>
      <Box sx={{ mt: 4, textAlign: "center", color: "gray" }}>
        <Typography variant="caption">Hashtag Generator &copy; 2025</Typography>
      </Box>
    </Container>
  );
}

export default App;
