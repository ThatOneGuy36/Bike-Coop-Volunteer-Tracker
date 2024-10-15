from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import math


newDBFile = 'table.db'
schemaFile = 'schema.sql'


app = Flask(__name__)


def connectDatabase():
    connection = sqlite3.connect(newDBFile)
    
    file = open(schemaFile)   
    connection.executescript(file.read())
        
    connection.commit()
    connection.close()
        
 

# The homepage of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    connectDatabase()
     
    connection = sqlite3.connect(newDBFile)

    cur = connection.cursor()
    
    
    # Get all volunteer information
    cur.execute("SELECT id, name, isStudent, num_hours FROM Volunteers;")
    data = cur.fetchall()
    
    cur.execute("SELECT VolunteerID, rewardName, COUNT(VolunteerID) as rewardNum FROM VolunteerRewards GROUP BY VolunteerID, rewardName;")  
    rewardData = cur.fetchall()
    
    connection.commit()
    
    cur.close()
    connection.close()
    
    return render_template('VolunteerHours.html', data=data, rewardData=rewardData)
    
    
@app.route('/redeem_reward', methods=['POST'])
def redeem_reward():
    connection = sqlite3.connect(newDBFile)
    cursor = connection.cursor()
    
    volunteer_id = request.form['volunteerId']
    reward_name = request.form['rewardName']
    
    # Remove the reward from VolunteerRewards table
    cursor.execute("DELETE FROM VolunteerRewards WHERE rowid IN (SELECT rowid FROM VolunteerRewards WHERE volunteerID = ? AND rewardName = ? LIMIT 1)", (volunteer_id, reward_name))
        
    # Add the reward to RedeemedRewards table
    cursor.execute("INSERT INTO RedeemedRewards (volunteerID, rewardName, dateRedeemed) VALUES (?, ?, DATE('now'));", (volunteer_id, reward_name))
        
    # Commit the transaction
    connection.commit()

    cursor.close()
    connection.close()
    
    return redirect(url_for('index'))
    
    

# Gives the user the ability to add a record to the database, assuming all inputs are valid   
@app.route('/create', methods=['POST'])
def create():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()

    name = request.form['VolunteerName']
    
    
    try:
        isStudent = request.form['isStudent']
        isStudent = True
    
    except:
        isStudent = False
    
    
    if (name == ""):
        return render_template('Error.html', data=('create', 'Missing field: `Name`'))
        
    else:
        pass
        
        
    try:
        cur.execute("INSERT INTO Volunteers (isStudent, rewardTier, name, num_hours) VALUES (?, ?, ?, ?)", (isStudent, 1, name, '0'))
        
    
    except:
        return render_template('Error.html', data=('create', 'Non-unique or non-integer id entered'))


    connection.commit()
        
    cur.close() 
    connection.close() 
    
    
    return redirect(url_for('index'))
    
    

# Allows the user to delete a student record from the database, assuming the student ID exists
@app.route('/delete', methods=['POST'])
def delete():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()
    
    vID = request.form['VolunteerID']


    if (vID == ""):
        return render_template('Error.html', data=('delete', 'Missing field: `Volunteer ID`'))

    cur.execute("DELETE FROM Volunteers WHERE id = ?", (vID,))
    cur.execute("DELETE FROM VolunteerRewards WHERE volunteerID = ?", (vID,))
    cur.execute("DELETE FROM RedeemedRewards WHERE volunteerID = ?", (vID,))
    connection.commit()

    cur.close() 
    connection.close() 
    
    return redirect(url_for('index'))



# Allows the user to modify a current student's email in the database
@app.route('/update_hours', methods=['POST'])
def update_hours():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()
    
    vID = request.form['VolunteerID']
    addedHours = request.form['addedHours']
    
    
    if (vID == ""):
        return render_template('Error.html', data=('update', 'Missing field: `Volunteer ID`'))



    # Calculate how many 2 hour rewards should be added
    currentHours = cur.execute("SELECT num_hours FROM Volunteers WHERE id=?", (vID,)).fetchone()
    
    studentStatus = cur.execute("SELECT isStudent FROM Volunteers WHERE id=?", (vID,)).fetchone()
    
    
    if (currentHours == []):
        return redirect(url_for('index'))
    
    
    numTwoHourRewards = calculateNumTwoHourRewards(currentHours[0], float(addedHours))
    
    for i in range(numTwoHourRewards):
        if (studentStatus[0]):
            cur.execute("INSERT INTO VolunteerRewards (volunteerID, rewardName) VALUES (?, ?)", (vID, "Free Can of Nestea"))
            
        else:
            cur.execute("INSERT INTO VolunteerRewards (volunteerID, rewardName) VALUES (?, ?)", (vID, "Free Booking Slot"))
        
        
        
    # Update the total number of hours
    cur.execute("UPDATE Volunteers SET num_hours=num_hours+? WHERE id=?", (addedHours, vID))
    
    
    # Check reward tier to see if the person should be considered for the next prize
    currentTier = cur.execute("SELECT rewardTier FROM Volunteers WHERE id = ?", (vID,)).fetchone()[0]
    totalHours = cur.execute("SELECT num_hours FROM Volunteers WHERE id = ?", (vID,)).fetchone()[0]
    
    
    reward, updateTier = calculateRewardFromTier(currentTier, totalHours)
    
    if (updateTier):
        cur.execute("INSERT INTO VolunteerRewards (volunteerID, rewardName) VALUES (?, ?)", (vID, reward))
        cur.execute("UPDATE Volunteers SET rewardTier=rewardTier + 1 WHERE id=?", (vID,))

    connection.commit()

        
    cur.close() 
    connection.close() 
    
    return redirect(url_for('index'))
    
    
# Allows the user to modify a current student's email in the database
@app.route('/update_name', methods=['POST'])
def update_name():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()
    
    vID = request.form['VolunteerID']
    newName = request.form['vName']
    
    
    if (vID == ""):
        return render_template('Error.html', data=('update', 'Missing field: `Volunteer ID`'))
        
    elif (newName == ""):
        return render_template('Error.html', data=('update', 'Missing field: `New Name`'))
        
        
    cur.execute("UPDATE Volunteers SET name=? WHERE id=?", (newName, vID,))
     

    connection.commit()

        
    cur.close() 
    connection.close() 
    
    return redirect(url_for('index'))
    
    
    
# Allows the user to modify a current student's email in the database
@app.route('/update_student', methods=['POST'])
def update_student_status():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()
    
    vID = request.form['VolunteerID']
    newStatus = request.form['vStatus']
    
    if (newStatus == "true"):
        newStatus = 1
        
    else:
        newStatus = 0
    
    
    if (vID == ""):
        return render_template('Error.html', data=('update', 'Missing field: `Volunteer ID`'))
        
        
    cur.execute("UPDATE Volunteers SET isStudent=? WHERE id=?", (newStatus, vID,))
     

    connection.commit()

        
    cur.close() 
    connection.close() 
    
    return redirect(url_for('index'))



# Allows the user to delete a student record from the database, assuming the student ID exists
@app.route('/print', methods=['POST'])
def printRewards():
    connection = sqlite3.connect(newDBFile)
    cur = connection.cursor()
    
    vID = request.form['volunteerIdPrint']            


    if (vID == ""):
        return render_template('Error.html', data=('printRewards', 'Missing field: `Volunteer ID`'))


    cur.execute("SELECT name FROM Volunteers WHERE id = ?", (vID,))
    volunteerName = cur.fetchone()
    
    cur.execute("SELECT rewardName, dateRedeemed FROM RedeemedRewards WHERE volunteerID = ?", (vID,))
    redeemInfo = cur.fetchall()
    
    cur.execute("SELECT rewardName, COUNT(rewardName) AS numReward FROM RedeemedRewards WHERE volunteerID = ? GROUP BY rewardName", (vID,))
    quantityInfo = cur.fetchall()
    
    printData = []
    printData.append(volunteerName)
    printData.append(redeemInfo)
    printData.append(quantityInfo)
    
    connection.commit()

    cur.close() 
    connection.close() 
    
    return render_template('RedeemedRewards.html', printData=printData)



def calculateNumTwoHourRewards(currentHours, addedHours):  
    # CurrentHours % 2 to ensure we don't double up on rewards
    if (currentHours < 2 and currentHours + addedHours < 2):
        return 0
        
    elif (currentHours < 2):
        return math.floor((currentHours + addedHours) / 2)
        
    return math.floor(((currentHours % 2) + addedHours) / 2)
    
    

# Flag is a variable which tells the program that we should update the person's reward tier after this
# It's used right after receiving a reward from the current tier, and updates the tier to ensure the person doesn't receive duplicates of the reward in the current tier 
def calculateRewardFromTier(rTier, tHours):
    reward = ""
    flag = False
    
    
    if (rTier == 1 and tHours >= 10):
        reward = "Patch Kit"
        flag = True
        
    elif (rTier == 2 and tHours >= 20):
        reward = "Bike Coop Bottle"
        flag = True
        
    elif (rTier == 3 and tHours >= 30):
        reward = "Tire Levers"
        flag = True
        
    elif (rTier == 4 and tHours >= 40):
        reward = "Bike Coop Shirt"
        flag = True
        
    elif (rTier == 5 and tHours >= 50):
        reward = "ParkTool Multitool"
        flag = True
    
    elif (rTier == 6 and tHours >= 60):
        reward = "ParkTool Apron"
        flag = True
        
    elif (rTier == 7 and tHours >= 70):
        reward = "Bike Lube"
        flag = True
        
    elif (rTier == 8 and tHours >= 80):
        reward = "50$ MSRP Credit"
        flag = True
        
    elif (rTier == 9 and tHours >= 90):
        reward = "10% off MSRP Catalogue"
        flag = True
        
    elif (rTier == 10 and tHours >= 100):
        reward = "20% off MSRP Catalogue"
        flag = True
        
    elif (rTier == 11 and tHours >= 120):
        reward = "???"
        flag = True
    
    
    return reward, flag
    
    



if __name__ == '__main__':
   app.run(debug=False)
