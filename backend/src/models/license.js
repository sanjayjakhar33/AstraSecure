const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const License = sequelize.define('License', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    key: { type: DataTypes.STRING, unique: true },
    user_id: DataTypes.INTEGER,
    device_id: DataTypes.INTEGER,
    plan: DataTypes.STRING,
    valid: { type: DataTypes.BOOLEAN, defaultValue: true },
    expires_at: DataTypes.DATE,
    payment_provider: DataTypes.STRING,
    payment_id: DataTypes.STRING
  }, {
    timestamps: true,
    tableName: 'licenses'
  });
  return License;
};
