# Raspberry Pi Gate

**Learn to install a Raspberry Pi 5 server at home:**  
[![image](https://github.com/user-attachments/assets/e49c6165-4828-4561-9a95-c49be9e7771e)](https://youtu.be/dMZApM_3itA)  

- Learn how to set up your Pi 5 at home with a DDNS for a "static" IP:  
  [https://github.com/EloiStree/HelloEloiTeachingVideo/issues/127](https://github.com/EloiStree/HelloEloiTeachingVideo/issues/127)  

- Learn more about using the Pi 5 as an integer server:  
  [https://www.youtube.com/@EloiTeaching/search?query=🍺.io](https://www.youtube.com/@EloiTeaching/search?query=🍺.io)  


 Code on my Pi 5:   
- **Twitch Bot**: [GitHub Repository](https://github.com/EloiStree/2024_12_11_HelloMegaMaskTwitchBot)   
- **Discord Bot**: [GitHub Repository](https://github.com/EloiStree/2024_12_07_HelloMegaMaskDiscordBot)  
- **NoIP DDNS**: [Github Repository](https://github.com/EloiStree/2024_12_11_NoIpUpdateFromPiPython)  

I have several Raspberry Pi at home that are not used and that could be used.

You will find here some code in python that I can trigger on my Pi to allows relay message.

The idea here is to avoir on server to received all the message of the community on a single device.

Some step: https://github.com/EloiStree/HelloRustBending/issues/37

`sudo apt install git`


```
sudo apt update
sudo apt install python3 python3-venv python3-pip -y

git config --global user.email "name@gmail.com"
git config --global user.name "Name"

```



Launch Script at start:
- https://youtu.be/DUGZC-tNm2w?t=95
```

chmod +x yourscript.py
cd /lib/systemd/system
sudo touch yourscript.service
sudo nano yourscript.service
which python3
whoami
```

[Unit]
Description=Bot Discord
After=network.target

[Service]
ExecStart=/usr/bin/python3 /git/discord_bot/RunBot.py
WorkingDirectory=/git/discord_bot/
StandardOutput=inherit
StandardError=inherit
Restart=always

[Install]
WantedBy=multi-user.target



sudo systemctl enable discord_bot.service
sudo systemctl start discord_bot.service



An other user dependant: 

`nano ~/.bashrc`

```
# https://github.com/EloiStree/2024_12_07_HelloMegaMaskDiscordBot
@reboot /usr/bin/python3 /git/discord_bot/RunBot.py &
# https://github.com/EloiStree/2024_12_11_HelloMegaMaskTwitchBot
@reboot /usr/bin/python3 /git/twitch_bot/RunBot.py &

```
```
``
``
``
