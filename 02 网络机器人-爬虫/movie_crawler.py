import csv
from lxml import html
from lxml import etree
import requests
import os

BASE_URL = "https://www.themoviedb.org/"
RANK_URL = "https://www.themoviedb.org/movie"
RANK_URL2 = "https://www.themoviedb.org/discover/movie/items" #第二页之后的访问路径
MOVIE_LIST_FILE = 'csv_data/movies.csv'

def save_movie_info(movie_info):
    if not os.path.exists(MOVIE_LIST_FILE):
        os.makedirs(os.path.dirname(MOVIE_LIST_FILE))
    with open(MOVIE_LIST_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['电影名称', '上映时间', '类型', '时长', '评分', '导演', '简介', '详情链接'])
        writer.writeheader()
        writer.writerows(movie_info)
    print("电影信息已保存到", MOVIE_LIST_FILE)

def get_movie_info(movie_url_list):
    movie_info_list = []
    for url in movie_url_list:
        print("正在爬取", url)
        response = requests.get(url)
        document = html.fromstring(response.text)

        # 获取电影名称
        movie_name = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
        movie_release = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')
        movie_type = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
        movie_runtime = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
        movie_score = document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
        movie_author = document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()')
        movie_introduce = document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')

        # 返回详情-字典
        movie_info = {
            '电影名称': movie_name[0].strip() if movie_name else '',
            '上映时间': movie_release[0].strip() if movie_release else '',
            '类型': movie_type[0].strip() if movie_type else '',
            '时长': movie_runtime[0].strip() if movie_runtime else '',
            '评分': movie_score[0].strip() if movie_score else '',
            '导演': movie_author[0].strip() if movie_author else '',
            '简介': movie_introduce[0].strip() if movie_introduce else '',
            '详情链接': url
        }
        movie_info_list.append(movie_info)
    return movie_info_list

def main():
    all_movies = []
    for page_num in range(1, 6):
        print(f"正在爬取第 {page_num} 页数据...")
        # 1.发送网页请求
        if page_num == 1:
            response = requests.get(RANK_URL, timeout=60) #
        else:
            response = requests.post(RANK_URL2, f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num} &primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-26&show_me=everything&sort_by=popularity.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=0&vote_count.lte=&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=", timeout=60)

        # 2. 解析网页数据
        document = html.fromstring(response.text)
        movie_list = document.xpath(f"//*[@id='page_{page_num}']/div[@class='media-card-list contents w-full']/div[@class='media-list-results contents']")
        # 3. 获取电影列表
        # 输出字符串
        # print(etree.tostring(movie_list[0], encoding="utf-8", method="html").decode("utf-8"))
        for movie in movie_list[0]:
            movie_urls = movie.xpath('./div/div/a/@href')
            print(movie_urls, 'movie_urls:')
            all_movies.append(BASE_URL + movie_urls[0])

    # 获取电影详情信息
    movie_info = get_movie_info(all_movies)

    # 保存电影信息到csv
    save_movie_info(movie_info)

if __name__ == "__main__":
    main()