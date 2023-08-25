import requests, json

# connect api
word = input("請輸入要查詢的國字：")
url = "https://www.moedict.tw/uni/{}".format(word)
response = requests.get(url)
response.raise_for_status()

# download datas
# typecasting：str to dict
datas = json.loads(response.text)

# 1st 層：顯示查詢字詞、部首、筆畫
print("查詢字詞：", datas["title"])
if "radical" in datas["heteronyms"]:
    print("部首：{}，筆畫：{}".format(datas["radical"], datas["stroke_count"]))

# 2nd 層：顯示注音、羅馬拼音、漢語拼音
for i in range(len(datas["heteronyms"])):
    print("注音：{}，羅馬拼音：{}，漢語拼音：{}".format(
        datas["heteronyms"][i]["bopomofo"].replace("（語音）", "".lstrip()),
        datas["heteronyms"][i]["bopomofo2"].replace("（語音）", "".lstrip()),
        datas["heteronyms"][i]["pinyin"].replace("（語音）", "".lstrip())
    ))

    print("----------------------------------------------------------------------------")

    # 3rd 層：顯示解釋、詞性、範例、引用、連結
    for j in range(len(datas["heteronyms"][i]["definitions"])):
        print("解釋：{}".format(datas["heteronyms"][i]["definitions"][j]["def"]))
        if "type" in datas["heteronyms"][i]["definitions"][j]:
            print("詞性：<{}詞>".format(datas["heteronyms"][i]["definitions"][j]["type"]))
        if "example" in datas["heteronyms"][i]["definitions"][j]:
            print("範例：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["example"])))
        if "quote" in datas["heteronyms"][i]["definitions"][j]:
            print("引用：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["quote"])))
        if "link" in datas["heteronyms"][i]["definitions"][j]:
            print("連結：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["link"])))

        # 3rd 層分隔線
        if j < len(datas["heteronyms"][i]["definitions"]) - 1:
            print("----------------------------------------------------------------------------")
    
    # 2nd 層分隔線
    if i < len(datas["heteronyms"]) - 1:
        print("============================================================================")
    
