from langchain_community.tools import tool
# from crewai_tools import tool
import oracledb

@tool("connectToDB")
def connectToDB():
    "Connect to Oracle DB"
    # conn=oracledb.connect('SYS',1, 'Bamboo@1', 'localhost', '1521', 'xe')
    conn = oracledb.connect(
            user = 'SYS',
            mode = oracledb.AUTH_MODE_SYSDBA,
            password = 'Bamboo@1',
            host = 'localhost',
            port = '1521',
            sid = 'xe'  
    )
    return conn

@tool("executeSqlQuery")
def executeSqlQuery(sql):
    "Execute SQL Query and return the results" 
    # conn=connectToDB.connectToDB('SYS',1, 'Bamboo@1', 'localhost', '1521', 'xe')
    conn = oracledb.connect(
        user = 'SYS',
        mode = oracledb.AUTH_MODE_SYSDBA,
        password = 'Bamboo@1',
        host = 'localhost',
        port = '1521',
        sid = 'xe'  
    )
    cursor = conn.cursor()
    print("SQL ---> ", sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

                               