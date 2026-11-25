# Diocesan Estates Management System

## Presentation script and demonstration guide

**Institution:** Church of Uganda, Diocese of Madi West Nile  
**Department:** Diocesan Estates Department  
**Purpose:** A single, controlled system for managing the Diocese's property portfolio, tenants, leases, revenue, operations, records, risks, and staff activity.

---

## 1. Opening statement

Good morning. I am presenting the Diocesan Estates Management System, a web-based platform designed to give the Estates Department
one reliable place to manage the complete life cycle of church property.

The system brings together information that is often scattered across notebooks, spreadsheets, paper files, messaging applications, 
and individual staff computers. It gives management a current view of property ownership, occupancy, rental income, expenses, 
maintenance, compliance, development projects, land disputes, risks, assets, visitors, parking, utilities, and estate documents.

The main reason to adopt the system is control. Every important estate record has a structured form, a clear status, a responsible 
workflow, and a traceable update path. This improves decision-making, reduces duplication, supports accountability, and makes it 
easier to identify overdue or high-risk matters before they become expensive problems.

---

## 2. What the application solves

The application addresses the following operational problems:

- Property information is stored in a searchable master register.
- Buildings and units are connected to their parent property.
- Tenants, occupancy records, and leases are linked together.
- Lease activity can automatically update unit occupancy and create an invoice.
- Payments update invoice balances and payment status.
- Finance staff can compare billed income, collected income, expenses, receivables, and cash flow.
- Maintenance requests can be tracked from reporting to completion.
- Inspections provide condition, safety, and maintenance evidence.
- Compliance documents can be monitored for expiry.
- Development projects can be monitored against budgets and target dates.
- Land disputes and risks have owners, statuses, next-action dates, and mitigation information.
- Assets, contractors, visitors, parking spaces, utility meters, and meter readings have dedicated registers.
- Estate documents can be attached to properties and marked confidential.
- Notifications highlight important events such as new leases, maintenance requests, and lease renewals.
- Search allows staff to find records across several modules quickly.
- Audit logs record common create, update, and delete actions.

---

## 3. Application layout and navigation

After login, the user sees a persistent left sidebar and a top bar.

### Left sidebar

The sidebar is divided into two sections.

**Estates Office**

1. Dashboard
2. Property portfolio
3. People and tenancy
4. Finance
5. Estates operations

**Governance**

6. Records and controls
7. My staff account
8. Register staff
9. Notifications

The grouped items use expandable sections. Clicking a group heading opens or closes its submenu. 
The active page is highlighted so the user always knows where they are.

### Top bar

- The list button collapses or expands the sidebar, which is useful on smaller screens.
- The search box searches properties, tenants, leases, invoices, payments, expenses, assets, contractors, and visitors.
- Search suggestions appear while typing at least two characters. Clicking a result opens that record's detail or edit page.
- The bell icon opens notifications and shows an indicator when unread items exist.
- The user chip opens the staff profile.
- The sign-out button ends the current session.

### Common page controls

Most register pages use the same pattern:

- A primary button such as **New property**, **Add tenant**, **Create lease**, or **New risk** opens a form.
- A light **Edit** button opens the same form with existing values.
- A red **Delete**, **Trash**, or **Move to trash** button opens a confirmation page before deletion.
- **Cancel** returns to the previous page.
- **Save record** validates the form, stores the record, writes an audit entry, displays a success message, and returns to the relevant register.
- Validation errors appear beside the affected fields and the user remains on the form until the information is corrected.

---

## 4. Dashboard demonstration

I would start the live demonstration on the Dashboard because it gives the panel an immediate view of management value.

The dashboard calculates its figures from the current database and uses today's date to identify matters requiring attention.

### Portfolio indicators

- Total properties
- Active properties
- Total units
- Occupied units
- Vacant or available units
- Reserved units
- Units under maintenance
- Occupancy rate

The occupancy rate is calculated as occupied units divided by total units. 
These indicators help management understand how much of the portfolio is producing value and where capacity is unused.

### Finance indicators

- Receivables and outstanding invoice balances
- Overdue invoices and overdue balance
- Current-month collections
- Previous-month collections for comparison
- Current-month expenses
- Current-month net cash flow

An invoice balance is never shown below zero. Payments are counted from payment records, and the dashboard excludes cancelled invoices from receivables.

### Tenancy and lease indicators

- Active tenants
- Active leases
- Leases expiring within the next 30 days
- Active leases already past their end date

These indicators help the Estates Office act before revenue is lost or a tenancy becomes irregular.

### Maintenance and inspection indicators

- Open maintenance requests
- Urgent or high-priority maintenance
- Estimated and actual maintenance costs
- Inspections scheduled within the next 30 days

### Development and asset indicators

- Active or approved projects
- Projects over budget
- Total approved project budget
- Total project expenditure
- Asset count
- Assets requiring attention because of poor condition, damage, repair status, or expired warranty

### Governance indicators

- Open land disputes
- Critical risk items
- Risk reviews due soon
- Expired compliance records
- Compliance records expiring soon
- Properties without a title reference
- Total estate documents
- Confidential document count

### Dashboard activity panels

The dashboard also shows recent payments, open maintenance work, active development projects, unresolved disputes, risk oversight, and recent audit activity. Each panel has a link to the corresponding register so the user can move from a summary to the underlying records.

---

## 5. Property portfolio

Open **Property portfolio** and select **Master property register**.

### Master property register

The register lists properties by name and shows the property code, property type, location, status, ownership, and unit count. The property list can be filtered by property name or property code.

### Add property

The property form captures:

- Unique property code
- Property name
- Type: residential, commercial, office, retail, industrial, mixed use, or land
- Address, city, and country
- Owner name
- Description
- Status: active, inactive, or under development
- Purchase value
- Tenure type, with Church owned as the default
- Title reference
- Parish and archdeaconry
- Latitude and longitude
- Acquisition date
- Protected flag

After saving, the user returns to the property register. A property may be opened to see its detail page.

### Property detail page

The detail page presents the property identity and its related information. It is the logical parent for buildings, units, documents, inspections, assets, expenses, projects, disputes, risks, compliance records, visitors, parking spaces, and other operational information.

### Add building

The building form links a building to a property and captures the building name and number of floors. After saving, the user returns to the property register.

### Add unit

The unit form links a unit to a property and optionally to a building. It captures:

- Unit number
- Floor
- Unit type
- Bedrooms and bathrooms
- Area in square metres
- Monthly rent
- Service charge
- Status: available, occupied, reserved, maintenance, or unavailable

Units are the connection point between property, tenant, lease, invoice, maintenance, inspection, meter, and occupancy records.

### Property actions

- **Edit** updates the property, building, or unit.
- **Delete** opens a confirmation screen.
- A property cannot be safely removed when protected records depend on it. The system reports the linked record types and advises the user to deactivate the record or resolve the dependencies first.

---

## 6. People and tenancy

Open **People and tenancy**.

### Tenants

The tenant register can be searched by full name, tenant ID, or phone number.

The tenant form captures:

- Unique tenant ID
- Full name
- Phone and email
- National ID
- Address
- Emergency contact
- Status: active, inactive, or prospect
- Notes

The **Edit** button updates the tenant. The delete action asks for confirmation and can be blocked if a linked lease, invoice, or payment protects the record.

### Occupancy records

An occupancy record connects a tenant to a unit. It captures move-in date, move-out date, and whether the occupancy is active. The register orders active occupancies first and then the most recent move-in dates.

The preferred workflow is usually to create the occupancy through an active lease because the lease process synchronizes the occupancy automatically. A direct occupancy record is still available in the interface for the specifically configured user account.

### Leases

The lease register shows total leases, active leases, leases expiring soon, and active leases past their end date. Lease records are ordered by end date so the nearest deadlines appear first.

The lease form captures:

- Unique lease number
- Tenant
- Unit
- Start date and end date
- Rent
- Deposit
- Service charge
- Payment frequency
- Notice period in days
- Status: draft, active, expired, terminated, or renewal pending
- Terms
- Renewal-notice flag

The system protects the relationship between the tenant, unit, and lease. When an active or renewal-pending lease is saved:

1. The unit status becomes occupied.
2. A tenant-unit occupancy record is created or updated.
3. The tenant is marked active.
4. The system creates or retrieves an invoice linked to the lease.
5. The invoice amount is rent plus service charge.
6. The initial paid amount comes from the deposit when the invoice is first created.

When a lease is no longer active or renewal-pending, the unit can return to available unless another active lease still occupies it.

The unit details endpoint also supports the lease form by returning unit number, rent, service charge, and property information for the selected unit.

### Lease renewal workflow

An active lease that falls within the 30-day renewal window can move to renewal pending. The system can email the tenant when an email address exists, mark the notice as sent to prevent duplicate messages, and create high-priority staff notifications. Reminder processing can also notify staff and tenants at expiry milestones without changing the renewal status again.

---

## 7. Finance

Open **Finance** and select **Finance dashboard**.

The finance dashboard displays:

- Total billed from invoices
- Total collected from payments
- Total expenses
- Recent invoices
- Recent payments

### Create invoice

The invoice form captures invoice number, tenant, optional unit, issue date, due date, description, amount, paid amount, status, and optional linked lease. In normal lease operation, the lease workflow can create the invoice automatically.

Invoice statuses are unpaid, partially paid, paid, overdue, or cancelled. The balance equals amount less paid amount, never below zero.

### Record payment

The payment form captures receipt number, tenant, optional invoice, payment date, amount, payment method, reference, and notes. Payment methods are cash, bank transfer, mobile money, card, and cheque.

When a payment is saved or deleted, the related invoice is recalculated:

- No payment means unpaid, unless the due date has passed.
- A payment below the invoice amount means partially paid.
- Payment equal to or greater than the invoice amount means paid.
- A past-due unpaid invoice becomes overdue.

This prevents finance staff from manually maintaining balances in multiple places.

### Add expense

The expense form captures optional property, category, description, amount, expense date, vendor, and reference. Categories include maintenance, utilities, security, cleaning, staff, tax, insurance, and other.

The expense flows back to the finance dashboard and the main dashboard's cash-flow calculations.

---

## 8. Maintenance

The maintenance module is available at the maintenance route and is represented on the main dashboard, although it is not currently listed as a separate sidebar group.

The maintenance register tracks:

- Unique request number
- Unit
- Reporting staff member
- Category
- Description
- Priority: low, normal, high, or urgent
- Status: reported, assigned, in progress, awaiting parts, completed, or closed
- Estimated cost and actual cost
- Scheduled date and completed date
- Assigned person or contractor

The workflow is:

1. A user creates a maintenance request.
2. The request begins as reported.
3. Staff assign the work and update its status as work progresses.
4. Costs and dates are updated as evidence becomes available.
5. Completed or closed requests leave the open-maintenance dashboard count.

When a new request is created, active staff users receive a high-priority notification.

---

## 9. Estates operations

Open **Estates operations** and select **Operations overview**.

The overview combines operational registers and highlights:

- Total inspections
- Assets
- Active contractors
- Expired and upcoming compliance items
- Active projects
- Open disputes
- Open risks
- Visitors still on site

### Inspections

The inspection register records property, optional unit, inspection type, inspection date, inspector, condition, recommendations, and score out of 100. Types include move in, routine, move out, safety, and maintenance.

**New inspection** opens the form. **Edit** updates the inspection. **Delete** asks for confirmation.

### Development projects

The project register tracks project code, property, project name, sponsor, description, status, start date, target date, approved budget, spent amount, and approval reference.

Statuses are proposed, approved, active, on hold, completed, or cancelled. The dashboard highlights approved or active projects and identifies projects whose spent amount exceeds the approved budget.

### Disputes and encroachment

The dispute register records a unique reference, property, claimant, summary, status, assigned officer, next action date, and resolution. Statuses are open, in mediation, in court, resolved, and closed.

The register helps management distinguish unresolved cases from completed cases and follow the next action date.

### Risk register

Each risk has a unique reference, optional property, title, description, likelihood, impact, mitigation, owner, review date, and status. Likelihood and impact use low, medium, high, and critical levels.

The dashboard treats a risk as critical when both likelihood and impact are high or critical, unless the risk is closed.

### Compliance

The compliance register tracks property, title, reference, expiry date, status, and notes. It supports a clear view of expired documents and documents approaching expiry within 30 days.

**New compliance item** opens the form. **Edit** updates the record. **Delete** asks for confirmation.

### Assets

The asset register captures property, unique asset code, name, category, purchase date, purchase cost, condition, warranty expiry, and notes.

The asset detail page shows the asset and its property. The **Trash** action opens a confirmation screen. In this build, the trash action deletes the record after confirmation rather than providing a recovery bin.

### Contractors

The contractor register captures name, service, phone, email, address, and active status. The detail page provides the contractor information. Contractors can be created, edited, viewed, and moved through the delete confirmation flow.

### Visitors

The visitor register supports estate access control. It records property, host name, visitor name, phone, vehicle registration, purpose, check-in time, and check-out time.

The detail page shows host, phone, vehicle, check-in, and check-out. When check-out is blank, the interface identifies the visitor as still on site. The operations dashboard counts visitors whose check-out is missing.

### Parking

The parking register records property, space number, assigned person, vehicle registration, monthly fee, and active status. It supports allocation and tracking of estate parking spaces.

### Utility meters and readings

The meter register records unit, meter number, utility type, and active status. Utility types are electricity, water, and gas.

The reading register records meter, reading date, current reading, previous reading, and notes. The meter page links to the reading page, and both pages provide add, edit, and delete actions.

---

## 10. Records and controls

Open **Records and controls**.

### Estate records

Estate records provide a central document register. Each record can contain:

- Title
- Category: land title, lease agreement, building plan, report, policy/manual, or other
- Reference
- Optional linked property
- Uploaded file
- Description
- Owner
- Confidential flag

The user can add, edit, and delete a record. Confidential documents can be identified separately for governance and management attention.

### Diocese profile

The Diocese profile stores institutional identity and control information:

- Church name
- Diocese name
- Department name
- Postal address
- Location
- Effective date
- Review date
- Approved by
- Approval date
- Active status

The profile area lists records, opens a detail page, supports adding and editing profiles, and provides a delete confirmation flow.

### Administration

The Administration link opens Django administration. It is intended for users with the necessary staff or superuser privileges and provides administrative access to the registered models, including core records, properties, tenants, leases, finance, maintenance, and operations.

---

## 11. Staff accounts, access, and roles

### What the current build enforces

- The dashboard and application modules require a logged-in user.
- Staff registration creates a user, marks the account as staff, logs the user in, and redirects to the dashboard.
- A user can update first name, last name, email, and username from **My staff account**.
- Password change is available from the account area.
- Password reset provides the standard reset, confirmation, and completion flow.
- The Administration link relies on Django's staff/admin access rules.
- Notifications are associated with individual users.

### Important access-control limitation to disclose to the panel

The current codebase does not define named roles such as Estates Manager, Finance Officer, Property Officer, Maintenance Officer, or Viewer with different permissions. Most application views use authentication checks, meaning any authenticated user can reach the ordinary create, edit, and delete workflows unless deployment-level controls add further restrictions.

There are two current interface exceptions tied to the username `j`:

- **Record occupancy** is shown in People and tenancy only for username `j`.
- **Create invoice** is shown in Finance only for username `j`.

These are interface visibility rules, not a complete security role system. The recommended adoption decision is to keep the modules but add formal Django groups and permissions before production use. Suggested roles are:

| Suggested role | Recommended access |
|---|---|
| Estates Manager | Dashboard, all registers, approvals, records, risks, disputes, and administration oversight |
| Property Officer | Properties, buildings, units, inspections, assets, compliance, and documents |
| Tenancy Officer | Tenants, occupancies, leases, renewals, and tenant-related records |
| Finance Officer | Invoices, payments, expenses, receivables, collections, and finance reporting |
| Operations Officer | Maintenance, inspections, contractors, visitors, parking, meters, and projects |
| Governance/Records Officer | Estate records, Diocese profile, compliance, risks, disputes, and audit review |
| Viewer/Board Reviewer | Read-only dashboard and approved registers |
| System Administrator | User accounts, Django administration, configuration, backups, and technical support |

The system already has a good foundation for this improvement because its records are separated into models and its business operations are organized into modules.

---

## 12. Audit trail, notifications, and controls

### Audit trail

Common create, update, and delete operations use a shared workflow that writes an AuditLog entry containing:

- User
- Action
- Model name
- Object ID
- Description
- IP address when available
- Timestamp

The dashboard displays recent audit activity for management review.

### Notifications

Notifications have a title, message, URL, priority, read state, and timestamps. The bell badge shows unread notifications. Opening the notifications page lists recent user notifications and marks unread items as read.

The system creates staff notifications for new maintenance requests and new leases. Lease renewal processing can also generate high-priority notifications and emails where the tenant has an email address.

### Validation and safe deletion

Forms validate required fields and display field-level errors. Relationships use protected deletion where appropriate, so users cannot casually remove a tenant, unit, or property that is still needed by linked financial or lease records. Delete actions require an explicit confirmation POST request.

---

## 13. Recommended live demonstration sequence

For a short panel demonstration, I would use this sequence:

1. **Login** and show the branded Diocese layout.
2. **Dashboard** and explain portfolio, finance, lease, maintenance, risk, and compliance indicators.
3. Open **Property portfolio** and show a property, building, and unit relationship.
4. Open **People and tenancy** and show a tenant and occupancy record.
5. Create or open a **Lease** and explain the automatic unit, occupancy, and invoice synchronization.
6. Open **Finance** and show the invoice, payment, balance, and status relationship.
7. Open **Operations overview** and show inspections, projects, disputes, risks, compliance, assets, visitors, parking, and utilities.
8. Use the top-bar **search** to find a tenant, property, or asset and open the result.
9. Open **Notifications** and explain how staff receive operational alerts.
10. Open **Records and controls** and show a linked estate document and Diocese profile.
11. Open **My staff account** and explain profile and password management.
12. Close with the adoption case and the formal role-permission improvement required before production rollout.

---

## 14. Adoption case for the panel

The system should be adopted because it creates a practical management control layer for the Diocese's estates.

### Operational value

Staff work from one current source of information instead of maintaining disconnected registers. A property can be followed from its identity and title reference through buildings, units, tenants, leases, invoices, payments, maintenance, inspections, documents, risks, and compliance.

### Financial value

The application connects leases, invoices, payments, and expenses. This gives management a clearer view of what has been billed, what has been collected, what is overdue, what has been spent, and whether monthly cash flow is improving.

### Governance value

The system records responsible owners, statuses, dates, references, approvals, documents, risks, disputes, and audit activity. This supports reporting to diocesan leadership and reduces dependence on personal memory or informal follow-up.

### Risk and compliance value

The dashboard brings overdue leases, expiring compliance items, missing title references, critical risks, open disputes, and assets needing attention to the surface. This helps the Estates Department act before issues become losses or legal exposure.

### Service value

Tenants and units are linked to leases and maintenance. Staff can see what work is open, who reported it, the priority, the estimated cost, the actual cost, and the completion status.

### Scalability value

The application separates the major business areas into modules, uses reusable forms and register patterns, supports uploaded records, and can be extended with formal roles, reports, exports, backups, and integrations.

---

## 15. Recommended implementation conditions

To move from a strong working system to a production-grade diocesan platform, I recommend:

- Replace the username-specific visibility rules with formal groups and model permissions.
- Restrict staff registration to an authorized administrator or approval workflow.
- Add a read-only role for leadership and board review.
- Add backup, restore, and data-retention procedures.
- Add exportable reports for finance, occupancy, leases, compliance, and risks.
- Add a visible Maintenance item to the sidebar for easier discovery.
- Add recovery or archival behavior if the word “trash” is intended to mean recoverable deletion.
- Configure production email, secure deployment settings, HTTPS, and media-file access controls.
- Train staff on data quality, especially title references, lease dates, payment references, and document confidentiality.
- Pilot the system with a controlled set of properties before full diocesan migration.

These are controlled improvements, not reasons to reject the application. The core workflow already covers the main estate-management needs and gives the Diocese a structured base for adoption.

---

## 16. Closing statement

The Diocesan Estates Management System gives the Diocese visibility, accountability, and continuity across its property portfolio. It turns estate information into operational evidence that management can search, review, update, and act on.

Adopting the application will help the Estates Department protect property records, improve occupancy and revenue oversight, follow up maintenance and compliance, manage projects and disputes, and provide leadership with timely information. With formal role permissions and the recommended production controls added, the system can become the Diocese's central platform for responsible estate administration.

**Final message:** The value of this application is not only that it stores records. It connects the records so that a change in one part of estate management can be understood and acted on in the other parts.

---

## Appendix: module-to-record map

| Module | Main records | Main outcome |
|---|---|---|
| Dashboard | Calculated portfolio, finance, tenancy, maintenance, governance, and audit indicators | Management overview |
| Property portfolio | Properties, buildings, units | Structured asset register |
| People and tenancy | Tenants, occupancies, leases | Controlled tenancy lifecycle |
| Finance | Invoices, payments, expenses | Revenue and expenditure control |
| Maintenance | Maintenance requests | Work tracking and cost visibility |
| Estates operations | Inspections, projects, disputes, risks, compliance, assets, contractors, visitors, parking, meters, readings | Operational control |
| Records and controls | Estate documents, Diocese profiles, administration | Governance and evidence |
| Staff account | Registration, profile, password change, password reset | Account continuity |
| Notifications | User alerts and renewal notices | Timely follow-up |
| Search | Cross-module record lookup | Faster retrieval |
| Audit | User action history | Accountability |
