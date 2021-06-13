#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     To generate rtdb files
#
# Author:      10098468
#
# Created:     10-07-2018
# Copyright:   (c) 10098468 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sqlite3
def main():

    #Creating SQLite Table
    OutputDirectory = "rt_ATWR_V2_report3.db"
    conn = sqlite3.connect(OutputDirectory)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists tags
                     (text TEXT, event, jitter, driver, expression, name, type, category, value, archive, param1, param2, param3, param4, param5, param6, param7, param8, protocol, instrument, active)''')
    c.execute("CREATE UNIQUE INDEX if not exists tag_index ON tags (name)")


    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.


    InputDirectory = "rtdb_csv_Report3.csv"
    f = open(InputDirectory)

    iterf = iter(f)
    next(iterf)

    data = []
    for line in f:
        data_line = line.rstrip().split(',')
        data.append(data_line)
        # Insert a row of data
        c.execute("INSERT INTO tags VALUES ('"+ data_line[0]+"','"+ data_line[1]+"','"+data_line[2]+"','"+data_line[3]+"','"+data_line[4]+"','"+data_line[5]+"','"+data_line[6]+"','"+data_line[7]+"','"+data_line[8]+"','"+data_line[9]+"','"+data_line[10]+"','"+data_line[11]+"','"+data_line[12]+"','"+data_line[13]+"','"+data_line[14]+"','"+data_line[15]+"','"+data_line[16]+"','"+data_line[17]+"','"+data_line[18]+"','"+data_line[19]+"','"+data_line[20]+"')")

        # Save (commit) the changes
        conn.commit()


##    conn.close()
    #print len(data_line)
    print "Done!"

if __name__ == '__main__':
    main()
