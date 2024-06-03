import React, { useState } from 'react';
import axios from 'axios';
import { Box, Grid, TextField, Button, InputLabel, MenuItem, FormControl, Select, Typography } from '@mui/material';

const Ir = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResultsDisplay, setSearchResultsDisplay] = useState('');
  const [searchCategory, setSearchCategory] = useState('');




  const handleSearch = async () => {
    try {
      console.log("Sending search request...");
      let response;
      const headers = {};

      if (searchCategory === 'type1') {
        const dataToSend = { query: searchQuery, type: searchCategory };
        const config = {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        };
        response = await axios.post('http://localhost:5000/search', dataToSend,config );

      } else if (searchCategory === 'type2') {
        const formData =  {query: searchQuery, type: searchCategory };
        const config = {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
          },
        };
        response = await axios.post('http://localhost:5000/search2', formData,config);
      }

      if (response && response.data) {
        console.log("Response received:", response.data);
        if (searchCategory === 'type1') {
          setSearchResultsDisplay(JSON.stringify(response.data, null, 2));
        } else if (searchCategory === 'type2') {
          setSearchResultsDisplay(JSON.stringify(response.data, null, 2));
        }
      } else {
        console.log('Empty response received from server');
        setSearchResultsDisplay('No results found');
      }
    } catch (error) {
      console.error('Error searching:', error);
      setSearchResultsDisplay('Error searching. Please try again.');
    }
  };

  // const handleSearch = async () => {
  //   try {
  //     console.log("Sending search request...");
  //     let response;
  //     let dataToSend;
  //     const headers = {};
  
  //     if (searchCategory === 'type1') {
  //       // إذا كان النوع JSON
  //       dataToSend = { query: searchQuery, type: searchCategory };
  //       headers['Content-Type'] = 'application/json';
  //     } else {
  //       // إذا كان النوع غير JSON
  //       dataToSend = new FormData();
  //       dataToSend.append('query', searchQuery);
  //       dataToSend.append('type', searchCategory);
  //     }
  
  //     response = await axios.post('http://localhost:5000/search', dataToSend, { headers });
    
  //     // التحقق من وجود بيانات في الاستجابة
  //     if (response.data) {
  //       // تنسيق وطباعة الريسبونس
  //       console.log("Response received:", JSON.stringify(response.data, null, 2));
  //       // تعيين البيانات إلى الحالة إذا كانت موجودة
  //       setSearchResultsDisplay(response.data);
  //       // عرض نتائج البحث على الشاشة
  //       setSearchResultsDisplay(JSON.stringify(response.data, null, 2));
  //     } else {
  //       console.log('Empty response received from server');
  //       setSearchResultsDisplay('No results found');
  //     }
  //   } catch (error) {
  //     console.error('Error searching:', error);
  //     setSearchResultsDisplay('Error searching. Please try again.');
  //   }
  // };
  

  const handleCategoryChange = (event) => {
    setSearchCategory(event.target.value);
  };

  return (
    <Box
      sx={{
        flexGrow: 1,
        padding: 2,
        backgroundColor: 'white',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        minWidth: '98vw',
      }}
    >
      <Grid item xs={12} md={6}>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
        >
          <TextField
            label="Search here"
            variant="outlined"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            fullWidth
            sx={{ marginBottom: 1, minWidth: '800px'}}
          />
          <FormControl fullWidth sx={{ marginBottom: 2 }}>
            <InputLabel id="search-category-label">Search Category</InputLabel>
            <Select
              labelId="search-category-label"
              id="search-category"
              value={searchCategory}
              label="Search Category"
              onChange={handleCategoryChange}
            >
              <MenuItem value={'type1'}>type1</MenuItem>
              <MenuItem value={'type2'}>type2</MenuItem>
            </Select>
          </FormControl>
          <Button variant="contained" color="primary" onClick={handleSearch}>
            Search
          </Button>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', color: 'blue' }}>
            {searchResultsDisplay}
          </Typography>
        </Box>
      </Grid>
    </Box>
  );
};

export default Ir;
