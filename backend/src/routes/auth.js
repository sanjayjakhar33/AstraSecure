const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { User } = require('../models');
const router = express.Router();

router.post('/register', async (req, res) => {
  const { email, password } = req.body;
  const password_hash = bcrypt.hashSync(password, 10);
  try {
    const user = await User.create({ email, password_hash });
    res.json({ success: true, userId: user.id });
  } catch (err) {
    res.status(400).json({ success: false, message: 'Registration failed', error: err.message });
  }
});

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ where: { email } });
  if (!user || !user.validPassword(password)) {
    return res.status(401).json({ success: false, message: 'Invalid credentials' });
  }
  const token = jwt.sign({ id: user.id, email: user.email }, process.env.JWT_SECRET);
  res.json({ success: true, token });
});

module.exports = router;
