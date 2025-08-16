const express = require('express');
const { Subscription } = require('../models');
const router = express.Router();

// This is a placeholder for subscription endpoints

// List subscriptions for a user
router.get('/user/:userId', async (req, res) => {
  const { userId } = req.params;
  const subs = await Subscription.findAll({ where: { user_id: userId } });
  res.json(subs);
});

module.exports = router;
