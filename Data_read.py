from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ExceptionResponse

# Configuration
MODBUS_SERVER_IP = '172.16.0.20' #Put your modbus IP address
MODBUS_PORT = 502
UNIT_ID = 1  # Slave ID

# Address ranges
ADDRESS_RANGES = [
    (0, 76),      # 0 to 75
    (250, 16),    # 250 to 265
]

def read_modbus_range(client, address, count):
    try:
        # Only keyword arguments allowed in pymodbus 3.x
        result = client.read_holding_registers(address=address, count=count, slave=UNIT_ID)

        if isinstance(result, ExceptionResponse):
            print(f"Modbus exception at address {address}: {result}")
            return None
        elif result.isError():
            print(f"Error reading at address {address}: {result}")
            return None
        else:
            return result.registers

    except Exception as e:
        print(f"Exception while reading: {e}")
        return None

def main():
    client = ModbusTcpClient(host=MODBUS_SERVER_IP, port=MODBUS_PORT)
    if not client.connect():
        print("Failed to connect to Modbus server.")
        return

    for address, count in ADDRESS_RANGES:
        print(f"\nReading {count} registers from address {address}...")
        data = read_modbus_range(client, address, count)
        if data:
            for i, val in enumerate(data):
                print(f"Address {address + i}: {val}")

    client.close()

if __name__ == "__main__":
    main()
