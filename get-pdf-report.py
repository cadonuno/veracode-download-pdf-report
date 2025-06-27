import argparse
from veracode_api_py import Applications, Sandboxes, VeracodeAPI
from veracode_api_py.apihelper import APIHelper
import xml.etree.ElementTree as ET

def get_application(application_name):
    applications = Applications().get_by_name(application_name)
    for application in applications:
        if application["profile"]["name"] == application_name:
            return application
    raise Exception(f"Unable to find application named {application_name}")

def get_sandbox(application_guid, sandbox_name):
    sandboxes = Sandboxes().get_all(application_guid)
    for sandbox in sandboxes:
        if sandbox["name"] == sandbox_name:
            return sandbox
    raise Exception(f"Unable to find sandbox named {sandbox_name}")

def get_build(application, sandbox, version):
    build_list_bytes = VeracodeAPI().get_build_list(application["id"], sandbox["id"] if sandbox else None)
    build_list_str = build_list_bytes.decode("utf-8")
    build_list = ET.ElementTree(ET.fromstring(build_list_str)).getroot()
    if version:
        for build in build_list.iter():
            if "version" in build.attrib and build.attrib["version"] == version:
                return build
    elif len(build_list):
        return build_list[len(build_list)-1]
    
    raise Exception(f"Unable to find scan version {version}")

def save_report(build, report_type, output):
    api_helper = APIHelper()

    if not report_type or "summary_report" == report_type:        
        bytes = api_helper._xml_request(api_helper.baseurl + "/4.0/summaryreportpdf.do", "GET", params={"build_id": build.attrib["build_id"]})
    else:
        bytes = api_helper._xml_request(api_helper.baseurl + "/4.0/detailedreportpdf.do", "GET", params={"build_id": build.attrib["build_id"]})
    with open(output, "wb") as binary_file:
        binary_file.write(bytes)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Gets Summary Report for a specific scan and application")
    parser.add_argument("-a", "--application", required=True, help="Name of the application")
    parser.add_argument("-s", "--sandbox", required=False, help="Name of the sandbox")
    parser.add_argument("-v", "--version", required=False, help="Name of the scan (defaults to latest)")
    parser.add_argument("-rt", "--report_type", required=False, help="Report Type (defaults to summary_report - can also be set to detailed_report)")
    parser.add_argument("-o", "--output", required=False, help="Output file to store pdf report (defaults to detailed_report/summary_report.pdf)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    application_name = args.application
    sandbox_name = args.sandbox
    version = args.version
    report_type = args.report_type
    output = args.output

    if report_type:
        report_type = report_type.lower().strip()
        if not report_type in ["detailed_report", "summary_report"]:
            raise Exception(f"Invalid report type '{report_type}'. Supported types are: summary_report and detailed_report")

    if not output:
        output = "detailed_report.pdf" if (report_type and report_type == "detailed_report") else "summary_report.pdf"

    application = get_application(application_name)
    if sandbox_name:
        sandbox = get_sandbox(application["guid"], sandbox_name)
    else:
        sandbox = None

    build = get_build(application, sandbox, version)

    save_report(build, report_type, output)

main()