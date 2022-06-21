import requests
from PIL import Image,ImageDraw,ImageFont
import urllib
from io import BytesIO

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
large_font = ImageFont.truetype('./font/setofont.ttf', 40)
font = ImageFont.truetype('./font/setofont.ttf', 30)
medium_font = ImageFont.truetype('./font/setofont.ttf', 26) 
small_font = ImageFont.truetype('./font/setofont.ttf', 22)
# large_font = ImageFont.truetype('../font/setofont.ttf', 40)
# font = ImageFont.truetype('../font/setofont.ttf', 30)
# medium_font = ImageFont.truetype('../font/setofont.ttf', 26) 
# small_font = ImageFont.truetype('../font/setofont.ttf', 22)

cast = {
    "c_cast":2,
    "q_cast":0,
    "e_cast":1,
    "x_cast":3,
}

def battle_generate_image(data):
    im = Image.new("RGB",(1000,1000),(255,255,255))
    avpos = 0
    for i in data:
        req = urllib.request.Request(i["image"] ,headers=header)
        with urllib.request.urlopen(req) as response:
            img = response.read()
        avatar = Image.open(BytesIO(img))
        avatar = avatar.resize((180,180))
        imdraw = ImageDraw.Draw(im)
        imdraw.rectangle((0,avpos,200,avpos+200),fill=(45, 52, 54,1))
        im.paste(avatar,(10,avpos+10))
        if i["haswin"]:
            imdraw.rectangle((200,avpos,1000,avpos+200),fill=(0, 184, 148,1))
        else:
            imdraw.rectangle((200,avpos,1000,avpos+200),fill=(214, 48, 49,1))
        kill = str(i["stats"]["kills"])
        death = str(i["stats"]["deaths"])
        assists = str(i["stats"]["assists"])
        hs = str(i["hs"])
        adr = str(i["adr"])
        kd = str(i["kd"])
        round = str(i["round"]["win"]) + "/" + str(i["round"]["lost"])
        imdraw.text((230,avpos+50), "round\n" + round,fill=(255,255,255,255),font=large_font)
        imdraw.text((390,avpos+50), "kd\n" + kd,fill=(255,255,255,255),font=large_font)
        imdraw.text((490,avpos+50), "K\n" + kill,fill=(255,255,255,255),font=large_font)
        imdraw.text((590,avpos+50), "D\n" + death,fill=(255,255,255,255),font=large_font)
        imdraw.text((690,avpos+50), "A\n" + assists,fill=(255,255,255,255),font=large_font)
        imdraw.text((790,avpos+50), "hs\n" + hs,fill=(255,255,255,255),font=large_font)
        imdraw.text((890,avpos+50), "adr\n" + adr,fill=(255,255,255,255),font=large_font)
        avpos+=200
    buffer = BytesIO()
    im.save(buffer, 'png')
    buffer.seek(0)
    return buffer
    
def one_battle_generate_image(data):
    igd = requests.get("https://valorant-api.com/v1/agents",headers=header).json()

    def get_agent(name):
        for i in igd["data"]:
            if i["displayName"] == name:
                return i["abilities"]
    im = Image.new("RGB",(1000,1000),(255,255,255))
    imdraw = ImageDraw.Draw(im)
    avpos = 0
    imdraw.rectangle((0,0,500,1000),fill=(214, 48, 49,1))
    imdraw.rectangle((500,0,1000,1000),fill=(0, 184, 148,1))
    
    for i in data["red"]:
        req = urllib.request.Request(i["image"] ,headers=header)
        pimage = get_agent(i["character"])
        with urllib.request.urlopen(req) as response:
            img = response.read()
        avatar = Image.open(BytesIO(img))
        avatar = avatar.resize((100,100))
        im.paste(avatar,(0,avpos))
        kill = str(i["stats"]["kills"])
        death = str(i["stats"]["deaths"])
        assists = str(i["stats"]["assists"])
        hs = str(i["hs"])
        adr = str(i["adr"])
        kd = str(i["kd"])
        imdraw.text((110,avpos+10), i["name"],font=medium_font)
        imdraw.text((110,avpos+50), "kd\n" + kd,fill=(255,255,255,255),font=font)
        imdraw.text((210,avpos+50), "K\n" + kill,fill=(255,255,255,255),font=font)
        imdraw.text((270,avpos+50), "D\n" + death,fill=(255,255,255,255),font=font)
        imdraw.text((330,avpos+50), "A\n" + assists,fill=(255,255,255,255),font=font)
        imdraw.text((380,avpos+50), "hs\n" + hs,fill=(255,255,255,255),font=font)
        imdraw.text((430,avpos+50), "adr\n" + adr,fill=(255,255,255,255),font=font)
        imdraw.rectangle((0,avpos+190,500,avpos+200),fill=(45, 52, 54,1))
        ppos = 0
        for j in i["ability"]:
            img = pimage[int(cast[j])]["displayIcon"]
            req = urllib.request.Request(img ,headers=header)
            with urllib.request.urlopen(req) as response:
                img = response.read()
            img = Image.open(BytesIO(img))
            img = img.resize((50,50))
            im.paste(img,(ppos+20,avpos+120))
            imdraw.text((ppos+80,avpos+120), str(i["ability"][j]),fill=(255,255,255,255),font=font)
            ppos+=100


        avpos+=200
    avpos = 0
    for i in data["blue"]:
        req = urllib.request.Request(i["image"] ,headers=header)
        pimage = get_agent(i["character"])
        with urllib.request.urlopen(req) as response:
            img = response.read()
        avatar = Image.open(BytesIO(img))
        avatar = avatar.resize((100,100))
        im.paste(avatar,(500,avpos))
        kill = str(i["stats"]["kills"])
        death = str(i["stats"]["deaths"])
        assists = str(i["stats"]["assists"])
        hs = str(i["hs"])
        adr = str(i["adr"])
        kd = str(i["kd"])
        imdraw.text((610,avpos+10), i["name"],font=medium_font)
        imdraw.text((610,avpos+50), "kd\n" + kd,fill=(255,255,255,255),font=font)
        imdraw.text((710,avpos+50), "K\n" + kill,fill=(255,255,255,255),font=font)
        imdraw.text((770,avpos+50), "D\n" + death,fill=(255,255,255,255),font=font)
        imdraw.text((830,avpos+50), "A\n" + assists,fill=(255,255,255,255),font=font)
        imdraw.text((880,avpos+50), "hs\n" + hs,fill=(255,255,255,255),font=font)
        imdraw.text((930,avpos+50), "adr\n" + adr,fill=(255,255,255,255),font=font)
        imdraw.rectangle((500,avpos+190,1000,avpos+200),fill=(45, 52, 54,1))
        ppos = 500
        for j in i["ability"]:
            img = pimage[int(cast[j])]["displayIcon"]
            req = urllib.request.Request(img ,headers=header)
            with urllib.request.urlopen(req) as response:
                img = response.read()
            img = Image.open(BytesIO(img))
            img = img.resize((50,50))
            im.paste(img,(ppos+20,avpos+120))
            imdraw.text((ppos+80,avpos+120), str(i["ability"][j]),fill=(255,255,255,255),font=font)
            ppos+=100


        avpos+=200
    imdraw.rectangle((490,0,500,1000),fill=(45, 52, 54,1))
    #im.show()
    buffer = BytesIO()
    im.save(buffer, 'png')
    buffer.seek(0)
    return buffer


def get_placer_battle_info(player,tag,place):
    """
    hs = head/body+head*100%
    adr = int(damage/round)
    """
    
    data = requests.get(f"https://api.henrikdev.xyz/valorant/v3/matches/{place}/{player}/{tag}",timeout=10,headers=header)
    if data.status_code !=200:
        raise Exception("not found player data")
    data = data.json()
    pdlist = []
    for i in data["data"]:
        pdata = {}
        pdata["mode"] = i["metadata"]["mode"]
        # 玩家資料
        players = i["players"]["all_players"]
        for j in players:
            if j["name"] == player:
                pdata["stats"] = j["stats"]
                pdata["team"] = j["team"]
                pdata["damage"] = j["damage_made"]
                pdata["image"] = j["assets"]["agent"]["small"]
                break
        # 地區資料
        pdata["map"] = i["metadata"]["map"]
        if i["teams"][pdata["team"].lower()]["rounds_won"] > i["teams"][pdata["team"].lower()]["rounds_lost"]:
            pdata["haswin"] = True
        else:
            pdata["haswin"] = False
        pdata["round"] = {
            "win":i["teams"][pdata["team"].lower()]["rounds_won"],
            "lost":i["teams"][pdata["team"].lower()]["rounds_lost"],
            "rounds":i["metadata"]["rounds_played"]
        }
        if pdata["stats"]["headshots"]+pdata["stats"]["bodyshots"] == 0:
            pdata["hs"] = "0%"
        else:
            pdata["hs"] = str(int(pdata["stats"]["headshots"]*100/(pdata["stats"]["headshots"]+pdata["stats"]["bodyshots"]))) + "%"
        pdata["adr"] = str(int(pdata["damage"]/pdata["round"]["rounds"]))
        pdata["kd"] = str(round(pdata["stats"]["kills"]/pdata["stats"]["deaths"],2))
        pdlist.append(pdata)
    return pdlist

def get_one_battle(player,tag,place,ct):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    data = requests.get(f"https://api.henrikdev.xyz/valorant/v3/matches/{place}/{player}/{tag}",timeout=10,headers=header)
    if data.status_code !=200:
        raise Exception("not found player data")
    data = data.json()
    pdata = {}
    pdata["mode"] = data["data"][ct]["metadata"]["mode"]
    pdata["rounds"] = data["data"][ct]["metadata"]["rounds_played"]
    pdata["red"] = []
    pdata["blue"] = []
    for i in data["data"][ct]["players"]["red"]:
        rpdata = {}
        rpdata["name"] = i["name"]
        rpdata["stats"] = i["stats"]
        rpdata["damage"] = i["damage_made"]
        rpdata["image"] = i["assets"]["agent"]["small"]
        rpdata["ability"] = i["ability_casts"]
        rpdata["character"] = i["character"]
        if rpdata["stats"]["headshots"]+rpdata["stats"]["bodyshots"] == 0:
            rpdata["hs"] = "0%"
        else:
            rpdata["hs"] = str(int(rpdata["stats"]["headshots"]*100/(rpdata["stats"]["headshots"]+rpdata["stats"]["bodyshots"]))) + "%"
        rpdata["adr"] = str(int(rpdata["damage"]/pdata["rounds"]))
        rpdata["kd"] = str(round(rpdata["stats"]["kills"]/rpdata["stats"]["deaths"],2))
        pdata["red"].append(rpdata)
    for i in data["data"][ct]["players"]["blue"]:
        bpdata = {}
        bpdata["name"] = i["name"]
        bpdata["stats"] = i["stats"]
        bpdata["damage"] = i["damage_made"]
        bpdata["image"] = i["assets"]["agent"]["small"]
        bpdata["ability"] = i["ability_casts"]
        bpdata["character"] = i["character"]
        if bpdata["stats"]["headshots"]+bpdata["stats"]["bodyshots"] == 0:
            bpdata["hs"] = "0%"
        else:
            bpdata["hs"] = str(int(bpdata["stats"]["headshots"]*100/(bpdata["stats"]["headshots"]+bpdata["stats"]["bodyshots"]))) + "%"
        bpdata["adr"] = str(int(bpdata["damage"]/pdata["rounds"]))
        bpdata["kd"] = str(round(bpdata["stats"]["kills"]/bpdata["stats"]["deaths"],2))
        pdata["blue"].append(bpdata)
    return pdata
            



if __name__ == '__main__':
    one_battle_generate_image(get_one_battle("phillychi3","4353","ap",0))
    #print(get_placer_battle_info("phillychi3","4353","ap"))
    #print(get_one_battle("phillychi3","4353","ap",0))
    