# daily Task Log Builder

This is a tools to convert your Markdown like Task log
into a formatted table.

## Install
install the packages:
```shell
pipenv install
```

## A Simple Example
1. configure your username in `configure.json` file
```JSON
{"user_name": "Flash"}
```

2. Assume you wrote a log file called `demo.md`
```md
# 27/Apr/22
8:00 day-to-day communication work and planning
8:30 #8280 AI Recommend by email is broken
  * setup up debug tools
9:19 Wrong Ask Formatting Emails Issue
  * communicate with Helen
9:38 break
9:44 n8n User Stories Delivery
10:00 daily meetings with Nash and Chase
12:00 break

```
3. you can generate it with
```shell
$ pipenv run ./make_report.py demo.md
Date 日期    Day    Persons Involved    Time 时间      Category 工作列别    Priority 重要性    Description 内容描述                          Estimate Hours    Total Hours  Status 完成状态
-----------  -----  ------------------  -------------  -------------------  -----------------  ------------------------------------------  ----------------  -------------  -----------------
27/Apr/22    Wed    Flash               8:00 - 8:30    Communication        Medium             day-to-day communication work and planning              0.5            0.5   DONE
27/Apr/22    Wed    Flash               8:30 - 9:19    Tasks                High               #8280 AI Recommend by email is broken                   0.82           1.32  DONE
                                                                                                 * setup up debug tools
27/Apr/22    Wed    Flash               9:19 - 9:38    Communication        Medium             Wrong Ask Formatting Emails Issue                       0.32           1.64  DONE
                                                                                                 * communicate with Helen
27/Apr/22    Wed    Flash               9:44 - 10:00   Tasks                Medium             n8n User Stories Delivery                               0.27           1.91  DONE
27/Apr/22    Wed    Chase, Flash, Nash  10:00 - 12:00  Communication        Low                daily meetings with Nash and Chase                      2              3.91  DONE
```
## Shortcuts
1. preview your .md file with `./preview.sh demo.md`
2. generate excel out with email message with `./generate.sh demo.md`
## Helps
```shell
./make_report.py --help
Usage: make_report.py [OPTIONS] FILE_NAME

Options:
  --daily BOOLEAN  Only show the latest daily
  --email BOOLEAN  Show email messages
  --excel BOOLEAN  generate execle output file
  --help           Show this message and exit.
```

## Configure Email Service
you can add a `.env` file to save your email settings like:
```md
SMTP_SERVER=smtp.partner.outlook.cn
PORT=587
EMAIL_SENDER=flash@cgptalent.com
EMAIL_PASSWORD=yourEmailPassword
EMAIL_TO=foo@icloud.com
EMAIL_CC=foo@gmail.com,bar@gmail.com
BODY='Hi Tom,
    Please take a look at my daily logs.'

```
