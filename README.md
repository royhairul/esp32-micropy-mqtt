# ESP32 IoT Sensor dengan MQTT dan OLED

Proyek ini merupakan implementasi IoT menggunakan ESP32, sensor DHT11, OLED SSD1306, serta komunikasi dengan MQTT melalui broker HiveMQ.

## Perangkat Keras yang Digunakan
- ESP32
- Sensor DHT11
- OLED SSD1306 (I2C)
- LED merah dan kuning

## Koneksi Pin
| Perangkat    | Pin ESP32 |
|-------------|----------|
| DHT11       | GPIO 4   |
| OLED SCL    | GPIO 22  |
| OLED SDA    | GPIO 21  |
| LED Kuning  | GPIO 15  |
| LED Merah   | GPIO 18  |

## Konfigurasi MQTT
- **Broker**: HiveMQ (broker.hivemq.com)
- **Client ID**: ``
- **Topik Publish**: ``
- **Topik Subscribe**: ``

## Instalasi dan Penggunaan
### 1. Instalasi Library yang Dibutuhkan
Pastikan Anda memiliki pustaka berikut di dalam ESP32:
- `umqtt.simple`
- `network`
- `ssd1306`
- `dht`

### 2. Konfigurasi WiFi
Ganti bagian berikut dengan SSID dan password WiFi Anda:
```python
SSID = "YOUR_WIFI_SSID"      # Ganti dengan SSID WiFi
PASSWORD = "YOUR_WIFI_PASSWORD"   # Ganti dengan Password WiFi
```
