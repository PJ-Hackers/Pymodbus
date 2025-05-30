# Pymodbus Scripts

Simple Python scripts to read from and write to Modbus devices using the `pymodbus` library.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/PJ-Hackers/Pymodbus.git
cd Pymodbus
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Scripts

Open either `Read_data.py` or `Change_data.py` in any text editor.

* Replace the **IP address** with your Modbus device’s IP
* Set the **Modbus unit ID**, **register address**, and other required values

### 4. Run the Scripts

To **read data** from a Modbus device:

```bash
python read_data.py
```

To **write data** to a Modbus device:

```bash
python change_data.py
```
