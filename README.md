# Market-environment

## Uppgift
Detta är en fortsättning av mitt [Förra Projekt](https://github.com/abbsimoga/Enstaka-programerings-projekt/tree/master/Enstaka_programering/StockMarket)

## Bakgrund
I denna fortsättning använde jag mig utav bibloteket **_OpenAI gym_** för att skapa mitt egna *enviornment*. Med bakgrundskunskaper från **_Hands-On Q-Learningwith Python_** och praktiska kunskaper där jag skulle intregrera **_Q-Lerning_** till tre redan skapade gym [*Taxi*, *CartPole* och *Bandit*](https://colab.research.google.com/drive/1RwkDfI0lxFZmXXNk1q88PWA7HQiJjlBL#scrollTo=Ac6y6qG-3kV3). Arbetet började med skapandet av ett eget *Tic Tac Toe* [gym](https://github.com/abbsimoga/TicTacGym) pga enkelheten följd [Medium länk](https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa). Större del av detta arbetet följde min förra kod och exemplerna ovan men även denna [Medium länk](https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e).



# Grafer

### Avläsande av graf
<De första 450 värderna som inte är markerade är 'observation'>
<De markerade värderna tyder på 'agents'>

## Slutsatser
Tydlig visning på 'agentens' observation av marknadens flöde
När observationen liknar framtida 'states' kan 'agenten' använda det till sin vinst
![png](docs/Capture3.JPG)

mönster

Tydlig visning på när 'agentens' observation inte håller sig konsistant
När observationen tyder på tillväxt kommer agenten skapa en 123 
![png](docs/Capture1.JPG)

exempel2:
![png](docs/Capture2.JPG)

Agenten hittar lätt mönster på tydlig tillväxt och tillbakagång och lär sig att gissning på 

Medelvärde av tio itterationer på följd = 1.2935849431816784
![png](docs/Capture7.JPG)

Förra projekt (Förra projekt (https://github.com/abbsimoga/Enstaka-programerings-projekt/tree/master/Enstaka programering/StockMarket)
) invisterade på måfå och visade tillväxt och tillbakagång på ca +-5%

21772/20000 = 1.0886
![png](docs/Capture4.JPG)
![png](docs/Capture5.JPG)

Visar på att invistering på aktsier innom sp500 leder till tillväxt
23625/20000 = 1.18125
![png](docs/Capture6.JPG)