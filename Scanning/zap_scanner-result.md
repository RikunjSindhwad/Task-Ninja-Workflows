- Input
```bash
cat << "EOF" | tee urls.txt
https://ginandjuice.shop/
https://ginandjuice.shop/about
https://ginandjuice.shop/blog
https://ginandjuice.shop/blog/post?postId=1
https://ginandjuice.shop/catalog
https://ginandjuice.shop/catalog/cart
https://ginandjuice.shop/catalog/filter?category=Accessories
https://ginandjuice.shop/catalog/product?productId=1
https://ginandjuice.shop/login
https://ginandjuice.shop/my-account
https://ginandjuice.shop/post?postId=1
https://ginandjuice.shop/resources/js/MyComponent
https://ginandjuice.shop/vulnerabilities
EOF
```


- Visuals
```bash
  root@robensive> Task-Ninja -w zap_scanner.yaml -noBanner -v url_list=urls.txt
[Workflow-Credit] Tasked Workflow 'ZAP Scanner' Workflow-Author=Rikunj Sindhwad
------------------------------------------------------------------------------------------------------------------------
[Start] [2023-09-15T04:48:40Z] Task Started TaskName=Create Required Directories
------------------------------------------------------------------------------------------------------------------------
[Task-Info] Task is Static TaskName=Create Required Directories
[Static-Task: Create Required Directories] [2023-09-15T04:48:40Z] Executing Task
------------------------------------------------------------------------------------------------------------------------
[Success] [2023-09-15T04:48:40Z] Task Finished TaskName=Create Required Directories
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
[Start] [2023-09-15T04:48:41Z] Task Started TaskName=Downnload zap yaml
------------------------------------------------------------------------------------------------------------------------
[Task-Info] Task is Static TaskName=Downnload zap yaml
[Static-Task: Downnload zap yaml] [2023-09-15T04:48:41Z] Executing Task
------------------------------------------------------------------------------------------------------------------------
[Success] [2023-09-15T04:48:41Z] Task Finished TaskName=Downnload zap yaml
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
[Start] [2023-09-15T04:48:42Z] Task Started TaskName=Modify ZAP config
------------------------------------------------------------------------------------------------------------------------
[Task-Info] Task is Static TaskName=Modify ZAP config
[Static-Task: Modify ZAP config] [2023-09-15T04:48:42Z] Executing Task
------------------------------------------------------------------------------------------------------------------------
[Success] [2023-09-15T04:48:43Z] Task Finished TaskName=Modify ZAP config
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
[Start] [2023-09-15T04:48:44Z] Task Started TaskName=run ZAP
------------------------------------------------------------------------------------------------------------------------
[Task-Info] Task is Static TaskName=run ZAP
[Static-Task: run ZAP] [2023-09-15T04:48:44Z] Executing Task
------------------------------------------------------------------------------------------------------------------------
[Success] [2023-09-15T04:50:18Z] Task Finished TaskName=run ZAP
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
[Start] [2023-09-15T04:50:19Z] Task Started TaskName=Result-Check
------------------------------------------------------------------------------------------------------------------------
[Task-Info] Task is Static TaskName=Result-Check
[Static-Task: Result-Check] [2023-09-15T04:50:19Z] Executing Task
"Cross Site Scripting (Reflected)","High (Medium)","https://ginandjuice.shop/catalog/filter?category=Accessories%0A%0D%0A%0D%3CscrIpt%3Ealert%281%29%3B%3C%2FscRipt%3E","category","GET","<scrIpt>alert(1);</scR
ipt>"
"Cross Site Scripting (Reflected)","High (Medium)","https://ginandjuice.shop/login","username","POST","';alert(1);'"
"Vulnerable JS Library","Medium (Medium)","https://ginandjuice.shop/resources/js/angular_1-7-7.js","","GET","/*
 AngularJS v1.7.7"
result saved in hive/out/ZAP-Result.CSV
------------------------------------------------------------------------------------------------------------------------
[Success] [2023-09-15T04:50:19Z] Task Finished TaskName=Result-Check
------------------------------------------------------------------------------------------------------------------------
[Workflow-Complete] Workflow 'ZAP Scanner' Execution Complete Workflow-Author=Rikunj Sindhwad
```


- STDOUT Log
```bash
Found Java version 11.0.20
Available memory: 31641 MB
Using JVM args: -Xmx7910m
680 [main] INFO  org.parosproxy.paros.Constant - Copying default configuration to /root/.ZAP/config.xml
818 [main] INFO  org.parosproxy.paros.Constant - Creating directory /root/.ZAP/session
819 [main] INFO  org.parosproxy.paros.Constant - Creating directory /root/.ZAP/dirbuster
819 [main] INFO  org.parosproxy.paros.Constant - Creating directory /root/.ZAP/fuzzers
819 [main] INFO  org.parosproxy.paros.Constant - Creating directory /root/.ZAP/plugin
Automation plan failures:
        Job report-json failed to generate report:
No X11 DISPLAY variable was set, but this program performed an operation which requires it.
Automation plan warnings:
        Job spider error accessing URL https://ginandjuice.shop/catalog/filter?category=Accessories status code returned : 404 expected 200
        Job spider error accessing URL https://ginandjuice.shop/post?postId=1 status code returned : 404 expected 200
        Job spider error accessing URL https://ginandjuice.shop/resources/js/MyComponent status code returned : 404 expected 200
```
- STDERR Log
```log
Sep 15, 2023 4:48:48 AM java.util.prefs.FileSystemPreferences$1 run
INFO: Created user preferences directory.
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
Sep 15, 2023 4:49:37 AM org.openqa.selenium.remote.service.DriverService$Builder getLogOutput
INFO: Driver logs no longer sent to console by default; https://www.selenium.dev/documentation/webdriver/drivers/service/#setting-log-output
```

- RESULT
```bash
 cat hive/out/ZAP-Result.CSV
"Cross Site Scripting (Reflected)","High (Medium)","https://ginandjuice.shop/catalog/filter?category=Accessories%0A%0D%0A%0D%3CscrIpt%3Ealert%281%29%3B%3C%2FscRipt%3E","category","GET","<scrIpt>alert(1);</scRipt>"
"Cross Site Scripting (Reflected)","High (Medium)","https://ginandjuice.shop/login","username","POST","';alert(1);'"
"Vulnerable JS Library","Medium (Medium)","https://ginandjuice.shop/resources/js/angular_1-7-7.js","","GET","/*
 AngularJS v1.7.7"
```
