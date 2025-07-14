// components/TripSearchForm.jsx
import { useState, useEffect } from "react";

import {
  Button, Grid, TextField, Paper, MenuItem, FormControl, InputLabel, Select
} from "@mui/material";

import axios from '../api/axios';

export default function TripSearchForm({ onSearch }) {
  const [form, setForm] = useState({ from_: "", to: "", date: "" });
  const [locations, setLocations] = useState([]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("form for chosen from, to and date", form)
    onSearch(form);
  };

  useEffect(()=>{
    const fetchLocations = async () => {
      try {
        const res = await axios.get("/locations/");
        setLocations(res.data);
      } catch (e) {
        alert("Failed to load locations.");
      }
  };
  fetchLocations();
  }, [])

  
return (
    <Paper sx={{ p: 3, mb: 4 }}>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth select name="from_" defaultValue='From (Location)' label="From (Location)" onChange={handleChange}>
              <MenuItem value="From (Location)" disabled>From (Location)</MenuItem>
                {locations.map((loc) => (
                  <MenuItem key={loc.id} value={loc.state}>
                    {loc.local_government} ({loc.state})
                  </MenuItem>
                ))}
              </TextField>
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth name="to" select defaultValue='To (Location)' label="To (Location)" onChange={handleChange}>
              <MenuItem value="To (Location)" disabled>To (Location)</MenuItem>
                {locations.map((loc) => (
                  <MenuItem key={loc.id} value={loc.state}>
                    {loc.local_government} ({loc.state})
                  </MenuItem>
                ))}
              </TextField>
          </Grid>
          <Grid item xs={12} sm={4}>
            <TextField fullWidth name="date" type="date" onChange={handleChange} InputLabelProps={{ shrink: true }} />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" type="submit">
              Search Trips
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );}
