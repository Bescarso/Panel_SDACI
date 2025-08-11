import socket
import pyodbc

# Parámetros de conexión
SERVER = "localhost"  # o "localhost\\SQLEXPRESS"
PORT = 1433           # puerto típico de SQL Server
DATABASE = "SDACI"
USERNAME = "sa"
PASSWORD = "Blacksuede123*"

def check_sql_service(server, port):
    print(f"🔍 Probando conexión al puerto {port} en {server}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((server, port))
        print("✅ Puerto abierto: SQL Server está escuchando en la red.")
        return True
    except socket.error as e:
        print(f"❌ No se puede conectar al puerto {port} en {server}: {e}")
        return False
    finally:
        sock.close()

def test_pyodbc_connection():
    print("🔍 Probando conexión con pyodbc...")
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER},{PORT};"
            f"DATABASE={DATABASE};"
            "Encrypt=no;"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};",
            timeout=5
        )
        print("✅ Conexión a SQL Server exitosa con pyodbc.")
        conn.close()
    except pyodbc.InterfaceError as e:
        print("❌ Error de interfaz ODBC (posible driver incorrecto o no instalado):", e)
    except pyodbc.OperationalError as e:
        print("❌ Error de conexión (credenciales, base de datos o configuración de SQL Server):", e)

if __name__ == "__main__":
    if check_sql_service(SERVER, PORT):
        test_pyodbc_connection()


check_sql_service(SERVER, PORT)
test_pyodbc_connection()