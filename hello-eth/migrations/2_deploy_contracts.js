const FakeProduct = artifacts.require("FakeProduct");

module.exports = function(deployer) {
  deployer.deploy(FakeProduct);
};
