# !/usr/bin/python

"""
Task 2: repeat task 1 topology, with car0 simultaneous bicasting (eNodeB1+RSU1, eNodeB2+RSU1)
"""

import os
import time
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI

import sys
gnet=None

# Store metrics here
c0_throughput0 = 'c0_throughput0.data'          # car0 throughput phase 1
client_throughput0 = 'client_throughput0.data'	# client throughput phase 1
c0_throughput1 = 'c0_throughput1.data'          # car0 throughput phase 2
client_throughput1 = 'client_throughput1.data'  # client throughput phase 2
c0_throughput2 = 'c0_throughput2.data'          # car0 throughput phase 3
client_throughput2 = 'client_throughput2.data'  # client throughput phase 3

c0_latency0 = 'c0_latency0.data'		        # car0 latency phase 1
c0_latency1 = 'c0_latency1.data'		        # car0 latency phase 2
c0_latency2 = 'c0_latency2.data'		        # car0 latency phase 3

c0client_iperf0 = 'c0client_iperf0.data'	    # car0-client phase 1    
c0client_iperf1 = 'c0client_iperf1.data'	    # car0-client phase 2
c0client_iperf2 = 'c0client_iperf2.data'	    # car0-client phase 3

c0_latency0 = 'c0_latency0.data'		        # car0 latency phase 1
c0_latency1 = 'c0_latency1.data'		        # car0 latency phase 2
c0_latency2 = 'c0_latency2.data'		        # car0 latency phase 3

c0client_iperf0 = 'c0client_iperf0.data'	    # car0-client phase 1
c0client_iperf1 = 'c0client_iperf1.data'	    # car0-client phase 2
c0client_iperf2 = 'c0client_iperf2.data'	    # car0-client phase 3

# Implement the graphic function in order to demonstrate the network measurements
def graphic():
    plt.clf()    # clear current figure

    # Throughput
    for j in range(0,3):	

        f1 = open('./' + 'client_throughput' + str(j) + '.data', 'r')
        f1_lines = f1.readlines()
        f1.close()

        f2 = open('./' + 'c0_throughput' + str(j) + '.data', 'r')
        f2_lines = f2.readlines()
        f2.close()

        rx = []
        d_rx = []
        tx = []
        d_tx = []
        time_rx = []
        time_tx = []

        i = 0
        #read line by line
        for x in f1_lines:    
            p = x.split()	
            t = p[1].split(':')
            rx.append(int(t[1]))   # get RX bytes
            if len(rx) > 1:
                d_rx.append(rx[i] - rx[i - 1])
            i += 1

        i = 0
        for x in f2_lines:    
            p = x.split()
            t = p[5].split(':')
            tx.append(int(t[1]))   # get TX bytes
            if len(tx) > 1:
                d_tx.append(tx[i] - tx[i - 1])
            i += 1

        # create time axes
        i = 0
        for x in range(len(d_tx)):    
            time_tx.append(i)
            i = i + 0.5

        i = 0
        for x in range(len(d_rx)):    
            time_rx.append(i)
            i = i + 0.5
        
        fig = plt.figure(figsize=(16,6))    # start a figure
        g = fig.add_subplot(121)            # add 1st subfigure
        g.plot(time_rx, d_rx)
        plt.xlabel('Time')
        plt.ylabel('Bytes')
        plt.ylim([-100, 100000])
        plt.title('Client - RX')

        b = fig.add_subplot(122)            # add 2nd subfigure
        b.plot(time_tx, d_tx)
        plt.xlabel('Time')
        plt.ylabel('Bytes')
        plt.ylim([-100, 100000])
        plt.title('Car0 - TX')

        plt.savefig('Plot_Throughput_phase' + str(j) + '.png')
        plt.clf()

    # Latency
    for j in range(0,3):
        f1 = open('./' + 'c0_latency' + str(j) + '.data', 'r')
        f1_lines = f1.readlines()
        f1.close()

        lat = []
        time = []
        i = 1
        fl =  len(f1_lines) - 5
        while i <= fl:  
            x = f1_lines[i]  
            p = x.split()
            t = p[6].split('=')
            lat.append(float(t[1]))
            i = i +1
        i = 1
        for x in range(len(lat)):    
            time.append(i)
            i = i + 1
        
        plt.plot(time,lat)
        plt.xlabel('Time (ms)')
        plt.ylabel('Ping number')
        plt.savefig('Plot_Latency_phase' + str(j) + '.png')
        plt.clf()

    # Jitter and Packet Loss
    for j in range(0,3):
        time_jitter = []
        time_loss = []
        jitter = []
        loss =[]
        f1 = open('./' + 'c0client_iperf' + str(j) + '.data', 'r')
        f1_lines = f1.readlines()
        f1.close()
        i = 7
        while i < len(f1_lines):
            x = f1_lines[i] 
            p = x.split()
            l = len(p)
            if l > 12:
                t = p[l-1].split('%')
                t2 = t[0].split('(')
                loss.append(float(t2[1]))
                jitter.append(float(p[l-5]))
            i = i + 1
        i = 1
        for x in range(len(loss)):    
            time_loss.append(i)
            i = i + 1
        i = 1
        for x in range(len(jitter)):    
            time_jitter.append(i)
            i = i + 1
        plt.plot(time_jitter,jitter)
        plt.xlabel('Iperf number')
        plt.ylabel('Jitter (ms)')
        plt.savefig('Plot_Jitter_phase' + str(j) + '.png')
        plt.clf()
        plt.plot(time_loss,loss)
        plt.xlabel('Iperf number')
        plt.ylabel('Packet Loss (%)')
        plt.savefig('Plot_PacketLoss_phase' + str(j) + '.png')
        plt.clf()
    print "ready"    

def apply_experiment(car,client,switch):
    
    taskTime = 20

    #time.sleep(2)
    print "Applying first phase"

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')  # eNodeB1 to client
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')  # client to eNodeB1
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')      # eNodeB2 drop
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')      # RSU1 drop

    car.cmd('ip route add 200.0.10.2 via 200.0.10.100')		

    # car latency
    car.cmd('ping 200.0.10.2  -c 20 >> %s &' % c0_latency0)     # latency phase 1

    # car-client iperf
    client.cmd('iperf -s -u -i 1 >> %s &' % c0client_iperf0)    # iperf metrics phase
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # car-client throughput
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:        # RX and TX data phase 1
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' % c0_throughput0)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' % client_throughput0)
            i += 0.5

    print "Moving node"
    car.moveNodeTo('100,100,0')

    #time.sleep(2)
    print "Applying second phase"

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')   # eNodeB1 to client  
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')   # RSU1 to client
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1,3') # client to eNodeB1 & RSU1
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')       # eNodeB2 drop
    
    # car latency
    car.cmd('ping 200.0.10.2  -c 20 >> %s &' % c0_latency1)     # latency phase 2

    # car-client iperf
    client.cmd('iperf -s -u -i 1 >> %s &' % c0client_iperf1)    # iperf metrics phase
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # car-client throughput
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:        # RX and TX data phase 2
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' % c0_throughput1)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' % client_throughput1)
            i += 0.5
   
   # print "*** Running CLI"
   # CLI(gnet)

    print "Moving nodes"
    car.moveNodeTo('150,100,0')

    #time.sleep(2)
    print "Applying third phase"

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')      # eNodeB1 drop
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')  # eNodeB2 to client
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')  # RSU1 to client 
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')# client to eNodeB2 & RSU1

    car.cmd('ip route del 200.0.10.2 via 200.0.10.100')       # delete previous phase's routings
	
    # car latency
    car.cmd('ping 200.0.10.2  -c 20 >> %s &' % c0_latency2)    # latency phase 3

    # car-client iperf
    client.cmd('iperf -s -u -i 1 >> %s &' % c0client_iperf2)   # iperf metrics phase 3
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # car-client throughput
    timeout = time.time() + taskTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break;
        if time.time() - currentTime >= i:        # store RX and TX data phase 3
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' % c0_throughput2)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' % client_throughput2)
            i += 0.5

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car0 = net.addCar('car%s' % (0), wlans=2, ip='10.0.0.%s/8' % (0 + 1), \
    mac='00:00:00:00:00:0%s' % 0, mode='b')


    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=50)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    client.cmd('ifconfig client-eth0 200.0.10.2')
    car0.cmd('modprobe bonding mode=3')
    car0.cmd('ip link add bond0 type bond')
    car0.cmd('ip link set bond0 address 02:01:02:03:04:08')
    car0.cmd('ip link set car0-eth0 down')
    car0.cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
    car0.cmd('ip link set car0-eth0 master bond0')
    car0.cmd('ip link set car0-wlan0 down')
    car0.cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car0.cmd('ip link set car0-wlan0 master bond0')
    car0.cmd('ip link set car0-wlan1 down')
    car0.cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car0.cmd('ip link set car0-wlan1 master bond0')
    car0.cmd('ip addr add 200.0.10.100/24 dev bond0')
    car0.cmd('ip link set bond0 up')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Stream video using VLC
    car0.cmdPrint("sudo vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    client.cmdPrint("sudo vlc rtp://@200.0.10.2:5004 &")

    car0.moveNodeTo('65,100,0')

    os.system('ovs-ofctl del-flows switch')

    time.sleep(3)

    apply_experiment(car0,client,switch)

    # Generate graph
    graphic()

    # kills all the xterms that have been opened
    #os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
