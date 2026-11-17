# Equipment Rental Deposit

- Course: DS 441 A - Blockchain: Theory & Practices
- Student: Nguyễn Hữu Tâm | ID: 29211134854

## Mô tả
Smart contract quản lý tiền cọc (test Ether) cho một thiết bị. Owner đăng thiết bị với tiền cọc cố định; renter trả cọc để thuê; chỉ owner xác nhận trả hàng, khi đó hoàn cọc cho renter và thiết bị được giải phóng.

## Quy tắc trong contract (không chỉ ở giao diện)
- `rent()`: chỉ khi item available, người gọi không phải owner, và gửi đúng bằng tiền cọc.
- `confirmReturn()`: chỉ `owner` (modifier `onlyOwner`), chỉ khi item đang được thuê.
- Events: `ItemListed`, `ItemRented`, `ReturnConfirmed`.

## Yêu cầu
- Ganache (GUI), Remix IDE, VS Code, Python 3.10+, MetaMask
- `pip install web3 py-solc-x`
- Chỉ dùng tài khoản/ETH test của Ganache. KHÔNG dùng private key hay tiền thật.

## Cấu hình mạng Ganache / MetaMask
| Tham số | Giá trị |
|---|---|
| RPC URL | http://127.0.0.1:7545 |
| Chain ID | 1337 (Network ID 5777) |
| Currency | ETH |
| Hardfork | Merge (EVM version: paris) |

Import private key của 3 tài khoản Ganache vào MetaMask: index 0 = Owner, index 1 = Renter, index 2 = Other.

## Deploy
**Cách A - Remix:** mở `contracts/EquipmentRental.sol` -> compile 0.8.20, EVM version `paris` -> Deploy & Run -> Environment: Injected Provider - MetaMask (tài khoản Owner, mạng Ganache) -> constructor args: `"Canon EOS R5", 1000000000000000000` (1 ETH) -> copy địa chỉ contract.

**Cách B - Python:** `python deploy_and_test.py` (deploy + chạy test tự động).

## Chạy giao diện
```
cd equipment-rental
python3 -m http.server 8000
```
Mở http://localhost:8000 -> Connect Wallet -> dán địa chỉ contract -> Load Contract.

## Kịch bản demo
1. Account 0 (Owner) deploy contract.
2. Account 1 (Renter) bấm **Rent** -> thành công, status = RENTED.
3. Account 2 (Other) bấm **Rent** -> bị từ chối ("Item already rented").
4. Account 1 (Renter) bấm **Confirm Return** -> bị từ chối ("Only owner").
5. Account 0 (Owner) bấm **Confirm Return** -> hoàn cọc cho Renter, status = AVAILABLE.

## Kết quả test
(Dán output của `deploy_and_test.py` và screenshot vào đây)

## Nguồn tham khảo / hỗ trợ
- Mã nguồn được hỗ trợ soạn thảo bởi Claude (Anthropic); đã được tôi đọc hiểu và kiểm thử.
- ethers.js v6 (cdnjs), web3.py, py-solc-x.