## PG System

karkhana.io Assignment

After installing frappe bench get PG System app using bench install-app --branch master https://github.com/PatelAasif-Official/PG-System.git

#### License

We have 7 Doctype

1. Room
2. Check-In and Check-Out
3. Customer
4. Payment Entry
5. Employee
6. Periodic Maintenance
7. Work Log

   ###1. Room
Room doctype store the room data, Room has following fields.
1. Room Number
2. Type of Occupency - Select having options such as Single Occupency, Double Sharing, Triple Sharing and Multiple Sharing
3. Type of Room -Select having AC and Non-AC
4. Number of Beds - Will be fixed for Single Occupency, Double Shaing and Triple Sharin editable for Multiple Sharing.
5. Status - Having options Available, Occupied, Partially Occupied and Under Maintenance this status will be readonly and system will automatically change the status.
6. Number Of Beds Available - All the status will be updated based on this int field, if this is 0 mean room is fully occuoied if this equal to Number of Beds then Available.
7. Price - Currency field can be updated after submission.
8. Photos - to show on web portal
![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/28921704-e4fd-49e0-8b6f-e6d56601f825)


  ###2.Check-In and Check-Out
Check-In and Check-Out is doctype that store the data regarding customer checkin and checkout, this doctype having following fields
1. Room Type - Select field user needs to select the type as customer wants AC or Non-AC room so we can apply filter on the linked field of the Room doctype
2. Room - Link field with Room doctype, it will show only Available, Partially Occupied and AC or Non-AC room.
3. Type Of Room, Room Number, Price Per Night all this field will auto fetched from the Room Doctype
4. Guest - Link field with Customer doctype.
5. Guest Name, Mobile Number, Email Address field will be fetched from Customer Doctype.
6. Guest First Name, Guest Last Name is the field which will be used as data field when the booking is happeding from Website portal. System will automatically create customer using this information if the etry if happeding from Portal.
7. Check In Date - Mandatory field, will store date for checking, also validate if past date is selected.
8. status - document status is Draft means booked Manager can not able to submit mean do checking before the Checkin date, submit is checkin, and Check Out.
9. Check out Date - There is button whick will be seen only to role PG Manager, by the button user can process with the checkout.

![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/c081c2cb-0d5f-48ad-85b4-7497e4d1d567)


  ###3.Customer
Customer doctype store the basic information about the Customer, this doctype have following fields
1. First Name, Middle Name, Last Name - Data field to store cusomer full name
2. Full Name - Data but read-only system will automatically ganerate the Full Name based on the above fields.
3. Identity Type - Select field having options Aadhaar Card, PAN Card, Driving Licence, Passport and Other,
4. ID Card Attached - Attach type of fields mandatory as this document oftem required in the hotels. This will be required while guest book the room, manager can ask for the identity while checkin.
5. Name of ID Card - Data field, display if user select Other on Identity Type.
6. Mobile Number, Email Address - contact details used to send the Invoice and contact later
7. Address - Small Text field if ID did not have proper or user want to add address manually.


![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/1958ef6f-b736-4dc5-a647-7312e6e10922)


   ###4.Payment Entry
Payment entry to Collect the Payemnt after checkout, this doctype have following fields. User only need to select Checkin and Checkout entry it will fetche all the data from respective link doctype 
1. booking - Link with Check-in and Check-out.
2. Guest, Guest Full Name, Guest Email, Check In Date, Check Out Date, Room, Room Number and Price Per Night all this fields will be fetched from Respective linked doctypes
3. No of Night Stay - Read-only will be automatically calculated based on the checkin and checkout date
4. Total - total will be price * no night stay
5. Discount (Percent) - Optional
6. Grand Total - Total after Discount deduction if applicable
7. Paid On - date field read-on collect the payment entry creation date.
8. On submition an email notification will be trigger to the Customer Email address.

   ![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/442a9742-217d-4d27-ae0f-a7abbc1716cd)


   ###5. Employee
1. First Name, Middle Name, Last Name - Data field will hold the Employee name
2. Full Name - Data auto-created from above fields
3. Status - Select field having options Active, Left, On Leave and Inactive
4. User ID - Link with User doctype only shows after save.
5. Create User - Checkbox only shows before save, if checked system will automatically create an user and set teh name to User ID field.
6. Designation - Manager, Cleaner and Attendant (I do no have time to study on this more, so only three designations)
7. Joining Date - Date field store the date.
8. Email, Mobile Number - to store the contact details.
9. If Employee doesnot have user created then we show a button to create User for the Employee that will create user in Backend and set the created user name on the employee master.

    ![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/8667fcea-64e0-43ed-9406-4d976d6fb7c6)


    ###6. Periodic Maintenance
Periodic Maintenance is the doctype which will be created only by PG Manager, Using this Manager can create the Schedule job for the Future date such if we need to clean the Rooms on Feb 15, then Manager will create one Periodic Maintenance with the Schedule date having Feb 15. So on the Feb 15 system will automatically creates the Job Log to the Employee having room details in there work log. So this doctype have folllowing fields
1. Name of the Task - Name the Schedule task
2. Type of work - Select field having Room Service, Cleaning, Repair and inspections (Only this works got in my mind at that time)
3. status - Select, read_only having options Scheduled and  Work Log Created, while creating it will be Scheduled and at the time of creating will be change to Work Log Created automatically.
4. schedule date, schedule time, duration - To store the date, timing and Duration for the Employee.
5. description - To add extra note, Optinal

   ![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/11f244ad-546c-49bf-b69c-3dab9016514c)

   ###7. Work Log
work log will be automatically created by the system, it holds the following information for the employee
1. Employee - Link field with employee
2. Full Name - Name of the employee auto fetched
3. Status - status of the Task such as Pending, Completed and In Progress employee can change as per the task staus
4. Type of Work - fetched from Periodic Maintenance define the Nature of the Work
5. Periodic Maintenance - Link field with Periodic Maintenance
6. Duration - Read only show the Empoyee how much this task should tak
7. Schedule Date and Schedule Time of the task.
8. List Of Rooms - this is a child table read-only and show the employee which room he/she need to attend. This list of the room are evenly distributed among all the employee.
9. Description - Manager note for the Employees

![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/12030546-9c52-49da-8647-c3c762ae6eee)


Listing of the Room on the Web Page
Rooms automatically get piblised to the website but user change the status anytime using button Unpublished on the Room doctype, in the list view of the Room only Available, and Partailly Occupied room will be shown to the Guest user, on click a details view can be seen wich show the details and button to book now Screen shots are as following.
List view
![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/8ba20d78-a7c0-4ecc-8a10-ee7fdcd28b47)

Details view
![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/6167ac54-e3cf-42a1-bd84-eb590d01f18e)

Booking Screen
![image](https://github.com/PatelAasif-Official/PG-System/assets/88040507/b61fa8af-2d65-45ab-b989-201b39fc540c)


MIT
