#Backend_script.py
import requests
import base64
import os
import tempfile
import json
import re
import time
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings
import sys
from io import StringIO
from myapp.models import Result,EmailCredentials
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def send_email(tenant_name, sender_email, sender_password, to, cc, subject, html_content):
    # Create the MIME object
    message = MIMEMultipart()

    # Add sender, recipient, cc, and subject to the MIME object
    message["From"] = sender_email
    message["To"] = ", ".join(to)
    message["Cc"] = ", ".join(cc)
    message["Subject"] = subject

    # HTML content of the email


    # Attach the HTML content to the MIME object
    message.attach(MIMEText(html_content, "html"))

    # Combine recipients and CC into a list for sendmail
    to_addresses = to + cc

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS for security
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_addresses, message.as_string())

    print(f"Email sent successfully to: {tenant_name}")
 

    # Connect to the SMTP server (Outlook server and port)
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587

def create_case(advisory_name, matched_count, tenant):
    if matched_count != 0:
        try:        
            payload = {
                "category": advisory_name,
                "description": f"Matched IOCs: {matched_count}",
                "event_time": str(timezone.now()),  # Adjust the timestamp as needed
                "title": f"Threat Advisory: {advisory_name}",
                "tenant": tenant
            }

            # Specify the Sporact API endpoint and authentication details
            sporact_url = "https://eventus.in.secops.trendmicro.com/api/cases/case/"
            sporact_api_key = "jOVEu.Po9PrrJtyeLrityqGoX9uUq1ePVVEuXJ" 

            headers = {
                'X-Api-Key': sporact_api_key,
                'Content-Type': 'application/json'
            }

            response = requests.post(sporact_url, headers=headers, json=payload)

            # Print the response code
            print("Sporact Case Creation Response Code:", response.status_code)
            print("Sporact Case Creation Reason:", response.reason)

        except Exception as e:
            print(f"Error creating case in Sporact: {e}")


class ConsoleCapture(StringIO):
    def __init__(self, *args, **kwargs):
        super(ConsoleCapture, self).__init__(*args, **kwargs)
        self.captured_messages = []

    def write(self, message):
        super().write(message)
        sys.__stdout__.write(message)
        self.captured_messages.append(message)

# prompt for required details
def process_input_data(advisory_type, advisory_number,advisory_name,advisory_file_name):
      # Create an instance of the custom stream handler
   

    try:
        console_capture = ConsoleCapture()
        sys.stdout = console_capture

        advisory_type = advisory_type
        advisory_number =advisory_number
        advisory_name = advisory_name
        advisory_file_name =advisory_file_name
        ioc_file = advisory_number + "-"+ advisory_name + ".csv"
        file_content = f"advisory_type: {advisory_type}\nadvisory_number: {advisory_number}\nadvisory_name: {advisory_name}\nadvisory_file_name: {advisory_file_name}"
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name  # Save the path for later use

        # user_input = Result(
        #     advisory_type=advisory_type,
        #     advisory_number=advisory_number,
        #     advisory_name=advisory_name,
        #     # advisory_file_name=advisory_file_name
        # )
        # user_input.save()
        captured_output = console_capture.captured_messages
        
    finally:
         sys.stdout = sys.__stdout__


  
    

    email_subject = f"Threat Advisory: {advisory_name}"

    # Input values
    github_username = "EVENTUSSECURITY"
    github_repo = "threatlabs"
    path="Threat%20Advisories/IOCs"


    # Set your email and password
    sender_email = "threat.advisories@eventussecurity.com"
    sender_password = "@#$%purplexdiana@#$%5151"

    def get_all_tenants():
        try:
            tenants = EmailCredentials.objects.values_list('tenant', flat=True).distinct()
            return list(tenants)
        except Exception as e:
            print(f"Error fetching tenants from the database: {e}")
            return []
        
    def get_all_credentials():
            credentials_dict = {}
            try:
                credentials_objects = EmailCredentials.objects.all()
                for credentials in credentials_objects:
                    tenant_name = credentials.tenant
                    credentials_dict[tenant_name] = {
                        'to': credentials.to.split(', '),
                        'cc': credentials.cc.split(', '),
                        'subject': email_subject,
                        'url': credentials.url,
                        'api_key': credentials.api_key,
                    }
                return credentials_dict
            except Exception as e:
                print(f"Error fetching credentials from the database: {e}")
                return {}
    all_tenants = get_all_tenants()
    
    # Fetch all credentials from the database
    all_credentials = get_all_credentials()

    # Define the email data list dynamically
    email_data_list = []

    for tenant_name in all_tenants:
        credentials = all_credentials.get(tenant_name)

        if credentials:
            email_data_list.append({
                "tenant": tenant_name,
                **credentials,
            })
        else:
            # Handle the case where credentials are not found
            print(f"Credenti`als not found for tenant: {tenant_name}")
       

                # Set the recipient email address
#     email_data_list = [
#     {
#         "tenant":"TRIAL",
#         "to": ["gaurav.landge@eventussecurity.com"],
#         "cc": ["gaurav.landge@eventussecurity.com"],
#         "subject": email_subject,
#     },

    
# ]

    # Create the MIME object
    message = MIMEMultipart()

    insyghts = [
        'SYSMEX',
        'KLINE',
        'NTUC',
        'FKT',
        'CAG',
        'RJT',
        'SFG',
        'CCS',
        'NHB',
        'IFFCO',
        'SIDBI'
        ]
    string_replace_pattern = [
        r'([^"]*image001\.(png|jpg|jpeg|gif)[^"]*)',
        r'([^"]*image002\.(png|jpg|jpeg|gif)[^"]*)',
        r'([^"]*image003\.(png|jpg|jpeg|gif)[^"]*)',
        # r'cid:image001\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        # r'cid:image002\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        # r'cid:image003\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        "COMPANYNAME", 
        "STRINGTOBEREPLACED"]

    string_replace_pattern_vuln = [
        r'([^"]*image001\.(png|jpg|jpeg|gif)[^"]*)',
        r'([^"]*image002\.(png|jpg|jpeg|gif)[^"]*)',
        r'([^"]*image003\.(png|jpg|jpeg|gif)[^"]*)',
        # r'cid:image001\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        # r'cid:image002\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        # r'cid:image003\.(png|jpg|jpeg)@[A-Fa-f0-9]+\.[A-Fa-f0-9]+', 
        "COMPANYNAME", 
        ]

    # customers = {
    # "TRIAL":['https://api.xdr.trendmicro.com','eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjaWQiOiJiNzc2NjQxNS1iZjJkLTQyOTUtYWE0MC0wYTQ0M2E3OTczMDAiLCJjcGlkIjoic3ZwIiwicHBpZCI6ImN1cyIsIml0IjoxNjgzMDI1MTI1LCJ1aWQiOiJtYWxjb2xtX3BAdHJlbmRtaWNyby5jb20iLCJldCI6MjE0NzQ4MzY0N30.SI3-6TYaD9f-A-nHlveo62KeM3o0axrpzVfYoPIyQVYknnWPQh_-dUANwb94wLlDSBtnuejN8dQjb63IaSMJ8imGmnNRjAYxAmDOVCtO6Bj2hOAbm2W7RGN9IEgxWNL8d--1a1M9HjH3ZEV6c58E3DGLngHEDxxi0EhBswlO81KLfStQBJfW0tbRuer-HHDIMoFDdIS3Av-0Y-gU272fFyuQiiiiXcUGadFt3Lh5FSPKY-tRTok6UpzsAYALuRx4CU33_fKQqjE9Jk1PNra77XIvzm8W8F7UZFXodzb6TY_fpe7gqYmkM_UBT1je2TpYIrAXS9awLX2sbs9sDGApj85VWO-3dxvth3ZRyg2D0_YG6CFczywXlXPxu66yw_LTYNDoYkhjnsFrMl3X7EJ8osXsVMxaJCNf9TcjWUdHJZo4K0KK24hxYwYDOBSp4hSjji2PwPMsl02aQekW_yr7Ifc8rRVOZ4s26ZfJGdXivrKCblagFRhh0aHD90pDaH7GjKiRKHnaAtlR9woQc-_YdsJbYp4rni12IwCAN5-C4BLleLaDd_ylkMnRqZHLzXdphjMMAPCVAMY4oGIcguMDFRvnBw3zMtLQnESnNN8g_Wszf20BU9Va87CWJqmyYc2KwKgNzbYyr50AnMoDqn1hZi_kYD3rKU2tHffAvQS3Ujk']
   
    # }

    task_urls = {}
    results = {}
    send_html = {}

    html_content = ""

    # storing the HTML content in "html_content" variable
    try:
        # Open the HTML file in read mode
        with open(advisory_file_name, "r", encoding="unicode_escape") as file:
            # Read the content of the file
            html_content = file.read()

        # Print or process the HTML content as needed
        # print(html_content)

    except FileNotFoundError:
        print(f"File not found: {advisory_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")


    if advisory_type == "M":
        github_token = "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"
        print(color.BOLD + "\n" + advisory_name + " - " + ioc_file + color.END) 
        print(color.GREEN + "Starting...\n" + color.END)

        # Define the GitHub API URL based on input values
        github_api_url = f"https://api.github.com/repos/{github_username}/{github_repo}/contents/{path}/{ioc_file}"
        
        # Make a GET request to the GitHub API with authentication
        try:
            response = requests.get(github_api_url, headers={"Authorization": f"token {github_token}"})
        except KeyboardInterrupt:
            print("PROCESS INTERRUPTED WHILE FETCHING THE IOC FILE: " + color.CYAN + color.UNDERLINE + ioc_file + color.END)
            exit(0)
        except:
            print("Error while fetching IOC file: " + color.RED + color.UNDERLINE + ioc_file + color.END)
            exit(0)
            
        
        # Check if the request was successful
        try:
            if response.status_code == 200:
                    data = response.json()
                    file_content = base64.b64decode(data.get('content', '')).decode('utf-8')
                
                    # Create a temporary file and write the content to it
                    with tempfile.NamedTemporaryFile(mode='w+', delete=False,encoding='utf-8') as file:
                        file.write(file_content)
            else:
                print(f"Failed to retrieve file. Status code: {response.status_code}")
        except KeyboardInterrupt:
            print(color.RED + "PROCESS INTERRUPTED WHILE CREATING TEMP FILE" + color.END)
            exit(0)
        except:
            print(color.RED + 'Error while writing in temp file' + color.END)
            exit(0)

        # for retriving data/credentials from database
        for email_credential in EmailCredentials.objects.all():
            try:
                url_base = email_credential.url
                url_path = '/v3.0/threatintel/intelligenceReports'
                token = email_credential.api_key
                customer_name = email_credential.tenant
                query_params = {}
                headers = {'Authorization': 'Bearer ' + token}
                data = {'reportName': advisory_name}
                files = {'file': (advisory_name + ".csv", open(f'{file.name}', encoding='utf-8-sig'), 'text/csv')}
            except ObjectDoesNotExist:
                print(f"Data not found for {email_credential.tenant}. Skipping...")        
           
            try:
                r = requests.post(url_base + url_path, params=query_params, headers=headers, data=data, files=files)
                # print("URL: "+r.url)

                if 'application/json' in r.headers.get('Content-Type', '') and len(r.content):
                    # print(json.dumps(r.json(), indent=4))
                    pass
                else:
                    print(r.text)

                data = json.loads(r.content)
            except KeyboardInterrupt:
                print(color.RED + "PROCESS INTERRUPTED WHILE UPLOADING THE FILE TO VISION ONE" + color.END)
                exit(0)
            except:
                print(color.RED + 'Error while uploading the file to Vision One...' + color.END)
                continue
            
            #checking if the error is for API key or URL
            if "error" in data or "Invalid Token" in data:
                print(color.RED + f'{customer_name}: <File sweep ERROR> (invalid API key/invalid URL)' + color.END)
                continue
            if "error" in str(data) or "4000021" in str(data):
                print(color.RED + customer_name + ": ERROR CODE <4000021>" + color.END)
                continue

            reportid = data[0]["headers"][0]["value"].split("/")[-1]

            #Trigger Sweeping

            url_path = '/v3.0/threatintel/intelligenceReports/sweep'

            query_params = {}
            headers = {'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json;charset=utf-8'}
            body = [{'id': reportid, 'sweepType': 'manual'}]

            try:
                r = requests.post(url_base + url_path, params=query_params, headers=headers, json=body)
            except KeyboardInterrupt:
                print(color.RED + "PROCESS INTERRUPTED WHILE SWEEPING" + color.END)
                exit(0)
            except:
                print(color.RED + "Error while sweeping..." + color.END)
                continue
            
            print("Sweeping started: " + customer_name)
            
            sweep_url = (r.json()[0])['headers'][0]['value']
            task_urls[customer_name] = [sweep_url, token]

        print(color.YELLOW + "\nPlease wait until the sweeping is completed...\n" + color.END)
        try:
            time.sleep(400)
        except:
            print(color.CYAN + "SCRIPT EXECUTION INTERRUPTED, YOU WILL NOT BE ABLE TO SEE THE RESULTS" + color.END)
            exit(0)
        # code for getting the results

        patterns = [
            (r"\[file:hashes\.'MD5' = '([a-fA-F0-9]+)'\]", "MD5 Hash Values"),
            (r"\[file:hashes\.'SHA-1' = '([a-fA-F0-9]+)'\]", "SHA-1 Hash Values"),
            (r"\[file:hashes\.'SHA-256' = '([a-fA-F0-9]+)'\]", "SHA-256 Hash Values"),
            (r"\[ipv4-addr:value = '(\d+\.\d+\.\d+\.\d+)'\]", "IP Addresses"),
            (r"\[domain-name:value = '([^']+)'\]", "Domain Names"),
            (r"\[url:value = '([^']+)'\]", "URLs"),
        ]

        print(color.GREEN + "Results:"+ color.END)
        for c in task_urls:
            # Set up headers
            client_name = c
            sweep_url = task_urls[c][0]
            apikey = task_urls[c][1]
            
            headers = {
                'Authorization': f'Bearer {apikey}'
            }

            try:
                response = requests.get(sweep_url, headers=headers)
                if response.status_code == 200:
                    # Parse JSON response
                    data = response.json()

                    # Extract values based on patterns and mask them
                    if data["status"] == "succeeded":
                        matched_values = []
                        for pattern, label in patterns:
                            matches = re.findall(pattern, json.dumps(data))
                            matched_values.extend(matches)

                        matched_count = len(matched_values)
                        # Build the output message
                        output_message = f'''<b><span style="font-size:13.0pt; color:#C00000">Action:</span></span></b><br /><br />We have conducted a manual sweep in your Vision One Account and '''
                        script_output_message = f'{client_name}: '

                        if matched_count != 0:
                            matched_values_str = f"{matched_count} match found.<br /><b>Matches Found:</b><br />"
                            script_matched_values_str = f"{matched_count} match found.\nMatches Found:"
                            for value in matched_values:
                                
                                # script_result = Result(
                                #     device_list=value,
                                # )
                                # script_result.save()

                                matched_values_str += f"&nbsp;" * 12 + value.replace(".", "[.]").replace("://", "[://]") + "<br />"
                                script_matched_values_str += f"\t" + value.replace(".", "[.]").replace("://", "[://]") + "\n"
                                
                            matched_values_str += "<br /><br />Also, the IOCs have been added to the Vision One Portal for further Detection."
                                                
                            output_message += matched_values_str
                            script_output_message += script_matched_values_str
                            
                        

                        else:
                            output_message += "no match found.<br />Also, the IOCs have been added to the Vision One Portal for further Detection."
                            script_output_message += "no match found."
                    else:
                        script_output_message = color.CYAN + client_name + ": FILE IS STILL SWEEPING..." + color.END
                    
                    print(script_output_message)
                    if "FILE IS STILL SWEEPING" not in script_output_message:
                        results[client_name] = output_message
                    
                else:
                    print(f'{client_name} (Response Error: {response.status_code}): Error getting results')
            except KeyboardInterrupt:
                print(color.RED + "PROCESS INTERRUPTED WHILE FETCHING THE RESULTS"+ color.END)
                exit(0)
            except requests.exceptions.RequestException as e:
                print(color.RED + f'Error: {e}' + color.END)
            except:
                print(color.RED + "Unknown error" + color.END)

         # Extract form data
        advisory_type = advisory_type
        advisory_number =advisory_number
        advisory_name = advisory_name
        advisory_file_name =advisory_file_name
        ioc_file = advisory_number + "-"+ advisory_name + ".csv"


        # script to send email to customers with results
        print(color.GREEN + "\nSending mail..." + color.END)  



        # create a dictionary with client name and its HTML content
        for company_name, string_to_be_replaced in results.items():
            if company_name in insyghts:
                continue
            
            replace_string = [
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/trentus.jpg",
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/threat-advisory.jpg",
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/tlp.gif",
                company_name,
                string_to_be_replaced
                ]
            email_html_content = html_content
            
            # print(replace_string)
            
            for thestring, stringtobereplaced in zip(string_replace_pattern, replace_string):
                email_html_content = re.sub(thestring, stringtobereplaced, email_html_content)
            
            send_html[company_name] = email_html_content


        for k,v in send_html.items():
            to = ""
            cc = ""
            subject = ""
            for t in email_data_list:
                if t["tenant"] == k:
                    to = t["to"]
                    cc = t["cc"]
                    subject = t["subject"]
                    continue
            if to != "":
                send_email(k, sender_email, sender_password, to, cc, subject, v)
                   
                script_result = Result(
                    advisory_type=advisory_type,
                    advisory_number=advisory_number,
                    advisory_name=advisory_name,
                    date_time=timezone.now(),
                    tenant=k,
                    iocs_matched=matched_count,
                    iocs_list=matched_values,
                )
                script_result.save()
                date_time = timezone.now()
                Result.objects.filter(date_time__isnull=True).update(date_time=date_time)

                create_case(advisory_name, matched_count, k)

    if advisory_type == "V":
        print(color.GREEN + "Starting sending advisories..." + color.END)
        for cust in email_data_list:
            replace_string = [
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/trentus.jpg",
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/threat-advisory.jpg",
                "https://raw.githubusercontent.com/worldhsayinghello/IOCs/main/Images/tlp.gif",
                cust["tenant"],
                ]
            email_html_content = html_content
            for thestring, stringtobereplaced in zip(string_replace_pattern_vuln, replace_string):
                email_html_content = re.sub(thestring, stringtobereplaced, email_html_content)

            # print(email_html_content)
            to = cust["to"]
            cc = cust["cc"]
            subject = cust["subject"]
            if to != "":
                try:
                    send_email(cust["tenant"], sender_email, sender_password, to, cc, subject, email_html_content)

                    script_result = Result(
                        advisory_type=advisory_type,
                        advisory_number=advisory_number,
                        advisory_name=advisory_name,
                        date_time=timezone.now(),
                        tenant=k,
                        iocs_matched=matched_count,
                        iocs_list=matched_values,
                            )
                    script_result.save()
                    date_time = timezone.now()
                    Result.objects.filter(date_time=True).update(script_codate_timempletion_time=date_time)
                except:
                    print(color.RED + "ERROR OCCURED WHILE SENDING ADVISORY TO " + cust["tenant"])
        print(color.GREEN + "COMPLETED" + color.END)
               
    return captured_output