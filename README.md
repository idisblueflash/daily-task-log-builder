# daily Task Log Builder

This is a tools to convert your Markdown like Task log
into a formatted table.

## Install
install the packages:
```shell
pipenv install
```

## A Simple Example
Assume you wrote a log file called `demo.md`
```md
# 27/Apr/22
8:00, daily warms up: 
  * email 
  * zulip 
  * planning
8:30, #8280 AI Recommend by email is broken: 
  * setup up debug tools
9:19, Wrong Ask Formatting Emails Issue: 
  * communicate with Helen
9:38, break
9:44, n8n User Stories Delivery
10:00, daily, Nash Chase
12:00, break
```
you can generate it with
```shell
$ pipenv run make_report.py demo.md
Date 日期    Day    Persons Involved    Time 时间        Category 工作列别    Priority 重要性    Description 内容描述                         Estimate Hours    Total Hours  Status 完成状态
---------  -----  ------------------  -------------  ---------------  --------------  -------------------------------------  ----------------  -------------  -------------
27/Apr/22  Wed    Flash               8:00 - 8:30    Daily Works      Low             daily warms up                                     0.5            0.5   DONE
                                                                                        * email
                                                                                        * zulip
                                                                                        * planning
27/Apr/22  Wed    Flash               8:30 - 9:19    Tasks            High            #8280 AI Recommend by email is broken              0.82           1.32  DONE
                                                                                        * setup up debug tools
27/Apr/22  Wed    Flash               9:19 - 9:38    Communication    Medium          Wrong Ask Formatting Emails Issue                  0.32           1.64  DONE
                                                                                        * communicate with Helen
27/Apr/22  Wed    Flash               9:44 - 10:00   Tasks            Medium          n8n User Stories Delivery                          0.27           1.91  DONE
27/Apr/22  Wed    Flash, Nash, Chase  10:00 - 12:00  Daily Works      Low             daily                                              2              3.91  DONE
```
