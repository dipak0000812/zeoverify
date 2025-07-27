require('dotenv').config();
const express = require('express');
const cors = require('cors');
const verifyRoute = require('./routes/verify');

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/verify', verifyRoute);

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Backend running on http://localhost:${PORT}`));
