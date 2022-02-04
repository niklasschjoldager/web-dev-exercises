from bottle import get, run, static_file, view

# Dictionary
person = {
  "id": "1",
  "name": "Niklas"
}


##############################
@get("/app.css")

def _():
  return static_file("app.css", root = ".")

##############################
@get("/")
@view("index")

def _():
  return 

##############################
@get("/my-data/<first_name>/<last_name>")

def _(first_name, last_name):
  return f"Hi {first_name} {last_name}."

##############################
@get("/person/<person_id>")

def _(person_id):
  person["last_name"] = "Schjoldager"
  return person_id

##############################
@get("/items")
@view("items")

def _():
  letters = ["a", "b", "x"]

  return "Yes" if "x" in letters else "No" # ternary operator

  # letters.append("d")

  # is_b_in_list = "No"
  
  # if "b" in letters:
  #   is_b_in_list = "Yes"

  # return is_b_in_list

  # print(type(letters))
  # print(dir(letters))

  # letters = ["a", "b", "c"]
  # print("#" * 30)
  # print(letters)

  # return letters
  

##############################
@get("/cart")

def _():
  name = "Niklas" #string
  year = 2022

  return f"Hi {name} the year is {year}" #f string
  # return "Hi " + name + " it is " + str(year)
  # return str(year) #type-cast or cast
  # return "Hi Niklas the year is 2022"

##############################
# Query strings
# every other varible after the 1st one starts with &
# 127.0.0.1:4444/test?id=1&name=a
@get("/test")
def _():
    school_name = request.params.get("school-name")
    year = request.params.get("year")
    age = request.params.get("age")
    return f"Hi, you are at {school_name}. The year is {year} and you are {age} years old"

##############################
# port from 0 to 65535
# reserved from 0 to 1024
run( host="127.0.0.1", port=3333, debug=True, reloader=True )