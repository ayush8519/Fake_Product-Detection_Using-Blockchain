// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

contract FakeProduct {

    // ---- USER STRUCT ----
    struct User {
        string username;
        string password;
        string email;
        string contact;
    }

    // ---- PRODUCT STRUCT ----
    struct Product {
        string productName;
        string productDesc;
        string productPrice;
        string barcodeSignature;  // digital signature derived from barcode image
        bool exists;
    }

    // ---- STORAGE ----
    mapping(uint => User) private users;
    uint public userCount;

    mapping(uint => Product) private products;
    uint public productCount;

    // ==================== USER FUNCTIONS ====================

    function addUser(
        string memory username,
        string memory password,
        string memory email,
        string memory contact
    ) public {
        userCount++;
        users[userCount] = User(username, password, email, contact);
    }

    function getUser(uint userId)
        public view
        returns (
            string memory username,
            string memory password,
            string memory email,
            string memory contact
        )
    {
        require(userId > 0 && userId <= userCount, "User not found");
        User memory u = users[userId];
        return (u.username, u.password, u.email, u.contact);
    }

    function getUserCount() public view returns (uint) {
        return userCount;
    }

    // ==================== PRODUCT FUNCTIONS ====================

    function addProduct(
        string memory productName,
        string memory productDesc,
        string memory productPrice,
        string memory barcodeSignature
    ) public {
        productCount++;
        products[productCount] = Product(productName, productDesc, productPrice, barcodeSignature, true);
    }

    function getProduct(uint productId)
        public view
        returns (
            string memory productName,
            string memory productDesc,
            string memory productPrice,
            string memory barcodeSignature
        )
    {
        require(products[productId].exists, "Product not found");
        Product memory p = products[productId];
        return (p.productName, p.productDesc, p.productPrice, p.barcodeSignature);
    }

    function getProductCount() public view returns (uint) {
        return productCount;
    }

    // ==================== AUTHENTICATE BARCODE ====================
    // Compare provided signature with stored signature for a product
    function authenticate(uint productId, string memory inputSignature)
        public view
        returns (bool)
    {
        require(products[productId].exists, "Product not found");
        return (keccak256(abi.encodePacked(products[productId].barcodeSignature))
                == keccak256(abi.encodePacked(inputSignature)));
    }
}
