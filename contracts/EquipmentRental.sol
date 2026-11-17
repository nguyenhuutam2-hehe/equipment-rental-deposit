// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Equipment Rental Deposit - DS 441 A
/// @notice Quản lý tiền đặt cọc (test Ether) cho MỘT thiết bị duy nhất.
contract EquipmentRental {
    address public owner;      // chủ thiết bị
    string  public itemName;   // tên thiết bị
    uint256 public deposit;    // tiền cọc cố định (wei)
    address public renter;     // người đang thuê (address(0) nếu trống)
    bool    public available;  // true = sẵn sàng cho thuê

    event ItemListed(address indexed owner, string itemName, uint256 deposit);
    event ItemRented(address indexed renter, uint256 amount);
    event ReturnConfirmed(address indexed renter, uint256 refunded);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(string memory _itemName, uint256 _deposit) {
        require(_deposit > 0, "Deposit must be > 0");
        owner = msg.sender;
        itemName = _itemName;
        deposit = _deposit;
        available = true;
        emit ItemListed(owner, _itemName, _deposit);
    }

    /// @notice Người thuê trả đúng tiền cọc để thuê thiết bị.
    function rent() external payable {
        require(available, "Item already rented");
        require(msg.sender != owner, "Owner cannot rent own item");
        require(msg.value == deposit, "Must send exact deposit");

        available = false;
        renter = msg.sender;
        emit ItemRented(msg.sender, msg.value);
    }

    /// @notice Chỉ owner xác nhận trả hàng -> hoàn cọc cho renter, giải phóng thiết bị.
    function confirmReturn() external onlyOwner {
        require(!available, "Item is not rented");

        address payable to = payable(renter);
        uint256 amount = deposit;

        // Effects trước, Interaction sau (chống reentrancy)
        renter = address(0);
        available = true;

        (bool ok, ) = to.call{value: amount}("");
        require(ok, "Refund failed");

        emit ReturnConfirmed(to, amount);
    }
}