## 利用python下载ECMWF数据

近期由于在工作实验室要研究影像数据，所以需要下载ECMWF（欧洲中期天气预报中心）的再分析数据，本人通过官网上提供的API借口，对ECMWF欧洲中心API进行批量下载。这种下载ECMWF数据的方法在[官网](https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets)上有非常详细的介绍。

### 注册账户并获取apiKey

1. 注册账户

  首先，我们需要注册一个ECMWF的账号，在官网点击[注册](https://apps.ecmwf.int/registration/)，如下图所示，进行注册：

  ![login](./download_ECMWF_data/login.png)

  在注册完成后，点击登陆即可。

2. 获取api key

  通过[此地址](https://api.ecmwf.int/v1/key/)可以获取API key。

  ![apikey](./download_ECMWF_data/apikey.png)

  再获取到此信息后，在`$HOME`下新建**.ecmwfapirc**，并将最后一栏内的信息，保存。

3. 安装ecmwf-api-client-python

  点击[此处](https://confluence.ecmwf.int/display/WEBAPI/Web-API+Downloads)可以下载合适的ecmwf-api-client-python安装包，进行安装。

  ```
  pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz
  ```

### 数据下载

1. 了解想要下载数据的信息

  点击[数据集](https://apps.ecmwf.int/datasets/)获取所有公开的数据集，如下图所示：

  ![datasets](./download_ECMWF_data/datasets.png)

  本人下载的是**ERA Interim**数据集，如下图所示：

  ![ERA Interim](./download_ECMWF_data/selecteddataset.png)

  选择下载月份、时间等信息，本人选择如下参数：

  ![params](./download_ECMWF_data/params.png)

  点击**View the MARS requests**,即可查看Python脚本代码

  ![viewpythoncode](./download_ECMWF_data/viewpythoncode.png)

  ![resultcode](./download_ECMWF_data/resultcode.png)

2. 参数详解

  主要注意以下几个参数：

  * date：选择下载数据的日期

  * param：不同的数据类型，有不同的参数，

      下面几个参数是本人下载的时候所查找的查找方式可以看上一节：

      ![paramsvalue](./download_ECMWF_data/paramsvalue.png)

  * format： 输出格式，可以指定为`netcdf`

  * target： 输出路径

3. 代码展示

  ```Python
  from ecmwfapi import ECMWFDataServer
  server = ECMWFDataServer()
  a = linecache.getlines('./month.txt')
  cur = datetime.datetime.now()

  for k, v in params.items():
      for i in range(2010, cur.year):
          if i % 4 == 0:
              m = 29
          else:
              m = 28
          for j in range(1, 13):
              if j == 2:
                  b = m
              else:
                  b = a[j - 1]
              if j < 10:
                  y = '0'+ str(j)
              else:
                  y = str(j)
              date = str(i) + '-' + y + '-01/to/' + str(i) + '-' + y + '-' + str(b)
              # print(date)
              # from ecmwfapi import ECMWFDataServer
              # server = ECMWFDataServer()
              filename = str(i) + y + '01' + k + '.nc'
              path = os.path.join(outfolder, k)
              if not os.path.exists(path):
                  os.makedirs(path)
              fullpath = os.path.join(path, filename)
              print('=====================================')
              print('start download {0}'.format(filename))
              server.retrieve({
                  'class': 'ei',
                  'dataset': 'interim',
                  'date': date,     # '2018-02-01/to/2018-02-28',
                  'expver': '1',
                  'grid': '0.75/0.75',
                  'levtype': 'sfc',
                  'param': v,  # '167.128',
                  'step': '0',
                  'stream': 'oper',
                  'time': '00:00:00',
                  'type': 'an',
                  'format': 'netcdf',
                  'target': fullpath
              })
              print('{0} file download success!'.format(filename))
              print('======================================')
  ```
