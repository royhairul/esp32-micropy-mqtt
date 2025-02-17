from machine import Pin, SoftI2C
from umqtt.simple import MQTTClient
import network
import dht
import time
import ssd1306

# KONFIGURASI WIFI
SSID = "YOUR_WIFI_SSID"      # Ganti dengan SSID WiFi
PASSWORD = "YOUR_WIFI_PASSWORD"   # Ganti dengan Password WiFi

# MQTT Server Parameters
MQTT_CLIENT_ID = ""
MQTT_BROKER = ""
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB = ""
MQTT_TOPIC_SUB = ""

# Inisialisasi OLED (SSD1306)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Inisialisasi Sensor DHT11
dht_pin = Pin(4)
dht_sensor = dht.DHT11(dht_pin)

# Inisialisasi LED
led_yellow = Pin(15, Pin.OUT)
led_red = Pin(18, Pin.OUT)

# Menyimpan Data Terakhir
last_temp = None
last_humidity = None

# Fungsi Modular untuk Menampilkan Informasi di OLED
def update_display(title, line1="", line2="", line3=None):
    oled.fill(0)  # Bersihkan layar
    oled.text(title, 0, 0)  # Judul utama
    oled.text(line1, 0, 20)  # Baris pertama
    oled.text(line2, 0, 35)  # Baris kedua
    if line3:
        oled.text(line3, 0, 50)  # Baris opsional ketiga
    oled.show()

# Fungsi Koneksi WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    update_display("WiFi", "Menghubungkan...", "", "")
    
    max_retries = 10
    while not wlan.isconnected() and max_retries > 0:
        time.sleep(1)
        max_retries -= 1
        print("Mencoba koneksi...")

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"Terhubung ke WiFi! IP: {ip}")

        update_display("WiFi Tersambung!", f"SSID: {SSID}", f"IP: {ip}")
        time.sleep(2)
    else:
        print("Gagal terhubung ke WiFi!")
        update_display("WiFi Gagal!", "Periksa SSID/Pass", "Coba lagi...")
        time.sleep(2)

# MQTT Message Callback
def message_callback(topic, msg):
    print("Message received on topic {}: {}".format(topic, msg.decode()))
    if msg.decode() == "turn_on":
        led_red.on()
        print("LED turned ON")
    elif msg.decode() == "turn_off":
        led_red.off()
        print("LED turned OFF")
    else:
        print("Unknown command:", msg.decode())

# Connect to MQTT Broker
def connect_mqtt():
    print("Connecting to MQTT server... ", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(message_callback)
    client.connect()
    print("Connected!")
    
    client.subscribe(MQTT_TOPIC_SUB)
    print("Subscribed to topic:", MQTT_TOPIC_SUB)
    return client

# Sambungkan ke WiFi saat boot
connect_wifi()

client = connect_mqtt()

# Loop Utama
while True:
    try:
        # Proses pesan MQTT yang masuk
        client.check_msg()

        dht_sensor.measure()  # Ambil data sensor
        suhu = dht_sensor.temperature()
        kelembaban = dht_sensor.humidity()

        if suhu != last_temp or kelembaban != last_humidity:
            led_yellow.on()
            time.sleep(0.5)
            led_yellow.off()

            print(f"Suhu: {suhu:.1f}°C | Kelembaban: {kelembaban:.1f}%")
            update_display("DHT11 Sensor", f"Suhu: {suhu:.1f}C", f"Kelembaban: {kelembaban:.1f}%")

             # Kirim data ke MQTT
            message = f"Suhu: {suhu:.1f}C | Kelembaban: {kelembaban:.1f}%"
            client.publish(MQTT_TOPIC_PUB, message)

            last_temp = suhu
            last_humidity = kelembaban

    except OSError as e:
        print("Gagal membaca sensor!", e)
        update_display("Sensor Error!")

    time.sleep(1)