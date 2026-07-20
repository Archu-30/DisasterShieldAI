# DisasterShield AI — Deployment Guide

This guide explains how to deploy **DisasterShield AI** to **Render** and **Streamlit Community Cloud**.

---

> ⚠️ **Important Note on Vercel vs Render / Streamlit Cloud**
> Streamlit applications require a persistent, long-running Python server process. **Vercel** is designed for static websites and serverless functions (Node.js/Next.js), so it **cannot run Streamlit apps**. 
> For hosting Streamlit apps, use **Render** or **Streamlit Community Cloud**.

---

## 1. Deploying on Render (Recommended SaaS Hosting)

Render provides free Python web service hosting with persistent background process support.

### Option A: Automatic Deployment via `render.yaml` Blueprint

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** → **Blueprint**.
3. Connect your GitHub repository (`Archu-30/DisasterShieldAI`).
4. Render will automatically detect `render.yaml`.
5. Under **Environment Variables**, set:
   - `GROQ_API_KEY`: Your Groq API Key
6. Click **Apply**. Render will build and deploy your application automatically.

### Option B: Manual Web Service Setup on Render

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** → **Web Service**.
3. Connect your repository: `Archu-30/DisasterShieldAI`.
4. Configure settings:
   - **Name**: `disastershield-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Under **Environment Variables**, add:
   - Key: `GROQ_API_KEY`, Value: `<your-groq-api-key>`
6. Click **Create Web Service**.

Your app live link on Render will be:  
`https://disastershield-ai.onrender.com` (or similar custom Render URL).

---

## 2. Deploying on Streamlit Community Cloud (Free 1-Click Hosting)

Streamlit Community Cloud is the official free hosting service built specifically for Streamlit apps.

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
2. Click **New app**.
3. Select your repository: `Archu-30/DisasterShieldAI`
4. Set settings:
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Advanced settings...** → **Secrets**:
   Add your secrets in TOML format:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Click **Deploy!**

Your live URL will be generated instantly (e.g. `https://disastershieldai.streamlit.app`).

---

## Environment Variables Required

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | **Yes** | API Key for Groq AI LLM model |
