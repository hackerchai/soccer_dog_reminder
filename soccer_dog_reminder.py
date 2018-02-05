#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib, urllib2, datetime, traceback, sys
from urllib import urlencode
from urllib2 import Request, urlopen


reload(sys)
sys.setdefaultencoding('utf8')


def main():
    try:

        football_api_appkey = ""

        sms_api_appcode = ""
        sms_api_appskin = 0000

        football_club = ""
        phone = 1234567890

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

            current_time_h = datetime.datetime.now()
            match_time_h = datetime.datetime(int(current_time_h.year), int(match_month), int(match_day),
                                             int(match_hour), int(match_minute), 0, 0)
            gap_time_days = (match_time_h - current_time_h).days

            if gap_time_days <= 1:
                gap_time_seconds = (match_time_h - current_time_h).seconds
                gap_time_hours = (gap_time_seconds / 3600) + gap_time_days * 24
                print gap_time_hours
                message = football_club_d + u'|' + match_type + u'|' + match_opponent + u'|' + match_month + u'月' + match_day + u'日' + match_hour + u'时' + match_minute + u'分' + u'|' + unicode(
                    gap_time_hours)
                return message
            else:
                message = "no recent match"
                return message
        else:
            print "%s:%s" % (football_match_data["error_code"], football_match_data["reason"])
    else:
        print "request football api error"


def sms_send(sms_api_appcode, sms_api_appskin, phone, message):
    sms_api_url_pre = 'http://fesms.market.alicloudapi.com'
    sms_api_url_path = '/smsmsg'
    sms_api_params = {
        "param": message,
        "phone": phone,
        "skin": sms_api_appskin,
    }
    sms_api_querys = urlencode(sms_api_params)
    sms_api_url = sms_api_url_pre + sms_api_url_path + '?' + sms_api_querys

    sms_api_request = Request(sms_api_url)
    sms_api_request.add_header('Authorization', 'APPCODE ' + sms_api_appcode)
    sms_api_response = urlopen(sms_api_request)
    sms_api_content = sms_api_response.read()
    sms_return_data = json.loads(sms_api_content)
    if sms_return_data:
        error_code = sms_return_data["Code"]
        if error_code == "OK":
            print "SMS is sent successfully"
        else:
            print sms_return_data["Message"]
    else:
        print "request sms api error"


if __name__ == '__main__':
    main()
