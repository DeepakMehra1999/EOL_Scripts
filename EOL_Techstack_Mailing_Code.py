#import some important libraries
import csv, smtplib, sys
import glob, os
from csv import reader
from csv import writer
from datetime import date

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prettytable import PrettyTable

#take input details from input file
from EOL_Input_File import *

today = date.today()

#present working directory
pwd = os.getcwd()

dir_path = pwd
#use glob function to create a list of paths of output files
list_of_paths_of_csv_files =  glob.glob(dir_path + "/*.csv")

#create a list to store output_file_data
list_to_store_output_file_data = []
for file in list_of_paths_of_csv_files:
  with open(file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader) #skip first row

    for line in csv_reader:
      list_to_store_output_file_data.append(line)


expired_data_list=[]
to_be_expired_data_list=[]
for i in range(len(list_to_store_output_file_data)):
    if (int(list_to_store_output_file_data[i][5])<0):
      expired_data_list.append(list_to_store_output_file_data[i][5])
    else:
      to_be_expired_data_list.append(list_to_store_output_file_data[i][5])



#Create a desired table for sending in mail
if (len(expired_data_list) != 0):
  table_with_days_of_EOL1 = PrettyTable(['Client','Environment','Techstack', 'Version', 'EOL', 'Days remaining of EOL'])
else:
  table_with_days_of_EOL1 = PrettyTable(["No Techstack is expired as of this date"])
if (len(to_be_expired_data_list) != 0):
  table_with_days_of_EOL2 = PrettyTable(['Client','Environment','Techstack', 'Version', 'EOL', 'Days remaining of EOL'])
else:
  table_with_days_of_EOL2 = PrettyTable(["No Techstack is about to expire in the next 180 days"])

#add 'Already Expired' string for having negative values and 'To be Expired' for positive values
for i in range(len(list_to_store_output_file_data)):
    if(int(list_to_store_output_file_data[i][5])<0):
      list_to_store_output_file_data[i][5]="Already Expired"
      table_with_days_of_EOL1.add_row(list_to_store_output_file_data[i])
    else:
      #list_to_store_output_file_data[i][5]="To be Expired"
      table_with_days_of_EOL2.add_row(list_to_store_output_file_data[i])


#code of email sending part
def main(argv):
        try:
                my_message1 = table_with_days_of_EOL1.get_html_string()
                my_message2 = table_with_days_of_EOL2.get_html_string()
                text = ""

                html1 = """\
                <html>
                        <head>
                        <style>
                                table{
                                  font-size:12px;
                                  color: #333333;
                                  border-width: 1px;
                                  border-color: #000000;
                                  border-collapse: collapse;
                                }
                                th {
                                  font-size:14px;
                                  background-color:#acc8cc;
                                  border-width: 1px;
                                  padding: 8px;
                                  border-style: solid;
                                  border-color: #000000;
                                  text-align:left;
                                }
                                tr {
                                  background-color: #FFFFFF;
                                }
                                td {
                                  font-size:12px;
                                  border-width: 1px;
                                  padding: 8px;
                                  border-style: solid;
                                  border-color: #000000;
                                  text-align:center;
                                  color: #FF0000;
                                  font-weight: bold;
                                }
                        </style>
                        </head>
                <body>
                <p>Hello All,<br><br>
                   Please find below the details regarding End-Of-Life(EOL) for Techstack across environments for all the clients.<br><br>
                   1. Tech-Stack that are already expired.
                   %s<br>
                </p>
                </body>
                </html>
                """ % (my_message1)

                html2 = """\
                <html>
                        <head>
                        <style>
                                table{
                                  font-size:12px;
                                  color: #333333;
                                  border-width: 1px;
                                  border-color: #000000;
                                  border-collapse: collapse;
                                }
                                th {
                                  font-size:14px;
                                  background-color:#acc8cc;
                                  border-width: 1px;
                                  padding: 8px;
                                  border-style: solid;
                                  border-color: #000000;
                                  text-align:left;
                                }
                                tr {
                                  background-color: #FFFFFF;
                                }
                                td {
                                  font-size:12px;
                                  border-width: 1px;
                                  padding: 8px;
                                  border-style: solid;
                                  border-color: #000000;
                                  text-align:center;
                                  color: #f50;
                                  font-weight: bold;
                                }

                        </style>
                        </head>
                <body>
                <p>
                   2. Tech-Stack that are about to expire.
                   %s<br>
                   Best Regards,<br>
                   Fosfor Automation Team<br>
                   <br>
                   <font style="color:red;"  >Note:</font> This is an auto-generated email. For any queries, please reach out to Fosfor.delivery@lntinfotech.com
                </p>
                </body>
                </html>
                """ % (my_message2)

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html1 + html2, 'html')
                # Create the root message and fill in the from, to, and subject headers
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Fosfor Client's Tech-Stack EndOfLife(EOL) Status - " + str(today.strftime("%d/%m/%y"))
                msg['From'] = sendFrom
                msg['To'] = sendTo
                msg.attach(part1)
                msg.attach(part2)
                msg['Cc'] = ', '.join(cc)
                recipients = receivers + cc

                server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
                server.ehlo()
                server.starttls()
                server.login(USER, PASS)
                server.sendmail(sender, recipients, msg.as_string())
                server.close()
                print('Email sent!')
        except Exception as e:
                print('Something with SMTP went wrong...')
                print(e)


if __name__ == "__main__":
    main(sys.argv)