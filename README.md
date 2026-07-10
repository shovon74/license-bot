# License Key Generator & Verification Service

This project contains two ways to generate license keys: a **Local CLI License Key Generator** (which runs offline without any configuration) and a **Telegram Integration** (which automates generation via Telegram chat).

---

## 1. Local License Generator (No `.env` Required)

You can generate license keys directly on your local machine using the command-line interface. This method does not require Telegram or a `.env` file.

### How to Run:
1. Open your terminal/command prompt.
2. Navigate to the project directory:
   ```bash
   cd c:\Users\Hp\Desktop\license-bot
   ```
3. Run the generator script:
   ```bash
   python generate_license.py
   ```
4. Follow the interactive prompts:
   - **Hardware ID (HWID)**: Press **Enter** to use your local machine's HWID, or paste the HWID of the target machine.
   - **Validity Days**: Enter the number of days the license should remain valid (e.g., `30` or `365`).

The script will display the license key and automatically save it to `license.key` in the same directory.

---

## 2. Telegram Integration (Requires `.env` Configuration)

The Telegram integration allows users to generate license keys via chat commands (e.g., `/gen <HWID> <DAYS>`). This requires a `.env` configuration file to connect to Telegram.

### Step 1: Create a `.env` File
Create a file named `.env` in the root directory of the project:

```env
# Telegram Token from @BotFather
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ

# Your Telegram User ID from @userinfobot (only this user can use the service)
ADMIN_USER_ID=987654321
```

### Step 2: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Service
Start the Telegram service on your local machine or server:
```bash
python telegram_license_bot.py
```
Once running, you can message the account on Telegram and use the `/gen` command.

---

## 3. Running/Updating on AWS EC2
If you are running the Telegram service on an AWS EC2 instance:
1. Connect to your instance (e.g., via EC2 Instance Connect).
2. Pull the latest code from GitHub:
   ```bash
   cd /home/ubuntu/license-bot
   git pull origin main
   ```
3. Ensure your `.env` file is present on the server (it is ignored by git, so you must create it manually on AWS using `nano .env` if it's not there).
4. Run or restart the service process on the server.
