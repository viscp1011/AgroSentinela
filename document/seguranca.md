# 🔐 Segurança — Red Team vs Blue Team (Cap. 9)

A natureza do AgroSentinela — dispositivos IoT no campo, API exposta e alertas
automáticos — cria uma superfície de ataque que precisa ser tratada. Esta seção
analisa as ameaças sob a ótica do **Red Team** (ataque) e as defesas do
**Blue Team** (proteção).

## Superfície de ataque

1. **Nó ESP32 no campo** — físico, conectividade Wi-Fi/celular.
2. **API FastAPI** — recebe leituras (`POST /api/leitura`) e serve dados.
3. **Infra AWS** — fila SQS, Lambda, SNS, DynamoDB.
4. **Canal de alerta (voz/SMS)** — entrega ao produtor.

## 🔴 Red Team × 🔵 Blue Team

| # | Ameaça (Red Team) | Defesa (Blue Team) |
|---|-------------------|--------------------|
| 1 | **Injeção de leituras falsas**: atacante envia ao `POST /api/leitura` valores forjados de umidade para forçar (ou suprimir) alertas e desperdiçar água. | Autenticação por **token/API key** por dispositivo; validação de faixa dos valores (umidade 0–0.6 m³/m³); **rate limiting**; assinatura HMAC do payload do ESP32. |
| 2 | **Spoofing do dispositivo**: clonar o `id_fazenda` de um nó legítimo. | Certificado/identidade única por dispositivo (**AWS IoT Core / mTLS**); rotação de credenciais; detecção de leituras duplicadas/impossíveis. |
| 3 | **DoS na API**: inundar a API com requisições e derrubar o serviço. | **API Gateway** com throttling, **WAF**, autoscaling serverless (Lambda), fila SQS para absorver picos (desacoplamento assíncrono). |
| 4 | **Interceptação de tráfego (MITM)**: ler/alterar dados entre ESP32 e backend. | **TLS/HTTPS** obrigatório fim a fim; rejeitar conexões em texto puro. |
| 5 | **Escalada de privilégio na nuvem**: comprometer a Lambda e acessar outros recursos. | **IAM com menor privilégio** (a Lambda só pode `sns:Publish` no tópico e `PutItem` na tabela — ver `template.yaml`); segregação de papéis; logs no CloudWatch. |
| 6 | **Vazamento de dados do produtor** (localização, contato). | Criptografia em repouso (DynamoDB/SNS KMS) e em trânsito; minimização de dados; conformidade com a **LGPD**. |
| 7 | **Phishing de alerta**: SMS/e-mail falso fingindo ser o AgroSentinela para enganar o produtor. | Remetente verificado e identidade consistente nas mensagens; orientação ao produtor; nunca pedir credenciais por SMS. |
| 8 | **Envenenamento do modelo (data poisoning)**: corromper o histórico para degradar a previsão do LSTM. | Validação e saneamento dos dados de treino; uso de fonte oficial (Open-Meteo); detecção de outliers; versionamento do dataset. |

## Boas práticas adotadas no projeto

- **Menor privilégio** explícito na policy IAM do `template.yaml`.
- **Desacoplamento assíncrono** (SQS) que aumenta a resiliência a picos/DoS.
- **Validação de schema** das leituras com Pydantic no FastAPI.
- **Sem segredos no código** (chaves/tokens via variáveis de ambiente).
- Recomendação de **TLS** e **API key por dispositivo** para produção.

## Conclusão de segurança

Mesmo sendo uma solução de baixo custo, o AgroSentinela trata segurança como
requisito de projeto, não como adendo. As defesas do Blue Team priorizam o que
tem maior impacto para o pequeno produtor: **integridade das leituras**
(para não desperdiçar água nem perder lavoura) e **privacidade dos dados**
(LGPD), apoiadas por uma arquitetura serverless que já nasce resiliente.
