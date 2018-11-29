目标：
1、爬取地址：http://www.a-hospital.com
2、爬取所有的疾病名称和疾病信息

功能：
1、scrapy-redis来爬取
2、Mysql和csv来存取数据
3、使用crawlSpider
4、config是文件配置密码

问题：
1、lpush name_start_urls 后面的url必须是编码，不能存在中文。
2、之前以为loader.processors 里面的方法是可以直接使用，但是要生效还是要定义ItemLoader类

haodf：https://www.haodf.com该网站所有的疾病名称
疾病百科：http://jbk.39.net/bw_t1/   疾病和症状