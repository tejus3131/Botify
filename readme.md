# Botify (Merchandise Monetarization)

Video Demo Link : [Here](https://drive.google.com/drive/folders/19x4Z77GjIJzK-xAV_kiMBA3lugg4tyLY?usp=drive_link)

## Introduction

Botify is a Discord bot designed to facilitate transactions between buyers and sellers within Discord servers. Leveraging the power of Uagents technology, Botify automates the transfer of funds from the buyer's wallet to the seller's wallet upon placing an order, providing a seamless and secure platform for merchandise monetization.

## Features

- Automated fund transfer from buyer's wallet to seller's wallet upon order placement.
- Integration with Discord for real-time communication and transaction processing.
- Secure handling of transactions using Uagents technology.
- Customizable settings for transaction parameters and user preferences.

## Installation and Setup

Follow these steps to install and set up Botify on your Discord server:

1. **Clone the Repository**:
   Clone the project repository from GitHub or download the source code as a ZIP file and extract it to your local machine.

2. **Install Dependencies**:
   Ensure you have Python installed on your system. Then, navigate to the project directory and install the required dependencies using pip:
   `
   pip install -r requirements.txt`

3. **Obtain Bot Token**:
   Visit the Discord Developer Portal [here](https://discord.com/developers/applications) and create a new application. Navigate to the "Bot" tab and click "Add Bot". Copy the bot token.

4. **Configure Bot Token**:
   Create a new file named `.env` in the project directory and add the following line, replacing 'TOKEN' with the bot token obtained in the previous step:

5. **Run the Bot**:
   Execute the Python script to run the bot:

6. **Invite the Bot to Your Server**:
Generate an OAuth2 URL for your bot from the Discord Developer Portal and invite the bot to your Discord server. Make sure to grant the necessary permissions for the bot to function correctly.

7. **Configure Bot Commands**:
Customize bot commands, features, and settings according to your preferences by editing the `bot_agent.py` script. You can add additional commands, modify existing ones, or integrate additional functionalities as needed.

8. **Test the Bot**:
Once the bot is running and invited to your server, test its functionality by interacting with it in Discord. Ensure that all commands work as expected and that the bot responds appropriately to user inputs.

## Usage

- Use the provided bot commands to view merchandise listings, place orders, and manage wallets.
- Follow the syntax and guidelines specified in the bot's command descriptions for seamless interaction.

## Contributing

Contributions to Botify are welcome! To contribute, follow these steps:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and submit a pull request.
- Ensure your code follows the project's coding standards and conventions.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Special thanks to the creators of the Uagents library for their valuable contribution to this project.
- We appreciate the support and feedback from the Discord community in testing and refining Botify.

## Contact Information

For questions, feedback, or support, please contact via [Mail](mailto:tejus3131@gmail.com).
