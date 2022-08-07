from flask import request, render_template, abort, Flask, redirect, url_for
from HelperFunctions import get_db_connection, generate_file_name, delete_file, ExecuteQuery

app = Flask(__name__)

delete_queries = 'delete from badges where id =?'
update_queries = 'update badges set students=? where id =?'
select_queries_with_name = 'select * from badges where name =?'
select_queries_with_id = 'select * from badges where id =?'
create_queries = 'INSERT INTO badges (name, description,badge,students) VALUES (?, ? ,?,?)'
image_basepath = "static/images/"
all_queries = 'select * from badges'


@app.route('/',methods = ['GET'])
def index():
    return render_template("file_upload_form.html")

@app.route('/deleteBadge',methods = ['GET','POST'])
def deleteBadge():
    print("inside deleteBadge method")
    if request.method == 'GET':
        args = request.args
        args = args.to_dict();
        print(args)
        id = args.get("id")
        result = ExecuteQuery(select_queries_with_id,(id,),True)
        if len(result) != 0:
            data = result[-1]
            print(list(data))
            fileName = data[3]
            ExecuteQuery(delete_queries,(id,),True)
            fileName = image_basepath+fileName
            delete_file(fileName)
            result = ExecuteQuery(all_queries, ("",), False)
            allData = []
            for i in result:
                data = dict()
                data["id"] = i[0]
                data["name"] = i[1]
                data["description"] = i[2]
                data["badge"] = i[3]
                data["students"] = list(i[4].split(","))
                allData.append(data)
            return render_template("allBadge.html", allbadges=allData)
        return "Badge not found"

@app.route('/createBadge', methods=['POST'])
def create():
    print("inside success method")
    if request.method == 'POST':
        file = request.files['file']
        description = request.form['description']
        name = request.form['name']
        students = request.form['students']
        fileName = file.filename
        print("file.filename ",fileName)
        result = ExecuteQuery(select_queries_with_name,(name,),True)
        if len(result)!=0:
            abort(403, description="Badge with this name already exists")
        if fileName=="" or fileName==None:
            print("empty")
        else:
            fileName = generate_file_name(fileName)
            print("fileName "+fileName)
            file_path = image_basepath+fileName
            file.save(file_path)
            # file_data = convertToBinaryData(file_path)
            ExecuteQuery(create_queries,(name,description,fileName,students),True)
            result = ExecuteQuery(all_queries,("",),False)
            allData = []
            for i in result:
                data = dict()
                data["id"] = i[0]
                data["name"] = i[1]
                data["description"] = i[2]
                data["badge"] = i[3]
                data["students"] = list(i[4].split(","))
                allData.append(data)
            return render_template("allBadge.html", allbadges=allData)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)

@app.route('/getBadges', methods=['GET'])
def getBadges():
    print("inside getBadges method")
    if request.method == 'GET':
        result = ExecuteQuery(all_queries,("",),False)
        print(len(result))
        label = ["id","name","description","badge","students"]
        allData = []
        for i in result:
            data = dict()
            data["id"]=i[0]
            data["name"] = i[1]
            data["description"] = i[2]
            data["badge"] = i[3]
            data["students"] = list(i[4].split(","))
            allData.append(data)
        return render_template("allBadge.html",allbadges=allData)
        # return allData

@app.route('/badge/verify', methods=['GET'])
def search():
    args = request.args
    args = args.to_dict();
    print(args)
    name = args.get("name")
    email = args.get("email")
    result = ExecuteQuery(all_queries,("",),False)
    finalResult = []
    for i in result:
        if name==i[1]:
            emails = str(i[4]).split(",")
            for j in emails:
                if j==email:
                    finalResult.append(list(i))
    allData = []
    for i in finalResult:
        data = dict()
        data["id"] = i[0]
        data["name"] = i[1]
        data["description"] = i[2]
        data["badge"] = i[3]
        data["students"] = list(i[4].split(","))
        allData.append(data)
    return render_template("allBadge.html", allbadges=allData)
    if len(finalResult)==0:
        abort(403, description="for this user badge not found")

    return finalResult

@app.route('/addEmail', methods=['GET','POST'])
def addEmail():
    print("inside add email")
    args = request.args
    args = args.to_dict();
    print(args,request.form["name"],request.form["email"])
    name = request.form["name"]
    email = request.form["email"]
    id = request.form["id"]
    print("id",id)
    # con = get_db_connection()
    # result = con.execute(select_queries_with_name,(name,)).fetchall()
    # con.close()
    result = ExecuteQuery(select_queries_with_id,(id,),True)
    print("length",len(result))
    if(len(result)!=0):
        data = result[-1]
        print(list(data))
        new_email = data[4]+","+email
        print("new_email",new_email)
        ExecuteQuery(update_queries,(new_email,data[0]),True)
        result = ExecuteQuery(all_queries, ("",), False)
        allData = []
        for i in result:
            data = dict()
            data["id"] = i[0]
            data["name"] = i[1]
            data["description"] = i[2]
            data["badge"] = i[3]
            data["students"] = list(i[4].split(","))
            allData.append(data)
        return render_template("allBadge.html", allbadges=allData)
    return "Badge not found"




if __name__ == '__main__':
    app.run(debug=True)