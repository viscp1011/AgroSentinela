# 🎬 Roteiro do vídeo — AgroSentinela (até 5 min)

> Legenda: **[TELA]** = o que mostrar no OBS · **[FALA]** = o que dizer.
> Antes de gravar: deixe abertos -> (1) o painel em http://localhost:8000/app,
> (2) o Wokwi no VS Code com a simulação pronta, (3) o VS Code nos arquivos do código,
> (4) o PDF/README. No OBS, crie uma cena de "Captura de Tela" (Display Capture).

---

## 0:00 – 0:20 · Abertura (OBRIGATÓRIO no início)
**[TELA]** Painel do AgroSentinela aberto (a tela bonita dos campos).
**[FALA]**
"Olá! Eu sou o Vitório, do Grupo 14, e essa é a minha Global Solution: o **AgroSentinela**.
E já começo dizendo: **QUERO CONCORRER**.
O AgroSentinela é um ajudante de irrigação de baixo custo, com inteligência artificial,
para o pequeno produtor rural."

## 0:20 – 0:55 · O problema e a solução (o pitch)
**[TELA]** Continue no painel, passando o mouse pelos cartões dos campos.
**[FALA]**
"O pequeno produtor irriga no escuro: ou joga água demais, desperdiçando água e energia,
ou descobre tarde que a lavoura secou. O AgroSentinela resolve isso unindo um sensor barato,
dados de clima reais de satélite e **duas inteligências artificiais** que dizem, de forma
simples e por voz, **se, quando e quanto irrigar** cada cultura."

## 0:55 – 1:30 · Integração das disciplinas (arquitetura)
**[TELA]** Abra a imagem `assets/arquitetura.png` (ou a seção do README/PDF com o diagrama).
**[FALA]**
"O projeto integra todas as disciplinas da fase num fluxo único: o **ESP32** mede o campo;
o **backend em Python com FastAPI** junta com o clima real da Open-Meteo; uma **rede neural
LSTM** prevê o risco hídrico; um **algoritmo genético** otimiza a rega; a **AWS serverless**
dispara o alerta; um **assistente de voz** avisa o produtor; e tudo aparece no **painel**."

## 1:30 – 3:15 · DEMONSTRAÇÃO PRÁTICA (a parte mais importante)
**[TELA]** Painel `localhost:8000/app`, mostrando os 4 campos.
**[FALA]** "Aqui estão vários campos ao mesmo tempo, cada um com um sensor ESP32 e uma cultura
diferente. Cada cartão mostra um semáforo: verde, tudo certo; vermelho, precisa de água."

**[TELA]** Clique num campo (ex.: Arroz) para abrir os detalhes; mostre os dois gráficos.
**[FALA]** "Ao abrir um campo, vejo as duas IAs trabalhando. Este gráfico é a **rede neural LSTM**:
ela prevê como a terra vai secar; a faixa vermelha é a zona de risco. Este outro é o
**algoritmo genético**: as barras azuis são o plano de rega que gasta o mínimo de água."

**[TELA]** Troque a cultura do campo no seletor (ex.: de Arroz para Mandioca) e mostre os números mudando.
**[FALA]** "E cada cultura tem uma sede diferente. Olha: trocando a cultura, a recomendação de
água muda na hora — o arroz pede muita água, a mandioca quase nada."

**[TELA]** Vá ao Wokwi no VS Code, inicie/mostre a simulação e **arraste um potenciômetro** para baixo.
(Plano B, se o Wokwi falhar: num terminal rode `python src/esp32/enviar_leitura_teste.py 0.10 soja campo-soja`.)
**[FALA]** "Esse dado vem do sensor de verdade. Quando eu mexo no potenciômetro do ESP32,
simulando a terra secando..."

**[TELA]** Volte ao painel (atualize) e mostre o cartão ficando vermelho / o alerta aparecendo.
**[FALA]** "...o painel reage na hora: o campo entra em risco e o sistema gera o alerta."

**[TELA]** Clique no botão **"Ouvir o aviso por voz"** e deixe o áudio tocar.
**[FALA]** "E o produtor é avisado por voz, em português — acessível pra quem não tem
familiaridade com telas." (deixe a voz falar)

## 3:15 – 4:10 · Por dentro do código (as 2 IAs)
**[TELA]** VS Code abrindo `src/backend/modelo_lstm.py` (mostre a arquitetura da rede).
**[FALA]** "Por dentro: a IA 1 é uma rede neural recorrente LSTM, treinada com **17 mil horas
reais** de clima de Ribeirão Preto, com erro de só **0,01**."
**[TELA]** Abra `src/backend/algoritmo_genetico.py`.
**[FALA]** "A IA 2 é um algoritmo genético: ele testa milhares de planos de rega e escolhe o
que mantém a planta saudável gastando menos água — economia acima de **75%**."
**[TELA]** Abra `src/esp32/esp32.ino` rapidamente.
**[FALA]** "O ESP32 é programado em orientação a objetos, com quatro sensores, e a infraestrutura
de alertas é serverless na AWS, com CloudFormation."

## 4:10 – 5:00 · Resultados, impacto e fechamento
**[TELA]** PDF na página de Resultados (ou o README).
**[FALA]**
"Os resultados: dados reais, duas IAs funcionando, dez culturas suportadas e mais de 75% de
economia de água. O impacto é direto: o pequeno produtor protege a colheita, economiza água e
energia, e ganha agricultura de precisão com custo quase zero.
Isso é o AgroSentinela: tecnologia simples e barata, de grande impacto no campo.
Obrigado — e **QUERO CONCORRER**!"

---

## ✅ Checklist antes de gravar
- [ ] Backend rodando (`scripts/RODAR_AGROSENTINELA.bat`) e painel aberto.
- [ ] Wokwi pronto (ou o script de teste à mão como plano B).
- [ ] Volume do PC ligado (para o alerta de voz tocar).
- [ ] Falar "QUERO CONCORRER" no começo E no fim.
- [ ] Manter abaixo de 5 minutos.
- [ ] Postar no YouTube como **"não listado"** e colar o link onde a entrega pedir.

## 💡 Dicas de OBS
- Cena única "Display Capture" já resolve; ou crie cenas separadas (Painel / Wokwi / VS Code / PDF) e troque com atalhos.
- Grave o áudio do sistema (Desktop Audio) para o alerta de voz entrar no vídeo.
- Faça um teste de 20s antes para conferir áudio e nitidez do texto.
