import re,os,requests
from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime
from time import sleep

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
		error_msg = "Client Side Error: Unidentified Methods or Restriced Action\nYour computer failed to access the website due to internal failure."
		error_prompt = Label(screen , text = eror_msg , font=("courier", 14), fg = "red" , bg = "black")
		error_prompt.pack()
		return False

	if request.status_code == 500 or request.status_code == 501 :
		error_msg = "We recieved an error on the server side.Please try again after some time"
		error_prompt = Label(screen , text = error_msg , font=("courier", 14), fg = "red" , bg = "black")
		error_prompt.pack()
		return False
	return False


def getdata():
	country_name = getcountry()
	#Fetch URL Data
	try:
		data = requests.get("https://www.worldometers.info/coronavirus/country/" + country_name + "/")
	except  OSError :
		error_msg = "Please check you internet connectivity and then try again later."
		error_prompt = Label(screen , text = error_msg , font=("courier", 14), fg = "red" , bg = "black")
		error_prompt.pack()
		sleep(50)
		exit()


	if handle_request(data):
		#Fetch Data

		extractor = re.compile(r'<\s*?div\s*?class\s*?=\s*?\"maincounter-number\".*?>\n*?<span.*?>(.*)<\/span>\n*?<\s*\/div\s*>')
		numbers = extractor.findall(data.text)


		if len(numbers) !=3 :
			error_msg = "No inforamtion found for the given country.\nPlease recheck if the given Country name is valid"
			error_prompt = Label(screen , text = error_msg , font=("courier", 14), fg = "red", bg = "black")
			error_prompt.pack()

		else:
			for i in range(0,len(numbers)):
				if(numbers[i]=="N/A"):
					numbers[i] = "No Data Found"

			date_obj = datetime.now()
			date = date_obj.strftime("%d/%m/%Y  at %H:%M:%S")
			text = "\nReport created on " + date
			new_text = Label(screen, text = text, font=("courier", 9), fg = "yellow", bg = "black", anchor= "w")
			new_text.pack()


			tcases = "\nShowing Report For : {}".format(country_name.upper())
			new_text = Label(screen, text = tcases, font=("courier", 16), fg = "green", bg = "black")
			new_text.pack()


			#Show Total Cases
			tcases = "\rTotal cases\t: "+numbers[0]
			new_text = Label(screen, text = tcases, font=("courier", 13), fg = "yellow", bg = "black")
			new_text.config()
			new_text.pack()

			#Show Total Deaths
			tcases = "\rTotal deaths\t: "+numbers[1]
			new_text = Label(screen , text = tcases ,font=("courier", 13) , fg = "yellow", bg = "black")
			new_text.pack()

			#Show Total Recovered
			tcases = "\rTotal Recovered\t: "+numbers[2]
			new_text = Label(screen ,text = tcases, font=("courier", 13), fg = "yellow", bg = "black")
			new_text.pack()

			extractor1 = re.compile(r'<\s?li\s*class="news_li".*?>(.*)\sin')
			text = extractor1.findall(data.text)
			report = "\nToday's Cases : " + re.sub(r'(<strong>|<\/strong>)','',text[0])
			report1 = "Yesterday's Cases : " + re.sub(r'(<strong>|<\/strong>)','',text[1])


			new_text = Label(screen , text = report ,font=("courier", 13), fg = "yellow" , bg = "black")
			new_text.pack()
			new_text = Label(screen , text = report1 ,font=("courier", 13), fg = "yellow" , bg = "black")
			new_text.pack()

			tcases = "\n---------------------------------------------------------------\n"
			new_text = Label(screen, text = tcases , fg = "yellow", bg = "black")
			new_text.pack()

if __name__=='__main__':
	screen = Tk()
	screen.title("Covid 19 Tracker")
	screen.configure(bg = "black")
	screen.geometry("900x500")

	bg_image = ImageTk.PhotoImage(Image.open("bg.jpeg"))
	bg_label = Label(image = bg_image)
	bg_label.place(x=0, y=0, relwidth=0.6, relheight=1.2)

	#Display Intro Text
	welcome_text = Label(screen, text = "COVID19 Tracker", font = ("aria",30,'bold','italic'), fg = "steel blue", bg = "black")
	welcome_text.pack()

	#Getting String From User
	namestr = StringVar()
	name = Entry( textvariable = namestr )

	#Creating Button
	click_me = Button (text = "Run Check", fg = "black", bg = "green", command = getdata )

	name.pack()
	click_me.pack()

	screen.mainloop()
