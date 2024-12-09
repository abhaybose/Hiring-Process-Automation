import oracledb

def connectToDB(user, mode,  password, host, port, sid):
    try:
        if mode == 1:
            privilege = oracledb.AUTH_MODE_SYSDBA
        if mode == 2:
            privilege = oracledb.AUTH_MODE_SYSOPER
        if mode == 3:
            privilege = oracledb.AUTH_MODE_SYSASM

            
            
            
        conn = oracledb.connect(
            user = user,
            mode = oracledb.AUTH_MODE_SYSDBA,
            password = password,
            host = host,
            port = port,
            sid = sid  
        )
        return conn
    except oracledb.Error as e:
        print(e)
        return None