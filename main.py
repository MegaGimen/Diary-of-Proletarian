from datetime import datetime, timedelta, date
import random
from scipy import stats
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def random_replace(text, old, replacements):
    """用列表中的随机字符串替换所有匹配，每个匹配替换多次"""
    n = 20  
    p = 0.75
    binom_dist = stats.binom(n, p)
    success_time = binom_dist.rvs()
    
    def replace_func(match):
        # 对每个匹配进行success_time次替换
        result = match.group(0)
        for _ in range(success_time):
            result = random.choice(replacements)
        return result
    
    return re.sub(re.escape(old), replace_func, text)



class DiaryElement:
    def __init__(self,date,template,weather,location,mapping):
        self.date=date
        self.template=template
        self.weather=weather
        self.location=location
        self.mapping=mapping
    def _replace_(self,content):
        for keyword in self.mapping.keys():
            content=random_replace(content,keyword,self.mapping[keyword])
        return content
    def __str__(self):
        ret=f'''
日期：{self.date}

地点：{self.location}

天气：{self.weather}

{self._replace_(self._replace_(self.template))}

'''
        return ret
        
工作日内容模板='''
今天早上6点起，草草地刷完牙洗完脸就坐上了去公司的地铁。在地铁上，<地铁事件>。总之，9点钟就到了公司并打卡，崭新的一天开始了！。

在工作时，<工作时的随机事件>。


终于熬过去了！哈哈哈哈，18：00准时下班！真不容易！真没想到强迫加班本来是个违法的事情，但我却把不被强制加班视为幸福的！难道我还要渴求被人不违法吗？

<下班>

<牢骚>

上地铁了，<地铁事件>

21：00了，回到家了，和妻子搂抱一会儿。

<晚上的随机事件>
'''

周六的内容模板='''
爽翻了！今天居然休息哈哈哈哈哈哈。今天我早上十一点才起的。

<消费时的爽快>

<晚上的随机事件>

就这样熬夜熬到凌晨两点！
'''

周日的内容模板='''
最后一天休息了！我得抓紧时间享受！

今天我早上十一点才起的。

<消费时的爽快>

<晚上的随机事件>

睡觉前哭了一会儿，难得和家里人见两面，明天又要分开了...又陷入了低潮吗。

今天不敢熬夜了，23点赶紧睡了。
'''

import json

with open('mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

FUTUREDAYS=360
today = date.today()
print(f"今天的日期: {today}")

for day in range(FUTUREDAYS):
    target=today+timedelta(days=day)
    if target.weekday() == 5:#周六
        template=周六的内容模板
    elif target.weekday()==6:#周日
        template=周日的内容模板
    else:
        template=工作日内容模板
    ele=DiaryElement(date=target,template=template,location="北京，西城",weather=random.choice(['晴', '多云', '阴', '小雨', '雾', '微风', '阵雨', '雷阵雨', '雪', '雨夹雪']),mapping=mapping)
    print(ele)
