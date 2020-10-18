# Product distribution management

This is a django web application which enables the retailers, companies and distributors to track their products, create receipts and extract information from the receipts.


# Table of contents
 - [Project Structure](#project-structure)
   - [Authentication](#authentication)
   - [Receipt management](#receipt-management)
 - [Running the website](#running-the-website)

# Project structure
## Authentication

The user is retailer, distributor or Company. 

The company and distributor can create receipts by adding products or extract information from an exisiting receipt and track the products (were the products defective, reached the destination on time or not).

SQLite3 is used for storing the authentication information.

## Receipt management

This allows the user to extract information from a receipt or create a new receipt by adding products.

# Running the website
```bash
cd prod_dist
```
```python
python manage.py runserver
```
This starts the website in 127.0.0.1:8000 address.