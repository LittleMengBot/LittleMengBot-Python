# -*- coding: utf-8 -*
# 这是一个推特视频解析的模块，需要用到推特的api：https://developer.twitter.com/
# pip3 install tweepy
from typing import List
import tweepy
import re

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
# 此四项请从推特开发者平台获取。

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, proxy = 'socks5://127.0.0.1:9050')   # 调用系统Tor接口。默认是9050，请自行修改。

def check_url(url:str):
    if re.search(r"https?:\/\/twitter.com\/[0-9-a-zA-Z_]{1,20}\/status\/([0-9]*)", url) is not None:    # 判断链接合法
        return True
    else:
        return False

def getTweetVideo(url:str) ->List[str, bool]:
    return_result = []
    if check_url(url) == True:
        if url[-5] == '?':
            id = url[:-5].split('/')[-1]
        else:
            id = url.split('/')[-1]
        result = api.get_status(id = id)
        result_json = result._json
        try:
            video_list = result_json['extended_entities']['media'][0]['video_info']['variants']
            new_video_list = []
            for video in video_list:
                if 'bitrate' in video:
                    new_video_list.append(video)
                    
            new_s = sorted(new_video_list, key = lambda e:e.__getitem__('bitrate'), reverse = True)    # 按照视频比特率排序，返回最高的元素。
            video_url = new_s[0]['url']
            # print(video_url)
        except:
            return_result.append("")
            return_result.append(False)
            return return_result
        return_result.append(video_url)
        return_result.append(True)
        return return_result
    else:
        return_result.append("")
        return_result.append(False)
        return return_result