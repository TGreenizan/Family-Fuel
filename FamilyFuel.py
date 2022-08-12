#loading imports
import os
import json
from web3 import Account
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import requests


load_dotenv("SAMPLE.env")

# Define and connect a new Web3 provider

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
private_key= os.getenv("PRIVATE_API_KEY")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")


def generate_account(w3,private_key):
    account = Account.privateKeyToAccount(private_key)
    return account

#pull in Eth ACCT
account= generate_account(w3,private_key)
with st.sidebar:

    st.write("loaded Account Address", account.address)
    st.write("Smart Contract Address", contract_address)

    st.image('./Logo-Family-Fuel.png')
################################################################################
# Contract Helper function:
# 1. Loads the contract once using ganache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

#Load the contract ABI. generated from remix
    with open(Path('./contract/EKOT.json')) as f:
        contract_abi = json.load(f)

#Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

#Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


#Load the contract
contract = load_contract()
address=account.address

st.markdown("---")
st.title("Allowance Credit System")
st.write("Choose an account to get started")
#accounts = w3.eth.accounts
address2 = st.selectbox("Select Account", ("Player1", "Player2", "Player3", "Game Master"))
st.markdown("")
st.write('You selected:', address2)
st.markdown("---")
#########---- Below value to be clear prior to going live####
gold_pile=st.text_input("Enter the correct Account Address: ", value="0xE43805fB65C879Cb550D3d2845e9FC56d14b3061")


#function designed to call the mint function.  this will currently need to be completed on the contract directly.
st.markdown("---")
st.markdown("Allowance Payment Portal")


#text box to capture reason for tokens to be awarded. 
Mint_details = st.text_input("Enter Details of Awarded EKOT tokens")
amount_to_mint = st.slider("Enter the amount of EKOT to be awarded", min_value=1, max_value=50, value=25)
nonce=w3.eth.get_transaction_count(contract_address)
recipt = address2, Mint_details, amount_to_mint

if st.button("Confirm Payment"):
    mints = contract.functions.mint(gold_pile, int(amount_to_mint)
    ).buildTransaction({
    'chainId':4,
    'gas':3000000,
    'nonce': nonce
     })

    st.write("Transaction receipt mined:")
    st.write("Thank you")
    st.write("Raw TX: ", mints)
    st.write("congratulations!", recipt," EKTO ")
    st.text(Mint_details)
    
#####- removed due to code breaking. additional work required to get Mint/Burn to work from the Streamlit interface.  #### 
    #signed_tx=account.sign_transaction(mints)
    #st.write("Signed TX Hash: ", signed_tx.rawTransaction)
    #tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    st.write("Transaction mined")
    
st.markdown("---")

################################################################################
# Convert EKOT Gold Token to GOLD
## -- EKOT will be BURNT - Gold will be used in "DnD Type Game or used for family decisions" 

# - - long term Goal is ERC 1155   -- Gold will be usable in game and IRL *Family decisions
################################################################################
st.markdown("## Convert your EKOT to Game Night GOLD")
st.markdown("1 EKOT = 10 GOLD")

name = st.selectbox("Select Campaign/Game", ("StarFinder", "Rise of the Runelords", "Monopoly"))
EKOT_amount = st.slider("Enter the amount of EKOT you wish to Convert to Game Currency", min_value=1, max_value=100,  value=50)



if st.button("Convert"):
    burn_hash = contract.functions.burn(
              int(EKOT_amount)
    ).buildTransaction({
    'chainId':4,
    'gas':3000000,
    'nonce': nonce
     })
    st.write("Transaction receipt mined:")
    st.write("Thank you")
    #st.write(dict(receipt))
    st.write("Raw TX: ", burn_hash)
    
#####- removed due to update breaking. additional work required to get Mint/Burn to work from the Streamlit interface.  ####    
    #signed_burn=account.sign_transaction(burn_hash)
    #st.write("Signed TX Hash: ", signed_burn.rawTransaction)
    #tx_hash = w3.eth.send_raw_transaction(signed_burn.rawTransaction)
    
    st.write("Transaction mined")
    st.write(EKOT_amount, "EKTO has been removed from ", address2, "'s  Account")
    st.write("Happy Gaming!")

st.markdown("---")

