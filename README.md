# Cert Yeeter 9000

My roommate, despite being a highly paid defense contractor and electrical engineer, gets his microcontrollers from his sock drawer and refuses to spend the two cents on an ESP32. So naturally the temperature sensors in our house are ESP8266 based and the InfluxDB Arduino library for these doesn't support any sort of proper SSL/TLS and they recommend you HARD CODE YOUR CERT FINGERPRINTS.

This is an API so these things can pull my SHA1 cert fingerprint on boot instead of having to rip these off the walls every 90 days to change it manually.