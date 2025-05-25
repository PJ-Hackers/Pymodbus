import time
from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ExceptionResponse

# Configuration
MODBUS_SERVER_IP = '172.16.0.20'  #Change with your modbus server address
MODBUS_PORT = 502
UNIT_ID = 1  # Slave ID

# Address ranges
ADDRESS_RANGES = [
    (0, 76),      # 0 to 75
    (250, 16),    # 250 to 265
]

def read_modbus_range(client, address, count):
    try:
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

def set_zero(client, address, count):
    # Temporarily set the registers to 0
    print(f"Setting {count} registers at address {address} to 0...")
    zero_values = [0] * count
    result = client.write_registers(address, zero_values, slave=UNIT_ID)
    if result.isError():
        print(f"Error setting zero at address {address}")
    else:
        print(f"Successfully set registers at address {address} to 0")

def restore_stable(client, address, original_values):
    # Restore the original values after modification
    print(f"Restoring original values at address {address}...")
    result = client.write_registers(address, original_values, slave=UNIT_ID)
    if result.isError():
        print(f"Error restoring original values at address {address}")
    else:
        print(f"Successfully restored original values at address {address}")

def main():
    client = ModbusTcpClient(host=MODBUS_SERVER_IP, port=MODBUS_PORT)
    if not client.connect():
        print("Failed to connect to Modbus server.")
        return

    for address, count in ADDRESS_RANGES:
        print(f"\nReading {count} registers from address {address}...")
        original_values = read_modbus_range(client, address, count)

        if original_values:
            # Override with 0 every second
            start_time = time.time()
            while time.time() - start_time < 90:
                set_zero(client, address, count)  # Set to zero every second
                time.sleep(1)  # Wait for 1 second

            # After 1 minute, restore the original values
            restore_stable(client, address, original_values)

    client.close()

if __name__ == "__main__":
    main()
