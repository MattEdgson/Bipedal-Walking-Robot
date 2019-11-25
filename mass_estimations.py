# Program to calculate the Mass of Bipedal robot and location of the Centre of mass form set components

# Also calculates how much mass should be added as a 'Spinal mass' to shift the Centre of mass of the robot onto one foot for walking.

# dictionary of available components with name, x length(cm), y length(cm), mass(g)
components = {
    'arduino': [120, 30, 101],
    'spine': [20, 45, 60],
    'servo': [45, 20, 60],
    'battery': [50, 30, 45],
    'body': [120, 110, 165],
    'thigh': [45, 40, 30],
    'shin': [45, 40, 30],
    'foot': [50, 3, 10],
    'spinalMass': [0, 0, 0]
}

# Dictionary of components added to the robot assembly, appended using addComponent()
# component name:[x co-ordinates(cm), y co-ordinates(cm), mass(g), and x and y co-ordinates of the Centre of Mass (cm)]
robotComp = {
    'component': [],
    'x1': [],
    'x2': [],
    'y1': [],
    'y2': [],
    'mass': [],
    'mx': [],
    'my': []
}

# horizontal and vertical co-ordinates for component placement (cm)
hAnkle = components['foot'][1]
hShin = hAnkle + components['servo'][1]
hKnee = hShin + components['shin'][1]
hThigh = hKnee + components['servo'][1]
hHip = hThigh + components['thigh'][1]
hBody = hHip + components['servo'][1]
hSpine = hBody + components['battery'][1]
hAda = hSpine + components['spine'][1]
wSecondLeg = components['body'][0] - components['shin'][0]
wSecondBattery = components['body'][0] - components['battery'][0]
wSecondFoot = components['body'][0] - components['foot'][0]
wSpine = components['battery'][0]


# list of components needed with x and y co-ordinates of where they've been placed (cm)
compNeeded = [
    ['foot', 0, 0],
    ['servo', 0, hAnkle],
    ['shin', 0, hShin],
    ['servo', 0, hKnee],
    ['thigh', 0, hThigh],
    ['servo', 0, hHip],
    ['body', 0, hBody],
    ['battery', 0, hBody],
    ['spine', wSpine, hSpine],
    ['arduino', 0, hAda],
    ['battery', wSecondBattery, hBody],
    ['foot', wSecondFoot, 0],
    ['servo', wSecondLeg, hAnkle],
    ['shin', wSecondLeg, hShin],
    ['servo', wSecondLeg, hKnee],
    ['thigh', wSecondLeg, hThigh],
    ['servo', wSecondLeg, hHip]
]


# Adds a requested component to a dictionary of components called robotComp() in order of component name:[x co-ordinates(cm), y co-ordinates(cm), mass(g), and x and y co-ordinates of the Centre of Mass (cm)]
def addComponent(robotList):
    name = robotList[0]
    x = robotList[1]
    y = robotList[2]
    listComp = list(components.keys())
    name = str(name)
    if not (name in listComp):
        print('Please enter a component from one of:')
        for i in listComp:
            print('    ' + i)
        return
    dx = components[name][0]
    dy = components[name][1]

    index = 0
    for i in robotComp['component']:
        if (name in i) and not (name == i):
            if (int(i[-1:]) >= index):
                index = ((int(i[-1:])) + 1)
        elif (name in i) and (name == i):
            robotComp['component'][robotComp['component'].index(i)] = name + '1'
            index = 2

    if index > 0:
        robotComp['component'].append(name + str(index))
    else:
        robotComp['component'].append(name)

    robotComp['x1'].append(x)
    robotComp['x2'].append(x + dx)
    robotComp['y1'].append(y)
    robotComp['y2'].append(y + dy)
    robotComp['mass'].append(components[name][2])
    robotComp['mx'].append(x + (0.5 * dx))
    robotComp['my'].append(y + (0.5 * dy))

    return (robotComp)


# Finds mass of assembly(g), x and y co-ordinates of the Centre of Mass (cm)
def centreOfMass(compDict):
    listComp = compDict['component']
    massTotal = 0
    massByDistanceX = 0
    massByDistanceY = 0

    for component in listComp:
        i = listComp.index(component)
        massByDistanceX += compDict['mass'][i] * compDict['mx'][i]
        massByDistanceY += compDict['mass'][i] * compDict['my'][i]
        massTotal += compDict['mass'][i]

    comX = massByDistanceX / massTotal
    comY = massByDistanceY / massTotal
    return (massTotal, comX, comY)


# calculates how much mass is needed to shift the CoM onto one foot (g)
def findSpine(components, massInfo):
    massTotal = massInfo[0]
    xTotal = massInfo[1]
    xM = (components['foot'][0])
    xS = xM / 2
    massSpineMin = massTotal * (xM - xTotal) / (xS - xM)
    return (massSpineMin)


def robotCom(robotStuff):  # iterates through list of requested components using addComponent() to create dictionary, then finds mass information
    for i in robotStuff:
        addComponent(i)

    # Mass of robot assembly before adding Spinal Mass
    massInfoBefore = centreOfMass(robotComp)
    print(massInfoBefore)

    # Mass of spinal mmass required to shift CoM onto one foot
    spineMass = round(findSpine(components, massInfoBefore))
    print(spineMass)

    totalMass = massInfoBefore[0] + spineMass

    components['spinalMass'][2] = spineMass

    # Adds New Spinal Mass to robot
    addComponent(['spinalMass', massInfoBefore[1], hSpine])
    massInfoAfter = centreOfMass(robotComp)  # Generates new Mass information
    print(massInfoAfter)

    return(massInfoAfter)


robotCom(compNeeded)
