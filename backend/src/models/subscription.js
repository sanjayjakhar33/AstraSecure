const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const Subscription = sequelize.define('Subscription', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    user_id: DataTypes.INTEGER,
    provider: DataTypes.STRING,
    status: DataTypes.STRING,
    started_at: DataTypes.DATE,
    expires_at: DataTypes.DATE,
    plan: DataTypes.STRING
  }, {
    timestamps: true,
    tableName: 'subscriptions'
  });
  return Subscription;
};
