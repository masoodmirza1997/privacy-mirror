<h1 align="center">🛡️ PRIVACY MIRROR</h1>
<p align="center"><b>Check your digital exposure — instantly, privately, and locally.</b></p>

<p align="center">
  <img src="hero.gif" width="600">
</p>

---

## 🔍 Overview

**Privacy Mirror** is a modern, elegant, privacy-focused web app built with **Streamlit**.  
It allows users to safely check whether their **email** or **phone number** appears in known public data breaches.

✨ **No accounts. No tracking. No data stored.**  
All checks run **locally in the browser session** using official providers like:

- **HaveIBeenPwned (Email Breaches)**
- **Dehashed (Phone Leak Search)**

The app also includes:

- Beautiful animated UI  
- Data visualizations (Plotly)  
- PDF report generation  
- Password generator  
- Security tips & safety playbook  
- Dark UI with custom CSS, hero sections, and a 4-step flow  

This repository contains the full app code (`privacy1.py`) and required assets.

---

## 🚀 Features

### ✔️ **Email Exposure Scan**
- Checks email against HaveIBeenPwned (requires API key)
- Shows breaches, compromised data types, severity, and breach timelines
- CSV export & detailed PDF report

### ✔️ **Phone Exposure Scan**
- Uses Dehashed API (optional)
- Lists matched records (if any)

### ✔️ **Interactive Visualizations**
- Bar chart of compromised data types
- Line chart of breaches over time
- Risk score gauge (SVG)

### ✔️ **Security Toolkit**
- Strong password generator  
- Personal “Safety Playbook”  
- Anti-phishing advice  
- Recommended security actions

### ✔️ **Privacy First**
- No user input stored  
- Privacy mode enabled by default  
- All computation inside session memory only 

---
