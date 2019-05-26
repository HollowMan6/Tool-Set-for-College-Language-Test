# Download-Tools-for-CET-Admission-Ticket

This is a Download Tool Coded Using Python Tkinter to Batch Download CET Admission Ticket（CET准考证批量下载工具）

[Win程序:](Download-Tools-for-CET-Admission-Ticket.exe) 

![](screenshoot.JPG) 

[下载工具脚本](Download-Tools-for-CET-Admission-Ticket.py)

[PDF信息处理脚本](Get-Info-from-CET-Admission-Ticket.py)

采用Python多线程Tkinter UI编程！PDF信息处理使用pdfminer3k库

说明：请将list.txt文件放在程序运行目录下后再运行本软件,list.txt一行代表一条数据，其格式为：

```text
姓名 证件号
... ...
```

运行下载工具的同时，请用浏览器打开[CET快速打印准考证网站](http://cet.etest.net.cn/Home/QuickPrintTestTicket)，输入你看到的验证码到下载工具中，并且获取Cookies中ASP.NET_SessionId和BIGipServercet_pool的值。如果提示验证码已过期，请点击网页中的验证码图片，以刷新验证码，再将该验证码输入到本下载工具中。如果总提示验证码已过期，请考虑是否为Cookies输入错误。

程序运行过程中向list.txt添加账号是无效的，必须重新运行程序。

程序重新运行时将恢复到初始状态。

下载结束后，请多次点击开始按钮，直到已查询账号数字不再增加，从而确保所有账号都已被下载。

下载完成之后，请直接解压Downloads目录下的zip文件到Downloads目录，并运行[PDF信息处理脚本](Get-Info-from-CET-Admission-Ticket.py)，随后将在目录下生成info.txt,其格式为：

```text
准考证号 姓名
... ...
```

上述步骤可以在Linux下运行[Shell脚本](Get-Info-from-CET-Admission-Ticket.sh)进行操作。

也可以使用如下命令：

首先，确保打开的目录是本Python脚本所在目录，然后，执行如下命令：

```shell
cd ./Downloads
unzip \*.zip
cd ..
python3 Get-Info-from-CET-Admission-Ticket.py
```

利用info.txt中的信息，可以进一步进行查分等操作。

**警告**：

***仅供测试使用，不可用于任何非法用途！***

***对于使用本代码所造成的一切不良后果，本人将不负任何责任！***

[Windows Program](Download-Tools-for-CET-Admission-Ticket.exe)

[Download Tool Script](Download-Tools-for-CET-Admission-Ticket.py)

[PDF Info Handling Script](Get-Info-from-CET-Admission-Ticket.py)

Using Python multithreading programming, UI Coded with Tkinter, PDF Info Handling realized by pdfminer3k.

Note: Please put the list.txt file in the program running directory before running the software. The list.txt line represents a data in the format of:

```text
Name ID
... ...
```

While running the Download Tool, open [CET Fast Admission Ticket Print](http://cet.etest.net.cn/Home/QuickPrintTestTicket) with a browser.
Enter the validation code you see into this Download Tool and get the values of ASP.NET_SessionId and BIGipServercet_pool in Cookies.
If the prompt verification code has expired, please click on the picture of the verification code in the web page to refresh the verification code, and then input the verification code into the Download Tool. If the total prompt verification code has expired, please consider whether the error is entered for Cookies.

It is invalid to add an account to list.txt during the running process of the program, and the program must be re-run.

The program restores to its initial state when it is re-run.

After the download is over, please click the start button many times until the number of inquired accounts no longer increases, so as to ensure that all accounts have been downloaded.

After downloading, please decompress the zip file from the Downloads directory directly to the Downloads directory and run the [PDF Info Handling Script](Get-Info-from-CET-Admission-Ticket.py). Then, info.txt will be generated under the directory in the format of:

```text

Name Admission-Ticket-number

... ...

```

The above steps can be performed by running the [shell script](Get-Info-from-CET-Admission-Ticket.sh) under Linux.

You can also use the following commands:

First, make sure that the open directory is the directory where the Python script is located. Then, execute the following command:

```shell
cd ./Downloads
unzip \*.zip
cd ..
python3 Get-Info-from-CET-Admission-Ticket.py
```

The information in info.txt can be used for further operations.

**Warning**:

***For TESTING ONLY, not for any ILLIGAL USE!***

***I will not be responsible for any adverse consequences caused by using this code.***