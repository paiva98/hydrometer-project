#include "esp_camera.h"       // esp32 use cammera
#include <WiFi.h>             // esp32 use Wifi
#include "camera_pins.h"      // esp32 pinout camera
#include <HTTPClient.h>       // http para enviar requisicoes

#define LED_BUILTIN 2         // Pino de LED

#define EAP_ANONYMOUS_IDENTITY ""
#define EAP_IDENTITY "<CPF>"
#define EAP_PASSWORD "<SENHA_SAPIES">"
#define SSID "WIFI-UFV2"

String urlAPI = "http://192.168.169.39:5000/send_image";  
String codigo = "3070";

HTTPClient http;              // Objeto http usado nas requisicoes

void conectWIFi(){
  // Loop para conetar a rede
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando-se à rede Wi-Fi...");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(2000); 
    digitalWrite(LED_BUILTIN, LOW);
    delay(2000);   
  }

  Serial.println("Conectado à rede Wi-Fi!");
}

void setCAM(){
  
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_UXGA;
  config.jpeg_quality = 10;
  config.fb_count     = 2;

  esp_err_t err = esp_camera_init(&config);
      
  if (err != ESP_OK) {
      Serial.printf("Falha ao inicializar a câmera 0x%x", err);
      return;
  }

  sensor_t * s = esp_camera_sensor_get();
  s->set_vflip(s, 1);  // Inverte a imagem verticalmente
  s->set_hmirror(s, 0); 
}

void setup() {

  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);

  // WiFi.begin(ssid, pass); // Define as configuracoes do wifi
  WiFi.begin(SSID, WPA2_AUTH_PEAP, EAP_ANONYMOUS_IDENTITY, EAP_IDENTITY, EAP_PASSWORD);
  conectWIFi();

  setCAM();
}

void loop() {
  delay(5000);
  /* 
   - Verificar se ainda está conectado.
   - Fica preso até conetar.
  */
  if(WiFi.status() != WL_CONNECTED){
    conectWIFi(); 
  }

  camera_fb_t *fb = esp_camera_fb_get();
  
  if (!fb) {
    Serial.println("Falha ao capturar a imagem");
  } else {
    Serial.println("Imagem capturada");
    
    http.begin(urlAPI); // Inicia a URL
    http.addHeader("Content-Type", "image/jpeg"); // Define o tipo de conteúdo
    http.addHeader("codigo", codigo); // Adiciona o código como um cabeçalho

    // Envia a requisição POST com a imagem
    int httpResponseCode = http.POST(fb->buf, fb->len);

    if (httpResponseCode > 0) {
      String response = http.getString(); // Obtém a resposta
      Serial.println(httpResponseCode); // Imprime o código de resposta HTTP
      Serial.println(response); // Imprime a resposta
    } else {
      Serial.print("Erro na requisição: ");
      Serial.println(httpResponseCode);
    }

    http.end(); // Finaliza a conexão
  }

  esp_camera_fb_return(fb);
}
