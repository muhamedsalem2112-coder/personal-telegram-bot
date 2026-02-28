# Personal Telegram Bot

## Setup and Deployment Instructions

This guide will help you set up and deploy your Telegram bot on Render.

### Prerequisites
- Make sure you have a Telegram account.
- Install Node.js and npm.

### Steps to Setup
1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/muhamedsalem2112-coder/personal-telegram-bot.git  
   ```  

2. **Navigate to the Project Directory**  
   ```bash  
   cd personal-telegram-bot  
   ```  

3. **Install Dependencies**  
   ```bash  
   npm install  
   ```  

4. **Set Up Bot Token**  
   - Create a `.env` file in the root directory of the project and add your Telegram bot token:
     ```bash  
     BOT_TOKEN=your_bot_token_here  
     ```

### Deployment on Render

1. **Create a Render Account**  
   Visit [Render.com](https://render.com) and sign up for an account.

2. **Create a New Web Service**  
   - Choose 'Web Service' from your Render dashboard.
   - Connect your GitHub repository to Render.

3. **Configure the Service**  
   - Set the Build Command:  
     ```bash  
     npm install  
     ```  
   - Set the Start Command:  
     ```bash  
     npm start  
     ```  
   - Set the Environment Variables:  
     - Add BOT_TOKEN with the value from your `.env` file.

4. **Deploy the Service**  
   Click the 'Create Web Service' button and wait for Render to build and deploy the application.

### Testing Your Bot
- Once deployed, you can interact with your bot on Telegram to test its functionality.

## Troubleshooting
- If you encounter issues, check the Render logs for errors or consult the Telegram Bot API documentation.