require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { sequelize } = require('./src/models');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Routes
app.use('/api/auth', require('./src/routes/auth'));
app.use('/api/license', require('./src/routes/license'));
app.use('/api/subscription', require('./src/routes/subscription'));
app.use('/api/payment', require('./src/routes/payment'));

const PORT = process.env.PORT || 4000;

sequelize.sync().then(() => {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
});
