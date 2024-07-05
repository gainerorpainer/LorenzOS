#include "storage.h"

namespace LOS::Storage
{
    StorageHandler::StorageHandler()
    {
        Serial.println("Loading EEPROM data...");

        EEPROM.begin(sizeof(PermanentData_t));
        EEPROM.get(0, Data);

        if (getCrc(Data.WifiConfig) != Data.WifiCRC)
        {
            Serial.println("WifiConfig CRC err, defaults have been restored");
            // load default WifiConfig and store into eprom
            WifiConfig = WifiConfig_t{};
            storeToEEprom();
        }

        Serial.println("Wifi Config:");
        Serial.println("\tSSID: " + Data.WifiConfig.SSID.asStr());
        Serial.println("\tPW: " + Data.WifiConfig.Password.asStr());
        Serial.println("\tHostname: " + Data.WifiConfig.HostName.asStr());
    }

    void StorageHandler::storeToEEprom()
        {
            // refresh crc
            Data.ParametersCRC = getCrc(Data.__parameter_data);
            Data.WifiCRC = getCrc(Data.WifiConfig);

            EEPROM.put(0, Data);
            EEPROM.commit();
        }
}