#!/bin/env python
#encoding=gbk
import sys
import os
import traceback
import urllib
#import enc
import time
import datetime

_postfix = ["com", "cn", "net", "org", "cc", "hk", "tv", "to", "edu", "me", "asia", "biz", "mobi", "ch",
#"xin",
"la", "co", "so", "kr", "tm"]
postfix = set(_postfix)
_prefix = ["www", "m", "wap", "click", "clickc", "e", "3g", "c", "sz", "cn", "sh", "bj", "mobile", "t", "hz",
#"dwz",
"wh", "cs", "tj", "nj", "cd", "gz", "cq", "4g", "u", "mail", "dg", "zh", "dp", "mall", "i", "ad", "wx",
#"creditcard",
"dl",
#"xm",
"hf", "jn", "qd", "zz",
#"china",
"yt", "ty",
"liuxue", "gd", "cc", "v", "w", "fs", "bbs", "detail", "6216", "tv", "g", "5g", "web", "zs", "app", "game", "clickserve", "vip", "xa", "bsch", "feixin", "sjz", "sy", "nb", "fz", "l", "yd", "nn", "nc", "lz", "sun", "pinganxyk", "pai", "tracker", "km", "wf", "qiantum", "yc", "aldi", "mm", "hs", "gy", "sempage", "baibock", "hk", "jc", "heb", "ych", "lx", "pz", "url", "aws", "lol", "adlp", "sj", "cnt"]
prefix = set(_prefix)

dwz = [
        # 短网址
        "dwz.cn",
        "t.cn",
        "lnk0.com",
        # 下面是从网上扒的短网址大全
        "dwz.cn","t.cn","5to.cn","d.ldawh.cn","jd.cn.hn","qq.cn.hn","tb.cn.hn","xsurl.cn","0.gg","0rz.tw","2.gp","2.ly","6du.in","6url.com","7rz.de","980.so","alturl.com","arm.in","bit.ly","chilp.it","cli.gs","cligs.com","clop.in","coge.la","cowurl.com","digbig.com","doiop.com","dot.tk","duanwz.com","durl.me","dwarfurl.com","dwz.tw","fon.gs","fwd4.me","fyad.org","gkurl.us","goo.gl","here.is","hex.io","hj.to","hurl.no","icp.cc","idek.net","ikr.me","irt.me","is.gd","is.gd","Jdem.cz","j.mp","Jump.IM","kks.me","kl.am","kore.us","krz.ch","lin.io","linkee.com","linkshrink.com","lnk.by","lnk.in","lnk.ly","lnk.nu","lnk.sk","l.pr","lt.tl","lurl.no","ly.my","mangk.us","metamark.net","micurl.com","migre.me","min2.me","minilink.org","miniurl.com","minurl.fr","moourl.com","mysp.in","myurl.in","nbx.ch","ndurl.com","nm.ly","notlong.com","omf.gd","ooqx.com","out.yijia.com","ow.ly","pendek.in","pic.gd","piko.me","piurl.com","plo.cc","p.ly","pnt.me","ppt.cc","pt2.me","puke.it","qik.li","qqurl.com","qr.cx","qurl.com","qux.in","rde.me","redir.ec","retwt.me","r.im","ri.ms","rnk.me","rrd.me","rt.nu","rubyurl.com","s4c.in","safe.mn","sai.ly","sfu.ca","shadyurl.com","shiturl.com","shorl.com","shorten-url.com","short.ie","shortn.me","short.to","shrten.com","shrtn.com","shrt.ws","shrunklink.com","shurl.net","shw.me","simurl.com","sina.lt","siteo.us","slki.ru","sl.ly","smallr.net","smallurl.in","smfu.in","snipie.com","snipurl.com","snkr.me","song.ly","srnk.net","su.pr","swu.me","tighturl.com","timesurl.at","tini.us","tiny.cc","tinypl.us","tinyurl.com","tllg.net","to.je","to.ly","topduan.com","to.vg","tra.kz","tr.im","trumpink.lt","tsort.us","tweetburner.com","tweet.me","twip.us","twirl.at","twtr.us","u6.gg","ubb.cc","uee.me","uiop.me","u.mavrev.com","unfaker.it","u.nu","urix.org","urizy.com","url.ag","urlborg.com","urlcorta.es","urlcut.com","urlg.info","url.ie","urli.nl","urlm.in","urloo.com","url.tool.cc","urlu.ms","ur.ly","urlz.at","urlzen.com","vb.ly","vi.ly","virl.com","vl.am","voizle.com","vtc.es","vzturl.com","w3t.org","w3t.org","wa.la","xiy.net","x.nu","xr.com","xrl.in","xrt.me","x.vu","xxsurl.de","yatcu.com","yep.it","Yourls.org","zapt.in","zi.me","zi.pe","zip.li","zipmyurl.com","z.pe","zz.gd",

        # 视频网站会购买大量的热门电视剧,热门综艺,所以把他们当作短网址逻辑来处理
        "www.youku.com/show_page",
        "i.youku.com/i",
        "list.youku.com",
        "v.qq.com",
        "g.iqiyi.com",
        ]

# domain = url.split("//")[-1].split("/")[0]
# 特殊case1: 不规范 "http://www.twabc.com.cn//"
# 特殊case2: 短网址 "http://dwz.cn/5JcUwu"
# 特殊case3: 大写   "http://DWZ.cn/5JcUwu"
# 域名本身不区分大小写,DWZ.cn与dwz.cn等价,但是查询串以及域名后面的目录是区分大小写的
def extract_domain(url):
    # 1.去掉协议 http:// 以及查询串
    url = url.strip('/').split('?')[0].split("://")[-1]
    # 2.处理短网址
    for d in dwz:
        if url.startswith(d):
            return url
    # 3.转小写
    # 大小写转换必须在短网址后面,因为短网址参数是区分大小写的
    # dwz.cn/5RKZNl与dwz.cn/5rkznl时不同的页面
    domain = url.lower()
    # 4.取主域
    domain = domain.split("/")[0]
    return domain

def extract_abbrev_domain(url):
    ############ copy from extract_domain 因为其中间有return,不能直接调用
    # 1.去掉协议 http:// 以及查询串
    url = url.split('?')[0].split("://")[-1]
    # 2.处理短网址
    for d in dwz:
        if url.startswith(d):
            return url
    # 3.转小写
    # 大小写转换必须在短网址后面,因为短网址参数是区分大小写的
    # dwz.cn/5RKZNl与dwz.cn/5rkznl时不同的页面
    domain = url.lower()
    # 4.取主域
    domain = domain.split("/")[0]
    ############

    # 5.进行domain规约
    keep_domain = domain
    if len(keep_domain) == 0:
        keep_domain = url

    ## 为了最大可能扩大匹配,在这里对domain做业务处理  ##
    fields = domain.split('.')

    last = len(fields) - 1
    for i in range(last, -1, -1):
        last = i
        if fields[i] not in postfix:
            break
    first = 0
    for i in range(0, len(fields)):
        first = i
        if fields[i] not in prefix:
            break
    domain = '.'.join(fields[first:last+1])

    if len(domain) == 0:
        domain = keep_domain

    # 处理特殊case
    #if domain == 'tmall':
    #    domain = 'taobao'
    #return domain
    return domain
