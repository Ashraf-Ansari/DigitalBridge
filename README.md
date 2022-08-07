# DigitalBadge  

Note: Project is focused on functionality. please ignore frontend page designs. Thanks

project setup  
1. download the project
2. Python 3.7 must be installed
3. go to project directory -> DigitalBadges
4. pip install -r requirements.txt
5. python init_db.py  > to initalize the database
6. python -m flask run // application will start

list of used Api's ( note: if any apy will not work please use copy paste the ure in the browser. 

project features

1. http://127.0.0.1:5000/     // in this page you can add the Digital Badges information. After uploading you will be redirecting to the page where you can see all the Badge Names , Badge Description , badges images and list of students who earned the badges.
2. In the page you can see delete button to delete the Badges which are no longer needed. you can see a input field where you can enter the students name who earned badges and click on addEmail button. their email will get added in the respective Badge Dropdown.

if anytime functionality will not work properly please try to refresh the page or try below commands.
1. http://127.0.0.1:5000/ use this api to upload the badges Details.
2. http://127.0.0.1:5000/getBadges this api where you can see all Badge details. you will get All functionality in this page.

