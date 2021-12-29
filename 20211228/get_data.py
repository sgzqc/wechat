from bs4 import BeautifulSoup
import  pandas as pd
import requests


def get_url_data(url,save_file):
    html = requests.get(url).content
    # print(html)
    html_data = str(html, 'utf-8')
    soup = BeautifulSoup(html_data, 'lxml')
    retsults = soup.find_all('d')

    comments = [comment.text for comment in retsults]
    comments_dict = {'comment': comments}
    df = pd.DataFrame(comments_dict)
    df.to_csv(save_file, encoding='utf-8')


if __name__ == "__main__":
    url = 'http://comment.bilibili.com/72036817.xml'
    #url = 'http://comment.bilibili.com/441219274.xml'
    save_file = './data/data_peiqi.csv'
    get_url_data(url,save_file)

