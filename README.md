# Gridcoin.StellarAnchor

A Proof of Concept anchor server for Gridcoin (GRC) on the Stellar network

## How to Test (on Testnet)

1. Head over to the [Stellar Demo Wallet](https://demo-wallet.stellar.org/) and select "Generate keypair for new account"
2. You should now have a public-private keypair. Copy the public key and open [Stellar Laboratory](https://laboratory.stellar.org/#account-creator?network=test) in a new tab.
3. Paste your public key into the input box under the heading "Friendbot: Fund a test network account", and click "Get test network lumens"
4. Now go back to the Demo Wallet page and click "Refresh account". You should see your `XLM` balance is now 10 000.
5. Next click the "Add asset" button.
6. In the dialog enter the asset code `GRC` and the home domain `stellar-testnet.gridcoin.app`
7. You should see a new box with `0 GRC` under the Balances section now.
8. Select "Add trustline" and then "Start" in the dialog.
9. Now, under the "Select action" dropdown, pick "SEP-24 Deposit". This will open a pop-up dialog to the anchor website, so you may need to allow pop-ups in your browser.
10. The anchor dialog will ask you how much Gridcoin you want to deposit and then provide an address for you to send your **TESTNET** GRC to.
11. _**Make sure you are using your Testnet Gridcoin wallet for this**_
12. Once you have sent your **TESTNET** GRC to the deposit address, you will have to wait for a bit for the anchor to pick up the confirmed transaction. 
    _Note: You may need to refresh the dialog box to see updates to the status of your transaction_
13. After you receive confirmation that your transaction is complete, you can close the anchor dialog, and you should see your GRC balance reflected in the demo wallet page.
