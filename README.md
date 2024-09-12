# Email Sending API with Microsoft Graph and Flask

## Overview

This repository contains a Python-based web API that leverages the Microsoft Graph API to send emails. The API supports multiple recipients in the `To`, `CC`, and `BCC` fields, and can also handle attachments. Authentication is managed using OAuth2.0, ensuring secure access to your Microsoft 365 account.

## Features

- **Send Emails**: Send emails to multiple recipients with support for CC, BCC, and attachments.
- **OAuth2.0 Authentication**: Securely authenticate using Azure AD with tenant ID, client ID, and client secret.
- **Flask-Based**: Simple and lightweight web API built using Flask.
- **Customizable From Address**: Specify the `from` address for emails.

## Requirements

- Python 3.7+
- Flask
- `msal` Python package
- Microsoft Azure account with appropriate permissions

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vaibhavwtg/python-sendmail.git
   cd python-sendmail
