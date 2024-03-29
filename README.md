# Secure-Voting-System-using-ML-Facial-Recognition
Project for CS/ECE 547/647 

## Abstract
Protecting the confidentiality, integrity, and authenticity of a vote and voter while ensuring false-positive and false-negative votes do not occur in elections has become an important and difficult topic in recent years. With the capabilities of adversaries continuing to grow, the mechanisms to protect data must keep up. We propose a multi-factor authentication scheme to ensure the correct person is voting. Utilizing a Raspberry Pi with a Camera to simulate a polling booth, it is attached to a monitor, keyboard, and mouse for user input an ID number and their information as the first factor of authentication. Data is sent and verified at a server, then the voter’s image for facial recognition biometrics is requested and captured as a second authentication factor. The proposed encryption scheme utilizes AES-256 to encrypt sent data, RSA-2048 for encrypting symmetric keys and creating the digital signature, and SHA-512 for hashing to verify the authenticity and integrity of the data. This is done to protect the information of the voter, and the vote, and prevent voter fraud. Images at the server utilize Amazon Rekognition to match captured images to existing images of that voter in the government’s database. AWS considers cloud security one of its “highest priorities”. Another encryption method and other machine learning models were also experimented with, and results are given. Once verified, the voter can submit their vote at the client end to be encrypted and sent to the server. The results and future of the project are analyzed and reflected upon.

## [Full Report](https://docs.google.com/document/d/1Gtg_C9WFiQCADlDQWh0FNX_N4302sr7p76pfCXgw18w/edit?usp=sharing)

## [Video Demonstration](https://drive.google.com/file/d/1auU4qeAU9vl0GKTH5rcNM7FOgrLuLkDX/view?usp=sharing)

Brought to you by:
1. Marcus Banoub
2. Brayden Bergeron
3. Daniel Lacayo
4. Alexander Pratt
5. Aleksei Rutkovski
