#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib, urllib2, datetime, traceback, sys
from urllib import urlencode
from urllib2 import Request, urlopen
from datetime import date

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    try:

        football_api_appkey = ""

        sms_api_appcode = ''
        sms_api_appskin = 'TP********'

        football_club = "巴塞罗那"
        phone = 123456789

        message = club_match_query(football_api_appkey, football_club).encode('utf-8')
        if message != "no recent match":
            sms_send(sms_api_appcode, sms_api_appskin, phone, message)

        else:
            print "no recent match"

    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print  'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():', traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()


def club_match_query(football_api_appkey, football_club):
    football_api_url = "http://op.juhe.cn/onebox/football/team"
    football_api_params = {
        "key": football_api_appkey,
        "dtype": "",
        "team": football_club,
    }
    football_api_params = urlencode(football_api_params)
    football_api_request = Request(football_api_url, football_api_params)
    football_api_response = urlopen(football_api_request)
    football_api_content = football_api_response.read()
    football_match_data = json.loads(football_api_content)
    if football_match_data:
        error_code = football_match_data["error_code"]
        football_club_d = football_club.decode("utf-8")
        if error_code == 0:
            # 寻找第一个还未进行的比赛
            for index in range(len(football_match_data["result"]["list"])):
                if football_match_data["result"]["list"][index]["c4R"] == "VS":
                    upcoming_match_id = index
                    break
            match_type = football_match_data["result"]["list"][upcoming_match_id]["c1"]
            match_date = football_match_data["result"]["list"][upcoming_match_id]["c2"]
            match_time = football_match_data["result"]["list"][upcoming_match_id]["c3"]

            if football_match_data["result"]["list"][upcoming_match_id]["c4T1"] == football_club_d:
                match_opponent = football_match_data["result"]["list"][upcoming_match_id]["c4T2"]
            else:
                match_opponent = football_match_data["result"]["list"][upcoming_match_id]["c4T1"]

            print match_type
            print match_date
            print match_time
            print match_opponent

            (match_month, match_day) = match_date.split("-")
            (match_hour, match_minute) = match_time.split(":")

            print match_day
            print match_month
            print match_hour
            print match_minute

            current_time_d = date.today()
            match_time_d = date(int(current_time_d.year), int(match_month), int(match_day))

            gap_time_days = (match_time_d - current_time_d).days

            if gap_time_days <= 1:
                current_time_h = datetime.datetime.now()
                match_time_h = datetime.datetime(int(current_time_h.year), int(match_month), int(match_day),
                                                 int(match_hour), int(match_minute), 0, 0)
                gap_time_seconds = (match_time_h - current_time_h).seconds
                gap_time_days = (match_time_h - current_time_h).days
                gap_time_hours = gap_time_seconds / 3600 + gap_time_days * 24
                print gap_time_hours
                message = "team1:"+football_club + ','  + "team2:"+match_opponent + ',' +"type:" + match_type + ',' + "date:" +match_month + "月" + match_day + "日" + match_hour + "时" + match_minute + "分" + ',' + "hour:" + str(
                    gap_time_hours)
                print message
                return message
            else:
                message = "no recent match"
                return message
        else:
            print "%s:%s" % (football_match_data["error_code"], football_match_data["reason"])
    else:
        print "request football api error"


def sms_send(sms_api_appcode, sms_api_appskin, phone, message):
    sms_api_url_pre = 'http://dingxin.market.alicloudapi.com'
    sms_api_url_path = '/dx/sendSms'
    sms_api_params = {
        "param": message,
        "mobile": phone,
        "tpl_id": sms_api_appskin,
    }
    sms_api_url = sms_api_url_pre + sms_api_url_path

    sms_api_en_params = urlencode(sms_api_params)
    sms_api_header = { 'Authorization' : 'APPCODE ' + sms_api_appcode}

    sms_api_request = Request(sms_api_url,sms_api_en_params,sms_api_header)
    sms_api_response = urlopen(sms_api_request)
    sms_api_content = sms_api_response.read()
    sms_return_data = json.loads(sms_api_content)
    #print sms_return_data
    if sms_return_data:
        error_code = sms_return_data["return_code"]
        if error_code == "00000":
            print "SMS is sent successfully"
        else:
            print sms_return_data["order_id"]
    else:
        print "request sms api error"


if __name__ == '__main__':
    main()
