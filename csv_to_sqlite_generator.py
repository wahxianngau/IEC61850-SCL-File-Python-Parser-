#-------------------------------------------------------------------------------
# Name:        Webmon Generator
# Purpose:     To generate webmon.db files
#
# Author:      10098468 Ngau Wah Xian
#
# Created:     10-07-2018
# Copyright:   (c) 10098468 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sqlite3
def main():

    #Creating SQLite Table
    OutputDirectory = "WebMon_ATWR_090818.db"
    conn = sqlite3.connect(OutputDirectory)
    c = conn.cursor()

    #-------------------------------For application Table------------------------------------
    c.execute('''CREATE TABLE if not exists application
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE, path TEXT, params NUMERIC)''')

    InputDirectory = "webmon_application_csv.csv"
    f = open(InputDirectory)

    iterf = iter(f)
    next(iterf)

    data = []
    for line in iterf:
        data_line = line.rstrip().split(',')
        data.append(data_line)
        # Insert a row of data
        c.execute("INSERT INTO application VALUES ('"+ data_line[0]+"','"+ data_line[1]+"','"+data_line[2]+"','"+data_line[3]+"')")

        # Save (commit) the changes
        conn.commit()

    #-------------------------------For Process Table-----------------------------------------------
    c.execute('''CREATE TABLE if not exists process
                    (id INTEGER PRIMARY KEY, application NUMERIC, param1 TEXT, param2 TEXT, param3 TEXT, param4 TEXT, param5 TEXT, param6 TEXT, param7 TEXT, param8 TEXT, param9 TEXT, param10 TEXT, active NUMERIC, alias text NOT NULL DEFAULT name);''')
    #c.execute("CREATE UNIQUE INDEX if not exists tag_index ON tags (name)")

    InputDirectory = "webmon_process_csv.csv"
    f = open(InputDirectory)

    iterf = iter(f)
    next(iterf)

    data = []
    for line in iterf:
        data_line = line.rstrip().split(',')
        data.append(data_line)
        # Insert a row of data
        c.execute("INSERT INTO process VALUES ('"+ data_line[0]+"','"+ data_line[1]+"','"+data_line[2]+"','"+data_line[3]+"','"+data_line[4]+"','"+data_line[5]+"','"+data_line[6]+"','"+data_line[7]+"','"+data_line[8]+"','"+data_line[9]+"','"+data_line[10]+"','"+data_line[11]+"','"+data_line[12]+"','"+data_line[13]+"')")

        # Save (commit) the changes
        conn.commit()


##    conn.close()
    #print len(data_line)
    print "Done!"

if __name__ == '__main__':
    main()
