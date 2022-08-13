##Welcome to the EKTO Token ERC20 Contract Front End.

# Family Fuel

# -- Fueling Responsible Money Management Through Crypto and Gaming --

#this is currently a Fun Project/proof of concept. using the EKTO token as an allowance for helping around the house. the below code when run through streamlit will take me to the Front end. this interface is designed to Mint new tokens as a result of a completed task.  textbox included to capture task that resulted in reward. this is currently saved to a .CSV dataframe. I can then reference this when completing the transaction on the contract.  intention long term is to integrate front end to smart contract completely as a completed proof of concept. Phase 2 is intended to expand on what and where the EKTO token can be used.

#loading imports
import os
import json
from web3 import Account
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import requests


load_dotenv("SAMPLE.env")

# Define and connect a new Web3 provider

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
private_key= os.getenv("PRIVATE_API_KEY")
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

#generating account details to be used with contract.
def generate_account(w3,private_key):
    account = Account.privateKeyToAccount(private_key)
    return account

#pull in Eth ACCT and display with logo on the sidebar
account= generate_account(w3,private_key)
with st.sidebar:

    st.write("loaded Account Address", account.address)
    st.write("Smart Contract Address", contract_address)

    st.image('./Logo-Family-Fuel.png')
#sidebar accsess control feature. 
    gold_pile=st.text_input("Enter the correct Account Address: ") 
    
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
address2 = st.selectbox("Select Account", ("Player1", "Player2", "Player3", "Game Master")) #to be updated with true names in final verson.
st.write('You selected:', address2)
st.markdown("---")

#function designed to call mint.  this will currently need to be completed on the contract directly.
st.markdown("---")
st.markdown("## Allowance Payment Portal")


#text box to capture reason for tokens to be awarded. 
Mint_details = st.text_input("Enter Details of Awarded EKOT tokens:")
amount_to_mint = st.slider("Enter the amount of EKOT to be awarded", min_value=1, max_value=50, value=25)
nonce=w3.eth.get_transaction_count(contract_address)
recipt = Mint_details, amount_to_mint

confirm_correct_player = st.write("Confirm that EKTO is to be removed/converted from: ", address2,"'s Account")
confirm = st.checkbox(address2)

if confirm:
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
    
        data=(recipt, gold_pile)
        df=pd.DataFrame(data)
        df.to_csv("./Capture/mint.csv", index=False)
    
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
st.markdown("---")

st.markdown("## Convert your EKOT to Game Night GOLD")
st.markdown("## Or put your EKOT towards family Votes")
st.markdown("1 EKOT = 10 GOLD")
st.markdown("5 EKOT = 1 Vote")


#select reason for conversion and number of EKTO to be Used

name = st.selectbox("Select Campaign/Game or Vote", ("StarFinder", "Rise of the Runelords", "Monopoly", "Vote"))
EKOT_amount = st.slider("Enter the amount of EKOT you wish to Convert to Game Currency", min_value=1, max_value=100,  value=50)

#confirm correct player selected with Checkbox
confirm_correct_player = st.write("Confirm that EKTO is to be removed/converted from: ", address2,"'s Account")
agree = st.checkbox('Confirm')

if agree:
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

#display recipt to user. additional work need to join with rinkeby
        st.write("Transaction mined")
        st.write(EKOT_amount, "EKTO has been removed from ", address2, "'s  Account")
        st.write("Happy Gaming!")    
    
##
#create and save .csv. currently used to record details of transactions to be translated to the contract. in the future this step should be done via MetaMask.
##
        data=("Burn", gold_pile, address2, EKOT_amount, name, "1EKOT = 10 GOLD")
        df=pd.DataFrame(data)
        df.to_csv("./Capture/burn.csv", index=False)
st.markdown("---")

