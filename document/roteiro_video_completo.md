# 🎬 Roteiro COMPLETO do vídeo — AgroSentinela
### Narração palavra por palavra + telas exatas

> **Como usar:** leia em voz alta o texto em **🗣️ FALA** e, ao mesmo tempo, faça o que está em **🖥️ TELA**.
> Duração total se ler tudo: ~6 min. Os blocos marcados **(OPCIONAL — cortar se passar de 5 min)** podem ser pulados.
>
> **Prepare antes (deixe tudo aberto em abas/janelas):**
> 1. Navegador no painel: `http://localhost:8000/app` (rode `scripts/RODAR_AGROSENTINELA.bat` antes).
> 2. VS Code com o **Wokwi** (simulação pronta) e com os arquivos `src/backend/modelo_lstm.py`,
>    `src/backend/algoritmo_genetico.py`, `src/esp32/esp32.ino`.
> 3. A imagem `assets/arquitetura.png` aberta.
> 4. O PDF `document/AgroSentinela_GlobalSolution_2026.pdf` na página de Resultados.
> No OBS: cena "Display Capture" + ative o **Desktop Audio** (para o alerta de voz entrar no vídeo).

---

## CENA 1 — Abertura (~25s)  [OBRIGATÓRIO no começo]
**🖥️ TELA:** Painel do AgroSentinela aberto (a tela com os campos), parado e bonito.

**🗣️ FALA:**
"Olá! Meu nome é Vitório Stevanatto, sou aluno da FIAP e represento o Grupo 14 na Global Solution.
E eu já começo com o mais importante: **QUERO CONCORRER**.
O projeto que eu vou te apresentar se chama **AgroSentinela** — e a ideia dele cabe numa frase:
é um agrônomo digital de plantão, de baixo custo, que ajuda o pequeno produtor rural a irrigar
na hora certa, com a quantidade certa de água, usando inteligência artificial."

---

## CENA 2 — O problema (~35s)
**🖥️ TELA:** Continue no painel, passando o mouse lentamente pelos cartões dos campos.

**🗣️ FALA:**
"Deixa eu te contar o problema que a gente resolve. O grande produtor já tem agricultura de
precisão: sensores, satélites, software. Mas o pequeno produtor, não. Ele irriga 'no escuro' —
ou joga água demais, e aí desperdiça água, energia elétrica do bombeamento e dinheiro; ou rega
de menos e descobre tarde demais que a lavoura entrou em estresse hídrico e a colheita já caiu.
Falta pra ele uma informação simples: 'preciso regar? quando? quanto?'. O AgroSentinela responde
exatamente essas três perguntas — e responde de um jeito que ele entende, inclusive por voz."

---

## CENA 3 — A ponte com a economia espacial (~25s)  (OPCIONAL — cortar se passar de 5 min)
**🖥️ TELA:** Painel, foco no cartão de clima (canto superior, "agora / tempo real").

**🗣️ FALA:**
"E onde entra a economia espacial, tema da Global Solution? Aqui: os dados que vêm do céu e do
espaço — clima, umidade do solo, imagens de satélite como o NDVI — só geram impacto na Terra
quando chegam, traduzidos em ação, na mão de quem planta. É a metáfora que guiou o projeto:
o 'drone barato de grande impacto'. Tecnologia simples e acessível, com efeito enorme no campo."

---

## CENA 4 — Arquitetura e integração das disciplinas (~45s)
**🖥️ TELA:** Abra a imagem `assets/arquitetura.png` em tela cheia. Acompanhe o fluxo com o cursor,
da esquerda para a direita, enquanto fala.

**🗣️ FALA:**
"Essa é a arquitetura completa, e ela mostra como o projeto integra todas as disciplinas da fase
num fluxo único. Começa no **ESP32**, o sensor no campo, programado em orientação a objetos.
Ele envia a leitura para o **backend em Python com FastAPI**, que junta esse dado com o **clima
real e gratuito da API Open-Meteo**. Esse conjunto alimenta a primeira IA, uma **rede neural LSTM**,
que prevê o risco hídrico. A previsão vai para a segunda IA, um **algoritmo genético**, que monta o
melhor plano de irrigação. Quando há risco, a **AWS serverless** — Lambda e SNS — dispara o alerta,
um **assistente de voz** comunica o produtor, e tudo aparece neste **painel**. Sensor, dados, duas
IAs, nuvem, voz e interface — todas as peças conversando."

---

## CENA 5 — Demonstração: o painel multi-campo (~30s)
**🖥️ TELA:** Volte ao painel `localhost:8000/app`. Mostre os 4 cartões de campos.

**🗣️ FALA:**
"Agora a demonstração prática. Aqui no painel eu tenho **vários campos ao mesmo tempo**, cada um
com o seu próprio sensor ESP32 e a sua cultura. Repare que cada cartão é bem direto, pensado para
o agricultor: tem o nome do campo, a cultura, um **semáforo** — verde quer dizer 'tudo certo',
vermelho quer dizer 'precisa de água' — uma barra com a umidade da terra, e um conselho em
linguagem simples, tipo 'regar tantos litros por metro quadrado'. Nada de jargão técnico."

---

## CENA 6 — As duas IAs nos gráficos (~50s)
**🖥️ TELA:** Clique num campo que esteja em risco (ex.: **Arroz**) para abrir os Detalhes.
Aponte o cursor para o primeiro gráfico enquanto explica, depois para o segundo.

**🗣️ FALA:**
"Quando eu abro um campo, eu vejo as duas inteligências artificiais trabalhando lado a lado.
Este primeiro gráfico é a **rede neural LSTM**, a IA número um. A linha mostra como a umidade do
solo deve evoluir nas próximas 24 horas, e essa faixa vermelha embaixo é a zona de risco: se a
linha entrar nela, a planta passa sede. O detalhe importante é que essa previsão **começa no valor
que o sensor está medindo agora** — ela reage ao campo de verdade.
Já este segundo gráfico é o **algoritmo genético**, a IA número dois. As barras azuis dizem
quanta água aplicar em cada hora — é o plano que gasta o **mínimo de água possível**. A linha
verde mostra a terra ficando saudável com esse plano, e a vermelha tracejada mostra como ela
ficaria se eu não fizesse nada. Dá pra ver o valor da otimização na hora."

---

## CENA 7 — Cada cultura tem uma sede diferente (~30s)
**🖥️ TELA:** No seletor de cultura do campo, troque de **Arroz** para **Mandioca** (ou Cana).
Mostre o número de "água recomendada" e os gráficos mudando.

**🗣️ FALA:**
"E o sistema entende que cada cultura é diferente. Olha o que acontece quando eu troco a cultura
deste campo: a recomendação de água muda na hora. O arroz, que é irrigado por inundação, pede
cerca de 40 milímetros; já a mandioca, que é rústica, pede quase nada. São as 10 culturas mais
plantadas do Brasil, cada uma com o seu alvo de umidade."

---

## CENA 8 — Wokwi ao vivo: o sensor de verdade (~40s)
**🖥️ TELA:** Vá para o **VS Code com o Wokwi** rodando. Mostre o ESP32 e os 4 potenciômetros.
**Arraste um potenciômetro para baixo**, simulando a terra secando. Mostre o serial enviando.
*(Plano B, se o Wokwi travar: abra um terminal e rode
`python src/esp32/enviar_leitura_teste.py 0.10 soja campo-soja`.)*

**🗣️ FALA:**
"E esse dado não é inventado — vem do sensor. Aqui no Wokwi eu tenho um ESP32 com quatro sensores,
um por campo. Cada potenciômetro é o sensor de umidade do solo de um campo. Quando eu arrasto este
potenciômetro para baixo, eu estou simulando a terra secando. Repare no terminal: o ESP32 está
enviando a leitura para o nosso backend, em tempo real."

---

## CENA 9 — O painel reage + alerta de voz (~35s)
**🖥️ TELA:** Volte ao painel e atualize (F5). Mostre o cartão daquele campo ficando **vermelho**.
Depois clique no botão **"🔊 Ouvir o aviso por voz"** e fique em silêncio enquanto o áudio toca.

**🗣️ FALA:**
"E o painel reage na hora: esse campo, que estava verde, agora ficou vermelho, em risco hídrico.
E é aqui que o projeto se completa — em vez de exigir que o produtor entenda gráficos, o sistema
**fala com ele**, em português:"
*(clique no botão e deixe a voz tocar até o fim)*

---

## CENA 10 — Por dentro do código (~50s)
**🖥️ TELA:** VS Code em `src/backend/modelo_lstm.py` — role até a função da arquitetura da rede.

**🗣️ FALA:**
"Rapidamente, por dentro. Esta é a IA número um, a rede neural LSTM, em TensorFlow. É uma rede
recorrente, que tem 'memória': ela olha as últimas 24 horas para prever as próximas. Foi treinada
com **17 mil horas de clima real** de Ribeirão Preto, e o erro de previsão ficou em apenas 0,01."

**🖥️ TELA:** Abra `src/backend/algoritmo_genetico.py`.
**🗣️ FALA:**
"Esta é a IA número dois, o algoritmo genético, com a biblioteca DEAP. Ele imita a seleção natural:
cria milhares de planos de rega, cruza e melhora os melhores, geração após geração, até achar o que
mantém a planta saudável gastando menos água — uma economia acima de 75%."

**🖥️ TELA:** Abra `src/esp32/esp32.ino`. (OPCIONAL: mostre `src/infra/template.yaml`.)
**🗣️ FALA:**
"E aqui o ESP32, em orientação a objetos, com as classes de sensor e de campo. A infraestrutura de
alertas é serverless na AWS, descrita em CloudFormation, com segurança por design e foco em LGPD."

---

## CENA 11 — Resultados e impacto + fechamento (~40s)  [OBRIGATÓRIO no fim]
**🖥️ TELA:** Abra o **PDF** na página de **Resultados** (ou o README). Depois pode voltar ao painel.

**🗣️ FALA:**
"Pra fechar, os resultados: dados climáticos reais, duas inteligências artificiais funcionando de
verdade, dez culturas suportadas, e mais de 75% de economia de água em relação a irrigar no escuro,
tudo numa arquitetura serverless de custo quase zero.
E o impacto é direto na vida do pequeno produtor: ele protege a colheita, economiza água e energia,
e passa a ter agricultura de precisão na palma da mão — com um simples aviso de voz.
Isso é o AgroSentinela: tecnologia simples e barata, de grande impacto no campo.
Muito obrigado pela atenção — e, de novo, **QUERO CONCORRER**!"

---

## ✅ Checklist final antes de subir o vídeo
- [ ] Disse "QUERO CONCORRER" no **início** e no **fim**.
- [ ] Mostrou: painel, troca de cultura, Wokwi/sensor, alerta de voz, código das 2 IAs.
- [ ] Áudio do sistema gravado (alerta de voz audível).
- [ ] Duração **abaixo de 5 minutos** (corte as cenas marcadas OPCIONAL se precisar).
- [ ] Postar no YouTube como **"não listado"** e entregar o link onde for pedido.
