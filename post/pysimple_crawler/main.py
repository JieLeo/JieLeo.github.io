import httpx
from bs4 import BeautifulSoup
import pprint
import json


class Base:
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url
        self.html = " "
        self.info_list = []

    def get_html(self):
        try:
            f = open(self.name + ".html", "r", encoding="utf-8")
            self.html = f.read()
            f.close()
        except Exception as e:
            r = httpx.get(self.url)
            f = open(self.name + ".html", "w", encoding="utf-8")
            f.write(r.text)
            f.close
            self.html = r.text

    def get_info(self):
        pass

    def write_info(self):
        with open(self.name + ".csv", "w", encoding="utf-8") as f:
            for row in self.info_list:
                f.write(row)

    def run(self):
        self.get_html()
        self.get_info()
        self.write_info()


class Nju(Base):
    def __init__(self, name, url) -> None:
        super().__init__(name, url)

    def get_info(self):
        soup = BeautifulSoup(self.html, "html.parser")
        for tag in soup.find_all("li", class_="news"):
            self.info_list.append(
                self.url
                + tag.contents[1].contents[0]["href"]
                + ","
                + tag.contents[1].contents[0].get_text()
                + ","
                + tag.contents[3].get_text()
                + "\n"
            )

# if __name__ == "__main__":
#     # r = httpx.get("https://yzb.nju.edu.cn/47840/list.htm")
#     # with open("nju.html", "w", encoding="utf-8") as f:
#     #     print(r.text)
#     #     f.write(r.text)

#     html = ""
#     with open("nju.html", 'r', encoding="utf-8") as f:
#         html = f.read()
#         info_list=[]
#         soup = BeautifulSoup(html, "html.parser")
#         for tag in soup.find_all("li", class_="news"):
#             # print(
#             #     "https://yzb.nju.edu.cn" + tag.contents[1].contents[0]["href"],
#             #     tag.contents[1].contents[0].get_text(),
#             #     tag.contents[3].get_text(),
#             # )
#             info_list.append(
#                 "https://yzb.nju.edu.cn"
#                 +tag.contents[1].contents[0]["href"]
#                 +","
#                 +tag.contents[1].contents[0].get_text()
#                 +","
#                 +tag.contents[3].get_text()
#                 +"\n"
#             )
#         with open("nju.csv",'w',encoding="utf-8") as f:
#             for row in info_list:
#                 f.write(row)


class Njfu(Base):
    def __init__(self, name, url) -> None:
        super().__init__(name, url)

    def write_info(self):
        with open(self.name + ".csv", "w", encoding="utf-8") as f:
            for row in self.info_list:
                f.write(row)

    def get_info(self):
        soup = BeautifulSoup(self.html, "html.parser")
        for tag in soup.find_all("script"):
            if "dataList" in tag.get_text():
                start_index = tag.get_text().find("dataList=") + len("dataList=")
                end_index = tag.get_text.find("var pagesData=")
                info = json.loads(tag.gettext()[start_index:end_index].rstrip()[:-1])
                for each_info in info:
                    for news in each_info["infolist"]:
                        self.info_list.append(
                            news["url"]
                            + ","
                            + news["infotitle"]
                            + ","
                            + news["daytime"]
                            + "\n"
                        )



if __name__ == "__main__":
    nju=Nju("Nju","https://yzb.nju.edu.cn/47840/list.htm")
    nju.run()
    # njfu=Njfu("Njuf","https://yz.njfu.edu.cn/sszs/")
    # njfu.run