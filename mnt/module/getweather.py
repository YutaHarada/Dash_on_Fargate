import datetime
import urllib.request
from bs4 import BeautifulSoup


def str2float(weather_data):
    try:
        return float(weather_data)
    except:  # NOQA
        return float(0)


def scraping(url, date):
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(markup=html, features="html.parser")
    trs = soup.find("table", {"class": "data2_s"})

    weather_info = []
    # table の中身を取得
    for tr in trs.findAll("tr")[4:]:
        tds = tr.findAll("td")

        if tds[1].string is None:
            break

        if tds[0].string == str(date.day):
            weather_info.append(date.month)
            weather_info.append(str2float(tds[2].string))
            weather_info.append(str2float(tds[3].string))
            weather_info.append(str2float(tds[6].string))
            weather_info.append(str2float(tds[7].string))
            weather_info.append(str2float(tds[8].string))
            weather_info.append(str2float(tds[9].string))
            weather_info.append(str2float(tds[10].string))
            weather_info.append(str2float(tds[11].string))
            weather_info.append(str2float(tds[12].string))
            weather_info.append(tds[13].string)
            weather_info.append(str2float(tds[16].string))

    return weather_info


def get_info():
    # データ取得開始・終了日
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    # 特徴量名
    fields = [
        "月",
        "気圧",
        "降水量",
        "平均気温",
        "最高気温",
        "最低気温",
        "平均湿度",
        "最小湿度",
        "平均風速",
        "最大風速（風速）",
        "最大風速（風向）",
        "日照時間",
    ]
    url = (
         "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?"
         f"prec_no=74&block_no=47893&year={yesterday.year}&month={yesterday.month}&day=&view=" # NOQA
    )

    feature = {x[0]: x[1] for x in zip(fields, scraping(url, yesterday))}

    return feature
