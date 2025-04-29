import streamlit as st
import hashlib
import datetime

# ----- Block & Blockchain Classes -----
class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(datetime.datetime.now(), "Genesis Block", "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(datetime.datetime.now(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

# ---------- Streamlit UI ----------
st.title("📦 Simple Blockchain Package Tracker")

# Use session state to persist the blockchain
if 'ledger' not in st.session_state:
    st.session_state.ledger = Blockchain()

ledger = st.session_state.ledger

st.subheader("📋 Current Package Tracking History")
for i, block in enumerate(ledger.chain):
    st.write(f"### Block {i}")
    st.json({
        "Timestamp": str(block.timestamp),
        "Data": block.data,
        "Hash": block.hash,
        "Previous Hash": block.previous_hash
    })

st.markdown("---")

# Form to add new block
st.subheader("➕ Add New Package Tracking Event")

with st.form("add_event"):
    package_id = st.text_input("Package ID")
    status = st.text_input("Status (e.g., Shipped, In Transit, Delivered)")
    submitted = st.form_submit_button("Add Block")

    if submitted:
        if package_id and status:
            data = {"package_id": package_id, "status": status}
            ledger.add_block(data)
            st.success("✅ New tracking event added to blockchain!")
            st.experimental_rerun()
        else:
            st.error("❌ Please fill in both fields.")

st.markdown("---")

# Blockchain integrity check
st.subheader("🔒 Blockchain Validation")
if ledger.is_valid():
    st.success("✅ Blockchain is valid and untampered.")
else:
    st.error("⚠️ Blockchain integrity check failed!")

