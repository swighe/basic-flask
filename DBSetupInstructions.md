Create a new AWSEducate Account

1.	What is AWSEducate?
https://aws.amazon.com/education/awseducate/#
AWS Educate provides an academic gateway for the next generation of IT and cloud professionals. AWS Educate is Amazon’s global initiative to provide students and educators with the resources needed to accelerate cloud-related learning.

2.	Register as a Student
https://www.awseducate.com/registration#APP_TYPE 

 
Note: 
1.	Ensure the institution name is “Hunter” and your email provided has the term Hunter in it.
2.	Course info: CSCI 39548 Practical Web Development

3.	Email verification:
You will receive an email with verification link (ensure you check your spam). It should have the following title: Email Verification – AWE Educate Application. Click on the link.

4.	Terms and Conditions:
Verification shall take you to terms and conditions page. Read and accept them.
 
5.	Under Review
You should receive an email 
Title: Thank you for applying to AWS Educate.
Body/Content: Thank you for applying for AWS Educate. We have received your application, and it is currently under review. You will receive an email once the review is complete.

From this point, your email should be under review.

6.	Approved
You should receive an email 
Title: AWS Application Approved 
From this point you should be able to activate your account and have access to the aws console

7.	Login to AWS console
Login to the console: https://console.aws.amazon.com/console and ensure you have access
Note: you will need to use the Hunter email and not your personal email.

8.	Login to AWS console
Login to the console: https://console.aws.amazon.com/console and ensure you have access
Note: you will need to use the Hunter email and not your personal email.

 

9.	Login to AWS console
Login to the console: https://console.aws.amazon.com/console and ensure you have access
Note: you will need to use the Hunter email and not your personal email.

10.	 Navigate to RDS Service (Managed Relational Database Service)
Under the AWS Services section, search for RDS keyword. Select Managed Relational Database Service option

11.	 Create database under Managed RDS getting started page
Click on the Create Database option
 

12.	 Select MariaDB engine 
Select MariaDB (preferred as it is the most cost-effective option available) 

Note: Feel free to use any of the database provided. Mysql, PG, MariaDB are easy to use lightweight solutions.


13.	 Select Dev/Test option (free usage tier)
Chose the Dev/Test option.
 


14.	 DB Configuration specifications
For a simple app, the smallest configuration should suffice.
Use default settings wherever applicable.
Ensure you select the following:
•	DB Instance Class: (db.t2.micro – 1 vCPU, 1 GiB RAM)
•	Muti-AZ Deployment : No
•	Settings:
o	DB Instance Identifier: Call it say : “MariaDb”
o	Master username: Fill in your master user
o	Master password: Fill in your master password
•	Note: The username + password credentials are for administration of the DB and NOT your application credentials.

Click Next

15.	 Advanced Settings
Apart from defaults, change the following settings:
1.	Network and Security
a.	Public accessibility: Yes (we want your db to be accessible from the external world (say Heroku app etc.)).
b.	Availability zone: Not necessary but you can select us-east-xxx so that your DB is located closer to you.
2.	Database Options
a.	Database name: Specify the name of the database. This is important.
3.	Backup: Choose what you believe suits your needs.
4.	Log Exports: If you wish, you can turn them all on.
5.	Deletion protection: Check mark this to enable deletion protection (preventing you to accidentally delete your db). You need to uncheck it if you wish to intentionally start from scratch.
Finally select Create Database


16.	 Database Creation
You should see a page like:
 

You can click on View DB Instance Details and see your database. Here’s an example of a URL to navigate to your DB page : https://console.aws.amazon.com/rds/home?region=us-east-1#dbinstance:id=common assuming you chose us-east-1 as your availability zone, common as the db name.
Additionally, you can go to Dashboard, Databases, Query Editor etc. to play around with your DB.

See below for an example:
 

Eg. I have a database instance setup with the following settings:
1.	Endpoint (hostname): common.ck0xkqjcz68b.us-east-1.rds.amazonaws.com
2.	Port: 3306 (typical of MariaDB)

17.	 Security Group Rules to allow external connections
On the home of Databases, you should see your Security Group Rules/Settings. By default, AWS keeps it internal, and even with external setting, it is restricted from a certain IP/IP range. You need:
1.	Click on the security group
2.	Go to Actions -> Edit Inbound rules
3.	Change Source to “Anywhere”
4.	Note: You can also add the IP from where you shall be calling the DB (eg Heroku app IP).

 


 
Accessing + tools for administering your database

See simple instructions here on how to create a new user (your application user in this case), grant access to read/write etc. from it. You will use admin credentials for this. Next, you can create your table(s), database(s) and grant access to app user just created to ensure that app user can read + write to this table.

http://www.daniloaz.com/en/how-to-create-a-user-in-mysql-mariadb-and-grant-permissions-on-a-specific-database/ 

Note: You can restrict access to read/write only and not grant drop/create database/table(s) which is recommended for app users.


Tools: You can use any tool. Eg. DBeaver free community version works well with most DB’s.
See couple of snapshots to setup new connection.

1.	Click Connection -> New Connection
2.	Select MariaDB Connection Type
 

3.	Select your hostname, database name, username and password. 
Note: You will need to sign in with admin credentials, create a user as mentioned 

4.	Repeat Then create a new connection step for non-admin user (app user) which you shall be using to read + insert records into the table.
 

 


You are all set!
