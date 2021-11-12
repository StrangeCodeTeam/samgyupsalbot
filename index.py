import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import *
from selenium import webdriver
import datetime
import time
import discord, asyncio, openpyxl, datetime
token = 
client = discord.Client()

@client.event
async def on_ready():
    print("준비완료")
    print(client.user)
    print("==========")
    await bt(['~help, ~도움', '~가입으로 가입후 이용'])
async def bt(games):
  await client.wait_until_ready()
  while not client.is_closed():
      for g in games:
          await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
          await asyncio.sleep(2.5) 
@client.event
async def on_message(message):
    def member():
        file = openpyxl.load_workbook("memberlist.xlsx")
        wb = file.active

        for i in range(1, 101):
            return wb["A" + str(i)].value == str(message.author.id)
    def check2(reaction, user):
        return user == message.author and str(reaction.emoji) in reactions
    user = message.author

    
    
    if message.content == "~가입":
        file = openpyxl.load_workbook("memberlist.xlsx")
        wb = file.active

        for i in range(1, 101):
            if wb["A" + str(i)].value == str(message.author.id):
                await message.channel.send("이미 가입된 사용자입니다.")
                break

            elif wb["A" + str(i)].value == None:
                embed = discord.Embed(title="회원 가입을 진행합니다", description="아래의 이모지에 반응하세요.")
                msg = await message.channel.send(embed=embed)

                await msg.add_reaction(yes)
                await msg.add_reaction(no)

                try:
                    reaction, user = await client.wait_for("reaction_add", check=check2, timeout=15)

                    if str(reaction.emoji) == yes:
                        await msg.delete()                

                        wb["A" + str(i)].value = str(message.author.id)
                        wb["B" + str(i)].value = str(message.author)
                        wb["C" + str(i)].value = str(datetime.datetime.now().replace(microsecond=0))
                        await message.channel.send("가입이 완료되었습니다.")
                        break
            
                    elif str(reaction.emoji) == no:
                        await msg.delete()
                        await message.channel.send("취소 되었습니다.")
                        break

                except asyncio.exceptions.TimeoutError:
                    await msg.delete()
                    await message.channel.send("시간이 초과되었습니다")
                    break

        file.save("memberlist.xlsx")


    if message.content == "~탈퇴":
        file = openpyxl.load_workbook("memberlist.xlsx")
        wb = file.active
    
        for i in range(1, 101):
            if wb["A" + str(i)].value == str(message.author.id):
                embed = discord.Embed(title="탈퇴를 진행합니다", description="아래의 이모지에 반응하세요.")
                msg = await message.channel.send(embed=embed)

                await msg.add_reaction(yes)
                await msg.add_reaction(no)

                try:
                    reaction, user = await client.wait_for("reaction_add", check=check2, timeout=15)
                
                    if str(reaction.emoji) == yes:
                        await msg.delete()
                        wb.delete_rows(i)
                        await message.channel.send("탈퇴처리가 정상적으로 완료되었습니다.")
                        break

                    elif str(reaction.emoji) == no:
                        await msg.delete()
                        await message.channel.send("취소 되었습니다.")
                        break

                except asyncio.exceptions.TimeoutError:
                    await msg.delete()
                    await message.channel.send("시간이 초과되었습니다")
                    break

            elif wb["A" + str(i)].value == None:
                await message.channel.send("가입하지 않은 사용자입니다.")
                break

        file.save("memberlist.xlsx")


    if message.content == "안녕":
        if member():
            await message.channel.send("안녕하세요!")
        
        else:
            await message.channel.send("당신은 회원이 아닙니다.")    
    
    if message.content == "~help" or message.content == "~도움":
        if member():
            embed1 = discord.Embed(title="SamGyupSal", description="삼겹살 봇은 StrangeCode와 함께합니다", color=0x62c1cc)
            embed1.add_field(name="BASIC", value="`~삼겹살봇`,`~초대`,`~유튜브`,`~청소`", inline=False)
            embed1.set_footer(text="With StrangeCode")
            await message.channel.send(embed=embed1)
        else:
            await message.channel.send("가입 후 이용하시길 바랍니다")
       
    
    if message.content == "~삼겹살봇":
        if member():
            await message.channel.send(f"{message.author.mention}, 개인 DM이 전송되었습니다.")
            await message.author.send("``` 안녕하십니까 삼겹살봇 입니다. ~help를 통해 명령어를 확인하시고 이용해 주세요. 삼겹살봇은 STRANGE CODE에서 개발 중인 봇으로 현재 개발 초기 단계에 있으며 오픈소스 봇 입니다 ```")
        else:
            await message.channel.send("가입 후 이용하시길 바랍니다")
    
    if message.content == "~초대":
        if member():
            embed2 = discord.Embed(title="삼겹살 봇 초대 링크", description="https://discord.com/api/oauth2/authorize?client_id=908528639023394827&permissions=0&scope=bot", color=0x62c1cc)
            await message.channel.send(embed=embed2)
        else:
            await message.channel.send("가입 후 이용하시길 바랍니다")

    if message.content.startswith("~유튜브"):
        if member():
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
        else:
            await message.channel.send("가입 후 이용하시길 바랍니다")

    if message.content.startswith("~청소"):
        if member():
            number = int(message.content.split(" ")[1])
            await message.delete()
            await message.channel.purge(limit=number)
            
            embed2 = discord.Embed(title=f"{number}개의 메세지 삭제 완료!", color=0x62c1cc)
            await message.channel.send(embed=embed2)
        else:
            await message.channel.send("가입 후 이용하시길 바랍니다")


yes = "⭕"
no = "❌"
reactions = [yes, no]

O = "▶"
X = "◀"
OX = [O, X]




client.run(token)
