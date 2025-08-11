import pyodbc
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()


server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

try:
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'TrustServerCertificate=no;'
        'Encrypt=no;'
        f'UID={username};'
        f'PWD={password};'
    )
    cursor = cnxn.cursor()
    
except pyodbc.Error as e:
    raise ConnectionError(f"Failed to connect to the database: {e}")

def device_finder(address_device: str = '') :

    query = '''
    SELECT 
    Label.idAddress,
    COALESCE(Label.name, 'SIN DATO') AS label_name,
    COALESCE(Label.reference, 'SIN DATO') AS label_reference,
    COALESCE(Device.name, 'SIN DATO') AS device_name,
    COALESCE(Floor.name, 'SIN DATO') AS floor_name,
    COALESCE(Building.name, 'SIN DATO') AS building_name
    FROM Label
    LEFT JOIN Device ON Label.idDevice = Device.idDevice
    LEFT JOIN Floor ON Label.idFloor = Floor.idFloor
    LEFT JOIN Building ON Floor.idBuilding = Building.idBuilding
    WHERE Label.idAddress = ?
    '''

    # Ejecutar la consulta con parámetros
    cursor.execute(query, (address_device,))
    rows = cursor.fetchall()

    dict_device = {
        'Device' : '',
        'Label' : '',
        'Floor' : '',
        'Building' : '',
        'Reference' : ''
    }
    # Imprimir resultados
    for row in rows:
        dict_device['Device'] = row.device_name
        dict_device['Label'] = row.label_name
        dict_device['Floor']= row.floor_name
        dict_device['Building']= row.building_name
        dict_device['Reference']= row.label_reference
    
    return dict_device


def device_history(address_device: str = ''):
    
    query = """
    SELECT History.idHistory, History.idType, History.date, History.description, History.action, Type.name AS type_name
    FROM History
    
    INNER JOIN Type ON History.idType = Type.idType

    WHERE History.idAddress = ?
    """

    cursor.execute(query, (address_device,))
    rows = cursor.fetchall()
    

    history_dict = {
        'idHistory': [],
        'Type':[],
        'Date':[],
        'Description':[],
        'Action':[],
    }

    for row in rows:
        history_dict['idHistory'].append(row.idHistory)
        history_dict['Type'].append(row.type_name.rstrip())
        history_dict['Date'].append(row.date)
        history_dict['Description'].append(row.description)
        history_dict['Action'].append(row.action)

    return history_dict


def add_history(address_device: str = '',
                type_maintenance: str = '',
                date: datetime = None,
                description: str = '',
                action: str = ''):
    
    query = """
    INSERT INTO History (idAddress, idType, date, description, action)
    VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(query, (address_device, type_maintenance, date, description, action))
    cnxn.commit()
   

def delete_history(idHistory: int = 0):
    
    query = """
    DELETE FROM History
    WHERE History.idHistory = ?
    """

    cursor.execute(query, (idHistory,))
    cnxn.commit()

