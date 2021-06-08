from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from module import msgresponse

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@傳送文字':
                        msgresponse.sendText(event)
                    elif mtext == '@傳送圖片':
                        msgresponse.sendImage(event)
                    elif mtext == '@傳送貼圖':
                        msgresponse.sendStick(event)
                    elif mtext == '@多項傳送':
                        msgresponse.sendMulti(event)
                    elif mtext == '@傳送位置':
                        msgresponse.sendPosition(event)
                    elif mtext == '@吱吱':
                        msgresponse.sendImage(event)
                    elif mtext == '@傳送聲音':
                        msgresponse.sendVoice(event)
                    elif mtext == '@傳送影片':
                        msgresponse.sendVedio(event)
                    elif mtext == '@快速選單':
                        msgresponse.sendQuickreply(event)

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
