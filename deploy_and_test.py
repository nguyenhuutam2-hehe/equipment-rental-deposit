"""Deploy + test EquipmentRental trên Ganache bằng web3.py.
Cài đặt:  pip install web3 py-solc-x
Chạy:     python deploy_and_test.py
"""
from pathlib import Path
from web3 import Web3
from solcx import compile_standard, install_solc

RPC = "http://127.0.0.1:7545"   # Ganache GUI (CLI dùng 8545)
SOLC = "0.8.20"

w3 = Web3(Web3.HTTPProvider(RPC))
assert w3.is_connected(), "Không kết nối được Ganache"
owner, renter, other = w3.eth.accounts[0], w3.eth.accounts[1], w3.eth.accounts[2]
DEPOSIT = w3.to_wei(1, "ether")

# ---- Compile ----
install_solc(SOLC)
src = Path(__file__).parent / "contracts" / "EquipmentRental.sol"
out = compile_standard({
    "language": "Solidity",
    "sources": {"EquipmentRental.sol": {"content": src.read_text()}},
    "settings": {
        "evmVersion": "paris",
        "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}},
    },
}, solc_version=SOLC)
c = out["contracts"]["EquipmentRental.sol"]["EquipmentRental"]
abi, bytecode = c["abi"], c["evm"]["bytecode"]["object"]

# ---- Deploy ----
Factory = w3.eth.contract(abi=abi, bytecode=bytecode)
rc = w3.eth.wait_for_transaction_receipt(
    Factory.constructor("Canon EOS R5", DEPOSIT).transact({"from": owner}))
rental = w3.eth.contract(address=rc.contractAddress, abi=abi)
print("Contract address:", rc.contractAddress)

results = []
def check(name, cond):
    results.append((name, cond))
    print(("[PASS] " if cond else "[FAIL] ") + name)

def expect_revert(name, fn):
    try:
        fn()
        check(name, False)
    except Exception as e:
        print("   revert:", str(e)[:100])
        check(name, True)

# ---- Test 1: thuê thành công ----
w3.eth.wait_for_transaction_receipt(rental.functions.rent().transact({"from": renter, "value": DEPOSIT}))
check("Rent thành công, renter đúng", rental.functions.renter().call() == renter)
check("available = False sau khi thuê", rental.functions.available().call() is False)

# ---- Test 2: thuê lần 2 bị từ chối ----
expect_revert("Reject lần thuê thứ 2",
    lambda: rental.functions.rent().transact({"from": other, "value": DEPOSIT}))

# ---- Test 3: người không phải owner xác nhận trả -> bị từ chối ----
expect_revert("Reject confirmReturn từ non-owner",
    lambda: rental.functions.confirmReturn().transact({"from": renter}))

# ---- Test 4: owner xác nhận -> hoàn cọc ----
before = w3.eth.get_balance(renter)
w3.eth.wait_for_transaction_receipt(rental.functions.confirmReturn().transact({"from": owner}))
after = w3.eth.get_balance(renter)
check("Renter nhận lại đúng tiền cọc", after - before == DEPOSIT)
check("Item được giải phóng", rental.functions.available().call() is True)
check("Contract balance = 0", w3.eth.get_balance(rental.address) == 0)

print(f"\nKết quả: {sum(ok for _, ok in results)}/{len(results)} test PASS")