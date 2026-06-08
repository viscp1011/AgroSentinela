/*
 * AgroSentinela - ESP32 com 4 NOS DE SENSOR (Wokwi) - Cap. POO com ESP32.
 * Um ESP32 simula 4 campos (1 potenciometro por cultura). Arraste cada
 * potenciometro para ver o cartao daquele campo mudar no painel.
 * Classes: SensorSolo (1 por pino) e NoDeCampo (1 por campo).
 * Ligacoes: pot1->GPIO34 (Soja), pot2->GPIO35 (Milho), pot3->GPIO32 (Arroz),
 *           pot4->GPIO33 (Cafe), DHT22->GPIO15 (compartilhado).
 * URL: VS Code -> http://host.wokwi.internal:8000 ; navegador -> tunel https.
 */
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include "DHT.h"

const char* WIFI_SSID   = "Wokwi-GUEST";
const char* WIFI_PASS   = "";
const char* URL_BACKEND = "http://host.wokwi.internal:8000/api/leitura";
#define PINO_DHT 15
#define TIPO_DHT DHT22
const unsigned long INTERVALO_MS = 4000;
DHT dht(PINO_DHT, TIPO_DHT);

class SensorSolo {
  private: uint8_t pino;
  public:
    SensorSolo(uint8_t p) : pino(p) {}
    void iniciar() { pinMode(pino, INPUT); }
    float lerUmidade() { return (analogRead(pino) / 4095.0) * 0.5; }
};

class NoDeCampo {
  private: SensorSolo solo; String id; String cultura;
  public:
    NoDeCampo(uint8_t pino, String idCampo, String cult) : solo(pino), id(idCampo), cultura(cult) {}
    void iniciar() { solo.iniciar(); }
    void publicar(float temperatura, float umidadeAr) {
      if (isnan(temperatura)) temperatura = 25.0;
      if (isnan(umidadeAr))   umidadeAr = 50.0;
      String json = "{";
      json += "\"id_fazenda\":\"" + id + "\",";
      json += "\"umidade_solo\":" + String(solo.lerUmidade(), 3) + ",";
      json += "\"temperatura\":" + String(temperatura, 1) + ",";
      json += "\"umidade_ar\":" + String(umidadeAr, 1) + ",";
      json += "\"cultura\":\"" + cultura + "\"";
      json += "}";
      if (WiFi.status() != WL_CONNECTED) return;
      HTTPClient http; String url = String(URL_BACKEND);
      if (url.startsWith("https")) {
        WiFiClientSecure cli; cli.setInsecure();
        http.begin(cli, url); http.addHeader("Content-Type", "application/json");
        http.addHeader("ngrok-skip-browser-warning", "true");
        int cod = http.POST(json); Serial.println("[" + id + "] HTTP " + String(cod) + " | " + json); http.end();
      } else {
        http.begin(url); http.addHeader("Content-Type", "application/json");
        int cod = http.POST(json); Serial.println("[" + id + "] HTTP " + String(cod) + " | " + json); http.end();
      }
    }
};

NoDeCampo campos[4] = {
  NoDeCampo(34, "campo-soja",  "soja"),
  NoDeCampo(35, "campo-milho", "milho"),
  NoDeCampo(32, "campo-arroz", "arroz"),
  NoDeCampo(33, "campo-cafe",  "cafe"),
};

void conectarWiFi() {
  Serial.print("[WiFi] Conectando"); WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.println(" conectado! IP: " + WiFi.localIP().toString());
}
void setup() {
  Serial.begin(115200); delay(500);
  Serial.println("AgroSentinela - 4 nos de sensor iniciando...");
  dht.begin();
  for (int i = 0; i < 4; i++) campos[i].iniciar();
  conectarWiFi();
}
void loop() {
  float t = dht.readTemperature(); float ar = dht.readHumidity();
  for (int i = 0; i < 4; i++) { campos[i].publicar(t, ar); delay(200); }
  delay(INTERVALO_MS);
}
