# Discord Bot: ScoreKeeperBot

ScoreKeeperBot is a lightweight Discord points bot that tracks user scores with Discord bot commands, persistent JSON storage, and configurable environment settings. It provides commands to view, add, and remove points for the user who runs each command.

## Install

1. Install Python 3.10 or newer.
2. Download or clone the project.
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project directory:

   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   POINTS_FILE=points.json
   ```

   `POINTS_FILE` is optional. If omitted, the bot stores scores in `points.json`.

6. Create a Discord application and bot in the Discord Developer Portal.
7. Enable the Message Content Intent for the bot.
8. Invite the bot to your server with permission to read messages and send messages.

## Use

Start the bot with:

```bash
python main.py
```

Use these commands in Discord:

```text
!points
```

Shows the current user's score.

```text
!give-points <amount>
```

Adds a positive whole number of points to the current user's score.

Example:

```text
!give-points 2
```

```text
!remove-points <amount>
```

Removes points from the current user's score. Scores cannot become negative.

Example:

```text
!remove-points 1
```

The bot saves scores by Discord user ID in the JSON file configured by `POINTS_FILE`. Invalid, missing, or non-positive amounts receive an explanatory error message.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/50c17f02-f3e3-4579-a13b-1a6894c9cfbd?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=50c17f02-f3e3-4579-a13b-1a6894c9cfbd
