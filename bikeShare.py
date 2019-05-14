'''

Bike Sharing Final Implementation
Programmer: Baadshah Verma
Date: November 30, 2018

This program is an application that will manage the bikes available for a bike sharing
network. The user is able to rent/return a bike at different stations and has some more functionality
as shown in getUserRequirements()

'''

import urllib.request
from math import *

def getAllStationData():
    
    '''This function reads in the data 'bikes.txt' from the webpage and it stores it within a nested
    dictionary. The key is the stationID and the values are the rest of the attributes. It will return
    this nested dictionary for use in other functions.'''

    response = urllib.request.urlopen("http://research.cs.queensu.ca/home/cords2/bikes.txt")
    html = response.readline()  #reads one line

    # initialize dictionary
    data = {}

    # iterate through txt file
    for i in range(0, 198):
        
        html = response.readline()  #reads one line
        line = html.decode('utf-8').split("\t")   #splits this line into a list

        # initialize inner dict
        inner_dict = {}

        # fill inner dict
        inner_dict['Name'] = line[1]
        inner_dict['Lat'] = float(line[2])
        inner_dict['Lon'] = float(line[3])
        inner_dict['Capacity'] = int(float(line[4]))
        inner_dict['Bikes Available'] = int(float(line[5]))
        inner_dict['Docks Available'] = int(float(line[6][:-2]))
        
        data[line[0]] = inner_dict    
            
    return data

def getUserRequirements():

    '''Function asks the user what they would like to do before proceeding (4 options).
    It will return the value received from user as an int.'''

    print('Please look at the options below and enter the number you would like to continue with \n ')
    
    print('''
(1) Show all information about a particular station

(2) Check if a bike available at a particular station. If so, how many bikes are
available? (If available, would you like to rent? If not, provide directions to nearest station)

(3) List all stations that have bikes available and rent bike from one of these stations

(4) List all stations that are not filled to capacity and return bike to one of these stations
''')
    
    while True:
        userRequirement = int(input("Please enter the number you would like to proceed with: "))
        if userRequirement in (1, 2, 3, 4):
            break
        else:
            print("The option you entered is invalid.")       
    return userRequirement

def retrieveStationID(data):

    '''Asks the user for the station ID that they would like to rent/return from.
    This function returns the stationID entered by the user.'''

    #ask user for stationID while error checking. If invalid stationID, reprompt
    while True:
        userStationID = input("Please input the station ID that you would like to rent/return from : ")
        if userStationID in data:
            break
        else:
            print("The stationID you entered was invalid.")
    return userStationID

def specificStationData(data, userStationID):
    '''This function will print all data about a specific station given the userStationID and dictionary'''

    print(data[userStationID])

def trackRentals(data, userStationID):
    '''This function will account for the rental. It will select the 'Bikes Available' attribute and subtract 1
    and add 1 to the 'Docks Available' attribute within the dictionary. It will return the updated dictionary.'''
    
    data[userStationID]['Bikes Available'] -= 1
    data[userStationID]['Docks Available'] += 1
    
    print("Thank you for renting your bike")
    return data #updated dictionary

def trackReturns(data, userStationID):
    '''This function will account for the return. It will select the 'Bikes Available' attribute and add 1
    and subtract 1 from the 'Docks Available' attribute within the dictionary. It will return the updated dictionary.'''

    data[userStationID]['Bikes Available'] += 1
    data[userStationID]['Docks Available'] -= 1
    
    print("Thank you for returning your bike")
    return data #updated dictionary

def checkAvailability(userStationID, data):
    '''This function will check to see if bikes are available at a particular station and will
    print the number of bikes available so that the user can see.'''

    numBikesAvailable = (data[userStationID]['Bikes Available'])
    print('\nAt station ' + str(userStationID) + ' there are ' + str(numBikesAvailable) + ' bikes available')
    return numBikesAvailable

def getNewLocation(data, userStationID):
    '''This function will find the nearest station to userStationID that has a bike available.
    It will return the value of the nearest station (key) '''
    for key in data:
        if key > userStationID and data[key]['Bikes Available'] > 0:
            return(key)

def getDirections(data, userStationID, location):
    '''This function will provide directions to the nearest station with a bike available.
    Using the longitude and latitude, it calculates the angle between the two stations
    and given that, it displays the direction that the user needs to go to get to the
    other station.'''

    #retrieving data from the dictionary and converting it to radians for calculation of bearing
    firstLat = radians(data[userStationID]['Lat'])
    firstLon = radians(data[userStationID]['Lon'])

    secondLat = radians(data[location]['Lat'])
    secondLon = radians(data[location]['Lon'])

    #calculating (x,y) coordinates to plug into bearing formula
    x = cos(secondLat) * sin(secondLon - firstLon)
    y = cos(firstLat) * sin(secondLat) - sin(firstLat) * cos(secondLat) * cos(secondLon - firstLon)

    #calculate bearing, round to 0 decimal points and convert to a positive value
    bearingDirection = abs(round(degrees(atan2(x,y)),0))

    #set of conditional statements providing location to nearest station
    if bearingDirection == 0:
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed NORTH to get to the station.")
    elif bearingDirection in range(0,90):
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed NORTH EAST to get to the station.")
    elif bearingDirection == 90:
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed EAST to get to the station.")
    elif bearingDirection in range(90, 180):
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed SOUTH EAST to get to the station.")
    elif bearingDirection == 180:
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed SOUTH to get to the station.")
    elif bearingDirection in range(180, 270):
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed SOUTH WEST to get to the station.")
    elif bearingDirection == 270:
        print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
        print("Proceed WEST to get to the station.")
    else:
        if bearingDirection in range(270, 360):
            print("The nearest station is at " + data[location]['Name'] + " which is station: " + location)
            print("Proceed NORTH WEST to get to the station.")

def bikesAvailable(data):
    '''This function prints out all stations that have bikes available in the following format
    (StationID : Number Available). 
    '''

    print("The following stations have bikes available (StationID : Number Available):")

    #runs through the dictionary printing out all stations that have Bikes Available
    for key in data:
        if data[key]['Bikes Available'] > 0:
            print(key, ':', data[key]['Bikes Available'])
    
def openStations(data):
    '''This function prints out all stations that have docks open in the following format
    (StationID : Docks Available)
    '''
    print("The following stations have open docks (StationID : Docks Available):")

    #runs through the dictionary printing out all stations that have Docks Available
    for key in data:
        if data[key]['Docks Available'] > 0:
            print(key, ':', data[key]['Docks Available'])

def runAgain():
    ''' This function asks the user if they want to continue using the software once
    their specific user code has run its course'''

    runAgain = input('Do you want to continue using the application (Y/N): ')
    
    while runAgain != 'Y' and runAgain != 'N':
        print("The option you entered is invalid")
        runAgain = input("Do you want to continue using the application (Y/N):")

    if runAgain == 'Y':
        return True
    elif runAgain == 'N':
        print("Thank you for using the app!")
        return False

def main():
    '''The main function is where all user options will be completed. The user will choose their option and
    depending on that option, I have set up statements that will call the respective functions in order to
    complete the task chosen by the user. The user has the ability to choose another option after they complete
    one.
    '''

    data = getAllStationData() #retrieves nested dictionary in the data variable

    state = True #set the state of the app equal to true in order to set up loop

    #initialize loop to run the program again if user would like to
    while state == True:

        userRequirement = getUserRequirements() #retrieves user requirement (what they would like to do)


        #completes userRequirement 1 
        if userRequirement == 1:
            userStationID = retrieveStationID(data)
            specificStationData(data, userStationID)
            state = runAgain()

        #completes userRequirement 2
        elif userRequirement == 2:
            userStationID = retrieveStationID(data)
            numBikesAvailable = checkAvailability(userStationID, data)
            
            if numBikesAvailable > 0:
                while True:
                    rentOrNot = input("Would you like to rent a bike from this station? (Y/N) ")
                    if rentOrNot == 'Y':
                        data = trackRentals(data, userStationID)
                        state = runAgain()
                        break
                    elif rentOrNot == 'N':
                        print("No Problem! ")
                        state = runAgain()
                        break
                    else:
                        print("The option you entered is invalid.")                
            else:
                print("I will show you the nearest location that has a bike available. \n ")
                location = getNewLocation(data, userStationID)
                getDirections(data, userStationID, location)
                state = runAgain()


        #completes userRequirement 3           
        elif userRequirement == 3:
            listOfBikesAvail = bikesAvailable(data)
            while True:            
                rentOrNot = input("Would you like to rent a bike from any of these stations? (Y/N) ")
                if rentOrNot == 'Y':
                    userStationID = retrieveStationID(data)
                    data = trackRentals(data, userStationID)
                    state = runAgain()
                    break
                elif rentOrNot == 'N':
                    print("No Problem! ")
                    state = runAgain()
                    break
                else:
                    print("The option you entered is invalid.")

        #completes userRequirement 4
        else:
            if userRequirement == 4:
                listOfOpenDocks = openStations(data)
                while True:
                    returnOrNot = input("Would you like to return a bike at any of these stations? (Y/N) ")
                    if returnOrNot == 'Y':
                        userStationID = retrieveStationID(data)
                        data = trackReturns(data, userStationID)
                        state = runAgain()
                        break
                    elif returnOrNot == 'N':
                        print("No Problem! ")
                        state = runAgain()
                        break
                    else:
                        print("The option you entered is invalid.")
            
main()
