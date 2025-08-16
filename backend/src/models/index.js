const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: false,
});

const User = require('./user')(sequelize);
const Device = require('./device')(sequelize);
const License = require('./license')(sequelize);
const Subscription = require('./subscription')(sequelize);

User.hasMany(Device, { foreignKey: 'user_id' });
Device.belongsTo(User, { foreignKey: 'user_id' });

User.hasMany(Subscription, { foreignKey: 'user_id' });
Subscription.belongsTo(User, { foreignKey: 'user_id' });

User.hasMany(License, { foreignKey: 'user_id' });
Device.hasMany(License, { foreignKey: 'device_id' });
License.belongsTo(User, { foreignKey: 'user_id' });
License.belongsTo(Device, { foreignKey: 'device_id' });

module.exports = { sequelize, User, Device, License, Subscription };
