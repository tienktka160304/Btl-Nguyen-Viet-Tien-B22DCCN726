from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Truy cập vào trang web
from ob import Player
from ob import Player_Manager
from ob import Squad
from ob import Squad_Manager

player_manager=Player_Manager()
squad_manager=Squad_Manager()


def validdata(n):
    if n=='': return "N/a"
    return float(n)

def getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName):
    resultPlayerData=[]
    resultSquadData=[]
    driver.get(url)
    try:
        time.sleep(3)

        # Lấy toàn bộ nội dung HTML sau khi trang đã tải xong
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        #player
        div_stats = soup.find('div', id=idPlayerTable)
        table = div_stats.find('table')
        tbody = table.find('tbody')
        tr_list=tbody.find_all('tr')

        miss=25
        for ind,i in enumerate(tr_list):    
            if(ind==miss):
                    miss=miss+25+1
                    continue
            arr=[]
            for index, value in enumerate(i.find_all('td')):
                if(index==1):
                    a=value.find('a')
                    if(a is not None):
                        span1=a.find('span', recursive=False)
                        span2=span1.find("span")
                        span2.extract()
                s=value.text.strip()

                if index>=4 and index!=lengthPlayerData:
                    s=s.replace(",","")
                    s=validdata(s)
                arr.append(s)
            arr.pop() # Loại bỏ giá trị không liên quan
            resultPlayerData.append(arr)

        #squad
        table = soup.find('table', id=idSquadTable)
        tbody = table.find('tbody')
        tr_list=tbody.find_all('tr')

        miss=25
        for ind,i in enumerate(tr_list):    
            arr=[]
            th=i.find("th")
            arr.append(th.text.strip())
            for index, value in enumerate(i.find_all('td')):
                s=value.text.strip()
                if index!=0:
                    s=s.replace(",","")
                    s=validdata(s)
                arr.append(s)
            resultSquadData.append(arr)
    except :
        print("Something went wrong")
    finally:
        print("Finish Page "+DataName)
    return [resultPlayerData,resultSquadData]



#start get Player and Team*******************************************************************************************************

url = 'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_playing_time"
lengthPlayerData=28
idSquadTable="stats_squads_playing_time_for"
# lengthSquadData=35
DataName="Playing Time"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s==None:
        new_s=Squad(*i[0:3])
        new_s.setPlayingTimeDetail(i[8:11],i[11:14],i[14:17],i[19:21])
        squad_manager.add_Squad(new_s)

#Player data
for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    s=squad_manager.findSquadByName(i[3])
    if p==None:
        new_p=Player(i[0],i[1],i[2],i[3],i[4])
        new_p.setPlayingTimeDetail(i[11:14],i[14:17],i[17:20],i[23:25])
        player_manager.add_Player(new_p)
        s.players.append(new_p)

#End get Player and Team***************************************************************************************************



url="https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats"
idPlayerTable="div_stats_standard"
lengthPlayerData=35
idSquadTable="stats_squads_standard_for"
lengthSquadData=32
DataName="Standard"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.poss=i[4]
        s.setPlaying_time(i[4:7])
        s.setPerformance([i[11],i[12],i[9],i[14],i[15]])
        s.setExpected(i[16:19])
        s.setProgression(i[20:22])
        s.setPer90(i[22:])
#player data
for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setPlaying_time(i[6:9])
        p.setPerformance([i[13],i[14],i[11],i[16],i[17]])
        p.setExpected(i[18:21])
        p.setProgression(i[22:25])
        p.setPer90(i[25:])


  

url = 'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_keeper"
lengthPlayerData=25
idSquadTable="stats_squads_keeper_for"
lengthSquadData=35
DataName="keeper"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setGoalkeeping(i[10:20],i[20:])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setGoalkeeping(i[6:16],i[16:])
        

url = 'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_shooting"
lengthPlayerData=24
idSquadTable="stats_squads_shooting_for"
lengthSquadData=35
DataName="Shooting"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setShooting(i[7:19],i[19:])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setShooting(i[3:15],i[15:])
        




url = 'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_passing"
lengthPlayerData=30
idSquadTable="stats_squads_passing_for"
lengthSquadData=35
DataName="Passing"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setPassing(i[7:12],i[12:15],i[15:18],i[18:21],i[21:])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setPassing(i[3:8],i[8:11],i[11:14],i[14:17],i[17:])



url = 'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_passing_types"
lengthPlayerData=22
idSquadTable="stats_squads_passing_types_for"
lengthSquadData=35
DataName="Passing Types"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setPassTypes(i[8:16],i[16:19],i[19:22])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setPassTypes(i[4:12],i[12:15],i[15:])





url = 'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_gca"
lengthPlayerData=23
idSquadTable="stats_squads_gca_for"
lengthSquadData=35
DataName="Goal and short creation"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setGoalShotCreation(i[7:9],i[9:15],i[15:17],i[17:23])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setGoalShotCreation(i[3:5],i[5:11],i[11:13],i[13:])





url = 'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_defense"
lengthPlayerData=23
idSquadTable="stats_squads_defense_for"
lengthSquadData=35
DataName="Defensive"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setDefensiveActions(i[7:12],i[12:16],i[16:23])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setDefensiveActions(i[3:8],i[8:12],i[12:])





url = 'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_possession"
lengthPlayerData=29
idSquadTable="stats_squads_possession_for"
lengthSquadData=35
DataName="Possession"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setPossession(i[7:14],i[14:19],i[19:27],i[27:29])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setPossession(i[4:11],i[11:16],i[16:24],i[24:26])






url = 'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
idPlayerTable="div_stats_misc"
lengthPlayerData=23
idSquadTable="stats_squads_misc_for"
lengthSquadData=35
DataName="Miscellaneous Stats"
list_player_result,list_squad_result=getDataFromWeb(url,idPlayerTable,idSquadTable,lengthPlayerData,DataName)

for i in list_player_result:
    p=player_manager.findPlayerByNameandTeam(i[0],i[3])
    if p!=None:
        p.setMiscStats(i[10:14]+i[18:20],i[20:23])
#squad data
for i in list_squad_result:
    s=squad_manager.findSquadByName(i[0])
    if s!=None:
        s.setMiscStats(i[6:10]+i[14:16],i[16:])




print("Number of squad ",len(squad_manager.list_squad))
print("Number of player ",len(player_manager.list_player))
driver.quit()



import pickle

with open("squads.pkl", "wb") as file:
    pickle.dump(squad_manager.list_squad, file)
print("Ghi thành công tất cả player vào file players.pkl và squads.pkl!")



player_manager.filtering()
player_manager.sortingByName()
import csv
from common import header
from common import row
with open('result.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    
    for player in player_manager.list_player:
        r=row(player)
        writer.writerow(r)
print("Ghi thành công vào file result.csv","Exam 1 Success",sep="\n")


import subprocess
# Mở file CSV
subprocess.Popen(["start", r"result.csv"], shell=True)














            
    





