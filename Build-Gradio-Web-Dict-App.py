import requests, json
import gradio as gr

# connect api
def moedict(word):
    re_str = ""
    url = "https://www.moedict.tw/uni/{}".format(word)
    response = requests.get(url)
    response.raise_for_status()

    # download datas
    # typecasting：str to dict
    datas = json.loads(response.text)

    # 1st 層：顯示查詢字詞、部首、筆畫
    re_str += "【" + datas["title"] + "】" + "\n"
    if "radical" in datas["heteronyms"]:
        re_str = "部首：{}，筆畫：{}".format(datas["radical"], datas["stroke_count"]) + "\n"

    # 2nd 層：顯示注音、羅馬拼音、漢語拼音
    for i in range(len(datas["heteronyms"])):
        re_str += "注音：{}，羅馬拼音：{}，漢語拼音：{}".format(
            datas["heteronyms"][i]["bopomofo"].replace("（語音）", "".lstrip()),
            datas["heteronyms"][i]["bopomofo2"].replace("（語音）", "".lstrip()),
            datas["heteronyms"][i]["pinyin"].replace("（語音）", "".lstrip())
        ) + "\n"

        re_str += "----------------------------------------------------------------------------\n"

        # 3rd 層：顯示解釋、詞性、範例、引用、連結
        for j in range(len(datas["heteronyms"][i]["definitions"])):
            re_str += "解釋：{}".format(datas["heteronyms"][i]["definitions"][j]["def"]) + "\n"
            if "type" in datas["heteronyms"][i]["definitions"][j]:
                re_str += "詞性：<{}詞>".format(datas["heteronyms"][i]["definitions"][j]["type"]) + "\n"
            if "example" in datas["heteronyms"][i]["definitions"][j]:
                re_str += "範例：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["example"])) + "\n"
            if "quote" in datas["heteronyms"][i]["definitions"][j]:
                re_str += "引用：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["quote"])) + "\n"
            if "link" in datas["heteronyms"][i]["definitions"][j]:
                re_str += "連結：{}".format(" | ".join(datas["heteronyms"][i]["definitions"][j]["link"])) + "\n"

            # 3rd 層分隔線
            if j < len(datas["heteronyms"][i]["definitions"]) - 1:
                re_str += "----------------------------------------------------------------------------\n"
        
        # 2nd 層分隔線
        if i < len(datas["heteronyms"]) - 1:
            re_str += "============================================================================\n"
    return re_str

# create Gradio connection object
grobj = gr.Interface(fn = moedict,
                     inputs = gr.inputs.Textbox(),
                     outputs = gr.outputs.Textbox())
grobj.launch()
      
