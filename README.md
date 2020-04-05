# Market-environment

# GAMMAL READ ME FIXAR SNART

## Uppgift
Detta är en fortsättning av mitt [Förra Projekt](https://github.com/abbsimoga/Enstaka-programerings-projekt/tree/master/Enstaka_programering/StockMarket).

I denna fortsättning använde jag mig utav bibloteket **_OpenAI gym_** för att skapa mitt egna *enviornment*. Med bakgrundskunskaper från **_Hands-On Q-Learning with Python_** och praktiska kunskaper där jag skulle intregrera **_Q-Lerning_** till tre redan skapade gym [*Taxi*, *CartPole* och *Bandit*](https://colab.research.google.com/drive/1riS_s-7JEpVC93Svd9LOPPtSsyTDs1xM#scrollTo=9mEFgm9qJJXu).

Arbetet började med skapandet av ett eget *Tic Tac Toe* [gym](https://github.com/abbsimoga/TicTacGym) på grund av arbetets komplexitet. [Här](https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa) är Medium länken jag följde för skapandet av *Tic Tac Toe* gymmet. Större del av detta arbetet följde min förra kod och exemplerna ovan men även denna [Medium länk](https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e).

# Förklarning av Q-Learning
Jag kommer härdan över nämna några ord som **_agent_**, **_enviornment_**, **_state_** med mera. Och ska försöka ge dig enkla förklarningar för vad dessa betyder. Samt ge dig en generell förståelse över hur RL-algorythmer funkar speciellt Q-Learning.

### RL-algorythmer och Q-Learning
**Reinforcement Learning** är en typ av maskininlärnings metod där en **_agent_** får **_rewards_** av sinna förra **_actions_** i ett **_environment_**.

### Environment & Agent
**_Environment_** är själva miljön som **_agenten_** agerar på. För spelet *Tic Tac Toe* är miljön "spel planen". För problemet *Taxi* är miljön "parkeringen". Och för detta *Market-environment* är miljön en "aktie". **_Environment_** skickar en **_state_** till **_agenten_** som med dess **_policy_** ska kunna ta en **_action_** baserad på vad det är för **_state_**. Sedan skickar **_environment_** det nästa **_state_** och en **_reward_** till **_agenten_** som används för att uppdatera **_policy_**. Denna loop avslutas när **_environment_** skickar en bool *Done*.
![png](docs/RL.png)

#### State, Action, Reward, Policy
**_Action_** är alla möjliga drag som **_agenten_** kan ta.

**_State_** är den nuvarande tillståndet som retunerades av **_environment_**.

**_Reward_** är en utvärdering av **_agentens_** förra **_action_**.

**_Policy_** är strategin som **_agenten_** använder för att bestämma nästa **_action_** baserad på det aktuella **_state_**. Typ **_agentens_** "kunskaper".


-Användning av Q-table som löser taxi problemet

-Användning av *** som löser cartpole problemet

-Testa använda båda och komma fram till vad som är bäst

-Argumentera för användningen av en marchove chain och varför det är bättre att se flera states

-Argumentera för olika Policys'. on policy / off policy. Även model-free / model-based.

-Argumentera för olika värden på gamma, alpha, beta etctra och varför det är bra att använda låg gamma i detta exempel. Tessta även med kod.

-Vad alla dessa har för effekter på algorythmen och varför du då använde x istället för y när du skulle lösa z.

# Grafer

### Avläsande av grafer
**_Blåa_** delen av grafen är *agentens* *observation* där den inte invisterar.

**_Gröna_** och **_röda_** markörer tyder på agentens gissning av *Short* och *Long* positioner. Förklarning för *Short* och *Long* finner du [Här](https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/stock-purchases-and-sales-long-and). **_Grön_** markör betyder att agenten gissade rätt och **_röd_** markör betyder att agenten gissade fel.

**_Totl Profit_** är multipliken av pengarna agenten började med. *Total Profit* på **2** betyder att agenten dubblade sin insats. Total Profit på **0.5** betyder att agenten förlorade halva sin insats.

**_max_possible_profit_** är den största möjliga multipliken av pengarna agenten började med.

**_Y-Axeln_** är värdet på aktsiens *["Close"]* värde, definition finner du [Här](https://www.investopedia.com/terms/c/closingprice.asp).

**_X-Axeln_** är indexen på [csv filerna](https://github.com/abbsimoga/Market-environment/tree/master/Market_environment/datasets). Ett steg i *X-Axeln* är en tidsperiod frammåt. För nerladdad data används [detta script](https://github.com/abbsimoga/Market-environment/blob/master/Data.py) där tidsperioden är i *Dygn*.

## Reflektion1
### Bild 1
Bilden nedan visar på *agentens* observation av marknadens flöde. När observationen **_det blå_** tydligt tyder på marknadens tillväxt använder *agenten* det till sin vinst se **_Total Profit_** i bild.
![png](docs/Capture3.JPG)

#### Bild 2:1
De två kommande bilder visar på när *agentens* observation inte håller sig konsistant under hela miljön. *Agenten* har under observationen lärt sig ett mönster och när det mönstret bryts på grund av aktsiers *"randomness"* vet inte *agenten* vad den ska göra och går i förlust se **_Total Profit_** i **Bild** **2:1** och **2:2**.
![png](docs/Capture1.JPG)

#### Bild 2:2
![png](docs/Capture2.JPG)

#### **_Slutsats1:1_** Agenten hittar lätt mönster på tydlig tillväxt och tillbakagång och kan använda det till sin vinst.

#### **_Slutsats1:2_** Agenten förstår sig inte på när mönstret bryts.

## Reflektion2
### Bild 3
Följande bild visar *medelvärde* av **tio** itterationer på följd som ger ett medelvinstvärde på **1.2935849431816784**
![png](docs/Capture7.JPG)

### Bild 4
Kommande bild visar på en körning av [Förra projektets](https://github.com/abbsimoga/Enstaka-programerings-projekt/tree/master/Enstaka_programering/StockMarket) *"AI"* som invisterade på måfå och visade tillväxt och tillbakagång på ca **+-5%**. Exact värde för denna körning = 21772/20000 = **1.0886**.
![png](docs/Capture4.JPG)

### Bild 5
Kommande bild visar på att invistering i aktsier *innom* **_sp500_** leder till *tillväxt* under **längre invisteringar**. Exact värde för **_engångsinvistering_** = 23625/20000 = **1.18125**
![png](docs/Capture6.JPG)

#### **_Slutsats2:1_** Jämförs dessa två *agenter* finner vi en tydlig förbättring vid användning av Q-Learning/RL-algorythmer.

#### **_Slutsats2:2_** Invistering i aktsier *innom* **_sp500_** leder till *tillväxt* under **_längre invisteringar_** betydligt bättre än min **_första_** agent men inte bättre än den **_nya_** som använder sig av Q-Learning ett typ av RL-algorythm.

## Framtida projekt

#### Använd flera aktsiers data för att minska förlusten vid stora dropp.
#### Göra fler tester av andra "policy" och "modell's"
#### Använd annan typ av RL-algorythm