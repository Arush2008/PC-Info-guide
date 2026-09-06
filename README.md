PCForce - PC Info Guide 

Overview

PCforce is an educational PC information website which is designed to help the users learn and understand PC and their components and use those understandings to actually build a PC. 
The website combines the information of the PC components and educational content. It also have component browsing, filtering so the user can actually find thier desired parts. 
I tried to make the whole website using Python, Flask, SQLAlchemy, SQLite, HTML and css but also used a little bit of javascript point to point so the website does actually work without loading the whole page again or changing the whole path of page. 



Purpose

The main purpose of this website is to teach the people who want to have a basic to advanced knowledge of PC or just want to learn on how to build a PC by themselves. It only shows the phyical components and their specific internal performance but the website does not shows on how to actually fix the internal things on a pc. The main purpose is to help user learn about the componnet, choose the components best fits to the used and the check if the pc they choose will do all thier work or they may need to upgrade few more things or degrade according to thier budget. 

Main focus of this website includes: 
    - Learch what each component on a PC do
    - Understand the specific specifications of those components
    - Finding the components which fits the users needs which can be using filters or searchbars. 
    - Understanding how compatible each component are with each other. 
    - helping them to build thier own pc which is well balanced and performs as the user needs it to be performing. 



Target Audience : 
    - My targeted audience will be anyone who is willing to build their own pc or just wanting to learn on how pcs work what each parts does and why each part is important to add in the pc. Audience may include a large amout of young teens a less larger amout of young adults and few adults as well. 
    this website will be user freindly and will help the user to under the learning components easily and will make sure the user understands what to do and how each things work. I made sure that the structure dont confuse the user and use as easy language as I can. Although All the data is AI generated I have refined to be user freinds so the target audience can be anyone.


Main Features :

    Home Page
        - The home page introduce all my pages features and explain what users can do and how they can go with different steps like step 1 user can explore and learn from learning page and so on. The home page have all the buttons including the navigation bar which takes the user to the different page. The user can choose to just use the navigation bar or scroll down read the home page and click the buttons there to go to next the next page.
    
    Learning Pgae
        - The learning page includes all 9 needed components for a PC. Each component have a dadincated half page for the information so the user knows what part thye are actually learning and dont get confused while they are deeply reading a part. I tried to made the learning page as simpolified as I can where each section is seprated and have a lot of informations including the most common mistakes the user can make and also fun facts to keep the website entertaning insted of deep learning so the feel more like a fun interactive learning hub insted of a dedicated learning website. 
    
    Components Page
        - The components page have all the components in a row and the user can scroll to the right to see other componets in the same raw each component scroll have a dedicated page for that component so the user can have easy access to the page and see what they are doing instead of getting confused on what part is what. There will also be a button for all components where the user can see all the components which will be in blocks instead of scroll so the user can have a look to all the components and dont have to keep switching pages to find the different parts. 

    Build PC 
        - In Build PC page the user can build thier own pc by choosing the parts they like and the web page will help them to find the correct parts which are compatible with each other and can handel the parts properly. It also shows the total price of the choosen pc parts and also shows the total power usage of the choosen parts combined. There are some other features like the user can see the performance score of the pc they build which scores the pc out of 100. While the user is chooseing the part they could search their desired part and choose the part after searching it which will make finding the parts easy. and they could eather change that part by clicking the change button or remove the part which will remove the part they can also click clear button to clear the whole pc build. The build will locally be stored in the users computer but they cannot be save the pc they build. 







Update ------------

I am going to add new feature which saves all the builds at one place and it will be visible to everyone insted of single user since for that I will have to add login feature which will take time so I will just add a public visible feature to add pc builds and the user have to keep the name uniqe.
I will write everything here like what I did 1 by 1 to prove that I did not user AI and the codes writed are mine and I understand what I have writte.

STEP - 1
 I added a new table named builds which will have all the components and I added all the components in that table with a refrence to the other tables which just uses the id insted of the whole new text and I also added a build name which will be unique all over so the builds can be specified and easier to find. 

 STEP - 2
 - I added a builds model in the database.py which shows all the things of the database.
 - Then I added a new route in the views.py to send the content to the html.
 - I added new html page to show all the builds

 -I tested it by first addig random components to a build in the database and then running it and check if the html does work or not. (it did not work first but then I fixed few things to make it work and it does work now !)

