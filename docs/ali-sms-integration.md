# Alibaba Cloud SMS Integration Guide

Log in to the Alibaba Cloud console and enter the "SMS Service" page: https://dysms.console.aliyun.com/overview

## Step 1: Add signature
![Step](images/alisms/sms-01.png)
![Step](images/alisms/sms-02.png)

After the above steps, you will get the signature. Please write it to the smart console parameter, `aliyun.sms.sign_name`

## Step 2 Add template
![Step](images/alisms/sms-11.png)

After the above steps, you will get the template code. Please write it into the intelligent console parameters, `aliyun.sms.sms_code_template_code`

Note that the signature will take 7 working days to be successfully sent after the operator reports successfully.

Note that the signature will take 7 working days to be successfully sent after the operator reports successfully.

Note that the signature will take 7 working days to be successfully sent after the operator reports successfully.

You can wait until the report is successful before continuing.

## Step 3: Create SMS account and activate permissions

Log in to the Alibaba Cloud console and enter the "Access Control" page: https://ram.console.aliyun.com/overview?activeTab=overview

![Step](images/alisms/sms-21.png)
![Step](images/alisms/sms-22.png)
![Step](images/alisms/sms-23.png)
![Step](images/alisms/sms-24.png)
![Step](images/alisms/sms-25.png)

The above steps will get access_key_id and access_key_secret. Please write them into the intelligent console parameters, `aliyun.sms.access_key_id`, `aliyun.sms.access_key_secret`
## Step 4: Start the mobile phone registration function

1. Normally, after filling in the above information, there will be this effect. If not, a certain step may be missing.

![Step](images/alisms/sms-31.png)

2. Enable non-administrator users to register, and set the parameter `server.allow_user_register` to `true`

3. Enable the mobile phone registration function and set the parameter `server.enable_mobile_register` to `true`
![Step](images/alisms/sms-32.png)