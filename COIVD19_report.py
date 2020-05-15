import re,os,requests
from tkinter import *
from datetime import datetime
import time

def getcountry():
	#Get Country Name For URL
	country_name = (namestr.get()).strip()

	if(country_name=="USA" or country_name=="U.S.A." or country_name=="UnitedStates"):
	    country_name="us"
	if(country_name=="UK" or country_name=="U.K." or country_name=="United Kingdom"):
	    country_name="uk"
	if(country_name=="UAE" or country_name=="U.A.E." or country_name=="United Arab Emirates"):
	    country_name="united-arab-emirates"
	return country_name


def handle_request(request):

	if request.status_code == 200 :
		return True

	if request.status_code == 404:
		Error_prompt = "Client Side Error: Unidentified Methods or Restriced Action\nYour computer failed to access the website due to internal failure."
		error_text  = Label(screen , text = Error_prompt , fg = "red" , bg = "black")
		error_text.config(font=("courier", 14))
		error_text.pack()
		return False

	if request.status_code == 500 or request.status_code == 501 :
		Error_prompt = "We recieved an error on the server side.Please try again after some time"
		error_text  = Label(screen , text = Error_prompt , fg = "red" , bg = "black")
		error_text.config(font=("courier", 14))
		error_text.pack()
		return False
	return False


def getdata():
	country_name = getcountry()
	#Fetch URL Data
	try:
		data = requests.get("https://www.worldometers.info/coronavirus/country/" + country_name + "/")
	except  OSError :
		Err_msg = "Please check you internet connectivity and then try again later."
		err_prompt = Label(screen , text = Err_msg , fg = "red" , bg = "black")
		err_prompt.pack()
		time.sleep(5)
		exit()


	if handle_request(data):
		#Fetch Data			new_text.config(font=("courier", 16))

		extractor = re.compile(r'<\s*?div\s*?class\s*?=\s*?\"maincounter-number\".*?>\n*?<span.*?>(.*)<\/span>\n*?<\s*\/div\s*>')
		numbers = extractor.findall(data.text)


		if len(numbers) !=3 :
			Err_msg = "No inforamtion found for the given country.\nPlease recheck if the given Country name is valid"
			err_prompt = Label(screen , text = Err_msg , fg = "red" , bg = "black")
			new_text.config(font=("courier", 14))
			err_prompt.pack()

		else:
			for i in range(0,len(numbers)):
				if(numbers[i]=="N/A"):
					numbers[i] = "No Data Found"

			date_obj = datetime.now()
			date = date_obj.strftime("%d/%m/%Y  at %H:%M:%S")
			text = "\nReport created on " + date
			new_text = Label(screen , text = text , fg = "yellow" , bg = "black",anchor= "w")
			new_text.config(font=("courier", 9))
			new_text.pack()


			tcases = "\nShowing Report For : {}".format(country_name.upper())
			new_text = Label(screen , text = tcases , fg = "green" , bg = "black")
			new_text.config(font=("courier", 16))
			new_text.pack()


			#Show Total Cases
			tcases = "\rTotal cases\t: "+numbers[0]
			new_text = Label(screen , text = tcases , fg = "yellow" , bg = "black")
			new_text.config(font=("courier", 13))
			new_text.pack()

			#Show Total Deaths
			tcases = "\rTotal deaths\t: "+numbers[1]
			new_text = Label(screen , text = tcases , fg = "yellow" , bg = "black")
			new_text.config(font=("courier", 13))
			new_text.pack()

			#Show Total Recovered
			tcases = "\rTotal Recovered\t: "+numbers[2]
			new_text = Label(screen , text = tcases , fg = "yellow" , bg = "black")
			new_text.config(font=("courier", 13))
			new_text.pack()

			tcases = "\n---------------------------------------------------\n"
			new_text = Label(screen , text = tcases , fg = "yellow" , bg = "black")
			new_text.pack()


screen = Tk()
screen.title("Covid 19 Tracker")
screen.configure(bg = "black")
screen.geometry("900x500")

#Display Intro Text
welcome_text = Label(screen , text = "Coded at SigmaX" , font = ("Courier",24) ,fg = "white" , bg = "black")
welcome_text.pack()

#Getting String From User
namestr=StringVar()
name = Entry( textvariable = namestr )

#Creating Button
click_me = Button (text = "Run Check" , fg = "black" , bg = "green" , command = getdata )

name.pack()
click_me.pack()


screen.mainloop()
