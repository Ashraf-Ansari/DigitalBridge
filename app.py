from flask import request, render_template, abort, Flask
from HelperFunctions import get_db_connection, generate_file_name

app = Flask(__name__)

delete_queries = 'delete from badeges where name = ?'
create_queries = 'INSERT INTO badges (name, description,badge,students) VALUES (?, ? ,?,?)'
image_basepath = "static/images/"
all_queries = 'select * from badges'


@app.route('/',methods = ['GET'])
def index():
    return render_template("file_upload_form.html")

@app.route('/deleteBadge',methods = ['POST'])
def deleteBadge():
    if request.method == 'POST':
        name = request.form['name']
        con = get_db_connection()
        con.execute(delete_queries,name)
        con.commit()
        con.close()

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
        if fileName=="" or fileName==None:
            print("empty")
        else:
            fileName = generate_file_name(fileName)
            print("fileName "+fileName)
            file_path = image_basepath+fileName
            file.save(file_path)
            # file_data = convertToBinaryData(file_path)
            con = get_db_connection()
            con.execute(create_queries,(name,description,fileName,students))
            con.commit()
            con.close()
        return render_template("success.html")

@app.route('/getBadges', methods=['GET'])
def getBadges():
    print("inside getBadges method")
    if request.method == 'GET':
        con = get_db_connection()
        result = con.execute(all_queries).fetchall()
        print(len(result))
        allData = [list(i) for i in result]
        return allData

@app.route('/badge/verify', methods=['GET'])
def search():
    args = request.args
    args = args.to_dict();
    print(args)
    name = args.get("name")
    email = args.get("email")
    con = get_db_connection()
    result = con.execute(all_queries).fetchall()
    print("length", len(result))
    finalResult = []
    for i in result:
        if name==i[1]:
            emails = str(i[4]).split(",")
            for j in emails:
                if j==email:
                    finalResult.append(i)
    print(finalResult)
    if len(finalResult)==0:
        abort(403, description="for this user badge not found")

    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True)