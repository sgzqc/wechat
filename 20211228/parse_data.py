from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import jieba


def parse_data(csv_file,bake_img_file,font_file,stop_words_file,result_file):
    df = pd.read_csv(csv_file,header=None)
    text = ''
    for line in df[1]:
        text += ' '.join(jieba.cut(line,cut_all=False))

    backgroud_image = plt.imread(bake_img_file)
    stop_words = open(stop_words_file, encoding="utf8").read().split("\n")
    wc = WordCloud(
        background_color='white',
        mask = backgroud_image,
        font_path=font_file,
        max_words=2000,
        max_font_size=80,
        stopwords=stop_words,
        random_state=30
    )
    wc.generate_from_text(text)
    process_word = WordCloud.process_text(wc,text)
    # print(process_word.items())
    sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True)
    print(sort[:50])
    img_colors = ImageColorGenerator(backgroud_image)
    wc.recolor(color_func=img_colors)
    plt.imshow(wc)
    plt.axis('off')
    wc.to_file(result_file)
    print("done")


if __name__ == "__main__":
    csv_file = './data/data.csv'
    bake_img_file = './img/heart.jpeg'
    font_file = './font/SimHei.ttf'
    stop_words_file = './data/stopwords-zh.txt'
    result_file = './result/result_heart.jpg'
    parse_data(csv_file,bake_img_file,font_file,stop_words_file,result_file)

