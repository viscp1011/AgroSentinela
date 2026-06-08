# 🔌 Guia — 4 campos ao vivo no VS Code (1 ESP32, 4 sensores)

O ESP32 agora simula 4 CAMPOS (1 potenciômetro por cultura). Cada potenciômetro
controla um cartão diferente no painel. Só esses 4 campos aparecem.

## Ligações (já prontas no diagram.json)
- Potenciômetro 1 → GPIO34  (Campo da Soja)
- Potenciômetro 2 → GPIO35  (Campo do Milho)
- Potenciômetro 3 → GPIO32  (Várzea / Arroz)
- Potenciômetro 4 → GPIO33  (Sítio do Café)
- DHT22 → GPIO15 (temperatura/umidade do ar, compartilhado)

## Passo a passo
1. **Backend**: feche e reabra `RODAR_AGROSENTINELA.bat` (carrega o código novo).
2. **Recompile o ESP32**: rode `COMPILAR_ESP32.bat` de novo (o esp32.ino mudou!).
   A extensão do VS Code roda o firmware COMPILADO, não o .ino direto.
3. **Simule**: F1 → "Wokwi: Start Simulator" (pasta src/esp32 aberta).
   No serial deve aparecer 4 envios por ciclo:
   ```
   [campo-soja]  HTTP 200 | {...}
   [campo-milho] HTTP 200 | {...}
   [campo-arroz] HTTP 200 | {...}
   [campo-cafe]  HTTP 200 | {...}
   ```
4. **Painel**: abra `http://localhost:8000/app` e dê Ctrl+F5. Aparecem os 4 campos.
   **Arraste cada potenciômetro** → o cartão e os gráficos daquele campo mudam.
5. **Trocar cultura**: use o seletor dentro de cada cartão (a escolha do painel
   manda, mesmo que o ESP continue enviando outra).

## Importante
- Mudou o esp32.ino? Pare o simulador → `COMPILAR_ESP32.bat` → reabra o simulador.
- A URL do backend já está em `http://host.wokwi.internal:8000/api/leitura`.

## Plano B (sem Wokwi, à prova de falhas)
Com o backend no ar:
```
cd src/esp32
python enviar_leitura_teste.py --demo
```
Cria os mesmos 4 campos enviando o mesmo JSON que o ESP32 manda.
