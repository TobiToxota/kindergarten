<h1>kindergarten</h1>
 
<P>final project for cs50x https://cs50.harvard.edu/x/2022/</p>

<p>You can find the current main branch deployed on https://kindgrt.uber.space/</p>

<h2>About the web application:</h2>
<h4>An application for informing the parents of children within a kindergarten:</h4>
    <ul>
      <li>possibility to create a menu for the week. Create dishes and desserts for every weekday. If a kindergarten doesnt serve desserts, the app will responsively not show it.</li>
      <li>create a blog where the kindergarten can post important announcements and also where it can delete it. The announcements can be posted via a rich text editor from TINY MCE.</li>
      <li>create a filesystem where the kindergarten can provide the parents with important .pdf files. Securing that the kindergarten can only upload .pdf files and also using werkzeug secure_filenames.</li>
      <li>kindergarten can invite parents via parents email adress and will generate a hex-12 string for authentication, which the parents need to submit in their own register form</li>
      <li>the application will devide the users in two roles: admins and parents.</li>
  </ul>

---
<h3>Porpuse of this web application:</h3> Because most kindergartens have a static website and only really expensive kindergartens with a huge budget have applications which are mostly way more packed. I think the basic featureset of this app would be really beneficial for kindergartens (No need to print out handouts and hangouts) and for the parents (Overall planning for the week and just beeing informed)

---

<h2>Dependencies</h2> 
  <ul>
    <li>Flask==2.1.1</li>
    <li>Flask-SQLAlchemy==2.5.1</li>
    <li>Jinja2==3.1.1</li>
  </ul>    

---

<h3> How to run the dev environment:</h3>
<em>pip install flask</em><br>
<em>pip install flask-sqlalchemy</em><br>
<em>python3</em><br>
<em>from app import db</db><br>
<em>db.create_all()</db><br>
close python3 (ctrl+d)<br>
<em>flask run</em><br>

---

Things the app is still missing (imo): 
  <ul>
    <li>Badges for unseen content for the parents</li>
    <li>Email service which will automatically invite parents.</li>
    <li>Delete parents</li>
    <li>[...]</li>
  </ul>
  
---
https://www.youtube.com/watch?v=N355C4Nly2w
