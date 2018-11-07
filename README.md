# Anti-FruitFraud
這是一個沒在逛菜市場、不常買水果、不食人間煙火的軟體工程師，就近水果行買水果結果發現水果行的奇異果比全聯還貴，盛怒之下寫的一個小應用。

此小應用讓你可以透過已離不開你生活的 LINE 作為窗口，讓你能夠快速地紀錄水果的價格，避免自己在錯誤的時機與地點買到貴鬆鬆的水果。

其實你不記錄水果也可以啦～

# 如何開始？
1. 首先你會需要用到以下資訊，學會用自己的 LINE 帳號架設一個頻道
    ### ***Line Bot 教學***
    1. 使用[姚韋辰](https://yaoandy107.github.io/line-bot-tutorial/)的教程使用 Python LINE Bot SDK 及 HEROKU 平台架設一個簡單的回話機器人

    ### ***如何使用 HEROKU 提供的 postgresql 資料庫***
    - [provisioning-heroku-postgres](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres)

    ### ***Flask x Heroku x Database***
    - [Setting up flask app in heroku with a database](https://gist.github.com/mayukh18/2223bc8fc152631205abd7cbf1efdd41/)

2. Fork 此專案

3. 將你的專案內的 [app.py](/app.py) 中的token換成自己從LINE developer上產生的token

4. 至 [HEROKU](https://dashboard.heroku.com/) 登入到自己的專案底下的 Deploy 標籤，將 HEROKU 與 你的Github專案連結
    - 可以設定 Automatic deploys，當你的 Github 專案有新的 push 時 HEROKU就會自動拉取並建置、部屬

# Anti-FruitFraud 使用說明
1. **添加項目**
    
    在對話框中依序輸入「地點」 「項目」 「單價」並以「空白」分隔，系統會將你輸入的資訊記錄下來：

    ![Imgur](https://i.imgur.com/347pfiY.jpg)

    若你輸入的價格並非單價、有單位，可直接接在最後，那麼系統就不會用預設的「個」來寫入單位：
    ![Imgur](https://i.imgur.com/tj8NHPP.jpg)

2. **用地點找出曾經輸入過的水果價格**
    
    對話框中輸入曾經輸入過的地點，系統會顯示書最近五筆添加的資料
    ![Imgur](https://i.imgur.com/6MYYPhp.jpg)

3. **用水果叫出曾經輸入過的價格**
    
    對話框中輸入曾經輸入過的水果名稱，系統會顯示書最近五筆添加的資料
    ![Imgur](https://i.imgur.com/TBgeFoQ.jpg)