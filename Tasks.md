# BugsFixing

## 2024/07/21

1) [x] Fix skip to search button after url given if clicked again, should have a message telling user to repeat search since the search was done
2) [x] Fix state passed, the notification sent to the user should load his favourite language and not get it from state

## 2024/07/30

1) [x] Manage 404 response in http client request
   Problem arised when searching with an unexistent location
2) [ ] Manage Users with no username
   Problem when user has no telegram username we need another way to approve him


# NewBugsIntroducing

## 2024/07/23 

1) [x] Using the crafted url with search preferences scrape relevant listings informations.
   1) [x] Create template for listing container to access relevant infos
   2) [x] Create scraping function to get html body 
   3) [x] From html body using the template access all listings containers and extract relevant informations
2) [x] Using the scraped listings informations create and show listings to user

## 2024/07/27

1) [x] Add notification for admins when a new user subscribes
2) [x] In the house search add choice for buying houses too and adapt scraping
3) [x] Adapth for renting only rooms too

## 2024/07/30
1) [x] Change how the event loop is cretead, wanted behavior is to create only one instance and share it across the app where needed.
2) [ ] Add panic button handlers
   1) [x] stop handler when searching listings to prevent user from spam if needed.
   2) [ ] handler for admins to stop application execution.

## 2024/07/31
1) [x] Add a button to let user going to the previous question in search params handler