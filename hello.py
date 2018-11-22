# import the Flask class from the flask module
from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import numpy


laptops = pd.read_csv('finalLaptops.csv')
ram = laptops.Ram.values
for i in range(len(ram)):
    ram[i] = str(ram[i])

# create the application object
app = Flask(__name__)
app.secret_key = "super secret key"


# use decorators to link the function to a url


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')  # render a templat


@app.route('/shop')
def shop():
    return render_template('shop.html')  # render a template


@app.route('/cart')
def cart():
    return render_template('cart.html')  # render a template


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')  # render a template


@app.route('/form')
def form():
    return render_template('form.html')


def filterOut(laptopDF, typeNameVal, cpuVal, memoryVal, opsysVal, priceVal, ramVal):
    df=laptops
    if typeNameVal!='Any':
        df = df[df.TypeName == typeNameVal]
    if cpuVal!='Any':
        df = df[df.Cpu == str(cpuVal)]
    if ramVal!='Any':
        df = df[df.Ram == int(ramVal)]
    if memoryVal!='Any':
        df = df[df.Memory == memoryVal]
    if opsysVal!='Any':
        df = df[df.OpSys == opsysVal]
    if priceVal!='Any':
        df = df[df.Price == int(priceVal)]
    return df


def authenticate(user, password):
    global usersDict
    if user in usersDict:
        if password == usersDict[user]:
            flash('Premium user logged in')
            ##render funtion to form page
        else:
            flash('Incorrect password!')
            ##render function back to login page
    else:
        flash("This premium user doesn't exist")
        ##render function back to login page


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        type = request.form['type']
        RAM = 'Any'
        memory = request.form['memory']
        processor = request.form['processor']
        OS = request.form['OS']
        budget = request.form['budget']
        formList = [type, RAM, memory, processor, OS, budget]
        if budget == 'High':
            price = '3'
        elif budget == 'Medium':
            price = '2'
        else:
            price = '1'
        global laptops
        filteredDF = filterOut(laptops, type, processor, memory, OS, price, RAM)
        filteredLaptopNames = filteredDF.Product.values
        formList = list()
        for i in range(len(filteredLaptopNames)):
            formList.append(filteredLaptopNames[i])
        formList = list(set(formList))
        return render_template('test.html', formList=formList)
    else:
        return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/auth', methods=['post', 'get'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usersDict = {'manipalJpr@DELL': 'manipalPassword', 'dell@DELL': 'dellPassword',
                     'ourTeam@DELL': 'ourTeamPassword'}
        if username in usersDict:
            if password == usersDict[username]:
                flash('Premium user logged in')
                return redirect('form')
            else:
                flash('Incorrect password!')
                return redirect('login')
        else:
            flash("This premium user doesn't exist")
            return redirect('login')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
    type=None
    RAM=None
    memory=None
    processor=None
    OS=None
    budget=None
    formList=None
    usersDict = {'manipalJpr@DELL': 'manipalPassword', 'dell@DELL': 'dellPassword',
                 'ourTeam@DELL': 'ourTeamPassword'}
