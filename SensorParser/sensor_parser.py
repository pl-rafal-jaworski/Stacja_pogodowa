import sqlite3
import time
import datetime
import random

# import board
# import busio
# import adafruit_dht
# import adafruit_bmp280

import pms5003_lib


def db_init(db_path):
    conn = sqlite3.connect(db_path)

    create_table_pressure(conn)
    create_table_previous(conn)
    create_table_pm25(conn)
    create_table_temperature(conn)
    create_table_timestamp(conn)

    conn.close()

    print("Skonfigurowano bazę danych")


def create_table_pressure(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cisnienie (\n"
                   "	        wartosc	INTEGER,\n"
                   "	        id	INTEGER PRIMARY KEY AUTOINCREMENT\n"
                   ")")
    conn.commit()


def create_table_previous(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS historyczne (\n"
                   "	        id	INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                   "	        temp	INTEGER,\n"
                   "	        pm	INTEGER,\n"
                   "	        cisnienie	INTEGER,\n"
                   "	        timestamp	INTEGER\n"
                   ")")
    conn.commit()


def create_table_pm25(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pm25 (\n"
                   "        	wartosc	INTEGER,\n"
                   "        	id	INTEGER PRIMARY KEY AUTOINCREMENT\n"
                   ")")
    conn.commit()


def create_table_temperature(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS temp (\n"
                   "	        wartosc	INTEGER,\n"
                   "	        id	INTEGER PRIMARY KEY AUTOINCREMENT\n"
                   ")")
    conn.commit()


def create_table_timestamp(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS timestamp (\n"
                   "	        id	INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                   "	        updateTime	TEXT\n"
                   ")")
    conn.commit()


def update_previous(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT wartosc FROM temp ORDER BY id DESC LIMIT 1")
    temperature = cursor.fetchall()[0][0]

    cursor.execute("SELECT wartosc FROM pm25 ORDER BY id DESC LIMIT 1")
    pm25 = cursor.fetchall()[0][0]

    cursor.execute("SELECT wartosc FROM cisnienie ORDER BY id DESC LIMIT 1")
    pressure = cursor.fetchall()[0][0]

    cursor.execute("SELECT updateTime FROM timestamp ORDER BY id DESC LIMIT 1")
    timestamp = cursor.fetchall()[0][0]

    data = [temperature, pm25, pressure, timestamp]
    insert_data_previous(conn, data)

    conn.commit()


def insert_data_pressure(conn, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cisnienie(wartosc) VALUES (?)", data)
    conn.commit()

    print("Wysłano dane: {}".format(data))


def insert_data_previous(conn, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historyczne(temp, pm, cisnienie, timestamp) VALUES (?,?,?,?)", data)
    conn.commit()

    print("Wysłano dane: {}".format(data))


def insert_data_pm25(conn, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pm25(wartosc) VALUES (?)", data)
    conn.commit()

    print("Wysłano dane: {}".format(data))


def insert_data_temperature(conn, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temp(wartosc) VALUES (?)", data)
    conn.commit()

    print("Wysłano dane: {}".format(data))


def insert_data_timestamp(conn, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO timestamp(updateTime) VALUES (?)", data)
    conn.commit()

    print("Wysłano dane: {}".format(data))


def sensors_init(simulation):
    dht22 = None
    bmp280 = None
    pms5003 = None

    if not simulation:
        dht22 = adafruit_dht.DHT22(board.D10)
        print("Skonfigurowano czujnik DHT22")

        i2c = busio.I2C(board.SCL, board.SDA)
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

        # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # bmp_cs = digitalio.DigitalInOut(board.D10)
        # bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)

        bmp280.mode(adafruit_bmp280.MODE_FORCE)
        bmp280.overscan_temperature(adafruit_bmp280.OVERSCAN_X16)
        bmp280.overscan_pressure(adafruit_bmp280.OVERSCAN_X16)
        print("Skonfigurowano czujnik BMP280")

        pms5003 = pms5003_lib.PMS5003()
        pms5003.mode(pms5003_lib.MODE_PASSIVE)
        pms5003.state(pms5003_lib.SLEEP)
        print("Skonfigurowano czujnik PMS5003")
    else:
        print("Praca w trybie symulacji czujników\n\n")

    return dht22, bmp280, pms5003


def dht22_read(simulation, dht22):
    dht22_temp = None
    dht22_humidity = None

    if not simulation:
        try:
            dht22_temp = dht22.temperature
            dht22_humidity = dht22.humidity
        except RuntimeError as e:
            print("Błąd odczytu czujnika DHT22: {}".format(e.args))
    else:
        dht22_temp = 21.0 + (random.randint(-1, 1) * 0.1) + random.randint(-2, 2)
        dht22_humidity = 40.0 + (random.randint(-1, 1) * 0.1) + random.randint(-2, 2)

    print("Odczytano dane z czujnika DHT22: {}*C {}%".format(dht22_temp, dht22_humidity))

    return dht22_temp, dht22_humidity


def bmp280_read(simulation, bmp280):
    bmp280_temp = None
    bmp280_pressure = None

    if not simulation:
        temp_t = bmp280.temperature
        pressure_t = bmp280.pressure

        if temp_t is not None:
            bmp280_temp = bmp280.temperature
        else:
            print("Błąd odczytu czujnika BMP280: Temperatura")

        if 300 < pressure_t < 1100:
            bmp280_pressure = pressure_t
        else:
            print("Błąd odczytu czujnika BMP280: Ciśnienie")
    else:
        bmp280_temp = 21.0 + (random.randint(-1, 1) * 0.0003) + random.randint(-2, 2)
        bmp280_pressure = 1013.25 + (random.randint(-1, 1) * 0.16) + random.randint(-2, 2)

    print("Odczytano dane z czujnika BMP280: {}*C {}hPa".format(bmp280_temp, bmp280_pressure))

    return bmp280_temp, bmp280_pressure


def pms5003_read(simulation, pms5003):
    pm10 = None
    pm25 = None
    pm100 = None

    if not simulation:
        try:
            pms5003.read()

            pm10 = pms5003.pm10
            pm25 = pms5003.pm25
            pm100 = pms5003.pm100
        except RuntimeError as e:
            print("Błąd odczytu czujnika PMS5503: {}".format(e.args))
    else:
        pm10 = 42 + random.randint(-1, 1) + random.randint(-2, 2)
        pm25 = 62 + random.randint(-1, 1) + random.randint(-2, 2)
        pm100 = 80 + random.randint(-1, 1) + random.randint(-2, 2)

    print("Odczytano dane z czujnika PMS5003: PM1.0: {}ug/m3 PM2.5: {}ug/m3 PM10: {}ug/m3".format(pm10, pm25, pm100))

    return pm10, pm25, pm100


def main():
    simulation = True

    db_path = "../REST/database.db"

    pms5003_delay = 15
    dht22_delay = 5
    bmp280_delay = 5

    db_init(db_path)
    dht22, bmp280, pms5003 = sensors_init(simulation)

    minute = 0
    update_db = False

    while True:
        pm10 = None
        pm25 = None
        pm100 = None

        dht22_temp = None
        dht22_humidity = None

        bmp280_temp = None
        bmp280_pressure = None

        current_time = int(datetime.datetime.now().timestamp())

        print("Data: {} - {}\n".format(current_time, datetime.datetime.fromtimestamp(current_time)))

        if minute % pms5003_delay == 0:
            pm10, pm25, pm100 = pms5003_read(simulation, pms5003)

            conn = sqlite3.connect(db_path)

            insert_data_pm25(conn, [round(pm25, 1)])

            conn.close()

            update_db = True

        if minute % dht22_delay == 0:
            dht22_temp, dht22_humidity = dht22_read(simulation, dht22)

            # conn = sqlite3.connect(db_path)
            # insert_data_temperature(conn, [round(dht22_temp, 1)])
            # conn.close()

            # update_db = True

        if minute % bmp280_delay == 0:
            bmp280_temp, bmp280_pressure = bmp280_read(simulation, bmp280)

            conn = sqlite3.connect(db_path)

            insert_data_pressure(conn, [round(bmp280_pressure, 1)])
            insert_data_temperature(conn, [round(bmp280_temp, 1)])

            conn.close()

            update_db = True

        if update_db:
            conn = sqlite3.connect(db_path)

            insert_data_timestamp(conn, [current_time])
            update_previous(conn)

            conn.close()

            print("")

            update_db = False

        time.sleep(1)
        minute += 1


if __name__ == "__main__":
    main()
