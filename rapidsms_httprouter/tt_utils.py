import requests
from django.conf import settings

send_url = 'http://sms.timortelecom.tl/perl/sms_post.cgi'
cookie_name = 'pagesmsck'
login = settings.TT_LOGIN
password = settings.TT_PASSWORD


def get_payload(phone, message):
    payload = {
        'INAPPLICATION': 1,
        'msg_total': message,
        'numbers_total': phone,
        'totalChars': len(message),
        'totalNumbers': len(phone),
        'Check': 'yes',
        'login': login,
        'password': password,
        'html': '1',
        'dest': phone,
        'totalCounter1': 19999 - len(message),
        'msg': message,
        'totalCounter': 160 - len(message),
        'data': '',
        'hora': '',
        'enviar.x': '0',  # This is the click on the image of the submit button
        'enviar.y': '0',
    }
    return payload


def send_message(phone, message, cookies, timeout=15):
    """ This method returns error codes """
    payload = get_payload(phone, message)
    r = requests.get(send_url, params=payload, cookies=cookies, timeout=timeout)
    reason = ""
    ret = 200

    # the status code is always 200
    if 'Mensagem submetida com sucesso para 1 destino(s)' in r.text:
        print "Success ! Theoretically sent >" + message + '< to #' + phone
        return ret
    elif len(r.text) == 0:
        reason = "no cookie ?"
        ret = 401
    elif 'Acesso nao autorizado - login invalido' in r.text:
        reason = "wrong cookie"
        ret = 401
    else:
        print len(r.text), r.text
        print r
        reason = "unknown"
        ret = 400

    print "Failure. Failed to send the message >" + message + '< to #' + phone
    print reason
    return ret


def get_login_cookies():
    login_url = 'http://sms.timortelecom.tl/cgi-bin/pagesms/corp/login.pl'
    login_fields = {'login': login,
                    'password': password,
                    'action': 'entrar',
                    'lang': 'en_GB'}

    r = requests.post(login_url, data=login_fields)
    cookie_value = r.cookies[cookie_name]
    cookies = dict({cookie_name: cookie_value})
    print "got the cookies", cookies
    return cookies


def working_sample():
    cookies = get_login_cookies()

    message = 'This is a test message sent by a python script. kthxbye!'

    phone = settings.WATCHDOG_ADMIN
    send_message(phone, message, cookies)


def failing_sample():
    message = 'This is a test message sent by a python script. kthxbye!'

    phone = settings.WATCHDOG_ADMIN
    print "sending message"
    res = send_message(phone, message, {})
    print res
    res = send_message(phone, message, {cookie_name: 'whatever'})
    print res

