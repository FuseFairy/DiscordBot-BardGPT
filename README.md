# DiscordBot-BardGPT
> ## Using Google Bard Chat AI on discord bot.

## Update
> ### 2023/6/5 : Use SQLite storage of individual cookies so it doesn't reset when the bot restarts, it can also be exported for later use.

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
   
 * `!bardunload [file_name_in_cogs_folder]`: Disable command from the specified file.
 * `!bardload [file_name_in_cogs_folder]`: Enable the command from the specified file.
 
   ![load & unload](https://i.imgur.com/opjDBn9.png)
  
 * `!bardclean`: Empty discord_bot.log file.
 * `!bardgetLog`: Get discord_bot.log file. Real-time tracking of the bot's operating status.
   
   ![getLog](https://i.imgur.com/LHX4yWV.png)
 
 * `!bardgetdb`: Export Bard_id.db file
   
    ![getdb](https://i.imgur.com/fgW7rPO.png)
   
 * `!bardupload [__Secure-1PSID]`: Set default __Secure-1PSID.
 
   ![upload](https://i.imgur.com/ef2oPTh.png)
   
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
   * Go to [https://bard.google.com/](https://bard.google.com/)
   * F12 for console
   * Session: Go to Application → Cookies → `__Secure-1PSID`. Copy the value of that cookie.

4. Start run your bot, hosted locally or on a server.

   -> Recommended Free Servers: [fly.io](https://fly.io/)

## Credits
* Bard - [https://github.com/acheong08/Bard](https://github.com/acheong08/Bard)
* other - [https://github.com/Zero6992/chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)

## Contributors

This project exists thanks to all the people who contribute.

 <a href="https://github.com/FuseFairy/DiscordBot-BradGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=FuseFairy/DiscordBot-BardGPT" />
 </a>
