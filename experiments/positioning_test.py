import sys, getopt
import socket
import json
import pymysql
import jsonpickle
sys.path.insert(0,'..')
from calc import distance
from utils import Interval
import numpy as np
from positioning.positioning import Tag, Node, Position
from calc import multilateration as multi
from calc import distance
from utils import setup

DB_ENABLED = False
DB_TABLE = "position_testing"
GRAPH_ENABLED = True
SAMPLES_FOR_EACH_UPDATE = 20
NUMBER_OF_NODES_TO_USE = 8
POSITION_DIMENSIONS = 3
LOG_DISTANCE_ST_DEV = 2.0

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 11001

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 10000

listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listenSocket.bind((LISTEN_IP, LISTEN_PORT))

broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

if DB_ENABLED:
    # Open database connection
    db = pymysql.connect(host = "localhost", user = "root", passwd = "admin", db = "positioning", port = 3306, cursorclass = pymysql.cursors.DictCursor)

    # Prepare a cursor object using cursor() method
    cursor = db.cursor()
    print("Connected to database")

# Server info (IP and port no.) is broadcasted at regular intervals
def sendServerInfo(ip):
    message = "CONTROL_COMMAND:" + chr(10) + chr(32) + "position_server: " + ip + ":" + str(LISTEN_PORT)
    broadcastSocket.sendto(message.encode(), (BROADCAST_IP, BROADCAST_PORT))

def main(argv):
    global GRAPH_ENABLED
    global DB_ENABLED
    label = None
    totalCounter = 0
    allPositions = list()
    setupEnable = False

    opts, args = getopt.getopt(argv,"cdfghils:o",["channel=", "database=", "filter=", "graph=", "ip=", "label=", "setup="])
    del(args)

    if len(opts) == 0:
        print("A label must be set for the test to start: filter_test.py --label '<label>'")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("A label must be set for the test to start: filter_test.py --label '<label>'")
            sys.exit()
        elif opt in ("-i", "--ip"):
            ip = arg
            print(ip)
        elif opt in ("-l", "--label"):
            label = arg
            print("Label for test: ", label)
        elif opt in ("-g", "--graph"):
            GRAPH_ENABLED = True
        elif opt in ("-d", "--database"):
            DB_ENABLED = True
        elif opt in ("-s", "--setup"):
            if str(arg) == "true":
                setupEnable = True
            else :
                setupEnable = False
        else:
            print("A label must be set for the test to start: filter_test.py --label '<label>'")
            sys.exit(2)

    if not label:
        print("A label must be set for the test to start: filter_test.py --label '<label>'")
        sys.exit(2)
    '''
    nodes = dict()
    nodes["b0:cf:4e:01:80:c1"] = Node(nodeID="b0:cf:4e:01:80:c1", x=3.27, y=3.46, z=0)
    nodes["b0:79:35:85:23:cd"] = Node(nodeID="b0:79:35:85:23:cd", x=1.16, y=7.95, z=0)
    nodes["b0:b8:11:7d:73:91"] = Node(nodeID="b0:b8:11:7d:73:91", x=1.16, y=3.46, z=0)
    nodes["b0:eb:88:71:90:e8"] = Node(nodeID="b0:eb:88:71:90:e8", x=1.16, y=5.87, z=0)
    nodes["b0:94:07:73:96:1e"] = Node(nodeID="b0:94:07:73:96:1e", x=0, y=6.97, z=0)
    nodes["b0:44:d6:f0:48:65"] = Node(nodeID="b0:44:d6:f0:48:65", x=3.27, y=5.75, z=0)
    nodes["b0:c3:af:19:3d:a0"] = Node(nodeID="b0:c3:af:19:3d:a0", x=3.85, y=1.34, z=0)
    nodes["b0:46:26:d6:60:14"] = Node(nodeID="b0:46:26:d6:60:14", x=1.53, y=1.27, z=0)
    '''
   
    interval = Interval.Interval(2, sendServerInfo, args=[ip,])
    print("Starting positioning test... Press CTRL + C to stop.")
    interval.start() 

    if setupEnable:
        setupConfig = dict()
        setupConfig["listenSocket"] = listenSocket
        setupConfig["broadcastSocket"] = broadcastSocket

        nodes = setup.setupNodes(setupConfig, fromFile=False) 
    else:
        nodes = setup.setupNodes(None, fromFile=True) 

        
    tags = dict()

    if GRAPH_ENABLED:
        import matplotlib.pyplot as plt
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.axis([-3, 10, -3, 10])

        ax.set_aspect(1)
        ax.grid(color='#cccccc', linestyle='-', linewidth=1)

    while True:
        try:
            rawData, addr = listenSocket.recvfrom(1024)
            data = json.loads(rawData)

            if not "nodeID" in data:
                continue

            ip = addr[0]
            nodeID = data['nodeID']
            timestamp = data['timestamp']
            address = data['address']
            rssi = data['RSSI']
            crc = data['CRC']
            lpe = data['LPE']
            counter = data['counter']
            syncController = data['syncController']
            channel = data['channel']

            if crc == 0 or lpe == 1:
                continue

            if nodeID not in nodes: 
                continue
            
            if address not in nodes[nodeID].tags: 
                nodes[nodeID].tags[address] = Tag(address)
                nodes[nodeID].tags[address].currentCounter = counter
                nodes[nodeID].tags[address].currentCounterAdvCount  = 0
                if address not in tags:
                    tags[address] = (1, 1, 1)

            nodes[nodeID].tags[address].rssi.append(rssi) 
            if nodes[nodeID].tags[address].currentCounter == counter:
                nodes[nodeID].tags[address].currentCounterAdvCount += 1
                if DB_ENABLED:
                    sql = "INSERT INTO %s VALUES(NULL, NULL, '%s', '%s', %d, '%s', %d, %d, %d, NULL, %d, NULL, %d, %d, %d, '%s')" % (DB_TABLE, nodeID, ip, timestamp , address, channel, counter, rssi, 0, crc, lpe, syncController, label)
            else:
                nodes[nodeID].tags[address].currentCounter = counter
                nodes[nodeID].tags[address].currentCounterAdvCount = 1

                selectedChannelRssi = max(nodes[nodeID].tags[address].rssi)

                nodes[nodeID].tags[address].kalman.predict()
                nodes[nodeID].tags[address].kalman.update(selectedChannelRssi)
                filteredRssi = nodes[nodeID].tags[address].kalman.x[0]
                nodes[nodeID].tags[address].filteredRssi = filteredRssi   
                nodes[nodeID].tags[address].rssi = list()         
            
                if DB_ENABLED:
                    sql = "INSERT INTO %s VALUES(NULL, NULL, '%s', '%s', %d, '%s', %d, %d, %d, %f, %d, NULL, %d, %d, %d, '%s')" % (DB_TABLE, nodeID, ip, timestamp , address, channel, counter, rssi, filteredRssi, 0, crc, lpe, syncController, label)

            if DB_ENABLED:
                cursor.execute(sql)
                db.commit()
            
            if totalCounter > 0 and totalCounter % 24 == 0:
                totalCounter += 1
                if GRAPH_ENABLED:
                    ax.cla()
                    ax.set_xlim((-5, 10))
                    ax.set_ylim((-5, 15))
                    plt.grid()
                
                for tagAddress in tags:
                    positions = list()
                    color = 'k'

                    for _, node in nodes.items():
                        x = node.position.x
                        y = node.position.y
                        z = node.position.z
                                       
                        # Log-distance path loss model      
                        node.tags[tagAddress].distance = round(distance.logDistancePathLoss(node.tags[tagAddress].filteredRssi, rssi_d0=-38.0, d0=1.0, n=2.6, stDev=LOG_DISTANCE_ST_DEV), 2)

                        radius = node.tags[tagAddress].distance
                        positions.append((x, y, z, radius))

                        if GRAPH_ENABLED:
                            circle = plt.Circle((x, y), radius=radius, color=color, alpha=0.1)
                            center = plt.Circle((x, y), radius=0.1, color='r', alpha=1)
                            
                            ax.add_patch(circle)
                            ax.add_patch(center)
                    
                    if len(positions) >= NUMBER_OF_NODES_TO_USE:
                        sortedPositions = sorted(positions, key=lambda x: x[3])
                        estimatedPosition = multi.multilateration(sortedPositions[:NUMBER_OF_NODES_TO_USE], dimensions=POSITION_DIMENSIONS)
                        allPositions.append(estimatedPosition)
                        tags[tagAddress] = estimatedPosition

                        print(estimatedPosition)
                    
                        if GRAPH_ENABLED:
                            positionIndicator = plt.Circle(estimatedPosition, radius=0.20, color="b", alpha=1)
                            ax.add_patch(positionIndicator)

                if GRAPH_ENABLED:
                    plt.draw()
                    plt.pause(0.0001)

        except KeyboardInterrupt:
            print("Shutting down interval...")
            interval.stop()
            if GRAPH_ENABLED:

                ax.cla()
                ax.set_xlim((-5, 10))
                ax.set_ylim((-5, 15))
                plt.grid()
                for _, node in nodes.items():
                    x = node.position.x
                    y = node.position.y
                    z = node.position.z
                    center = plt.Circle((x, y), radius=0.1, color='r', alpha=1)
                    ax.add_patch(center)

                x = list()
                y = list()
                
                for position in allPositions:
                    x.append(position[0])
                    y.append(position[1])

                    plt.plot(x, y, '-', color='b', alpha=0.1)

                plt.draw()
                plt.pause(0.0001)
                input("Press enter to exit")
            break

if __name__ == "__main__":
   main(sys.argv[1:])
