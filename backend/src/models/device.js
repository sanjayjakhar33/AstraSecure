const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const Device = sequelize.define('Device', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    user_id: DataTypes.INTEGER,
    fingerprint: DataTypes.STRING,
    last_seen: DataTypes.DATE
  }, {
    timestamps: true,
    tableName: 'devices'
  });
  return Device;
};
