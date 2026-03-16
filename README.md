# Approval Customizations - Odoo 18

A professional Odoo 18 module that extends the native Approvals module with custom approval categories and business logic.

## Features

- 4 custom approval categories:
  - **Claim Request** - with amount validation (max 500 EGP)
  - **Recruitment Request** - auto-creates Job Position on approval
  - **Travel Request** - with destination and date fields
  - **Equipment Request** - with equipment type and price validation (max 1500 EGP)
- Auto-assign approvers based on category using security groups
- Dynamic form fields that show/hide based on category
- Business validations using @api.constrains
- Automatic Job Position creation on Recruitment approval
- XPath view inheritance to extend existing Approvals form

## Technical Details

- **Odoo Version:** 18.0 Enterprise
- **Type:** Customization (inherits existing module)
- **Models:** `approval.request`, `approval.category`
- **Dependencies:** `approvals`, `hr`

## Installation

1. Copy the `approval_customizations` folder to your Odoo addons path
2. Restart Odoo server
3. Go to Apps → Update Apps List
4. Search for "Approval Customizations" and install

## Workflow

1. Employee creates an approval request and selects a category
2. Approvers are automatically assigned based on the category
3. Manager approves or rejects the request
4. On Recruitment approval → Job Position is created automatically

## Author

Ziad Waleed - Junior Odoo Developer
