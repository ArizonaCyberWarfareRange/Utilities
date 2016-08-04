import MySQLdb
import sys

# get teh variablea
host = sys.argv[1]
mac = sys.argv[2]
isMetal = sys.argv[3]
ip = sys.argv[4]

if isMetal == "y":
	isMetal = "Y"
else:
	isMetal = "N"


mac = mac.replace(":","")
DCID = "AZ01"

def GetNewNodeID():
	NodeID = 0

	sql = "select max(NodeID) + 1 from Nodes"
	nRows = curupd.execute(sql)
	if nRows > 0:
		trow = curupd.fetchone()
		NodeID = trow[0]

	sql = "select max(NodeID) + 1 from VirtualNodes"
	nRows = curupd.execute(sql)
	if nRows > 0:
		trow = curupd.fetchone()
		if trow[0] > NodeID:
			NodeID = trow[0]

	return NodeID


#Open the Database and get the device settings
db = MySQLdb.connect("71.216.236.10", "root", "ncr1pt", "azcwr")
db.autocommit(True)
cursor = db.cursor()
curupd = db.cursor()

# add the machine
if isMetal == "N":
	# Add the mac
	sql = "select * from rMACToNode where sMAC = '" + str(mac) + "'"
	nRows = cursor.execute(sql)
	if nRows < 1:
		# Get a new node id
		NodeID = GetNewNodeID()
		print "New NodeID: " + str(NodeID)

		# Add the Node
		sql = "insert into VirtualNodes values('" + DCID + "'," + str(NodeID) + ",'" + host + "',0,0,0,'new vm','',now(),now(),0)"
		print sql
		curupd.execute(sql)

		sql = "insert into rMACToNode values(" + str(NodeID) + ",'unknown','" + str(mac) + "',now(),0)"
		print sql
		curupd.execute(sql)

		if (ip <> "-"):
			sql = "insert into rIPToNode values(" + str(NodeID) + ",'eth0','" + str(ip) + "','255.255.0.0',now(),now(),0)"
			print sql
			curupd.execute(sql)
	else:
		print "This mac already exists!"
else:
        # Add the mac
        sql = "select * from rMACToNode where sMAC = '" + str(mac) + "'"
        nRows = cursor.execute(sql)
        if nRows < 1:
                # Get a new node id
                NodeID = GetNewNodeID()
                print "New NodeID: " + str(NodeID)

                # Add the Node
                sql = "insert into Nodes values('" + DCID + "'," + str(NodeID) + ",'" + host + "',0,0,0,'new vm','',now(),now(),0)"
                print sql
                curupd.execute(sql)

                sql = "insert into rMACToNode values(" + str(NodeID) + ",'unknown','" + str(mac) + "',now(),0)"
                print sql
                curupd.execute(sql)

                if (ip <> "-"):
                        sql = "insert into rIPToNode values(" + str(NodeID) + ",'eth0','" + str(ip) + "','255.255.0.0',now(),now(),0)"
                        print sql
                        curupd.execute(sql)
        else:
                print "This mac already exists!"

# close connections
curupd.close()
cursor.close()
db.close()

