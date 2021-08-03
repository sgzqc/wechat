# -*- coding: UTF-8 -*-
import time, json, requests
from prettytable import PrettyTable


def get_all_china(content):
    tmp_data = content["data"]
    area_data = json.loads(tmp_data)["areaTree"]
    country = area_data[0]

    country_list = []
    name = country["name"]
    today_confirm = country["today"]["confirm"]
    now_confirm = country["total"]["nowConfirm"]
    total_confirm = country["total"]["confirm"]
    total_heal = country["total"]["heal"]

    country_list.append([name, today_confirm, now_confirm, total_confirm, total_heal])
    return country_list


def get_all_province(content):
    tmp_data = content["data"]
    area_data = json.loads(tmp_data)["areaTree"]
    data = area_data[0]['children']

    province_list = []
    for province in data:
        name = province["name"]
        today_confirm = province["today"]["confirm"]
        now_confirm = province["total"]["nowConfirm"]
        total_confirm = province["total"]["confirm"]
        total_heal = province["total"]["heal"]
        province_list.append([name, today_confirm, now_confirm, total_confirm, total_heal])
    return province_list


def format_list_prettytable(title,province_list):
    table = PrettyTable(title)
    for province in province_list:
        table.add_row(province)
    table.border = True
    return table


def parse_jiangsu_province(content,key_province):
    tmp_data = content["data"]
    area_data = json.loads(tmp_data)["areaTree"]
    data = area_data[0]['children']

    city_list = []
    for province in data:
        name = province["name"]
        if name == key_province:
            children_list = province["children"]
            for children in children_list:
                city = children["name"]
                today_new = children["today"]["confirm"]
                now_confirm = children["total"]["nowConfirm"]
                total_confirm = children["total"]["confirm"]
                total_heal = children["total"]["heal"]
                city_list.append([city, today_new, now_confirm, total_confirm, total_heal])
    return city_list


def draw_plot(city_list):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.serif'] = ['SimHei']
    NowConfirm_list = [ item[2]  for item in city_list]
    TodayNet_list = [item[1] for item in city_list]
    city_list = [ item[0]  for item in city_list]

    plt.figure()
    plt.barh(range(len(NowConfirm_list)), NowConfirm_list, tick_label=city_list)
    plt.title("江苏省现有确诊分布")
    plt.show()

    plt.figure()
    plt.barh(range(len(TodayNet_list)), TodayNet_list, tick_label=city_list)
    plt.title("江苏省今日新增分布")
    plt.show()


def general_city_map(input_all):
    from pyecharts import options as opts
    from pyecharts.charts import Map
    from pyecharts.faker import Faker

    city_list = []
    todayconfirm = []
    nowconfirm = []
    totalconfirm=[]
    for input in input_all:
        city = input[0]
        if city == "境外输入":
            continue
        city_list.append(city + "市")
        todayconfirm.append(input[1])
        nowconfirm.append(input[2])
        totalconfirm.append(input[3])

    c_today = (
         Map()
            .add("今日新增人数", [list(z) for z in zip(city_list, todayconfirm)],
                maptype="江苏"

                )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="江苏疫情今日新增0803"),
                visualmap_opts=opts.VisualMapOpts(max_=int( (max(todayconfirm)//10+1)*10),
                                                  is_piecewise=True,
                                                  range_text=["High","Low"],
                                                  border_color="#000"
                                                  )
                )
            .render("map_jiangsu_0803_new.html")
    )
    c_confirm = (
        Map()
            .add("现有确诊人数", [list(z) for z in zip(city_list, nowconfirm)],
                 maptype="江苏",
                 is_selected=True,
                 is_map_symbol_show=True
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="江苏疫情现有确诊0803"),
            visualmap_opts=opts.VisualMapOpts(is_show=True,
                                              max_=250,
                                              is_calculable=True,
                                              is_piecewise=True,
                                              split_number=10,
                                              range_text=["High", "Low"],
                                              border_color="#000"
                                              )
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True)
        )
            .render("map_jiangsu_0803_confirm.html")
    )

    c_total = (
        Map()
            .add("累计确诊人数", [list(z) for z in zip(city_list, totalconfirm)],
                 maptype="江苏",
                 is_selected=True,
                 is_map_symbol_show=True
                 )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="江苏疫情累计确诊0803"),
            visualmap_opts=opts.VisualMapOpts(is_show=True,
                                              max_=320,
                                              is_calculable=True,
                                              is_piecewise=True,
                                              split_number= 10,
                                              range_text=["High", "Low"],
                                              border_color="#000"
                                              )
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True)
        )
            .render("map_jiangsu_0803_total.html")
    )



def parse():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    req = requests.get(url=url)
    content = json.loads(req.text)

    #print(content)
    print("中国疫情汇总:")
    country_list = get_all_china(content)
    country_title = ["Country", "TodayNew", "NowConfirm", "TotalConfirm", "Healed"]
    country_table = format_list_prettytable(country_title, country_list)
    print(country_table)


    print("中国各省疫情情况汇总:")
    province_list = get_all_province(content)
    province_title = ["Province", "TodayNew", "NowConfirm", "TotalConfirm", "Healed"]
    province_table = format_list_prettytable(province_title,province_list)
    print(province_table)

    print("江苏各市疫情情况汇总：")
    key_province = "江苏"
    city_list = parse_jiangsu_province(content,key_province)
    city_title = ["City", "TodayNew", "NowConfirm", "TotalConfirm", "Healed"]
    city_table = format_list_prettytable(city_title, city_list)
    print(city_table)


    general_city_map(city_list)




if __name__ == "__main__":
    parse()