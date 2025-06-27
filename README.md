# Veracode PDF report download

## Overview

This script downloads PDF Summary or Detailed reports from Veracode

## Installation

Clone this repository:

    git clone https://github.com/cadonuno/veracode-download-pdf-report.git

Install dependencies:

    cd veracode-download-pdf-report
    pip install -r requirements.txt

### Getting Started

It is highly recommended that you store veracode API credentials on disk, in a secure file that has 
appropriate file protections in place.

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>
    
### Running the script
    py get-pdf-report.py -a <application_name> [-s <sandbox_name> -v <scan_version> -rt <report_type> -o <output_file>]
        Fetches the <report_type> PDF report for the application called <application_name>.
        The report will be saved to a file called <output_file> (defaults to <report_type>.pdf).
        A <scan_version> can be provided to download a specific scan, otherwise, the latest scan will be fetched.
        By default, reports are downloaded from Policy Scans, but a <sandbox_name> can be provided to download a Sandbox Scan instead.

If a credentials file is not created, you can export the following environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python get-pdf-report.py -a <application_name> [-s <sandbox_name> -v <scan_version> -rt <report_type> -o <output_file>]

## License

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

See the [LICENSE](LICENSE) file for details
