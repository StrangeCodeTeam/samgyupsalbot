import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
token = access_token
client = discord.Client()
import os

@client.event
async def on_ready():
    print("준비완료")
    print(client.user)
    print("==========")
    await bt(['~help, ~도움'])
async def bt(games):
  await client.wait_until_ready()
  while not client.is_closed():
      for g in games:
          await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
          await asyncio.sleep(2.5) 
@client.event
async def on_message(message):
    user = message.author
    
    if message.content == "~help" or message.content == "~도움":
        embed1 = discord.Embed(title="SamGyupSal", description="삼겹살 봇은 StrangeCode와 함께합니다", color=0x62c1cc)
        embed1.add_field(name="BASIC", value="`~삼겹살봇`,`~초대`,`~유튜브`,`~청소`", inline=False)
        embed1.set_footer(text="With StrangeCode")
        embed1.add_field(name="TIME", value="`아직 이 기능은 지원하지 않습니다`", inline=False)
        embed1.add_field(name="GAME", value="`아직 이 기능은 지원하지 않습니다`", inline=False)
        await message.channel.send(embed=embed1)        
    
    if message.content == "~삼겹살봇":
        await message.channel.send(f"{message.author.mention}, 개인 DM이 전송되었습니다.")
        await message.author.send("``` 안녕하십니까 삼겹살봇 입니다. ~help를 통해 명령어를 확인하시고 이용해 주세요. 삼겹살봇은 STRANGE CODE에서 개발 중인 봇으로 현재 개발 초기 단계에 있으며 오픈소스 봇 입니다 ```")
    
    if message.content == "~초대":
        embed2 = discord.Embed(title="삼겹살 봇 초대 링크", description="https://discord.com/api/oauth2/authorize?client_id=908528639023394827&permissions=0&scope=bot", color=0x62c1cc)
        await message.channel.send(embed=embed2)

    if message.content.startswith("~유튜브"):
        keyword = message.content.replace("~유튜브", "")
        url = f"https://www.youtube.com/results?search_query={keyword}"

        msg = await message.channel.send(embed=discord.Embed(title="검색중입니다!\n아주 쬐끔 시간이 걸릴 수 있습니다",
                                                         description=f"[ {message.author.mention} ]", color=0xFF9900))

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()

        video_info = soup.find("a", attrs={"id": "video-title"})
        title = video_info.get("title")
        visit = video_info.get("aria-label").split(" ")[-1]
        href = video_info.get("href")

        await msg.delete()
        await message.channel.send(f"**{keyword} 의 검색 결과입니다.**\n\n{title} | 조회수 {visit}\nhttp://youtube.com{href}")


    if message.content.startswith("~청소"):
        number = int(message.content.split(" ")[1])
        await message.delete()
        await message.channel.purge(limit=number)
        await message.channel.send(f"{number}개의 메세지 삭제 완료!")
   
access_token = os.environ["BOT_token"]        
client.run(access_token)
