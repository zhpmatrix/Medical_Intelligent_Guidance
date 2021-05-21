import re
import json 
import requests
import pandas as pd
from tqdm import tqdm
from requests_html import HTMLSession
session = HTMLSession()

class Crawler:
    def crawler_for_chunyuyisheng(self, save_path="chunyuyisheng_data.csv"):
        examples = {}
        page_total = 30
        for page_num in tqdm(range(page_total)):
            data = session.get("https://www.chunyuyisheng.com/pc/qalist/?page="+str(page_num + 1)+"&high_quality=0")
            for div in data.html.xpath("//div[@class='qa-item qa-item-ask']"):
                for url in div.links:
                    each_data = session.get("https://www.chunyuyisheng.com"+url)
                    for question in each_data.html.xpath("//div[@class='bread-crumb-spacial']"):
                        [class_name, content] = question.text.split()
                        if class_name not in examples:
                            examples[class_name] = set()
                            examples[class_name].add(content)
                        else:
                            examples[class_name].add(content)
        data = []
        for key, values in examples.items():
            for value in list(values):
                data.append([value, key])
        data = pd.DataFrame(data, columns=["question", "label"])
        data.to_csv(save_path, index=False, sep="\t")
    
    def crawler_for_haodaifu(self, save_path="haodaifu_data.csv"):
        counter = 0
        for page_num in tqdm(range(2019, 2020)):
            data = session.get("https://www.haodf.com/sitemap-zx/"+str(page_num + 1)+"/")
            for url in re.findall("\[\d{4}-\d{2}-\d{2}\]", data.text):
                url = url[1:-1]
                questions = session.get("https://www.haodf.com/sitemap-zx/"+url.replace("-", "")+"_1/")
                for question in questions.html.xpath("//a[@href]"):
                    text = question.text
                    tag_list = set()
                    for link in question.links:
                        if "kanbing" in link:
                            link = "https:"+link
                            each_page = session.get(link)
                            for tag in each_page.html.xpath("//a[@class='capsule-item']"):
                                tag_list.add(tag.text)
                    if len(tag_list) > 0:
                        print(text)
                        print(tag_list)
                        example = {"question":text, "label": "_".join(list(tag_list))}
                        counter += 1
                        print(counter)
                        with open(str(page_num + 1)+"_"+save_path, "a") as writer:
                            writer.write(json.dumps(example, ensure_ascii=False)+"\n")
if __name__ == "__main__":
    crawler = Crawler()
    #crawler.crawler_for_chunyuyisheng()
    crawler.crawler_for_haodaifu()
