import requests
import time
import sys
class Course:
	def __init__(self, name, moments):
		self.name = name
		self.moments = moments
		self.size = len(moments)
def hack_studentportalen(username, password):
	usr = username
	pwd = password
	payload = {'user' : usr, 'pass2' : pwd} 
	r = requests.get("https://www3.student.liu.se/portal/login", params = payload)
	r2 = requests.get("https://www3.student.liu.se/portal/studieresultat/resultat?show_oavslut=oavslut&show_prov=prov", cookies = r.cookies)
	
	courses = r2.text[r2.text.find("Kursnamn") + 8 : r2.text.find("<!-- PORTAL TEXT END -->")]
	courses = courses[0 : courses.find("colspan")]
	slaughter_string = courses 				#Temporary copy of 'courses', this will be SLAUGHTERED :D
	course_list = [];
	while slaughter_string.find("<b>") > -1:
		moments = []
		slaughter_string = slaughter_string[slaughter_string.find("<b>") + 3:]
		course_name = slaughter_string[0 : slaughter_string.find("</b>")]
		course_substring  = slaughter_string[0 : slaughter_string.find("<b>")]
		while course_substring.find("<i>") > -1:
			course_substring = course_substring[course_substring.find("<i>") + 3:]
			moment_name = course_substring[0 : course_substring.find("</i>")]
			course_substring = course_substring[course_substring.find("<td>") + 4 : ]
			course_substring = course_substring[course_substring.find("</td>") + 5 : ]
			course_substring = course_substring[course_substring.find("<td>") + 4: ]
			moment_points = course_substring[: course_substring.find("</td>")]
			course_substring = course_substring[course_substring.find("<i>") : ]
			moments.append(moment_name + ": " + moment_points)
		temp = Course(course_name, moments)
		course_list.append(temp)
		slaughter_string = slaughter_string[slaughter_string.find("</b>"):]
	return course_list
	
if __name__ == "__main__":
	try:
		username = sys.argv[1]
		password = sys.argv[2]
	except:
		print "Wrong amount of arguments, probably (who knows, really?). Try it again, friend."
		sys.exit()
	while True:
		old_course_list = hack_studentportalen(username, password);
		time.sleep(10);
		new_course_list = hack_studentportalen(username, password);
		for i, j in zip(old_course_list, new_course_list):
			for moment in j.moments:
				if moment in i.moments:
					print "Nothing new"
				else:
					string = "New grade in " + i.name + " available!" + "Grade: " + moment
					data = {'to' : '+46734003770', 'from' : 'ExamWatch', 'message' : 'hi'}
					r = requests.post("SMS API OF CHOICE", auth=("USER","PASSWORD"),data=data)