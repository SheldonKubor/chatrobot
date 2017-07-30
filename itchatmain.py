#coding=utf8
import requests
import itchat
import os
import random
import time

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        print(r)
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    #defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None

    reply = get_response(msg['Text'])
    
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    if not msg['FromUserName'] == myUserName:
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         msg['Text']), 'filehelper')

    return reply

@itchat.msg_register(itchat.content.PICTURE)
def picture_reply(msg):
    print('recive img')
    user = itchat.search_friends(name='remakName') #好友备注
    userName = user[0]['UserName']
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    if not msg['FromUserName'] == myUserName:  #可根据不同的好友选择不同的图库
        itchat.send_msg(u"[%s]收到好友@%s 的一张图\n" %
                        (time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         ), 'filehelper')
        fileDir = './friendimg/%s%s' % (msg['User']['NickName'], msg['FileName'])
        msg['Text'](fileDir)
    if(userName == msg['FromUserName']):
        imgName = getImgName('./ying')
        if (imgName == 'meigui.jpg'):
            itchat.send('你最美，送你一朵小红花~', toUserName=msg['FromUserName'])
        itchat.send('@img@%s' % './ying/' + imgName, toUserName=msg['FromUserName'])
    else:
        imgName = getImgName('./images')
        if(imgName == 'meigui.jpg'):
            itchat.send('你最美，送你一朵小红花~', toUserName=msg['FromUserName'])
        itchat.send('@img@%s' % './images/'+imgName,toUserName=msg['FromUserName'])



def listImg(path):
    return os.listdir(path)
def getImgIndex(path):
    imgs = listImg(path)
    imgIndex = random.randint(0,len(imgs)-1)
    return imgIndex,imgs

def getImgName(path):
    imgIndex,imgs = getImgIndex(path)
    return imgs[imgIndex]

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()
