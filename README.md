# line bot practise

## Install package
``` shell
pip3 install -r requirements.txt
```

## Apply for LINE dev account
https://developers.line.biz/en/

## Migration
``` shell
# create 
python3 manage.py makemigrations

# sync
python3 manage.py migrate
```

## Set up Https by ngrok
LINE bot user webhook url as a link to server.
    1. require url not IP address.
    2. must https.

https://ngrok.com/download

## Run server
``` shell
python3 manage.py runserver 
./ngrok http 8000
```

## Allow hosts
``` python
ALLOWED_HOSTS = ['127.0.0.1', '20af8c34126e.ngrok.io']
```

## Add Webhook URL
![ngrok](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/ngrok.png)
![webhook](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/webhook.png)

## Reference
* https://github.com/henriquebastos/python-decouple