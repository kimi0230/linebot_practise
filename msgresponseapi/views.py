from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import msgresponse, templateresponse, postbackresponse
from urllib.parse import parse_qsl

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
                    elif mtext == '@按鈕樣板':
                        templateresponse.sendButton(event)
                    elif mtext == '@確認樣板':
                        templateresponse.sendConfirm(event)
                    elif mtext == '@轉盤樣板':
                        templateresponse.sendCarousel(event)
                    elif mtext == '@圖片轉盤':
                        templateresponse.sendImgCarousel(event)
                    elif mtext == '@購買披薩':
                        templateresponse.sendPizza(event)
                    elif mtext == '@yes':
                        templateresponse.sendYes(event)
                    elif mtext == '@圖片地圖':
                        templateresponse.sendImgmap(event)
                    elif mtext == '@日期時間':
                        templateresponse.sendDatetime(event)

            if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
                # 取得Postback資料
                backdata = dict(parse_qsl(event.postback.data))
                if backdata.get('action') == 'buy':
                    postbackresponse.sendBack_buy(event, backdata)
                elif backdata.get('action') == 'sell':
                    postbackresponse.sendBack_sell(event, backdata)
                elif backdata.get('action') == 'sell_date':
                    postbackresponse.sendDate_sell(event, backdata)
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
