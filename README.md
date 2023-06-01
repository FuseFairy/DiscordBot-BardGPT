# DiscordBot-BardGPT
> ## Using Google Bard Chat AI on discord bot.
   
## Features

<details>
   <summary>
   
   ### Slash command

   </summary>
   
> ### will create a personal conversation for each user.
   
* cookies setting(use personal Google Bard Cookies): `/bard_cookies [choice]`
  
  ![setting](https://i.imgur.com/Q5HS6SW.png)
  
   
* Bard: `/bard [message]`
  
  >**Warning** : Only up to 10 pictures will be displayed.

  ![Bard](https://i.imgur.com/cgIMRvw.png)
  
</details>

<details>
   <summary>
   
   ### Mention bot

   </summary>

> ### same feature as the slash command, but this will reply all user messages.

* Same as use `/bard`,

  ![mention1](https://i.imgur.com/0jAhbgY.png)

</details>

<details>
   <summary>
   
   ### Prefix command (available only to bot owner)

   </summary>
 
 > ### bot owner setting.
   
 * `!unload [file_name_in_cogs_folder]`: Disable command from the specified file.
 * `!load [file_name_in_cogs_folder]`: Enable the command from the specified file.
 
   ![load & unload](https://i.imgur.com/opjDBn9.png)
  
 * `!clean`: Empty discord_bot.log file.
 * `!getLog`: Get discord_bot.log file. Real-time tracking of the bot's operating status.
   
   ![getLog](https://i.imgur.com/LHX4yWV.png)
 
 * `!upload [.txt_file]`: Because Cookies will expire, so this command can set new Cookies directly. You just need to copy bing cookies and past,                           the Cookies will auto convert to .txt file.
 
   ![upload](https://i.imgur.com/UN1Ac7N.png)
</details>

## Install
```
pip install -r requirements.txt
```

## Usage
1. Rename the file`.env.dev`to`.env`, then open it and edit it. If you don't want a limit channel to mention a bot, you don't need to set up a MENTION_CHANNEL_ID, just leave it blank.
   ```
   DISCORD_BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   MENTION_CHANNEL_ID=123456789
   ```
   
2. Get Google Bard authentication.
   * Install the cookie editor extension for Chrome or Firefox.
   * Go to [https://bard.google.com/](https://bard.google.com/)
   * Click "Export" on the bottom right.
   * Paste your cookies into a file `cookies.json`

4. Start run your bot, hosted locally or on a server.

   -> Recommended Free Servers: [fly.io](https://fly.io/)

## Credits
* Bard - [https://github.com/acheong08/Bard](https://github.com/acheong08/Bard)
* other - [https://github.com/Zero6992/chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)
