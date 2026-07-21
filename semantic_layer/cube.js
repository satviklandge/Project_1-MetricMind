module.exports = {
  logger: (msg, params) => {
    console.log(`${msg}: ${JSON.stringify(params)}`);
  }
};
