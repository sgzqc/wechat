import stylecloud
from stop_words import get_stop_words
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def test1():
    stylecloud.gen_stylecloud(file_path='SJ-Speech.txt',
                              icon_name="fas fa-apple-alt")


def test2():
    stylecloud.gen_stylecloud(file_path='SJ-Speech.txt',
                              icon_name='fas fa-apple-alt',
                              colors='white',
                              background_color='black',
                              output_name='apple.png',
                              collocations=False)


def test3():
    stop_words = get_stop_words('english')
    stylecloud.gen_stylecloud(file_path='SJ-Speech.txt',
                              icon_name='fas fa-apple-alt',
                              palette='cartocolors.qualitative.Pastel_3',
                              background_color='black',
                              output_name='apple2.png',
                              collocations=False,
                              custom_stopwords=stop_words)



def test4():
    stop_words = get_stop_words('english')
    # create a mask based on the image we wish to include
    my_mask = np.array(Image.open('batman-logo.png'))
    # create a wordcloud
    wc = WordCloud(background_color='white',
                   mask=my_mask,
                   collocations=False,
                   width=600,
                   height=300,
                   contour_width=3,
                   contour_color='black',
                   stopwords=stop_words)

    with open('SJ-Speech.txt', encoding='gb18030' , errors='ignore') as txt_file:
        texto = txt_file.read()
    wc.generate(texto)

    image_colors = ImageColorGenerator(my_mask)
    wc.recolor(color_func=image_colors)

    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    wc.to_file('wordcloud2.png')
    plt.show()






if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()