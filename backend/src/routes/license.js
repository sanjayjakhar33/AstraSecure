const express = require('express');
const { License, User, Device } = require('../models');
const router = express.Router();
const { Op } = require('sequelize');

// Validate license
router.post('/validate', async (req, res) => {
  const { licenseKey, deviceFingerprint } = req.body;
  const license = await License.findOne({
    where: { key: licenseKey, valid: true, expires_at: { [Op.gt]: new Date() } }
  });
  if (!license) return res.status(400).json({ valid: false, message: 'Invalid or expired license' });

  const device = await Device.findOne({ where: { id: license.device_id, fingerprint: deviceFingerprint } });
  if (!device) return res.status(403).json({ valid: false, message: 'Unregistered device' });

  return res.json({ valid: true, plan: license.plan, expires_at: license.expires_at });
});

// Activate license for a device
router.post('/activate', async (req, res) => {
  const { userId, deviceFingerprint, plan, paymentProvider, paymentId } = req.body;
  try {
    let device = await Device.findOne({ where: { user_id: userId, fingerprint: deviceFingerprint } });
    if (!device) {
      device = await Device.create({ user_id: userId, fingerprint: deviceFingerprint, last_seen: new Date() });
    }
    const expiresAt = new Date();
    expiresAt.setMonth(expiresAt.getMonth() + 1);
    const licenseKey = Math.random().toString(36).substring(2, 18).toUpperCase();
    const license = await License.create({
      key: licenseKey,
      user_id: userId,
      device_id: device.id,
      plan,
      valid: true,
      expires_at: expiresAt,
      payment_provider: paymentProvider,
      payment_id: paymentId
    });
    res.json({ success: true, licenseKey: license.key, expires_at: license.expires_at });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
});

// List licenses for a user
router.get('/user/:userId', async (req, res) => {
  const { userId } = req.params;
  const licenses = await License.findAll({ where: { user_id: userId } });
  res.json(licenses);
});

module.exports = router;
