print("Importing libraries....")

import os
import sys

sys.path.append(os.getcwd())    #embedable python doesnt find local modules without this line

import time
import threading
import numpy as np
from scipy.spatial.transform import Rotation as R
import openvr
import tkinter as tk

moveThr = 0.1
moveMax = 0.2

rotThr = 0.3
rotMax = 0.5

def gui_thread():
    
    global moveThr, moveMax, rotThr, rotMax
    
    def save():
        print("Saved parameters")
        moveThr = mtVar.get()
        moveMax = mmVar.get()
        rotThr = rtVar.get()
        rotMax = rmVar.get()

    print("new thread started")
    window = tk.Tk()

    mtVar = tk.DoubleVar(value = moveThr)
    tk.Label(text="Move threshold", width = 50).pack()
    mt = tk.Scale(length=300,from_=0,to=1, digits=3,variable=mtVar,resolution=0.01, orient=tk.HORIZONTAL)
    mt.pack()
    
    mmVar = tk.DoubleVar(value = moveMax)
    tk.Label(text="Move maximum", width = 50).pack()
    mm = tk.Scale(length=300,from_=0,to=1, digits=3,variable=mmVar,resolution=0.01, orient=tk.HORIZONTAL)
    mm.pack()
    
    rtVar = tk.DoubleVar(value = rotThr)
    tk.Label(text="Rotation threshold", width = 50).pack()
    rt = tk.Scale(length=300,from_=0,to=1, digits=3,variable=rtVar,resolution=0.01, orient=tk.HORIZONTAL)
    rt.pack()
    
    rmVar = tk.DoubleVar(value = rotMax)
    tk.Label(text="Rotation maximum", width = 50).pack()
    rm = tk.Scale(length=300,from_=0,to=1, digits=3,variable=rmVar,resolution=0.01, orient=tk.HORIZONTAL)
    rm.pack()
    
    tk.Button(text='Save', command=save).pack()
    
    window.mainloop()

def sendToSteamVR(text):
    #Function to send a string to my steamvr driver through a named pipe.
    #open pipe -> send string -> read string -> close pipe
    #sometimes, something along that pipeline fails for no reason, which is why the try catch is needed.
    #returns an array containing the values returned by the driver.
    try:
        pipe = open(r'\\.\pipe\ApriltagPipeIn', 'rb+', buffering=0)
        some_data = str.encode(text)
        pipe.write(some_data)
        resp = pipe.read(1024)
    except:
        return ["error"]
    string = resp.decode("utf-8")
    array = string.split(" ")
    pipe.close()
    
    return array

def SendMove(x, y, rx, ry, a, b):
    return sendToSteamVR(" hipmoveinput " +
    str(x) + " " + 
    str(y) + " " + 
    str(rx) + " " + 
    str(ry) + " " + 
    str(a) + " " + 
    str(b))
    
def convert_steam_vr_matrix(pose):
    return np.array((
        (pose[0][0], pose[1][0], pose[2][0], 0.0),
        (pose[0][1], pose[1][1], pose[2][1], 0.0),
        (pose[0][2], pose[1][2], pose[2][2], 0.0),
        (pose[0][3], pose[1][3], pose[2][3], 1.0),
    ), dtype=np.float32)
 
print("Connecting to SteamVR")

gui = threading.Thread(target=gui_thread)
gui.start()

time.sleep(1)

handle = openvr.init(openvr.VRApplication_Overlay)

sendToSteamVR("addhipmove")

m_actionAnalongInput = openvr.k_ulInvalidActionHandle;
m_actionsetDemo = openvr.k_ulInvalidActionHandle;
m_actionPose = openvr.k_ulInvalidActionHandle;

openvr.VRInput().setActionManifestPath(os.getcwd()+"/bindings/hiplocomotion_actions.json")

m_actionAnalongInput = openvr.VRInput().getActionHandle("/actions/demo/in/AnalogInput")
m_actionPose = openvr.VRInput().getActionHandle("/actions/demo/in/Tracker")
m_actionsetDemo = openvr.VRInput().getActionSetHandle('/actions/demo')

trackerRotation = 0
hmdPosition = [ 0,0 ]
hmdRotation = 0

offsetHmd = 0
offsetHip = 0

centerHmd = [ 0,0 ]

recalibrate = True

print("Hip locomotion started!")

time.sleep(1)

counter = 0

neckOffset = np.array([ 0,-0.1,0.1,1 ])

while True:
    hmd_pose = convert_steam_vr_matrix(handle.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding,0,[])[0].mDeviceToAbsoluteTracking)
    #print(hmd_pose)
    hmdRotation = np.arctan2(hmd_pose[0][2],hmd_pose[2][2])
    
    hmd_pos = np.dot(neckOffset,hmd_pose)
    
    #print(hmd_pos)
    hmdPosition = [hmd_pos[0],hmd_pos[2]]
    
    action_sets = (openvr.VRActiveActionSet_t * 1)()
    action_set = action_sets[0]
    action_set.ulActionSet = m_actionsetDemo
    openvr.VRInput().updateActionState(action_sets)
    
    analog_data = openvr.VRInput().getAnalogActionData(m_actionAnalongInput, openvr.k_ulInvalidInputValueHandle)
    if not analog_data.bActive:
        time.sleep(0.1)
        recalibrate = True
        SendMove(0,0,0,0,0,0)
        continue
    
    pose_data = openvr.VRInput().getPoseActionDataForNextFrame(
        m_actionPose,
        openvr.TrackingUniverseStanding,
        openvr.k_ulInvalidInputValueHandle,
    )
    """if not pose_data.bActive:
        print(pose_data.bActive)
        time.sleep(0.1)
        continue"""
        
    tracker_pose = convert_steam_vr_matrix(pose_data.pose.mDeviceToAbsoluteTracking)
    trackerRotation = np.arctan2(tracker_pose[0][2],tracker_pose[2][2])

    if recalibrate:
        offsetHip = trackerRotation
        offsetHmd = hmdRotation
        centerHmd = [hmdPosition[0],hmdPosition[1]]
        recalibrate = False
        
    hmdPosition[0] -= centerHmd[0]
    hmdPosition[1] -= centerHmd[1]
    
    magnitude = np.sqrt(hmdPosition[0]**2 + hmdPosition[1]**2)
    angle = np.arctan2(hmdPosition[0],hmdPosition[1])
    
    newDataX = 0
    newDataY = 0
    
    if(magnitude > moveThr):
        newDataX = np.sin(angle+hmdRotation) * (magnitude-moveThr)/(moveMax-moveThr)
        newDataY = np.cos(angle+hmdRotation) * (magnitude-moveThr)/(moveMax-moveThr)

    angleRot = trackerRotation - offsetHip
    
    if angleRot > 3.14:
        angleRot -= 6.28
    if angleRot < -3.14:
        angleRot += 6.28
    
    newDataRx = 0
    
    if abs(angleRot) > rotThr:
        newDataRx = (abs(angleRot)-rotThr)/(rotMax-rotThr)
        newDataRx /= -abs(angleRot)/angleRot
     
    print("Sending data: " + str(newDataX) + ", " + str(newDataY) + ", rotation: " + str(newDataRx))

    print(SendMove(newDataX,newDataY,newDataRx, 0, 0, 0))

    time.sleep(0.02)
    
    if not gui.is_alive():
        break
