# from fastapi import FastAPI , HTTPException
# from web3 import Web3
# from dotenv import load_dotenv
# from pathlib import Path
# import os
# import json
# from pydantic import BaseModel

# #  """ Class for Data type """ 

# class MintRequest(BaseModel):
#      amount:int
# class DepositRequest(MintRequest):
#     token_address: str
# class RedeemRequest(DepositRequest):
#     pass
# class BurnRequest(MintRequest):
#     pass
# class DepositAndMintRequest(DepositRequest):
#     amount_dsc_to_mint: int
# class RedeemForDscRequest(DepositRequest):
#     amount_dsc_to_burn: int

# class LiquidateRequest(BaseModel):
#     collateral: str
#     user: str
#     debt_to_cover: int

# class DepositAndMintRequest(DepositRequest):
#     amount_dsc_to_mint: int

# class RedeemForDscRequest(DepositRequest):
#     amount_dsc_to_burn: int

# class UserAddress(BaseModel):
#     user: str

# class UserTokenRequest(UserAddress):
#     token: str
# class ApproveTokenRequest(BaseModel):
#     token_address: str
#     spender_address: str
#     amount: int

# class TokenMint(BaseModel):
#     amount: int
     
# load_dotenv()

# app=FastAPI()

# # """ Middleware  """
# # Add CORS middleware

# w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
# private_key=os.getenv("PRIVATE_KEY")
# public_address=os.getenv("PUBLIC_ADDRESS")
# contract_address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
# wbtc_address = Web3.to_checksum_address(os.getenv("WBTC_ADDRESS"))
# weth_address = Web3.to_checksum_address(os.getenv("WETH_ADDRESS"))
# dsc_address = Web3.to_checksum_address(os.getenv("DSC_ADDRESS"))

# abi_path = Path(__file__).resolve().parent.parent / "Blockchain-Foundry-StableToken" / "out" /"DSCEngine.sol"/"DSCEngine.json"


# if not w3.is_connected():
#     raise HTTPException(status_code=500, detail="Failed to connect to the Ethereum node")


# # """ ABI """
# with open(abi_path, "r") as abi_file:
#     contract_json = json.load(abi_file)
#     abi = contract_json["abi"]
    
# # Minimal ERC20 ABI for mint, approve, and allowance
# erc20_abi = [
#     {
#         "constant": False,
#         "inputs": [
#             {"name": "_spender", "type": "address"},
#             {"name": "_value", "type": "uint256"}
#         ],
#         "name": "approve",
#         "outputs": [{"name": "", "type": "bool"}],
#         "type": "function"
#     },
#     {
#         "constant": True,
#         "inputs": [
#             {"name": "_owner", "type": "address"},
#             {"name": "_spender", "type": "address"}
#         ],
#         "name": "allowance",
#         "outputs": [{"name": "", "type": "uint256"}],
#         "type": "function"
#     },
#     {
#         "constant": False,
#         "inputs": [
#             {
#             "name": "amount",
#             "type": "uint256"
#             }
#         ],
#         "name": "mint",
#         "outputs": [],
#         "payable": False,
#         "stateMutability": "nonpayable",
#         "type": "function"
# }
# ]

# # Initialize contracts
# contract = w3.eth.contract(address=contract_address, abi=abi)
# wbtc_contract = w3.eth.contract(address=wbtc_address, abi=erc20_abi)
# weth_contract = w3.eth.contract(address=weth_address, abi=erc20_abi)
# dsc_contract = w3.eth.contract(address=dsc_address, abi=erc20_abi)

# def build_tx(function, args):
#     """Helper to build and sign a transaction"""
#     nonce = w3.eth.get_transaction_count(public_address)
#     txn = function(*args).build_transaction({
#         "from": public_address,
#         "nonce": nonce,
#         "gas": 3000000,
#         "gasPrice": w3.to_wei("20", "gwei")
#     })
#     signed_txn = w3.eth.account.sign_transaction(txn, private_key)
#     return w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# # """ Function for API """
# async def approve_token(token_contract, spender_address, amount):
#     """Approve a spender to spend tokens for public_address"""
#     try:
#         spender_address = Web3.to_checksum_address(spender_address)
#         allowance = token_contract.functions.allowance(public_address, spender_address).call()
#         if allowance < amount:
#             tx_hash = build_tx(
#                 token_contract.functions.approve,
#                 [spender_address, amount]
#             )
#             return tx_hash.hex()
#         return None
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Approval failed: {str(e)}")

# @app.post("/approve-tokens")
# async def approve_tokens(data: ApproveTokenRequest):
#     try:
#         token_address = Web3.to_checksum_address(data.token_address)
#         spender_address = Web3.to_checksum_address(data.spender_address)
#         amount = data.amount

#         if amount <= 0:
#             raise HTTPException(status_code=400, detail="Amount must be positive")

#         # Validate token_address
#         token_contract = None
#         token_name = None
#         if token_address.lower() == wbtc_address.lower():
#             token_contract = wbtc_contract
#             token_name = "WBTC"
#         elif token_address.lower() == weth_address.lower():
#             token_contract = weth_contract
#             token_name = "WETH"
#         elif token_address.lower() == dsc_address.lower():
#             token_contract = dsc_contract
#             token_name = "DSC"
#         else:
#             raise HTTPException(status_code=400, detail="Invalid token address. Must be WBTC, WETH, or DSC.")

#         # Approve the token
#         tx_hash = await approve_token(token_contract, spender_address, amount)
#         if tx_hash:
#             return {f"{token_name}_approval": tx_hash}
#         return {"message": f"No approval needed for {token_name}; sufficient allowance already set"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/mint-wbtc")
# async def mint_wbtc(data: TokenMint):
#     try:
#         # Mint WBTC to user
#         tx_hash = build_tx(
#             wbtc_contract.functions.mint,
#             [data.amount]
#         )
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/mint-weth")
# async def mint_weth(data: TokenMint):
#     try:
#         # Mint WETH to user
#         tx_hash = build_tx(
#             weth_contract.functions.mint,
#             [data.amount]
#         )
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# # """  """
# @app.post("/deposit-collateral")
# async def deposit_collateral(data: DepositRequest):
#     try:
#         token = Web3.to_checksum_address(data.token_address)
#         tx_hash = build_tx(contract.functions.depositCollateral, [token, data.amount])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/mint-dsc")
# async def mint_dsc(data:MintRequest):
#     try:
#         tx_hash = build_tx(contract.functions.mintDsc, [data.amount])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/redeem-collateral")
# async def redeem_collateral(data: RedeemRequest):
#     try:
#         token = Web3.to_checksum_address(data.token_address)
#         tx_hash = build_tx(contract.functions.redeemCollateral, [token, data.amount])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/burn-dsc")
# async def burn_dsc(data: BurnRequest):
#     try:
#         tx_hash = build_tx(contract.functions.burnDsc, [data.amount])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/deposit-collateral-and-mint-dsc")
# async def deposit_collateral_and_mint_dsc(data: DepositAndMintRequest):
#     try:
#         token = Web3.to_checksum_address(data.token_address)
#         tx_hash = build_tx(contract.functions.depositCollateralAndMintDsc, [token, data.amount, data.amount_dsc_to_mint])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/redeem-collateral-for-dsc")
# async def redeem_collateral_for_dsc(data: RedeemForDscRequest):
#     try:
#         token = Web3.to_checksum_address(data.token_address)
#         tx_hash = build_tx(contract.functions.redeemCollateralForDsc, [token, data.amount, data.amount_dsc_to_burn])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/liquidate")
# async def liquidate(data: LiquidateRequest):
#     try:
#         collateral = Web3.to_checksum_address(data.collateral)
#         user = Web3.to_checksum_address(data.user)
#         tx_hash = build_tx(contract.functions.liquidate, [collateral, user, data.debt_to_cover])
#         return {"tx_hash": tx_hash.hex()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/account-information")
# async def get_account_information(data: UserAddress):
#     try:
#         user = Web3.to_checksum_address(data.user)
#         total_dsc_minted, collateral_value_in_usd = contract.functions.getAccountInformation(user).call()
#         return {
#             "total_dsc_minted": total_dsc_minted,
#             "collateral_value_in_usd": collateral_value_in_usd
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/collateral-balance")
# async def get_collateral_balance(data: UserTokenRequest):
#     try:
#         user = Web3.to_checksum_address(data.user)
#         token = Web3.to_checksum_address(data.token)
#         balance = contract.functions.getCollateralBalanceOfUser(user, token).call()
#         return {"balance": balance}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/health-factor")
# async def get_health_factor(data: UserAddress):
#     try:
#         user = Web3.to_checksum_address(data.user)
#         health_factor = contract.functions.getHealthFactor(user).call()
#         return {"health_factor": health_factor}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/collateral-tokens")
# async def get_collateral_tokens():
#     try:
#         tokens = contract.functions.getCollateralTokens().call()
#         return {"collateral_tokens": tokens}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/usd-value")
# async def get_usd_value(data: UserTokenRequest):
#     try:
#         token = Web3.to_checksum_address(data.token)
#         amount = contract.functions.getCollateralBalanceOfUser(data.user, token).call()
#         usd_value = contract.functions.getUsdValue(token, amount).call()
#         return {"usd_value": usd_value}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


######################################################################################################################

# New code for testing 

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from web3 import Web3
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Web3 Setup
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
if not w3.is_connected():
    raise HTTPException(status_code=500, detail="Failed to connect to RPC")

# Contract Setup
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
wbtc_address = Web3.to_checksum_address(os.getenv("WBTC_ADDRESS"))
weth_address = Web3.to_checksum_address(os.getenv("WETH_ADDRESS"))
dsc_address = Web3.to_checksum_address(os.getenv("DSC_ADDRESS"))

abi_path = Path(__file__).resolve().parent.parent / "Blockchain-Foundry-StableToken" / "out" / "DSCEngine.sol" / "DSCEngine.json"
with open(abi_path, "r") as abi_file:
    contract_json = json.load(abi_file)
    abi = contract_json["abi"]

contract = w3.eth.contract(address=contract_address, abi=abi)
erc20_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "amount", "type": "uint256"}],
        "name": "mint",
        "outputs": [],
        "type": "function"
    }
]

wbtc_contract = w3.eth.contract(address=wbtc_address, abi=erc20_abi)
weth_contract = w3.eth.contract(address=weth_address, abi=erc20_abi)
dsc_contract = w3.eth.contract(address=dsc_address, abi=erc20_abi)

# Request Models
class BaseTx(BaseModel):
    user: str

class MintRequest(BaseTx):
    amount: int

class DepositRequest(MintRequest):
    token_address: str

class RedeemRequest(DepositRequest):
    pass

class BurnRequest(MintRequest):
    pass

class DepositAndMintRequest(DepositRequest):
    amount_dsc_to_mint: int

class RedeemForDscRequest(DepositRequest):
    amount_dsc_to_burn: int

class LiquidateRequest(BaseModel):
    user: str
    collateral: str
    debt_to_cover: int

class ApproveTokenRequest(BaseModel):
    user: str
    token_address: str
    spender_address: str
    amount: int

class TokenMint(BaseTx):
    amount: int

class UserTokenRequest(BaseModel):
    user: str
    token: str

# Helper
def build_tx(user_address, function, args):
    nonce = w3.eth.get_transaction_count(user_address)
    txn = function(*args).build_transaction({
        "from": user_address,
        "nonce": nonce,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei")
    })
    signed = w3.eth.account.sign_transaction(txn, os.getenv("PRIVATE_KEY"))
    return w3.eth.send_raw_transaction(signed.raw_transaction)

# Endpoints

@app.post("/approve-tokens")
async def approve_tokens(data: ApproveTokenRequest):
    try:
        token = Web3.to_checksum_address(data.token_address)
        spender = Web3.to_checksum_address(data.spender_address)
        user = Web3.to_checksum_address(data.user)

        contract_map = {
            wbtc_address.lower(): wbtc_contract,
            weth_address.lower(): weth_contract,
            dsc_address.lower(): dsc_contract
        }

        token_contract = contract_map.get(token.lower())
        if not token_contract:
            return JSONResponse(status_code=400, content={"error": "Unsupported token"})

        allowance = token_contract.functions.allowance(user, spender).call()
        if allowance < data.amount:
            tx = build_tx(user, token_contract.functions.approve, [spender, data.amount])
            return {"tx_hash": tx.hex()}
        return {"message": "Allowance already sufficient"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/mint-wbtc")
async def mint_wbtc(data: TokenMint):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), wbtc_contract.functions.mint, [data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/mint-weth")
async def mint_weth(data: TokenMint):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), weth_contract.functions.mint, [data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/deposit-collateral")
async def deposit_collateral(data: DepositRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), contract.functions.depositCollateral,
                      [Web3.to_checksum_address(data.token_address), data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/mint-dsc")
async def mint_dsc(data: MintRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), contract.functions.mintDsc, [data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/deposit-collateral-and-mint-dsc")
async def deposit_and_mint(data: DepositAndMintRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user),
                      contract.functions.depositCollateralAndMintDsc,
                      [Web3.to_checksum_address(data.token_address), data.amount, data.amount_dsc_to_mint])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/burn-dsc")
async def burn_dsc(data: BurnRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), contract.functions.burnDsc, [data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/redeem-collateral")
async def redeem_collateral(data: RedeemRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user), contract.functions.redeemCollateral,
                      [Web3.to_checksum_address(data.token_address), data.amount])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/redeem-collateral-for-dsc")
async def redeem_for_dsc(data: RedeemForDscRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user),
                      contract.functions.redeemCollateralForDsc,
                      [Web3.to_checksum_address(data.token_address), data.amount, data.amount_dsc_to_burn])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/liquidate")
async def liquidate(data: LiquidateRequest):
    try:
        tx = build_tx(Web3.to_checksum_address(data.user),
                      contract.functions.liquidate,
                      [Web3.to_checksum_address(data.collateral), Web3.to_checksum_address(data.user), data.debt_to_cover])
        return {"tx_hash": tx.hex()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/account-information")
async def get_account_info(data: BaseTx):
    try:
        user = Web3.to_checksum_address(data.user)
        minted, usd = contract.functions.getAccountInformation(user).call()
        return {"total_dsc_minted": str(minted), "collateral_value_in_usd": str(usd)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# @app.get("/collateral-tokens")
# async def get_collateral_tokens():
#     try:
#         tokens = contract.functions.getCollateralTokens().call()
#         return {"collateral_tokens": tokens}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
@app.get("/collateral-tokens")
async def get_collateral_tokens():
    try:
        tokens = contract.functions.getCollateralTokens().call()

        # Ensure it's JSON-safe (i.e. list of strings)
        if not isinstance(tokens, list) or not all(isinstance(t, str) for t in tokens):
            return JSONResponse(status_code=500, content={"error": "Invalid token list returned from contract"})

        return JSONResponse(status_code=200, content={"collateral_tokens": tokens})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Server error: {str(e)}"})

@app.post("/collateral-balance")
async def get_collateral_balance(data: UserTokenRequest):
    try:
        balance = contract.functions.getCollateralBalanceOfUser(
            Web3.to_checksum_address(data.user),
            Web3.to_checksum_address(data.token)
        ).call()
        return {"balance": str(balance)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/health-factor")
async def get_health_factor(data: BaseTx):
    try:
        factor = contract.functions.getHealthFactor(Web3.to_checksum_address(data.user)).call()
        return {"health_factor": str(factor)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/usd-value")
async def get_usd_value(data: UserTokenRequest):
    try:
        user = Web3.to_checksum_address(data.user)
        token = Web3.to_checksum_address(data.token)
        amount = contract.functions.getCollateralBalanceOfUser(user, token).call()
        usd_value = contract.functions.getUsdValue(token, amount).call()
        return {"usd_value": str(usd_value)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
