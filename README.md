# DSC Protocol

**Decentralized Stability, Powered by AI**

DSC Protocol is a fully decentralized, overcollateralized, cross-chain stablecoin system backed by major assets like ETH, BTC, SOL, and tokenized real-world assets (RWAs). Built for real-world utility with AI-assisted smart liquidation and pricing.

---

## 🌐 Live Preview (Frontend)

[https://dsc-protocol-graphfieds-projects.vercel.app](https://dsc-protocol-graphfieds-projects.vercel.app)

---

## 🏗️ Monolith Repo Structure

```
DSC-Protocol/
👉️ apps/
👉️ ├ frontend/        # Frontend (React/Next.js)
👉️ └ protocol/        # Smart contracts (Foundry or Hardhat)
👉️ scripts/             # Automation or deploy scripts (optional)
👉️ .github/workflows/   # GitHub Actions for CI/CD
👉️ .gitignore
👉️ README.md
```

---

## ⚙️ Tech Stack

| Layer           | Stack / Tools                               |
| --------------- | ------------------------------------------- |
| Smart Contracts | Foundry / Solidity / Chainlink              |
| Frontend        | Next.js, React, Tailwind CSS                |
| Blockchain      | Base Sepolia (EVM), ETH, BTC, SOL           |
| Automation      | GitHub Actions                              |
| AI Utilities    | Oracle price + AI Liquidation (in progress) |

---

## 🚀 Features

* 🔗 **Cross-chain Collateral**: Supports ETH, BTC, SOL (RWA coming soon)
* 📈 **AI-Powered Stability Engine**
* 🧠 **Smart Liquidation via Oracle Feeds**
* 🔐 **Fully On-Chain Minting and Burning**
* 🖥️ **Modern dApp Interface**
* ⚒️ **CI/CD Ready (Smart contracts & Frontend)**

---

## 🧪 Run Locally

### 🔧 Prerequisites

* Node.js v18+
* Foundry (`curl -L https://foundry.paradigm.xyz | bash`)
* Metamask (for testing on Base Sepolia)

### 🖥️ Frontend

```bash
cd apps/frontend
pnpm install
pnpm run dev
```

### 🔐 Smart Contracts

```bash
cd apps/protocol/Blockchain-Foundry-StableToken
forge build
forge test
```

---

## 🌉 Deployment Flow

* ✅ Push to `main` triggers:

  * `forge test` (smart contracts)
  * `pnpm build` (frontend)
* 🎯 Optional: Auto-deploy via Vercel or other hosts

---

## 👨‍💻 Contributors

* **Yazib** — Founder of DSC and Blockchain Developer specializing in DeFi and smart contracts using Solidity, Rust, and multichain tools.
* **Fahad Ghouri** — Founder of Pakverse and a builder at the intersection of AI, Web3, and innovation with 10 years of experience.
* **Muhammad Mehdi** — Co-Founder & CTO of Pakverse, building scalable AI and Web3 solutions for the future.


<!-- 
---

## 🏆 Built for

**[Base APAC Hackathon 2024](https://base.org/hackathons)**
*Competing in the Real-World Utility + AI track.*

--- -->
<!-- 
## 📜 License

© 2024 DSC Protocol. All rights reserved. Licensed under custom or commercial terms. Contact the team for usage or partnership.

---

> For inquiries, reach out via [Pakverse](https://www.linkedin.com/company/pakverse) -->
