const { DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');

module.exports = (sequelize) => {
  const User = sequelize.define('User', {
    id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
    email: { type: DataTypes.STRING, unique: true },
    password_hash: DataTypes.STRING
  }, {
    timestamps: true,
    tableName: 'users'
  });

  User.prototype.validPassword = function(password) {
    return bcrypt.compareSync(password, this.password_hash);
  };

  return User;
};
