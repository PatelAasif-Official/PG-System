# PG System

A paying-guest / small hotel management app built on the
[Frappe Framework](https://frappeframework.com). It covers the full stay lifecycle —
listing rooms on a public website, taking bookings, checking guests in and out,
billing them, and scheduling housekeeping work for staff.

> **This is an assignment project.** It was built as a take-home assignment for
> karkhana.io in January 2024, to a short deadline. It is a demonstration of Frappe
> app development rather than production software — the scope is deliberately narrow
> and some areas are simplified. See [Scope and limitations](#scope-and-limitations).

## Installation

Install into an existing [bench](https://github.com/frappe/bench):

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/PatelAasif-Official/PG-System.git --branch master
bench --site $YOUR_SITE install-app pg_system
```

The app does not pin a Frappe version — it was built in January 2024 against the
then-current release.

Installing creates two roles via fixtures: **PG Manager** and **PG Employee**.

## How it fits together

```
Room  ──(booked via website or desk)──>  Check-in and Check-out  ──>  Payment Entry
  │                                              │                          │
  │  bed count drives room status                │  auto-creates Customer   │  emails invoice
  │                                              │  for portal bookings     │  on submit
  │
  └──<  Work Log  <──(hourly scheduler)──  Periodic Maintenance
              │
              └── rooms distributed evenly across active Employees
```

## Doctypes

### 1. Room

A bookable room, submittable, and published to the website as a
[Website Generator](https://frappeframework.com/docs/user/en/guides/portal-development/website-generator)
at `/rooms`.

| Field | Notes |
|---|---|
| Room Number | |
| Type Of Room | Occupancy: Single Occupancy, Double Sharing, Triple Sharing, Multiple Sharing |
| Type | AC or Non-AC |
| Number Of Beds | Set automatically to 1, 2 or 3 for the fixed occupancy types; editable only for Multiple Sharing |
| Status | Read-only: Available, Occupied, Partially Occupied, Under Maintenance |
| Number Of Beds Available | Drives Status — 0 means Occupied, equal to Number Of Beds means Available, anything between means Partially Occupied |
| Price | Currency, editable after submission |
| Photo | Shown on the web portal |

Status is derived, never set by hand. The one exception is **Under Maintenance**,
which the update logic leaves alone so a manager can take a room out of service
regardless of its bed count. A validation prevents available beds from exceeding the
room's total.

Rooms publish to the website automatically on save; the **Unpublish** button takes one
back down.

![Room](https://github.com/PatelAasif-Official/PG-System/assets/88040507/28921704-e4fd-49e0-8b6f-e6d56601f825)

### 2. Check-in and Check-out

One guest's stay in one room. Submittable, where the document state carries the
meaning:

- **Draft** — booked, not yet arrived
- **Submitted** — checked in
- **Checked Out** — via the Check Out button, visible only to PG Manager

Selecting a Room Type (AC / Non-AC) filters the Room link to matching rooms that are
Available or Partially Occupied. Room Number and Price Per Night are fetched from the
Room; guest name, mobile and email are fetched from the Customer.

Submitting is blocked before the check-in date, so a manager cannot check a guest in
early. On check-in the room's available beds decrease by one and on check-out they
increase by one, which re-derives the room's status. Checking into a room with no free
beds is rejected.

Bookings made through the website portal set the `from_portal` flag, and the app
creates a Customer record automatically from the guest's first name, last name, mobile
and email.

![Check-in and Check-out](https://github.com/PatelAasif-Official/PG-System/assets/88040507/c081c2cb-0d5f-48ad-85b4-7497e4d1d567)

### 3. Customer

Guest master. Full Name is composed automatically from first, middle and last name.

Identity Type offers Aadhaar Card, PAN Card, Driving Licence, Passport and Other, with
a free-text name field appearing for Other. An ID card attachment is required, since
hotels generally have to collect one. Mobile number and email address are used for the
invoice, and a free-text address field covers cases where the ID does not carry a
usable one.

![Customer](https://github.com/PatelAasif-Official/PG-System/assets/88040507/1958ef6f-b736-4dc5-a647-7312e6e10922)

### 4. Payment Entry

Billing after checkout. Select the booking and everything else is fetched from it —
guest, email, dates, room, room number and rate per night.

Nights are calculated from the check-in and check-out dates, with a same-day stay
counted as one night. Total is nights × rate; an optional percentage discount produces
the Grand Total. Only one Payment Entry is allowed per booking.

On submit, a **Hotel Invoice** email notification goes to the guest's email address.

![Payment Entry](https://github.com/PatelAasif-Official/PG-System/assets/88040507/442a9742-217d-4d27-ae0f-a7abbc1716cd)

### 5. Employee

Staff master, with Full Name composed the same way as Customer. Status can be Active,
Left, On Leave or Inactive. Designation is Manager, Cleaner or Attendant.

Ticking **Create User** before saving — or pressing the button on an existing record —
creates a Frappe User and links it back to the employee. The new user gets the
**PG Manager** role if their designation is Manager, otherwise **PG Employee**. Linking
to a User is what makes user permissions usable for staff.

![Employee](https://github.com/PatelAasif-Official/PG-System/assets/88040507/8667fcea-64e0-43ed-9406-4d976d6fb7c6)

### 6. Periodic Maintenance

A manager schedules housekeeping work for a future date — say, cleaning every room on
15 February. Type of Work is Room Service, Cleaning, Repair or Inspection. Past dates
are rejected, and the same type of work cannot be scheduled twice on one date.

Status moves from **Scheduled** to **Work Log Created** on its own once the work has
been handed out.

![Periodic Maintenance](https://github.com/PatelAasif-Official/PG-System/assets/88040507/11f244ad-546c-49bf-b69c-3dab9016514c)

### 7. Work Log

Created by the system, never by hand. An hourly scheduled job picks up every submitted
Periodic Maintenance scheduled for today that is still **Scheduled**, then:

1. Collects all Active employees and all rooms not Under Maintenance.
2. Splits the rooms into as-even-as-possible groups, one per employee, distributing
   the remainder so group sizes differ by at most one.
3. Creates a Work Log per employee carrying the work type, duration, schedule date and
   time, the manager's description, and that employee's room list as a read-only child
   table.
4. Flips the Periodic Maintenance to **Work Log Created**.

Employees update Status themselves — Pending, In Progress or Completed. A guard
prevents two Work Logs for the same employee and maintenance task.

![Work Log](https://github.com/PatelAasif-Official/PG-System/assets/88040507/12030546-9c52-49da-8647-c3c762ae6eee)

## Website portal

Rooms are published automatically and listed at `/rooms`. Only Available and Partially
Occupied rooms appear to guests. Clicking one opens a detail view with a **Book Now**
button leading to the `book-room` web form, which does not require a login and creates
both the booking and the guest's Customer record.

### List view

![List view](https://github.com/PatelAasif-Official/PG-System/assets/88040507/8ba20d78-a7c0-4ecc-8a10-ee7fdcd28b47)

### Detail view

![Detail view](https://github.com/PatelAasif-Official/PG-System/assets/88040507/6167ac54-e3cf-42a1-bd84-eb590d01f18e)

### Booking form

![Booking screen](https://github.com/PatelAasif-Official/PG-System/assets/88040507/b61fa8af-2d65-45ab-b989-201b39fc540c)

## Scope and limitations

Being a time-boxed assignment, several things were kept deliberately simple:

- **Designations** are limited to Manager, Cleaner and Attendant, and **work types** to
  Room Service, Cleaning, Repair and Inspection. Both were picked as reasonable
  examples rather than researched against how a real PG operates.
- **No availability calendar.** A room's status reflects only right now, so there is no
  way to see or reserve against future occupancy.
- **Work distribution ignores workload** — rooms are split evenly by count across
  active employees, with no regard for designation, shift or room size.
- **Payment is recorded, not processed.** There is no payment gateway; Payment Entry
  captures what was owed and emails an invoice.
- **The Role fixture is unfiltered**, so installing exports every role on the site
  rather than only PG Manager and PG Employee.

## License

MIT
