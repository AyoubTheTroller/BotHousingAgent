# Bugs Fixing

## 2024/07/21

1) [x] Fix skip to search button after url given if clicked again, should have a message telling user to repeat search since the search was done
2) [x] Fix state passed, the notification sent to the user should load his favourite language and not get it from state

## 2024/07/30

1) [ ] Manage 404 response in http client request
   Problem arised when searching with an unexistent location
2) [ ] Manage Users with no username
   Problem when user has no telegram username we need another way to approve him


# New Bugs Introducing

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