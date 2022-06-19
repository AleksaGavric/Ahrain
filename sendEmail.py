
import requests
import os
from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
from botocore.exceptions import ClientError

HTML_EMAIL_CONTENT = """
 <!doctype html>
<html>
  <head>
    <meta name="rainAlert" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Rail Alert</title>
    <style>
@media only screen and (max-width: 620px) {
  table.body h1 {
    font-size: 28px !important;
    margin-bottom: 10px !important;
  }

  table.body p,
table.body ul,
table.body ol,
table.body td,
table.body span,
table.body a {
    font-size: 16px !important;
  }

  table.body .wrapper,
table.body .article {
    padding: 10px !important;
  }

  table.body .content {
    padding: 0 !important;
  }

  table.body .container {
    padding: 0 !important;
    width: 100% !important;
  }

  table.body .main {
    border-left-width: 0 !important;
    border-radius: 0 !important;
    border-right-width: 0 !important;
  }

  table.body .btn table {
    width: 100% !important;
  }

  table.body .btn a {
    width: 100% !important;
  }

  table.body .img-responsive {
    height: auto !important;
    max-width: 100% !important;
    width: auto !important;
  }
}
@media all {
  .ExternalClass {
    width: 100%;
  }

  .ExternalClass,
.ExternalClass p,
.ExternalClass span,
.ExternalClass font,
.ExternalClass td,
.ExternalClass div {
    line-height: 100%;
  }

  .apple-link a {
    color: inherit !important;
    font-family: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
    text-decoration: none !important;
  }

  #MessageViewBody a {
    color: inherit;
    text-decoration: none;
    font-size: inherit;
    font-family: inherit;
    font-weight: inherit;
    line-height: inherit;
  }

  .btn-primary table td:hover {
    background-color: #34495e !important;
  }

  .btn-primary a:hover {
    background-color: #34495e !important;
    border-color: #34495e !important;
  }
}
</style>
  </head>
  <body style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">
    <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Check today's weather here</span>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f6f6f6; width: 100%;" width="100%" bgcolor="#f6f6f6">
      <tr>
        <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
        <td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; max-width: 580px; padding: 10px; width: 580px; margin: 0 auto;" width="580" valign="top">
          <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 580px; padding: 10px;">

            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border-radius: 3px; width: 100%;" width="100%">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;" valign="top">
                  <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                    <tr>
                      <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">
                        <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Good Morning,</p>
                        <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Chances are it will rain in the following hours:</p>
                        
                        <ul>

                          <li style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; color:#ff0000">DRIZZLE: 11:00AM - 30%</li>
                          <li style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; color:#ff0000">RAIN: 12:00PM - 40%</li>
                          <li style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; color:#ff0000">RAIN:&nbsp;&nbsp;1:00PM - 35%</li>
                          <li style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; color:#ff0000">DRIZZLE:&nbsp;&nbsp;2:00PM - 32%</li>

                        </ul>
                        
                        <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Min temperature: 71 F or 21 C°.</p>
                        <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Max temperature: 98 F or 36 C°.</p>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; box-sizing: border-box; width: 100%;" width="100%">
                          <tbody>
                            <tr>
                              <td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;" valign="top">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">
                                  <tbody>
                                    <tr>
                                      <td style="font-family: sans-serif; font-size: 14px; vertical-align: top; border-radius: 5px; text-align: center; background-color: #3498db;" valign="top" align="center" bgcolor="#3498db"> <a href="http://htmlemail.io" target="_blank" style="border: solid 1px #3498db; border-radius: 5px; box-sizing: border-box; cursor: pointer; display: inline-block; font-size: 14px; font-weight: bold; margin: 0; padding: 12px 25px; text-decoration: none; text-transform: capitalize; background-color: #3498db; border-color: #3498db; color: #ffffff;">Google Weather Report</a> </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </td>
                            </tr>
                          </tbody>
                        </table>
              
                        <p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 15px;">Thank you for using Ahrain ♥</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

            <!-- END MAIN CONTENT AREA -->
            </table>
            <!-- END CENTERED WHITE CONTAINER -->

            <!-- START FOOTER -->
            <div class="footer" style="clear: both; margin-top: 10px; text-align: center; width: 100%;">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                <tr>
                  <td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #999999; font-size: 12px; text-align: center;" valign="top" align="center">
                    <span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">Ahrain - 500 Wilson Blvd, Rochester NY, USA</span>
                    <br> Don't like these emails? <a href="http://i.imgur.com/CScmqnj.gif" style="text-decoration: underline; color: #999999; font-size: 12px; text-align: center;">Unsubscribe</a>.
                  </td>
                </tr>
                <tr>
                  <td class="content-block powered-by" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; color: #999999; font-size: 12px; text-align: center;" valign="top" align="center">
                    Powered by <a href="http://ahra.in" style="color: #999999; font-size: 12px; text-align: center; text-decoration: none;">Ahrain</a>.
                  </td>
                </tr>
              </table>
            </div>
            <!-- END FOOTER -->

          </div>
        </td>
        <td style="font-family: sans-serif; font-size: 14px; vertical-align: top;" valign="top">&nbsp;</td>
      </tr>
    </table>
  </body>
</html>

"""
CHARSET = "UTF-8"

load_dotenv()
accessKey = os.getenv('AWS_ACCESS_KEY')
accessSecret = os.getenv('AWS_ACCESS_KEY_SECRET')

msg = MIMEMultipart()
msg["Subject"] = "Rain incoming"
msg["From"] = "samzitestemail@gmail.com"
msg["To"] = 'samzitestemail@gmail.com'
msg["Body"] = {
                'Html': {
                    'Charset': CHARSET,
                    'Data': HTML_EMAIL_CONTENT,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': 'Some text as an email',
                }
}




# body = MIMEText(""" Here's your forecast for the day:
# 6% Friday 11:00 PM
# 7% Saturday 12:00 AM
# 7% Saturday 1:00 AM
# 3% Saturday 2:00 AM
# 2% Saturday 3:00 AM
# 2% Saturday 4:00 AM
# 3% Saturday 5:00 AM
# 5% Saturday 6:00 AM
# 4% Saturday 7:00 AM
# 2% Saturday 8:00 AM
# 1% Saturday 9:00 AM
# 0% Saturday 10:00 AM
# 0% Saturday 11:00 AM
# 0% Saturday 12:00 PM
# 0% Saturday 1:00 PM
# 0% Saturday 2:00 PM
# 0% Saturday 3:00 PM
# 0% Saturday 4:00 PM
# 0% Saturday 5:00 PM
# 0% Saturday 6:00 PM
# 0% Saturday 7:00 PM
# 0% Saturday 8:00 PM
# 0% Saturday 9:00 PM
# 0% Saturday 10:00 PM
# 0% Saturday 11:00 PM

#         * Min temp: 72 Fah, 22 Cel
#         * Max temp: 97 Fah, 36 Cel
# You can check the weather using the following link: https://www.google.com/search?q=charlotte+weather&oq=charlotte+weather&aqs=chrome..69i57.2478j0j4&sourceid=chrome&ie=UTF-8
# Have a nice and dry day!
# Ahrain
# """, "plain")
# msg.attach(body)

ses_client = boto3.client("ses", region_name='us-east-1', aws_access_key_id=accessKey, aws_secret_access_key=accessSecret)
# ses_client.send_raw_email(
#     Source="samzitestemail@gmail.com",
#     Destinations=['samzitestemail@gmail.com'],
#     RawMessage={"Data": msg.as_string()}
# )




try:
    #Provide the contents of the email.
    response = ses_client.send_email(
        Destination={
            'ToAddresses': [
                'samzitestemail@gmail.com',
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': HTML_EMAIL_CONTENT,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': 'Some text as an email',
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': 'Rain alert!',
            },
        },
        Source='samzitestemail@gmail.com',
        # If you are not using a configuration set, comment or delete the
        # following line
    )
# Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])