import json

import requests
from bs4 import BeautifulSoup

try:
    # 질병코드 질병증상 질병 영향곳 의료비지원여부 필요여부 코드
    export = []
    for idx in range(1, 114):
        print(idx)
        URL = f"https://helpline.kdca.go.kr/cdchelp/ph/rdiz/selectRdizInfList.do?menu=A0100&pageIndex={idx}&fixRdizInfTab=&rdizCd=&schKor=&schEng=&schCcd=&schGuBun=dizNm&schText=&schSort=kcdCd&schOrder=desc"
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "rowT dic_listT"})
        tbody = table.find("tbody")

        for i in tbody.find_all("tr"):
            code = (
                str(i.find_all("td")[1].find("a"))
                .replace(
                    """return false;" title="질환정보 바로가기"><span>질환정보 바로가기</span></a>""",
                    "",
                )
                .replace("""<a href="#" onclick="javascript:fn_moveDetail(""", "")
                .replace("');", "")
                .replace("'", "")
            )
            URLL = f"https://helpline.kdca.go.kr/cdchelp/ph/rdiz/selectRdizInfDetail.do?menu=A0100&pageIndex={idx}&fixRdizInfTab=&rdizCd={code.strip()}&schKor=&schEng=&schCcd=&schGuBun=dizNm&schText=&schSort=kcdCd&schOrder=desc"

            name = (
                str(i.find("td").find("dl").find("dt"))
                .replace("<dt>", "")
                .replace("</p></dt>", "")
                .split("<p>")
            )
            krname = name[0]
            engname = name[1]
            supported = str(i.find("td").find("dl").find_all("li")[2])

            if "지원" in supported:
                supported = True
            else:
                supported = False

            benefit_code = (
                str(i.find("td").find("dl").find_all("li")[4])
                .replace(
                    """<li style="padding-left: 20px !important"><span>산정특례 특정기호 :</span> """,
                    """""",
                )
                .replace("</li>", "")
            )
            kcd_code = (
                str(i.find("td").find("dl").find_all("li")[3])
                .replace("""<li><span>KCD코드 :</span> """, "")
                .replace("</li>", "")
            )

            if i.find("td").find("dl").find_all("li")[1].find("a"):
                benefit_bool = False
            else:
                benefit_bool = True

            resp_temp = requests.get(URLL).text
            soup2 = BeautifulSoup(resp_temp, "html.parser")
            tbody2 = soup2.find("table", {"class": "dic_viewT"}).find("tbody")

            affected = (
                tbody2.find_all("tr")[0]
                .find_all("td")[1]
                .text.replace("체내 : ", "")
                .replace("체외 : ", ",")
                .strip()
                .split(",")
            )
            symptoms = tbody2.find_all("tr")[1].find_all("td")[0].text.split(",")

            new = {
                "id": kcd_code,
                "name": krname,
                "subname": engname,
                "symptoms": symptoms,
                "affected": affected,
                "supported": supported,
                "required": benefit_bool,
                "code": benefit_code,
            }
            export.append(new)

except KeyboardInterrupt:
    pass

finally:
    with open("data.json", "w") as outfile:
        json.dump(export, outfile, ensure_ascii=False)
