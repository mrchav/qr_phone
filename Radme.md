#Put my car away (QR)

##Что умеет бот?
Бот просто создаст табличку под стекло автомобиля с вашим телефоном и QR кодом, 
наведя на который можно вам быстро позвонить

## Как использовать бота
* Перейдите по ссылке бота https://t.me/put_my_car_away_bot
* Наберите команду /start
* Следуйте инструкции

## Как развернуть проект
1. docker build -t qr_phone . 
2. docker run  -e TG_API='___________:*******************' qr_phone


## Какой стек использовался 

* **qrcode** - генерация QR кодов
* **PIL** - работа с изображением
* **aiogram** - бот для телеграмм
* **Docker** - контейнер