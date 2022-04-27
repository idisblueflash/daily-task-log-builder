from services import FlashDailyLog

if __name__ == '__main__':
    data = """
    8:00, daily warms up: email zulip planning
    8:30, #8280 AI Recommend by email is broken: * setup up debug tools
    9:19, Wrong Ask Formatting Emails Issue: communicate
    9:38, break
    9:44, n8n User Stories Delivery
    10:00, daily, Nash Chase
    12:00, break
    13:30, Wrong Ask Formatting Emails Issue: * Investigate * Build script to check detail
    16:00, Daily meeting, Nash Chase Serge Kimi
    16:50, break
    19:15, Wrong Ask Formatting Emails Issue: * Three samples checking
    20:15, Daily Task Report
    20:40, break
    """
    rows = [row.strip() for row in data.strip().split('\n')]

    service = FlashDailyLog('27/Apr/22', rows)
    service.handle()
    service.report()
