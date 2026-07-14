Below is a comprehensive Product Requirements Document (PRD) based on the exam sheet. I've expanded the requirements into a real-world project that follows Django best practices and would score well while also being portfolio-worthy.

---

# Product Requirements Document (PRD)

# Atlas Car Location

### Car Rental Management System

**Version:** 1.0

**Framework**

* Backend: Django 5
* Frontend: Django Templates + Bootstrap 5
* Database: PostgreSQL (SQLite for development)
* Authentication: Django Authentication
* ORM: Django ORM
* PDF: ReportLab
* Charts: Chart.js
* File Storage: Django Media
* Email: Django Email Backend

---

# Project Overview

Atlas Car Location wants a complete web application to manage every aspect of its car rental business.

The system should manage:

* Vehicle Fleet
* Customers
* Reservations
* Contracts
* Invoices
* Payments
* Maintenance
* Alerts
* Dashboard
* Reports

The application must follow Django MVT architecture.

---

# User Roles

## Administrator

Full permissions

Can

* Manage vehicles
* Manage customers
* Create reservations
* Generate invoices
* Register payments
* View dashboard
* Export reports
* Configure alerts

---

## Employee

Limited permissions

Can

* Create reservations
* Search customers
* Print contracts
* Register payments

Cannot

* Delete vehicles
* Change system settings

---

# Application Modules

---

# Module 1 — Vehicle Fleet Management

## Vehicle List

Display all vehicles as cards or table.

Each vehicle shows

* Photo
* Brand
* Model
* License Plate
* Category
* Daily Price
* Status

---

## Dashboard Statistics

Display

Total Vehicles

Available

Rented

Maintenance

Out of Service

---

## Vehicle Filters

Filter by

Category

* City
* SUV
* Sedan
* Utility
* Luxury

Status

* Available
* Rented
* Maintenance
* Out of Service

Brand

Transmission

Price

---

## Vehicle Details

Fields

License Plate

* Unique
* Moroccan format validation

Brand

Model

Manufacturing Year

Color

Category

Transmission

* Manual
* Automatic

Seats

Mileage

Last Revision Date

Daily Rental Price (MAD)

Security Deposit

Photo

Status

---

## CRUD Operations

Create Vehicle

Edit Vehicle

Delete Vehicle

View Details

Search

---

# Maintenance Module

Create maintenance record

Fields

Vehicle

Maintenance Type

Garage

Date

Cost

Notes

Mileage

---

## Maintenance History

Every vehicle displays

All maintenance operations

Chronological history

Total maintenance cost

---

## Automatic Maintenance Alert

System checks

If

Current Mileage

>

Configured Threshold

Show alert

Vehicle needs revision.

---

# Module 2 — Customer Management

Customer Information

Fields

National ID / Passport

First Name

Last Name

Nationality

Birth Date

Driving License Number

Driving License Expiration Date

Phone

Email

Address

Customer Type

* Individual
* Company
* Partner Agency

---

## Customer Validation

During reservation

If driver's license expired

Prevent reservation

Display warning

---

## Customer History

Display

Reservations

Payments

Invoices

Contracts

Total rentals

---

## CRUD

Add

Edit

Delete

Search

---

# Module 3 — Reservation Management

Create Reservation

Workflow

Step 1

Search Customer

By

Name

National ID

Passport

---

Step 2

Select Vehicle

Only available vehicles

No overlapping reservations

---

Step 3

Rental Information

Pickup Date

Return Date

Pickup Location

* Agency
* Airport
* Hotel Delivery

Return Location

---

Step 4

Additional Options

GPS

Baby Seat

Additional Driver

Each option has

Daily Price

---

## Automatic Calculations

Rental Days

Vehicle Price

Options

Deposit

Total

Generate Reservation Number

Example

RES-2026-00021

---

## Reservation Status

Pending

Confirmed

Active

Completed

Cancelled

---

## Reservation List

Columns

Reservation Number

Customer

Vehicle

Dates

Amount

Status

Actions

Confirm

Start

Close

Cancel

---

## Calendar View

Monthly Calendar

Weekly Calendar

Different colors

Pending

Confirmed

Active

Completed

Cancelled

Highlight overlapping reservations

---

# Module 4 — Contracts & Invoices

Generate Rental Contract PDF

Contains

Company Logo

Customer Information

Vehicle Information

Rental Conditions

Signature Areas

Terms & Conditions

---

Generate Invoice PDF

Invoice Number

Customer

Reservation

Rental Days

Daily Price

Options

Deposit

VAT 20%

Total Before Tax

VAT Amount

Total Including VAT

Footer

Company Stamp

Legal Notice

---

# Module 5 — Payments

Payment Methods

Cash

Bank Transfer

Credit Card

Cheque

---

Support Partial Payments

Example

Deposit

Remaining Balance

Final Payment

---

Automatically Calculate

Paid Amount

Remaining Amount

---

Generate Payment Receipt PDF

---

# Module 6 — Deposits

Track

Deposit Received

Deposit Returned

Return Date

Reason if partially returned

---

# Module 7 — Dashboard

KPIs

Total Reservations

Today's Reservations

Monthly Revenue

Yearly Revenue

Fleet Occupancy Rate

Average Revenue Per Vehicle

Most Rented Vehicles

Customer Nationality Distribution

---

Charts

Revenue per Month

Reservations per Month

Vehicle Category Distribution

Reservation Status Distribution

Top 5 Vehicles

---

# Module 8 — Alerts

Vehicle Return Tomorrow

Email Reminder

Dashboard Notification

---

Late Return

Vehicle not returned

Highlight in red

---

Maintenance Alert

Mileage exceeds threshold

---

License Expiration

Driver license expires within

30 days

---

Deposit Return Reminder

---

# Module 9 — Reports

Generate

Monthly Activity Report

PDF

Excel

---

Vehicle Fleet Report

Current Status

Availability

---

Revenue Report

Monthly

Quarterly

Yearly

---

Customer Report

Top Customers

Frequent Renters

Nationality Statistics

---

# Search

Global search

Search

Vehicle

Customer

Reservation

Invoice

Payment

---

# Authentication

Login

Logout

Forgot Password

Role Permissions

---

# Database Design

## Vehicle

* id
* license_plate
* brand
* model
* year
* color
* category
* transmission
* seats
* mileage
* last_revision
* daily_price
* deposit
* photo
* status
* created_at

---

## Maintenance

* id
* vehicle_id
* type
* garage
* date
* mileage
* cost
* notes

---

## Customer

* id
* cin
* passport
* first_name
* last_name
* nationality
* birth_date
* license_number
* license_expiration
* phone
* email
* address
* customer_type

---

## VehicleOption

* id
* name
* daily_price

Examples

GPS

Baby Seat

Additional Driver

---

## Reservation

* id
* reservation_number
* customer
* vehicle
* pickup_date
* return_date
* pickup_location
* return_location
* status
* deposit
* subtotal
* vat
* total

---

## ReservationOption

* reservation
* option
* quantity

---

## Invoice

* id
* invoice_number
* reservation
* subtotal
* vat
* total
* pdf

---

## Payment

* id
* reservation
* method
* amount
* payment_date
* reference

---

## Deposit

* id
* reservation
* amount_received
* amount_returned
* return_date
* notes

---

# Business Rules

* License plate must be unique.
* A vehicle cannot be reserved if its status is not **Available**.
* Reservation dates cannot overlap for the same vehicle.
* Customers with expired driving licenses cannot make new reservations.
* Total rental cost is calculated as: **(Daily Price × Number of Days) + Options + Deposit**.
* VAT is fixed at **20%**.
* Maintenance alerts are triggered when mileage exceeds the configured threshold.
* Only administrators can delete records.

---

# Recommended Django Apps Structure

```
atlas_car/
│
├── accounts/
├── dashboard/
├── vehicles/
├── maintenance/
├── customers/
├── reservations/
├── invoices/
├── payments/
├── reports/
├── alerts/
├── core/
```

---

# Bonus Features (Portfolio Enhancements)

* Responsive Bootstrap 5 interface
* AJAX search for vehicles and customers
* Dark mode toggle
* Dashboard cards with animated counters
* Image upload with preview
* Soft delete for records
* Activity logs for important actions
* Email reminders for returns and license expirations
* Automatic reservation number and invoice number generation
* Export reports to both PDF and Excel

This PRD translates the exam specification into a complete, production-style Django application with a clear architecture, data model, business rules, and feature set that would be suitable both for the exam and as a strong portfolio project.

